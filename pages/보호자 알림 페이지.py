import streamlit as st
st.title('아아아아')
st.write('ㅏ라라')
로그인
무료로 회원가입
나의 말:
GitHub에 올려서 Streamlit Community Cloud로 배포할 수 있는 Streamlit 앱을 만들어줘.
주제: [입력]
원하는 기능: [입력] (없으면 비워두기)
추가 요청사항: [선택]
규칙:
주제에 가장 적합한 기능과 화면 구성을 스스로 설계할 것
원하는 기능이 있으면 반드시 반영할 것
기능이 비어 있으면 주제에 맞게 필요한 기능을 스스로 제안하고 구현할 것
모든 앱이 동일한 형태가 되지 않도록 주제에 맞게 차별화할 것
오류가 발생하지 않도록 가장 단순하고 안정적인 방식으로 구현할 것
Streamlit Community Cloud에서 바로 배포 가능해야 함
실행 즉시 가능한 완전한 코드 제공
필요한 라이브러리만 사용
예외 처리 포함
초보자가 그대로 복사하여 사용할 수 있게 작성
AI 기능이 필요한 경우에만:
gemini-2.5-flash-lite 사용
Secret 이름은 반드시 GEMINI_API_KEY
API 오류 처리 포함
출력:앱 기획 설명app.pyrequirements.txtSecrets 설정 방법(필요 시)배포 방법

최우선 목표는 오류 없이 실행되는 것이며, 주제에 맞는 완성도 높은 앱을 만드는 것이다.

ChatGPT의 말:
좋아요. GitHub에 업로드한 뒤 Streamlit Community Cloud에서 바로 배포할 수 있도록 실행 가능한 전체 코드와 배포 설정까지 한 번에 구성해 드릴게요.

먼저 앱의 주제만 알려주세요. 원하는 기능이 없다면 주제에 맞게 화면 구성과 기능을 직접 설계하겠습니다.

Streamlit 앱 만들기
1. 앱 주제 (필수)

보호자 알림 페이지
2. 원하는 기능 (선택)

아이의 위치가 보호자가 지정한 위치에서 벗어나면 보호자에게 알림이가는 기능
3. 추가 요청사항 (선택)

없음
완성본에 포함할 내용
앱 기획: 주제에 어울리는 화면 구성과 핵심 기능

app.py: 복사해서 바로 실행할 수 있는 전체 코드

requirements.txt: 필요한 라이브러리만 포함

오류 처리: 잘못된 입력, 빈 데이터, 파일 처리 등 예상 가능한 오류에 대응

배포 안내: GitHub 저장소 생성부터 Streamlit Community Cloud 배포까지 단계별 설명

Secrets 설정: AI 기능이 필요한 경우에만 GEMINI_API_KEY 설정 안내

특별한 기능을 지정하지 않아도 괜찮습니다. 주제에 맞게 앱의 디자인과 기능을 차별화하고, 불필요한 라이브러리나 복잡한 설정을 피하면서 안정적으로 실행되도록 만들겠습니다.


나의 말:
GitHub 및 Streamlit Community Cloud 배포용 앱을 완성해 줘.
주제: 보호자 알림 페이지
원하는 기능: 아이의 위치가 보호자가 지정한 위치에서 벗어나면 보호자에게 알림이가는 기능
추가 요청사항: 없음
요구사항: 완전한 app.py와 requirements.txt, 필요한 경우 GEMINI_API_KEY Secrets 설정, 배포 방법, 예외 처리, 초보자용 설명을 제공. 가장 단순하고 안정적인 구현을 우선하고, 코드 전체를 복사해서 바로 실행할 수 있게 작성해 줘.

ChatGPT의 말:
보호자 알림 페이지 — Streamlit 앱 완성본
이 앱은 보호자가 아이의 안전 구역을 지정하고, 아이의 위치가 그 구역을 벗어나면 보호자에게 알림을 보내는 웹 앱입니다. GitHub에 업로드하고 Streamlit Community Cloud에서 배포할 수 있도록 구성하겠습니다.

