import streamlit as st

import math
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="꼬마 안전 지킴이",
    page_icon="🛝",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background-color: #FFFDF5;
    color: #30352F;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.hero {
    background: #FFF0BD;
    border: 2px solid #41473C;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    box-shadow: 4px 4px 0 #41473C;
    margin-bottom: 25px;
}
.hero h1 {
    color: #304C3B;
    font-size: 2.2rem;
}
.sketch-card {
    background: white;
    border: 2px solid #50564C;
    border-radius: 15px;
    padding: 18px;
    min-height: 145px;
    box-shadow: 3px 3px 0 #D8D6C8;
}
.safe {
    background: #E4F4D9;
    border: 2px solid #43804C;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
}
.danger {
    background: #FFE2D9;
    border: 2px solid #C94C3B;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

def calculate_distance(lat1, lon1, lat2, lon2):
    values = [lat1, lon1, lat2, lon2]

    if not all(math.isfinite(float(v)) for v in values):
        raise ValueError("좌표를 올바르게 입력해 주세요.")

    if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90):
        raise ValueError("위도는 -90~90 사이여야 합니다.")

    if not (-180 <= lon1 <= 180 and -180 <= lon2 <= 180):
        raise ValueError("경도는 -180~180 사이여야 합니다.")

    earth_radius = 6371000

    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    a = min(1.0, max(0.0, a))

    return 2 * earth_radius * math.asin(math.sqrt(a))

if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

with st.sidebar:
    st.header("⚙️ 안전 설정")

    playground_name = st.text_input(
        "놀이터 이름",
        value="우리 동네 놀이터",
    )

    st.subheader("📍 놀이터 중심 좌표")

    center_lat = st.number_input(
        "중심 위도",
        min_value=-90.0,
        max_value=90.0,
        value=37.566500,
        format="%.6f",
    )

    center_lon = st.number_input(
        "중심 경도",
        min_value=-180.0,
        max_value=180.0,
        value=126.978000,
        format="%.6f",
    )

    radius = st.slider(
        "안전 반경 (미터)",
        min_value=20,
        max_value=1000,
        value=100,
        step=10,
    )

    st.caption("기본 좌표는 서울 시청 부근의 예시 좌표입니다.")

st.markdown(f"""
<div class="hero">
    <h1>🛝 꼬마 안전 지킴이</h1>
    <p>놀이터를 벗어나면 보호자에게 알려요!</p>
    <p>📍 {playground_name}</p>
</div>
""", unsafe_allow_html=True)

st.subheader("🌼 안전 지킴이 사용 방법")

steps = [
    ("1. 🛝", "안전 구역 설정", "놀이터 위치와 반경을 정해요."),
    ("2. 🧒", "위치 입력", "아이의 좌표를 입력해요."),
    ("3. 🔔", "이탈 감지", "안전 구역 밖인지 확인해요."),
    ("4. 💌", "안전 확인", "결과와 확인 기록을 살펴봐요."),
]

cols = st.columns(4)

for col, (emoji, title, desc) in zip(cols, steps):
    with col:
        st.markdown(
            f"""
            <div class="sketch-card">
                <h3>{emoji}</h3>
                <b>{title}</b>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

st.subheader("🧒 아이의 현재 위치")

st.write(
    "아이의 위도와 경도를 입력한 다음 위치 확인 버튼을 눌러주세요."
)

with st.form("location_form"):
    col1, col2 = st.columns(2)

    with col1:
        child_lat = st.number_input(
            "아이의 위도",
            min_value=-90.0,
            max_value=90.0,
            value=float(center_lat),
            format="%.6f",
        )

    with col2:
        child_lon = st.number_input(
            "아이의 경도",
            min_value=-180.0,
            max_value=180.0,
            value=float(center_lon),
            format="%.6f",
        )

    submitted = st.form_submit_button(
        "🔎 아이 위치 확인하기",
        type="primary",
        use_container_width=True,
    )

if submitted:
    try:
        distance = calculate_distance(
            center_lat,
            center_lon,
            child_lat,
            child_lon,
        )

        is_safe = distance <= radius

        checked_at = datetime.now().astimezone().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        st.session_state.result = {
            "distance": distance,
            "is_safe": is_safe,
            "time": checked_at,
            "latitude": child_lat,
            "longitude": child_lon,
        }

        st.session_state.history.insert(
            0,
            {
                "확인 시각": checked_at,
                "거리(m)": round(distance, 1),
                "상태": "안전" if is_safe else "이탈",
            },
        )

        st.session_state.history = st.session_state.history[:20]

    except (ValueError, TypeError, OverflowError) as exc:
        st.error(f"위치를 확인할 수 없습니다: {exc}")
    except Exception as exc:
        st.error(f"오류가 발생했습니다: {exc}")

st.divider()
st.subheader("🚦 안전 상태")

result = st.session_state.result

if result is None:
    st.info("아이의 위치를 입력하고 확인 버튼을 눌러주세요.")

elif result["is_safe"]:
    st.markdown(
        f"""
        <div class="safe">
            <h2>🟢 안전 구역 안이에요!</h2>
            <p>아이의 위치가 설정된 놀이터 범위 안에 있습니다.</p>
            <h1>{result['distance']:.1f}m</h1>
            <p>놀이터 중심으로부터의 거리</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success("현재 입력된 좌표는 안전 구역 안에 있습니다.")

else:
    st.markdown(
        f"""
        <div class="danger">
            <h2>🚨 안전 구역을 벗어났어요!</h2>
            <p>보호자가 아이의 안전을 확인해 주세요.</p>
            <h1>{result['distance']:.1f}m</h1>
            <p>설정된 안전 반경: {radius}m</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.error("🚨 이탈 경고! 아이의 안전을 직접 확인해 주세요.")

if result is not None:
    st.caption(f"마지막 확인 시각: {result['time']}")

    st.write("**안전 반경 대비 거리**")
    st.progress(min(result["distance"] / radius, 1.0))

    st.caption(
        f"현재 거리: {result['distance']:.1f}m / "
        f"안전 반경: {radius}m"
    )

st.divider()
st.subheader("📋 최근 위치 확인 기록")

if st.session_state.history:
    st.dataframe(
        st.session_state.history,
        use_container_width=True,
        hide_index=True,
    )

    if st.button("🧹 기록 지우기"):
        st.session_state.history = []
        st.rerun()
else:
    st.caption("아직 확인 기록이 없습니다.")

st.divider()

st.warning(
    "이 앱은 입력한 좌표를 버튼을 눌렀을 때 확인하는 시제품입니다. "
    "자동 GPS 추적 및 실제 보호자 알림은 포함되어 있지 않습니다."
)

st.caption("꼬마 안전 지킴이 · 어린이 안전 위치 확인 서비스")
