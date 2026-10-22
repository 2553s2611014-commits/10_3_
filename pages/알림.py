
import math
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="안심 탐험대",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- 예쁜 디자인 ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

.stApp {
    background: linear-gradient(145deg, #f4faf1, #fffaf0);
    font-family: 'Nunito', sans-serif;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: #e6f2df;
}

.hero {
    background: linear-gradient(120deg, #285943, #76a96c);
    color: white;
    padding: 32px;
    border-radius: 28px;
    margin-bottom: 24px;
    box-shadow: 0 10px 28px #315b351c;
}

.hero h1 {
    color: white;
    font-size: 2.6rem;
    font-weight: 900;
    margin: 0;
}

.hero p {
    color: #eff9e9;
    font-size: 1.05rem;
    margin-bottom: 0;
}

.eyebrow {
    font-size: .85rem;
    letter-spacing: 2px;
    font-weight: 800;
    opacity: .85;
    margin-bottom: 8px;
}

.card {
    background: rgba(255,255,255,.92);
    border: 1px solid #e0ebd9;
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 8px 24px #304b2810;
}

.card h3 {
    color: #285943;
    margin-top: 0;
}

.small {
    color: #72806d;
    font-size: .92rem;
}

.safe {
    background: #e4f6df;
    color: #285943;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #c7e6bb;
    font-weight: 800;
    margin: 14px 0;
}

.danger {
    background: #fff0e7;
    color: #a54325;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #ffd0b8;
    font-weight: 800;
    margin: 14px 0;
}

div.stButton > button {
    border-radius: 15px;
    min-height: 3rem;
    font-weight: 800;
    border: 1px solid #d7e6cf;
}

div.stButton > button[kind="primary"] {
    background: #d96d52;
    color: white;
    border: none;
}

h1, h2, h3 {
    letter-spacing: -0.5px;
}
</style>
""", unsafe_allow_html=True)


# ---------- 기억할 정보 ----------
if "help_requested" not in st.session_state:
    st.session_state.help_requested = False

if "help_time" not in st.session_state:
    st.session_state.help_time = ""

if "help_message" not in st.session_state:
    st.session_state.help_message = "도움이 필요해요. 제 위치를 확인해 주세요."


# ---------- 제목 ----------
st.markdown("""
<div class="hero">
    <div class="eyebrow">LITTLE EXPLORERS · SAFETY FIRST</div>
    <h1>🌿 안심 탐험대</h1>
    <p>마음껏 놀고, 안심하고 돌아오자! 🧸</p>
</div>
""", unsafe_allow_html=True)


# ---------- 메뉴 ----------
with st.sidebar:
    st.markdown("## 🏡 탐험대 본부")
    st.write("안녕하세요! 안전하게 탐험해 봐요.")
    mode = st.radio(
        "누가 사용하나요?",
        ["🧑‍🧑‍🧒 보호자 모드", "🧒 아이 모드"]
    )

    st.markdown("---")
    st.markdown("### 🍀 안전 약속")
    st.write("📍 정해진 안전 구역 확인하기")
    st.write("💬 도움이 필요하면 알리기")
    st.write("👨‍👩‍👧 보호자와 함께 사용하기")
    st.markdown("---")
    st.caption("안심 탐험대 · 학습용 시제품")


# ---------- 거리 계산 ----------
def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371000

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1) * math.cos(p2)
        * math.sin(dl / 2) ** 2
    )
    a = min(1.0, max(0.0, a))

    return earth_radius * 2 * math.atan2(
        math.sqrt(a), math.sqrt(1 - a)
    )


# ---------- 메인 화면 ----------
map_col, help_col = st.columns([1.15, 0.85], gap="large")


# ---------- 지도와 안전 구역 ----------
with map_col:
    st.markdown("""
    <div class="card">
        <h3>🗺️ 우리 동네 안전 지도</h3>
        <div class="small">
        놀이터 위치와 아이의 위치를 입력하면 거리를 확인할 수 있어요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 🌳 놀이터 위치")

        c1, c2 = st.columns(2)
        with c1:
            park_lat = st.number_input(
                "놀이터 위도",
                value=37.5665,
                format="%.6f",
                help="놀이터의 위도 좌표를 입력하세요."
            )
        with c2:
            park_lon = st.number_input(
                "놀이터 경도",
                value=126.9780,
                format="%.6f",
                help="놀이터의 경도 좌표를 입력하세요."
            )

        radius = st.slider(
            "🟢 안전 구역 반경",
            min_value=20,
            max_value=1000,
            value=100,
            step=10,
            format="%d m"
        )

        st.markdown("---")
        st.markdown("### 🧒 아이의 위치")

        c3, c4 = st.columns(2)
        with c3:
            child_lat = st.number_input(
                "아이 위도",
                value=37.5668,
                format="%.6f"
            )
        with c4:
            child_lon = st.number_input(
                "아이 경도",
                value=126.9782,
                format="%.6f"
            )

        check_location = st.button(
            "🌱 안전 구역 확인하기",
            type="primary",
            use_container_width=True
        )

    valid = (
        -90 <= park_lat <= 90
        and -180 <= park_lon <= 180
        and -90 <= child_lat <= 90
        and -180 <= child_lon <= 180
    )

    if valid:
        distance = calculate_distance(
            park_lat, park_lon, child_lat, child_lon
        )

        if distance > radius:
            st.markdown(
                f"""
                <div class="danger">
                    <div style="font-size:2rem">🚨</div>
                    <div style="font-size:1.2rem">안전 구역 밖이에요!</div>
                    놀이터 중심에서 약 {distance:.0f}m 떨어져 있어요.
                    보호자와 함께 위치를 확인해 주세요.
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="safe">
                    <div style="font-size:2rem">🌼</div>
                    <div style="font-size:1.2rem">안전 구역 안이에요!</div>
                    놀이터 중심에서 약 {distance:.0f}m 떨어져 있어요.
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### 📍 위치 미리보기")
        st.map(pd.DataFrame({
            "latitude": [park_lat, child_lat],
            "longitude": [park_lon, child_lon],
        }))

        if check_location:
            st.toast("안전 구역 확인 완료! 🌿")

    else:
        st.error("위도와 경도 값을 다시 확인해 주세요.")


# ---------- 긴급 도움 요청 ----------
with help_col:
    st.markdown("""
    <div class="card">
        <h3>🆘 긴급 도움 센터</h3>
        <div class="small">
        혼자 해결하기 어려울 때 도움 요청 상태를 등록할 수 있어요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if mode == "🧒 아이 모드":
        st.markdown("""
        <div class="danger">
            <div style="font-size:2.5rem">🧸</div>
            <div style="font-size:1.15rem">도움이 필요하나요?</div>
            아래 버튼을 눌러 도움 요청을 등록해요.
        </div>
        """, unsafe_allow_html=True)

        st.session_state.help_message = st.text_area(
            "💌 전달할 메시지",
            value=st.session_state.help_message,
            max_chars=250,
            placeholder="예: 놀이터에서 보호자를 찾고 있어요."
        )

        if st.button(
            "🆘 도움 요청하기",
            type="primary",
            use_container_width=True
        ):
            st.session_state.help_requested = True
            st.session_state.help_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            st.rerun()

        if st.session_state.help_requested:
            st.markdown(
                f"""
                <div class="danger">
                    <h3>🚨 도움 요청이 등록됐어요</h3>
                    <p>요청 시간: {st.session_state.help_time}</p>
                    <p>메시지: {st.session_state.help_message}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.warning(
                "이 화면에 요청 상태가 표시됩니다. "
                "다른 휴대전화로 자동 전송되지는 않아요."
            )

            if st.button("요청 확인 완료", use_container_width=True):
                st.session_state.help_requested = False
                st.session_state.help_time = ""
                st.rerun()

    else:
        st.markdown("""
        <div class="safe">
            <div style="font-size:2.5rem">💚</div>
            <div style="font-size:1.2rem">보호자 안전 관제실</div>
            아이의 안전 구역과 도움 요청 상태를 확인해요.
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.help_requested:
            st.markdown(
                f"""
                <div class="danger">
                    <h3>🚨 도움 요청 상태</h3>
                    <p>요청 시간: {st.session_state.help_time}</p>
                    <p>메시지: {st.session_state.help_message}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("현재 등록된 도움 요청이 없어요. 🌱")

        st.caption(
            "현재 버전은 서로 다른 기기 간 자동 공유를 지원하지 않습니다."
        )


# ---------- 하단 안내 ----------
st.markdown("---")
st.markdown("""
<div style="
    text-align:center;
    padding:18px;
    color:#71816b;
">
    <div style="font-size:1.5rem">🌿 🧸 🌼</div>
    <b>안심 탐험대</b><br>
    작은 탐험도 안전하게, 매일매일 즐겁게!<br>
    <span style="font-size:.8rem">
    학습용 시제품 · 실제 GPS 추적 및 긴급 알림 서비스가 아닙니다.
    </span>
</div>
""", unsafe_allow_html=True)