먼저 중요한 구현상의 차이가 있습니다. Streamlit 웹 앱만으로는 아이의 위치를 백그라운드에서 계속 추적하거나, 앱이 닫혀 있어도 자동으로 알림을 보낼 수 없습니다. 이를 안정적으로 구현하려면 아이의 휴대전화에서 위치를 전송하는 기능과 알림 전송 서비스가 추가로 필요합니다.

아래 첫 번째 버전은 실행 안정성을 우선해 다음 기능을 구현합니다.

보호자가 안전 구역의 중심 좌표와 허용 반경을 설정합니다.

아이의 현재 GPS 좌표를 입력하거나 기기의 위치를 가져와 안전 구역 이탈 여부를 확인합니다.

안전 구역 밖으로 벗어나면 화면에 경고를 표시하고 이탈 기록을 남깁니다.

보호자 연락처와 알림 설정을 관리할 수 있습니다.

실제 문자·푸시 알림 연동을 위한 확장 지점을 명확히 분리합니다.

1. 앱 기획 및 화면 구성
안전 구역 관리
보호자가 지정한 집, 학교, 학원 등의 중심 좌표와 안전 반경을 설정합니다.

위치 확인
아이의 위도와 경도를 입력해 안전 구역 내부인지 확인합니다. 두 지점 사이의 거리는 GPS 좌표를 이용해 계산합니다.

이탈 알림
안전 구역을 벗어나면 경고를 표시하고, SMTP 이메일 설정을 완료한 경우 보호자에게 이메일을 전송합니다.

이탈 기록
현재 브라우저 세션에서 확인한 위치와 이탈 여부를 기록하고 CSV 파일로 다운로드할 수 있습니다.

작동 방식
① 보호자가 안전 구역 설정

② 아이의 GPS 좌표 확인

③ 거리와 허용 반경 비교

구역 내부

정상 표시

구역 이탈

경고 및 이메일

2. GitHub 저장소 파일 구성
다음 두 파일만 있으면 기본 앱을 실행할 수 있습니다.


text
guardian-alert/
├── app.py
└── requirements.txt
이 버전에서는 AI API 키나 별도 위치 계산 라이브러리가 필요하지 않습니다.

3. app.py — 전체 코드
아래 코드를 그대로 복사해 app.py 파일로 저장하세요.


python

import csv
import io
import math
import re
import smtplib
import streamlit as st

from datetime import datetime
from email.message import EmailMessage


st.set_page_config(
    page_title="보호자 안전 알림",
    page_icon="🛡️",
    layout="centered",
)

st.title("🛡️ 보호자 안전 알림")
st.caption("아이의 위치가 지정한 안전 구역을 벗어나는지 확인합니다.")

# -----------------------------
# 초기 상태
# -----------------------------
if "records" not in st.session_state:
    st.session_state.records = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# -----------------------------
# 위치 계산
# -----------------------------
def valid_coordinates(lat, lon):
    return (
        -90 <= lat <= 90
        and -180 <= lon <= 180
        and math.isfinite(lat)
        and math.isfinite(lon)
    )


def distance_meters(lat1, lon1, lat2, lon2):
    """두 GPS 좌표 사이의 대략적인 지표면 거리를 미터로 계산합니다."""
    earth_radius = 6_371_000

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    delta_p = math.radians(lat2 - lat1)
    delta_l = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_p / 2) ** 2
        + math.cos(p1)
        * math.cos(p2)
        * math.sin(delta_l / 2) ** 2
    )
    a = min(1.0, max(0.0, a))

    return earth_radius * 2 * math.asin(math.sqrt(a))


