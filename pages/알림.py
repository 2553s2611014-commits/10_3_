
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
}
div.stButton > button[kind="primary"] {
    background: #e981a0;
    border: 2px solid #e981a0;
    color: white;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.75);
    border-radius: 24px;
    border-color: #f6dce3;
}
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

# ---------- 상단 ----------
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
    st.write("🎤 마이크는 직접 허용하기")
    st.write("🆘 위험하면 어른에게 알리기")
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

# ---------- 화면 배치 ----------
left, right = st.columns([1.15, 0.85], gap="large")

# ---------- 안전 지도 ----------
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
            min_value=20,
            max_value=1000,
            value=100,
            step=10,
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
        dist = distance_m(
            park_lat, park_lon, child_lat, child_lon
        )

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

# ---------- 도움 요청과 마이크 ----------
with right:
    st.markdown("""
    <div class="sticker">
        <h3>🆘 도움 요청 우체통</h3>
        <div class="small-note">
        도움이 필요하면 요청을 등록하고, 원할 때 짧은 소리를 녹음해 확인해요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if mode == "🐰 아이 모드":
        st.markdown("""
        <div class="status-danger">
            <div style="font-size:2.5rem">🧸 💌</div>
            <h3>도움이 필요하나요?</h3>
            아래에서 도움 요청을 등록할 수 있어요.
        </div>
        """, unsafe_allow_html=True)

        st.session_state.help_message = st.text_area(
            "💌 전달할 메시지",
            value=st.session_state.help_message,
            max_chars=250,
            placeholder="예: 보호자를 찾고 있어요."
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
            st.markdown(f"""
            <div class="status-danger">
                <h3>💌 도움 요청이 등록됐어요!</h3>
                시간: {st.session_state.help_time}<br>
                내용: {st.session_state.help_message}
            </div>
            """, unsafe_allow_html=True)

            st.warning(
                "요청은 현재 앱 화면에 표시됩니다. "
                "보호자 휴대전화로 자동 전송되지는 않습니다."
            )

            if st.button("확인 완료 ♡", use_container_width=True):
                st.session_state.help_requested = False
                st.session_state.help_time = ""
                st.rerun()

        st.markdown("---")
        st.markdown("### 🎤 마이크로 소리 확인하기")
        st.info(
            "주변 소리를 녹음하려면 직접 시작 버튼을 누르고 "
            "브라우저의 마이크 권한을 허용해 주세요. "
            "다른 사람에게 녹음 사실을 알리고 동의를 받아 주세요."
        )

        try:
            audio = st.audio_input(
                "🎙️ 녹음 시작하기",
                sample_rate=16000,
                key="child_audio"
            )

            if audio is not None:
                st.success("🔴 녹음이 완료됐어요!")
                st.audio(audio, format="audio/wav")
                st.caption(
                    "녹음된 소리는 이 화면에서 재생할 수 있어요. "
                    "보호자에게 전송되지는 않습니다."
                )
        except Exception:
            st.warning(
                "현재 Streamlit 버전에서 마이크 입력을 지원하지 않을 수 있어요. "
                "requirements.txt에 streamlit을 입력하고 앱을 다시 실행해 주세요."
            )

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

        st.markdown("""
        <div class="sticker">
            <h3>🎧 주변 소리 기능 안내</h3>
            아이 기기에서 직접 녹음한 소리는 현재 해당 화면에서만 재생할 수 있어요.
            보호자 기기로 실시간 전달하려면 별도의 기기 연결 기능이 필요해요.
        </div>
        """, unsafe_allow_html=True)

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
    학습용 시제품 · 실제 GPS 추적이나 기기 간 긴급 알림은 지원하지 않습니다.
    </div>
</div>
""", unsafe_allow_html=True)
