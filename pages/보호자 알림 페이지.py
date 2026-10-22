import streamlit as st
st.title('보호자 알림 페이지')
st.write('아이가 지정한 위치에서 벗어나면 보호자에게 알림이 가는 기능')

import csv
import io
import math
from datetime import datetime

import streamlit as st


# --------------------------------------------------
# 앱 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="안심존 | 아이 위치 안전 관리",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fb;
    }
    .main .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        background: linear-gradient(120deg, #173b67, #2875a8);
        padding: 28px;
        border-radius: 18px;
        color: white;
        margin-bottom: 20px;
    }
    .hero h1 {
        color: white;
        margin-bottom: 8px;
    }
    .hero p {
        color: #e7f2ff;
        margin-bottom: 0;
    }
    .small-note {
        color: #667085;
        font-size: 0.88rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 위치 및 거리 계산
# --------------------------------------------------
def valid_coordinate(lat, lon):
    """위도와 경도가 유효한 범위인지 확인합니다."""
    return (
        math.isfinite(lat)
        and math.isfinite(lon)
        and -90 <= lat <= 90
        and -180 <= lon <= 180
    )


def distance_meters(lat1, lon1, lat2, lon2):
    """두 좌표 사이의 거리를 하버사인 공식으로 계산합니다."""
    earth_radius = 6_371_000

    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )
    a = max(0.0, min(1.0, a))

    return 2 * earth_radius * math.asin(math.sqrt(a))


def format_distance(meters):
    if meters >= 1000:
        return f"{meters / 1000:.2f} km"
    return f"{meters:.0f} m"


# --------------------------------------------------
# 세션 상태 초기화
# --------------------------------------------------
if "events" not in st.session_state:
    st.session_state.events = []

if "last_status" not in st.session_state:
    st.session_state.last_status = None

if "last_check" not in st.session_state:
    st.session_state.last_check = None

if "last_distance" not in st.session_state:
    st.session_state.last_distance = None

if "last_child_location" not in st.session_state:
    st.session_state.last_child_location = None

if "last_zone_name" not in st.session_state:
    st.session_state.last_zone_name = None


# --------------------------------------------------
# 사이드바: 안전 구역 설정
# --------------------------------------------------
st.sidebar.title("⚙️ 안전 구역 설정")
st.sidebar.caption("보호자가 관리하는 안심존의 기준입니다.")

zone_name = st.sidebar.text_input(
    "안전 구역 이름",
    value="우리 집",
    max_chars=50,
)

center_lat = st.sidebar.number_input(
    "안전 구역 중심 위도",
    min_value=-90.0,
    max_value=90.0,
    value=37.5665,
    step=0.0001,
    format="%.6f",
)

center_lon = st.sidebar.number_input(
    "안전 구역 중심 경도",
    min_value=-180.0,
    max_value=180.0,
    value=126.9780,
    step=0.0001,
    format="%.6f",
)

radius = st.sidebar.slider(
    "안전 구역 반경",
    min_value=50,
    max_value=3000,
    value=300,
    step=50,
    format="%d m",
)

st.sidebar.divider()
st.sidebar.markdown("**안심존 판정 기준**")
st.sidebar.write(f"📍 기준 위치: {zone_name or '이름 미설정'}")
st.sidebar.write(f"⭕ 허용 반경: {radius:,}m")
st.sidebar.caption(
    "중심 좌표와 아이의 좌표 사이의 직선거리를 기준으로 판정합니다."
)


# --------------------------------------------------
# 상단 화면
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🛡️ 안심존</h1>
        <p>아이의 위치를 확인하고, 안전 구역 이탈 여부를 관리하세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "현재 버전은 좌표 입력 기반 시뮬레이터입니다. "
    "GPS를 백그라운드에서 자동 추적하거나 실제 문자·푸시 알림을 "
    "전송하지 않습니다."
)


# --------------------------------------------------
# 아이 위치 입력
# --------------------------------------------------
st.subheader("📍 아이 위치 확인")
st.write(
    "아이의 현재 좌표를 입력한 뒤 확인 버튼을 누르세요. "
    "아래 샘플 좌표로 이탈 상황을 테스트할 수도 있습니다."
)