# -----------------------------
# 이메일 알림
# -----------------------------
def send_alert_email(recipient, distance, radius, checked_at):
    """
    Streamlit Secrets에 SMTP 설정이 있을 때만 이메일을 전송합니다.
    SMTP 설정이 없거나 전송에 실패하면 False를 반환합니다.
    """
    try:
        host = st.secrets.get("SMTP_HOST", "")
        port = int(st.secrets.get("SMTP_PORT", 465))
        username = st.secrets.get("SMTP_USER", "")
        password = st.secrets.get("SMTP_PASSWORD", "")
        sender = st.secrets.get("ALERT_FROM_EMAIL", username)

        if not all([host, username, password, sender, recipient]):
            return False, "SMTP 설정이 없습니다."

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", recipient):
            return False, "보호자 이메일 주소를 확인해 주세요."

        message = EmailMessage()
        message["Subject"] = "[보호자 안전 알림] 안전 구역 이탈"
        message["From"] = sender
        message["To"] = recipient
        message.set_content(
            "아이의 위치가 지정된 안전 구역을 벗어났습니다.\n\n"
            f"확인 시각: {checked_at}\n"
            f"안전 구역 반경: {radius:.0f}m\n"
            f"구역 중심에서의 거리: {distance:.0f}m\n\n"
            "이 알림은 앱에서 위치를 확인한 시점에 생성되었습니다. "
            "실시간 백그라운드 추적을 의미하지 않습니다."
        )

        if port == 465:
            with smtplib.SMTP_SSL(host, port, timeout=10) as server:
                server.login(username, password)
                server.send_message(message)
        else:
            with smtplib.SMTP(host, port, timeout=10) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(message)

        return True, "이메일 전송을 요청했습니다."

    except Exception:
        # 로그인 정보나 서버 오류 내용을 화면에 노출하지 않습니다.
        return False, "이메일 전송에 실패했습니다. SMTP 설정을 확인해 주세요."


# -----------------------------
# 보호자 설정
# -----------------------------
st.sidebar.header("⚙️ 안전 구역 설정")

zone_name = st.sidebar.text_input(
    "안전 구역 이름",
    value="우리 집",
    max_chars=50,
)

zone_lat = st.sidebar.number_input(
    "안전 구역 중심 위도",
    min_value=-90.0,
    max_value=90.0,
    value=37.5665,
    format="%.6f",
)

zone_lon = st.sidebar.number_input(
    "안전 구역 중심 경도",
    min_value=-180.0,
    max_value=180.0,
    value=126.9780,
    format="%.6f",
)

radius = st.sidebar.number_input(
    "안전 구역 반경 (미터)",
    min_value=50,
    max_value=10000,
    value=300,
    step=50,
)

parent_email = st.sidebar.text_input(
    "보호자 이메일",
    placeholder="parent@example.com",
    help="SMTP 설정을 완료하면 이 주소로 이탈 알림을 보냅니다.",
)

st.sidebar.info(
    "위도와 경도는 지도 앱에서 확인할 수 있습니다. "
    "안전 구역 설정은 현재 세션에서 사용됩니다."
)

# -----------------------------
# 메인 화면
# -----------------------------
st.subheader("📍 현재 위치 확인")

st.write(
    f"**설정된 구역:** {zone_name or '이름 없음'}  \n"
    f"**허용 반경:** {radius:,}m"
)

st.caption(
    "현재 버전은 GPS 좌표를 직접 입력받습니다. "
    "휴대전화 위치를 자동으로 읽거나 백그라운드에서 추적하지 않습니다."
)

with st.form("location_form"):
    child_lat = st.number_input(
        "아이의 현재 위도",
        min_value=-90.0,
        max_value=90.0,
        value=37.5665,
        format="%.6f",
        help="예: 37.566500",
    )

    child_lon = st.number_input(
        "아이의 현재 경도",
        min_value=-180.0,
        max_value=180.0,
        value=126.9780,
        format="%.6f",
        help="예: 126.978000",
    )

    check_location = st.form_submit_button(
        "현재 위치 확인",
        type="primary",
        use_container_width=True,
    )

