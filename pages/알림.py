
import math
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="안심 탐험대 🍓",
    page_icon="🍓",
    layout="wide",
)

# ---------- 디자인 ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Nunito:wght@400;600;700;800&display=swap');

.stApp {
    background: #fff8f5;
    color: #59464b;
    font-family: 'Nunito', sans-serif;
}
[data-testid="stSidebar"] {
    background: #ffe5ec;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}
h1, h2, h3, p, label {
    font-family: 'Jua', sans-serif;
}
h1 { color: #df7291; }
h2, h3 { color: #bf7189; }

.hero {
    background: linear-gradient(135deg, #ffdce6, #fff0c9);
    padding: 30px;
    border: 3px solid white;
    border-radius: 30px;
    box-shadow: 0 7px 0 #f5d1dc;
    margin-bottom: 24px;
}
.hero h1 {
    font-family: 'Jua', sans-serif;
    font-size: 2.8rem;
    margin: 0;
}
.hero p {
    font-size: 1.05rem;
    color: #966777;
    margin-bottom: 0;
}
.sticker {
    background: white;
    border: 2px dashed #f2b5c6;
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 18px;
}
.status-safe {
    background: #e9f5df;
    border: 2px solid #c5dfb4;
    border-radius: 24px;
    padding: 22px;
    color: #47754c;
    margin: 14px 0;
}
.status-danger {
    background: #ffe3e1;
    border: 2px solid #f4aaa8;
    border-radius: 24px;
    padding: 22px;
    color: #a6424e;
    margin: 14px 0;
}
div.stButton > button {
    border-radius: 18px;
    min-height: 3rem;
    border: 2px solid #f5c6d4;
    background: #fff;
    color: #bb6682;
    font-family: 'Jua', sans-serif;
    font-size: 1rem;
    transition: 0.2s;
}
div.stButton > button:hover {
    background: #ffe4ed;
    border-color: #e99bb4;
    color: #a74f6d;
}
div.stButton > button[kind="primary"] {
    background: #e981a0;
    border: 2px solid #e981a0;
    color: white;
}
div.stButton > button[kind="primary"]:hover {
    background: #d96789;
    color: white;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.75);
    border-radius: 24px;
    border-color: #f6dce3;
}
div[data-testid="stMetric"] {
    background: white;
    border: 2px solid #f6dce3;
    padding: 15px;
    border-radius: 20px;
}
hr { border-color: #f4d6df; }
.small-note {
    color: #a17b86;
    font-size: .9rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- 상태 저장 ----------
if "help_requested" not in st.session_state:
    st.session_state.help_requested = False
if "help_time" not in st.session_state:
    st.session_state.help_time = ""
if "help_message" not in st.session_state:
    st.session_state.help_message = "도움이 필요해요. 저를 확인해 주세요."

# ---------- 상단 배너 ----------
st.markdown("""
<div class="hero">
    <div style="font-size:2.2rem">🍓 🐰 🌷</div>
    <h1>안심 탐험대</h1>
    <p>오늘도 안전하고 행복하게 탐험하자! ♡</p>
    <div style="margin-top:12px">✿ 작은 발걸음도 소중하게 ✿</div>
</div>
""", unsafe_allow_html=True)

# ---------- 사이드바 ----------
with st.sidebar:
    st.markdown("# 🎀 탐험 수첩")
    st.write("오늘의 탐험 준비 완료?")
    mode = st.radio(
        "사용 모드 선택",
        ["🧸 보호자 모드", "🐰 아이 모드"]
    )
    st.markdown("---")
    st.markdown("### 🍀 안전 약속")
    st.write("🌷 안전 구역 확인하기")
    st.write("🍓 위치를 바르게 입력하기")
    st.write("🧸 어려우면 어른에게 알리기")
    st.markdown("---")
    st.caption("made with ♡ · 안심 탐험대")

# ---------- 거리 계산 ----------
def distance_m(lat1, lon1, lat2, lon2):
    r = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1) * math.cos(p2)
        * math.sin(dl / 2) ** 2
    )
    a = min(1.0, max(0.0, a))
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# ---------- 본문 배치 ----------
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown("""
    <div class="sticker">
        <h3>🗺️ 나의 안전 지도</h3>
        <div class="small-note">
        놀이터와 아이의 좌표를 입력하면 거리를 계산해 줘요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 🌳 놀이터 위치")
        a, b = st.columns(2)
        with a:
            park_lat = st.number_input(
                "놀이터 위도", value=37.5665, format="%.6f"
            )
        with b:
            park_lon = st.number_input(
                "놀이터 경도", value=126.9780, format="%.6f"
            )

        radius = st.slider(
            "💚 안전 구역 크기",
            min_value=20, max_value=1000,
            value=100, step=10,
            format="%d m"
        )

        st.markdown("---")
        st.markdown("### 🐰 아이의 위치")
        c, d = st.columns(2)
        with c:
            child_lat = st.number_input(
                "아이 위도", value=37.5668, format="%.6f"
            )
        with d:
            child_lon = st.number_input(
                "아이 경도", value=126.9782, format="%.6f"
            )

        check = st.button(
            "🍓 안전 확인하기",
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
        dist = distance_m(park_lat, park_lon, child_lat, child_lon)

        if dist <= radius:
            st.markdown(f"""
            <div class="status-safe">
                <div style="font-size:2.4rem">🌼 🐰 🌼</div>
                <h3>안전 구역 안이에요!</h3>
                놀이터 중심에서 약 <b>{dist:.0f}m</b> 떨어져 있어요.<br>
                오늘도 즐거운 탐험을 해 봐요 ♡
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-danger">
                <div style="font-size:2.4rem">🚨 🍓 🚨</div>
                <h3>안전 구역 밖이에요!</h3>
                놀이터 중심에서 약 <b>{dist:.0f}m</b> 떨어져 있어요.<br>
                보호자와 함께 위치를 확인해 주세요.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 📍 지도 미리보기")
        st.map(pd.DataFrame({
            "latitude": [park_lat, child_lat],
            "longitude": [park_lon, child_lon],
        }))

        if check:
            st.toast("안전 확인 완료! 🍓")
    else:
        st.error("위도와 경도 값을 확인해 주세요.")

with right:
    st.markdown("""
    <div class="sticker">
        <h3>🆘 도움 요청 우체통</h3>
        <div class="small-note">
        도움이 필요할 때 요청 상태를 남길 수 있어요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if mode == "🐰 아이 모드":
        st.markdown("""
        <div class="status-danger">
            <div style="font-size:2.5rem">🧸 💌</div>
            <h3>괜찮아, 도움을 요청해도 돼!</h3>
            아래 버튼을 눌러 요청을 등록해 줘.
        </div>
        """, unsafe_allow_html=True)

        st.session_state.help_message = st.text_area(
            "💌 전달할 메시지",
            value=st.session_state.help_message,
            max_chars=250,
            placeholder="예: 보호자를 찾고 있어요."
        )

        if st.button(
            "🆘 도움 요청 보내기",
            type="primary",
            use_container_width=True
        ):
            st.session_state.help_requested = True
            st.session_state.help_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            st.rerun()

        if st.session_state.help_requested:
            st.markdown(f"""
            <div class="status-danger">
                <h3>💌 요청 상태가 등록됐어요!</h3>
                시간: {st.session_state.help_time}<br>
                내용: {st.session_state.help_message}
            </div>
            """, unsafe_allow_html=True)
            st.warning(
                "이 요청은 현재 앱 화면에만 저장돼요. "
                "다른 휴대전화로 실제 알림이 전송되지는 않아요."
            )
            if st.button("확인 완료 ♡", use_container_width=True):
                st.session_state.help_requested = False
                st.session_state.help_time = ""
                st.rerun()

    else:
        st.markdown("""
        <div class="status-safe">
            <div style="font-size:2.5rem">💗 🏡 💗</div>
            <h3>보호자 안전 수첩</h3>
            아이의 안전 구역과 도움 요청 상태를 확인해요.
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.help_requested:
            st.markdown(f"""
            <div class="status-danger">
                <h3>🚨 도움 요청 상태</h3>
                시간: {st.session_state.help_time}<br>
                내용: {st.session_state.help_message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("현재 등록된 도움 요청이 없어요. 🌷")

        st.caption("현재 버전은 기기 간 자동 공유를 지원하지 않아요.")

# ---------- 하단 ----------
st.markdown("---")
st.markdown("""
<div style="
    text-align:center;
    background:#ffe8ef;
    border:2px dashed #efb7c8;
    border-radius:24px;
    padding:24px;
">
    <div style="font-size:2rem">🍓 🐰 🌷 🧸</div>
    <h3>오늘도 무사히, 행복하게!</h3>
    <p style="color:#9b7180">
    안심 탐험대와 함께하는 작은 모험 ♡
    </p>
    <div style="font-size:.8rem;color:#a17b86">
    학습용 시제품 · 실제 GPS 추적이나 긴급 알림 서비스가 아닙니다.
    </div>
</div>
""", unsafe_allow_html=True)