with st.form("location_form"):
    col1, col2 = st.columns(2)

    with col1:
        child_lat = st.number_input(
            "아이의 현재 위도",
            min_value=-90.0,
            max_value=90.0,
            value=float(center_lat),
            step=0.0001,
            format="%.6f",
        )

    with col2:
        child_lon = st.number_input(
            "아이의 현재 경도",
            min_value=-180.0,
            max_value=180.0,
            value=float(center_lon),
            step=0.0001,
            format="%.6f",
        )

    submitted = st.form_submit_button(
        "🔎 위치 확인하기",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# 위치 판정 및 이벤트 기록
# --------------------------------------------------
if submitted:
    try:
        if not zone_name.strip():
            st.error("안전 구역 이름을 입력해 주세요.")
        elif not valid_coordinate(center_lat, center_lon):
            st.error("안전 구역 좌표가 올바르지 않습니다.")
        elif not valid_coordinate(child_lat, child_lon):
            st.error("아이의 좌표가 올바르지 않습니다.")
        else:
            distance = distance_meters(
                center_lat,
                center_lon,
                child_lat,
                child_lon,
            )

            is_outside = distance > radius
            new_status = "이탈" if is_outside else "안전"
            previous_status = st.session_state.last_status

            now = datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S %z")

            st.session_state.last_check = timestamp
            st.session_state.last_distance = distance
            st.session_state.last_child_location = (
                child_lat,
                child_lon,
            )
            st.session_state.last_zone_name = zone_name.strip()

            # 안전 상태가 바뀔 때만 이벤트를 기록합니다.
            if previous_status != new_status:
                if is_outside:
                    event_type = "🚨 안전 구역 이탈"
                    message = (
                        f"{zone_name.strip()} 안전 구역을 벗어났습니다."
                    )
                else:
                    event_type = (
                        "✅ 안전 구역 복귀"
                        if previous_status == "이탈"
                        else "🟢 안전 상태 확인"
                    )
                    message = (
                        f"{zone_name.strip()} 안전 구역 안에 있습니다."
                    )

                st.session_state.events.insert(
                    0,
                    {
                        "확인 시각": timestamp,
                        "이벤트": event_type,
                        "안전 구역": zone_name.strip(),
                        "거리(m)": round(distance, 1),
                        "반경(m)": radius,
                        "위도": child_lat,
                        "경도": child_lon,
                        "내용": message,
                    },
                )

            st.session_state.last_status = new_status

    except (ValueError, OverflowError) as exc:
        st.error(f"위치 계산 중 문제가 발생했습니다: {exc}")
    except Exception:
        st.error(
            "위치를 확인하지 못했습니다. 입력값을 확인하고 다시 시도해 주세요."
        )


# --------------------------------------------------
# 현재 상태 대시보드
# --------------------------------------------------
st.divider()
st.subheader("📊 현재 안전 상태")

status = st.session_state.last_status
distance = st.session_state.last_distance

col1, col2, col3 = st.columns(3)

with col1:
    if status is None:
        st.metric("현재 상태", "확인 필요")
    elif status == "이탈":
        st.metric("현재 상태", "🚨 이탈")
    else:
        st.metric("현재 상태", "🟢 안전")

with col2:
    st.metric(
        "안전 구역까지의 거리",
        format_distance(distance) if distance is not None else "—",
    )

with col3:
    if distance is None:
        remaining = "—"
    elif distance <= radius:
        remaining = format_distance(radius - distance)
    else:
        remaining = format_distance(distance - radius)

    st.metric(
        "반경 여유 / 초과",
        remaining,
        help="안전 구역 안에서는 남은 거리, 밖에서는 초과 거리를 표시합니다.",
    )

if status == "이탈" and distance is not None:
    st.error(
        f"🚨 안전 구역 이탈 감지: "
        f"설정 반경보다 {format_distance(distance - radius)} "
        f"더 멀리 있습니다."
    )
elif status == "안전":
    st.success("현재 입력된 위치는 안전 구역 안에 있습니다.")
else:
    st.info("아이의 좌표를 확인하면 안전 상태가 여기에 표시됩니다.")

if st.session_state.last_check:
    st.caption(f"마지막 위치 확인: {st.session_state.last_check}")

if st.session_state.last_child_location:
    lat, lon = st.session_state.last_child_location
    st.caption(f"마지막 확인 좌표: {lat:.6f}, {lon:.6f}")


# --------------------------------------------------
# 샘플 좌표 테스트
# --------------------------------------------------
st.divider()
st.subheader("🧪 빠른 테스트")

st.write(
    "샘플 좌표는 현재 안전 구역 중심을 기준으로 생성합니다. "
    "아래 버튼을 누르면 해당 좌표가 표시되므로, "
    "위치 확인 폼에서 좌표를 입력한 뒤 판정할 수 있습니다."
)

sample_col1, sample_col2 = st.columns(2)

with sample_col1:
    st.markdown("**🟢 안전 구역 안**")
    st.code(
        f"위도: {center_lat:.6f}\n경도: {center_lon:.6f}",
        language="text",
    )

with sample_col2:
    st.markdown("**🔴 안전 구역 밖**")
    # 위도 약 0.01도 차이는 약 1.1km입니다.
    # 극지방에서도 유효한 좌표 범위를 유지합니다.
    sample_lat = max(-89.0, min(89.0, center_lat + 0.02))
    sample_lon = center_lon

    st.code(
        f"위도: {sample_lat:.6f}\n경도: {sample_lon:.6f}",
        language="text",
    )

st.caption(
    "샘플 좌표는 참고용입니다. 실제 거리는 안전 구역 중심과 "
    "샘플 좌표 사이의 거리로 계산됩니다."
)


# --------------------------------------------------
# 보호자 알림 이력
# --------------------------------------------------
st.divider()
st.subheader("🔔 보호자 알림 센터")

events = st.session_state.events

if events:
    alerts = [event for event in events if event["이벤트"] == "🚨 안전 구역 이탈"]
    safe_returns = [
        event for event in events
        if event["이벤트"] == "✅ 안전 구역 복귀"
    ]

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("기록된 이벤트", len(events))
    metric2.metric("이탈 이벤트", len(alerts))
    metric3.metric("복귀 이벤트", len(safe_returns))

    st.dataframe(
        events,
        use_container_width=True,
        hide_index=True,
    )

    # 표준 라이브러리만으로 CSV 파일 생성
    csv_buffer = io.StringIO()
    fieldnames = list(events[0].keys())

    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=fieldnames,
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(events)

    st.download_button(
        "⬇️ 알림 이력 CSV 다운로드",
        data=("\ufeff" + csv_buffer.getvalue()).encode("utf-8"),
        file_name="ansimzone_alert_history.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if st.button("알림 이력 초기화", type="secondary"):
        st.session_state.events = []
        st.session_state.last_status = None
        st.session_state.last_check = None
        st.session_state.last_distance = None
        st.session_state.last_child_location = None
        st.session_state.last_zone_name = None
        st.rerun()

else:
    st.info(
        "아직 기록된 이벤트가 없습니다. "
        "아이의 위치를 확인하면 이력이 생성됩니다."
    )


# --------------------------------------------------
# 하단 안내
# --------------------------------------------------
st.divider()
st.markdown("### 🔐 개인정보 및 사용 안내")
st.markdown(
    """
    - 좌표는 위치 판정에 사용됩니다. 아이의 위치를 입력할 때 보호자의
      동의를 받고 필요한 정보만 사용하세요.
    - 알림 이력은 현재 브라우저 세션에 연결된 Streamlit 세션 상태에
      저장됩니다. 앱 재시작이나 세션 종료 후에도 보존되는 영구 저장소는 아닙니다.
    - 여러 보호자에게 실시간 알림을 전달하려면 별도의 서버 저장소와
      이메일·문자·푸시 알림 서비스를 연결해야 합니다.
    - 이 앱의 결과만으로 아이의 안전을 보장할 수는 없습니다.
    """
)
3. requirements.txt
프로젝트에 requirements.txt 파일을 만들고 다음 한 줄만 입력하세요.


text

streamlit>=1.40.0,<2.0.0
별도의 지도 라이브러리, 데이터베이스, AI 라이브러리는 필요하지 않습니다.

4. Secrets 설정 방법
설정할 Secrets가 없습니다.

이 앱은 Gemini API나 외부 서비스 API를 사용하지 않으므로 GEMINI_API_KEY를 등록할 필요가 없습니다. 따라서 API 키 누락이나 API 호출 오류 없이 실행할 수 있습니다.

5. GitHub에 올리고 배포하기
1단계. GitHub 저장소 만들기
GitHub Vs. Bitbucket: Which Code Hosting Platform is Best? - Hatica
GitHub 저장소 생성

GitHub 에 로그인한 다음 New repository를 클릭합니다.

Repository name: ansimzone

공개 여부: Public 권장

Create repository 클릭

2단계. 파일 2개 업로드
저장소에 다음 구조로 파일을 올립니다.

ansimzone/

app.py

위에 제공한 전체 Python 코드

requirements.txt

Streamlit 의존성 한 줄

GitHub 저장소 화면에서 Add file → Create new file을 선택해 각 파일을 만들고 코드를 붙여 넣은 뒤 커밋하면 됩니다.

3단계. Streamlit Community Cloud 배포
① Streamlit Community Cloud 접속

share.streamlit.io 에 접속한 후 GitHub 계정으로 로그인합니다.

② 앱 생성

Create app을 선택하고 다음 정보를 입력합니다.

Repository: 본인의 ansimzone 저장소

Branch: main

Main file path: app.py

③ Deploy

Deploy를 클릭하면 의존성 설치와 앱 실행이 진행됩니다. 정상적으로 배포되면 공유할 수 있는 웹 주소가 제공됩니다.

6. 배포 후 테스트 방법
앱 왼쪽 메뉴에서 안전 구역 이름과 반경을 설정합니다.

아이 위치에 안전 구역 중심 좌표를 입력하고 위치 확인하기를 누릅니다.

상태가 안전으로 표시되는지 확인합니다.

안전 구역 밖에 있는 위도·경도를 입력하고 다시 확인합니다.

이탈 상태와 보호자 알림 센터의 이탈 기록이 생성되는지 확인합니다.

CSV 다운로드로 알림 이력을 저장할 수 있는지 확인합니다.

7. 현재 버전과 향후 확장 기능
기능

현재 버전

안전 구역 및 반경 설정

지원

좌표 기반 거리 계산

지원

안전·이탈 판정

지원

이탈 및 복귀 이력

지원

CSV 다운로드

지원

실시간 GPS 자동 추적

미지원

실제 SMS·푸시 알림

미지원

앱을 닫은 뒤에도 유지되는 이력

미지원

실제 서비스로 발전시키려면 다음 순서가 적합합니다.

1순위: 아이의 스마트폰에서 GPS 좌표를 자동으로 전송하도록 모바일 클라이언트 연결

2순위: 보호자 계정과 서버 데이터베이스를 추가해 위치 및 이력 저장

3순위: 이탈 이벤트가 발생하면 이메일 또는 문자 알림 전송

4순위: 지도 화면과 마지막 위치 갱신 시각 표시

특히 아이의 위치 정보는 민감한 개인정보이므로 보호자 인증, 전송 구간 암호화, 위치 정보 보관 기간 설정을 적용하는 것이 좋습니다.

이 구성은 GitHub에 업로드해 바로 배포를 시도할 수 있는 최소 의존성의 Streamlit 앱입니다. 다만 배포 성공 여부는 실제 저장소의 파일 내용과 Streamlit Cloud의 실행 환경에 따라 달라질 수 있으며, 실제 GPS 추적 및 외부 알림 기능은 별도 구현이 필요합니다.


ChatGPT는 AI라 실수할 수 있습니다.





     