if check_location:
    try:
        if not zone_name.strip():
            st.error("안전 구역 이름을 입력해 주세요.")

        elif not valid_coordinates(zone_lat, zone_lon):
            st.error("안전 구역 좌표가 올바르지 않습니다.")

        elif not valid_coordinates(child_lat, child_lon):
            st.error("아이의 좌표가 올바르지 않습니다.")

        else:
            distance = distance_meters(
                zone_lat,
                zone_lon,
                child_lat,
                child_lon,
            )

            outside = distance > radius
            checked_at = datetime.now().astimezone().strftime(
                "%Y-%m-%d %H:%M:%S %Z"
            )

            record = {
                "확인 시각": checked_at,
                "안전 구역": zone_name.strip(),
                "위도": child_lat,
                "경도": child_lon,
                "거리(m)": round(distance, 1),
                "허용 반경(m)": radius,
                "상태": "이탈" if outside else "정상",
                "이메일 전송": "미시도",
            }

            if outside:
                sent, message = send_alert_email(
                    parent_email.strip(),
                    distance,
                    radius,
                    checked_at,
                )

                record["이메일 전송"] = (
                    "전송 요청 성공" if sent else "전송 실패 또는 미설정"
                )

                st.session_state.last_result = {
                    "outside": True,
                    "distance": distance,
                    "radius": radius,
                    "email_sent": sent,
                    "email_message": message,
                    "checked_at": checked_at,
                }
            else:
                st.session_state.last_result = {
                    "outside": False,
                    "distance": distance,
                    "radius": radius,
                    "email_sent": False,
                    "email_message": "",
                    "checked_at": checked_at,
                }

            st.session_state.records.append(record)

    except Exception:
        st.error("위치 확인 중 문제가 발생했습니다. 입력값을 확인하고 다시 시도해 주세요.")


# -----------------------------
# 확인 결과
# -----------------------------
result = st.session_state.last_result

if result is not None:
    st.divider()
    st.subheader("📊 확인 결과")

    distance = result["distance"]
    radius_value = result["radius"]

    col1, col2 = st.columns(2)
    col1.metric("구역 중심과의 거리", f"{distance:,.0f}m")
    col2.metric("허용 반경", f"{radius_value:,.0f}m")

    if result["outside"]:
        st.error(
            f"🚨 안전 구역 이탈! "
            f"설정된 반경보다 {distance - radius_value:,.0f}m 더 멀리 있습니다."
        )

        if result["email_sent"]:
            st.success("보호자 이메일 전송을 요청했습니다.")
        else:
            st.warning(
                "이탈은 확인했지만 이메일 알림을 보내지 못했습니다. "
                + result["email_message"]
            )
    else:
        st.success("✅ 안전 구역 안에 있습니다.")

    st.caption(f"마지막 확인 시각: {result['checked_at']}")

# -----------------------------
# 기록 및 CSV 다운로드
# -----------------------------
st.divider()
st.subheader("🕒 위치 확인 기록")

records = st.session_state.records

if records:
    st.dataframe(
        list(reversed(records)),
        use_container_width=True,
        hide_index=True,
    )

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=list(records[0].keys()),
    )
    writer.writeheader()
    writer.writerows(records)

    st.download_button(
        "📥 기록 CSV 다운로드",
        data=output.getvalue().encode("utf-8-sig"),
        file_name="guardian_alert_history.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if st.button("기록 삭제", type="secondary"):
        st.session_state.records = []
        st.session_state.last_result = None
        st.rerun()
else:
    st.info("아직 확인 기록이 없습니다.")

# -----------------------------
# 사용 안내
# -----------------------------
with st.expander("ℹ️ 사용 시 주의사항"):
    st.markdown(
        """
        - 위치 확인 버튼을 눌렀을 때만 위치를 검사합니다.
        - 앱이 닫혀 있거나 위치 확인을 하지 않으면 이탈을 감지하지 않습니다.
        - 이메일 알림은 SMTP Secrets 설정이 있어야 작동합니다.
        - 기록과 설정은 영구 저장되지 않으며 세션 종료 시 사라질 수 있습니다.
        - GPS 오차로 인해 경계 부근에서 판정이 달라질 수 있습니다.
        - 이 앱은 긴급 구조 시스템을 대체하지 않습니다.
        - 실제 아이의 위치 정보는 필요한 범위에서만 수집하고 보호해 주세요.
        """
    )
