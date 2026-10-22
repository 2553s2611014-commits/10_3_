
import math
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="안심 탐험대 ♡",
    page_icon="🍓",
    layout="wide",
)

# ──────────────── 🌷 디자인 ────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Nunito:wght@400;600;700;800;900&display=swap');

:root {
    --pink: #e982a2;
    --pink-dark: #bd6483;
    --pink-light: #ffe5ed;
    --cream: #fff9f1;
    --green: #dcebd0;
    --green-dark: #537650;
    --ink: #654c55;
}

.stApp {
    background:
        radial-gradient(circle at 5% 8%, #ffe3ec 0, transparent 19%),
        radial-gradient(circle at 95% 22%, #fff0c9 0, transparent 18%),
        #fff9f5;
    color: var(--ink);
    font-family: 'Nunito', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4, label, button {
    font-family: 'Jua', sans-serif !important;
}

h1 { color: var(--pink-dark); }
h2, h3, h4 { color: #bd718a; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffe2eb, #fff0dc);
    border-right: 2px solid white;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #bd6483;
}

.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(120deg, #ffd7e4 0%, #fff0ce 58%, #e5f1d9 100%);
    padding: 34px 30px;
    border: 3px solid white;
    border-radius: 32px;
    box-shadow: 0 8px 0 #f4cbd8, 0 15px 35px #d98ba51b;
    margin-bottom: 26px;
}

.hero:after {
    content: "♡  ✿  ♡";
    position: absolute;
    right: 20px;
    top: 18px;
    font-size: 27px;
    color: #d87f9d;
    transform: rotate(8deg);
}

.hero h1 {
    font-size: clamp(2.2rem, 5vw, 3.5rem);
    line-height: 1.2;
    margin: 8px 0;
    color: #b85d7b;
}

.hero p {
    font-size: 1.05rem;
    color: #966777;
    margin-bottom: 0;
}

.eyebrow {
    font-size: .8rem;
    letter-spacing: 3px;
    color: #ad6b7e;
    font-weight: 900;
}

.ribbon {
    display: inline-block;
    background: #e982a2;
    color: white;
    padding: 7px 15px;
    border-radius: 30px;
    box-shadow: 0 3px 0 #d76f90;
    font-family: 'Jua', sans-serif;
    margin: 8px 0 14px;
}

.section-title {
    font-family: 'Jua', sans-serif;
    font-size: 1.35rem;
    color: #bd6483;
    margin: 8px 0 14px;
}

.sticker {
    position: relative;
    background: rgba(255,255,255,.92);
    border: 2px solid white;
    outline: 1px dashed #efb7c8;
    outline-offset: -8px;
    border-radius: 25px;
    padding: 23px;
    margin: 5px 0 19px;
    box-shadow: 0 7px 20px #d58ba51a;
}

.sticker h3 {
    margin-top: 0;
}

.note {
    background: #fff0c9;
    border-left: 5px solid #efc66e;
    border-radius: 10px 18px 18px 10px;
    padding: 15px 17px;
    color: #8c6d46;
    margin: 12px 0;
}

.safe {
    background: linear-gradient(135deg, #e9f5df, #f9fff2);
    border: 2px solid #c5dfb4;
    border-radius: 25px;
    padding: 24px;
    color: #47754c;
    margin: 17px 0;
    box-shadow: 0 6px 0 #d8e9cd;
}

.danger {
    background: linear-gradient(135deg, #ffe3e1, #fff0e8);
    border: 2px solid #f4aaa8;
    border-radius: 25px;
    padding: 24px;
    color: #a6424e;
    margin: 17px 0;
    box-shadow: 0 6px 0 #f6d0ca;
}

.big-emoji {
    font-size: 2.8rem;
    margin-bottom: 5px;
}

.mini-caption {
    font-size: .88rem;
    color: #a17b86;
}

div.stButton > button {
    min-height: 3.1rem;
    border-radius: 18px;
    border: 2px solid #f1bfd0;
    background: #fff;
    color: #b85d7b;
    font-family: 'Jua', sans-serif;
    font-size: 1rem;
    box-shadow: 0 3px 0 #f5d5df;
    transition: .18s;
}

div.stButton > button:hover {
    background: #ffe6ee;
    border-color: #e982a2;
    color: #a64d6b;
    transform: translateY(-1px);
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #ed91ad, #dd7093);
    color: white;
    border: 2px solid #e982a2;
    box-shadow: 0 4px 0 #c96586;
}

div.stButton > button[kind="primary"]:hover {
    background: #d96789;
    color: white;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,.78);
    border-radius: 24px;
    border-color: #f5d9e2;
}

div[data-testid="stMetric"] {
    background: white;
    border: 2px solid #f6dce3;
    border-radius: 21px;
    padding: 15px;
    box-shadow: 0 4px 0 #f8e6eb;
}

div[data-testid="stMetricLabel"] {
    color: #b7778b;
    font-family: 'Jua', sans-serif;
}

hr {
    border-color: #f3d5df;
}

input, textarea {
    border-radius: 14px !important;
}

div[data-baseweb="select"] > div {
    border-radius: 14px;
}

.footer {
    text-align: center;
    background: linear-gradient(120deg, #ffe5ed, #fff0d3);
    border: 2px dashed #eab0c2;
    border-radius: 27px;
    padding: 27px 15px;
    margin-top: 22px;
}

.footer-title {
    color: #bd6483;
    font-size: 1.35rem;
    font-family: 'Jua', sans-serif;
}

div[data-testid="stAlert"] {
    border-radius: 17px;
}
</style>
""", unsafe_allow_html=True)

# ──────────────── 🧸 상태 저장 ────────────────
if "help_requested" not in st.session_state:
    st.session_state.help_requested = False

if "help_time" not in st.session_state:
    st.session_state.help_time = ""

if "help_message" not in st.session_state:
    st.session_state.help_message = "도움이 필요해요. 저를 확인해 주세요."

# ──────────────── 🍓 상단 배너 ────────────────
st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ LITTLE EXPLORERS CLUB ✦</div>
    <div style="font-size:2rem; margin-top:10px;">🎀 🐰 🍓</div>
    <h1>안심 탐험대</h1>
    <p>오늘의 작은 모험도 안전하게, 행복하게 ♡</p>
    <div class="ribbon">🌷 SAFETY FIRST · LOVE ALWAYS 🌷</div>
    <div style="color:#a87580;">✧･ﾟ: *✧･ﾟ:* 나의 안전 다이어리 *:･ﾟ✧*:･ﾟ✧</div>
</div>
""", unsafe_allow_html=True)

# ──────────────── 사이드 메뉴 ────────────────
with st.sidebar:
    st.markdown("# 🎀 탐험 수첩")
    st.write("오늘도 즐거운 하루 보내기!")
    st.markdown("### 🌷 누구의 수첩인가요?")
    mode = st.radio(
        "사용 모드",
        ["🧸 보호자 모드", "🐰 아이 모드"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 🍀 오늘의 안전 약속")
    st.write("🍓 안전 구역 확인하기")
    st.write("💌 도움이 필요하면 요청하기")
    st.write("🎤 마이크는 직접 허용하기")
    st.write("🌷 모르는 사람을 따라가지 않기")

    st.markdown("---")
    st.markdown("""
    <div class="sticker" style="padding:18px;">
        <div style="font-size:2rem;">🐰</div>
        <b>오늘의 응원 메시지</b><br>
        <span class="mini-caption">
        너의 안전이 제일 소중해! ♡
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("made with ♡ · 안심 탐험대")

# ──────────────── 거리 계산 ────────────────
def distance_m(lat1, lon1, lat2, lon2):
    r = 6371000
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

    return 2 * r * math.atan2(
        math.sqrt(a), math.sqrt(1 - a)
    )

# ──────────────── 메인 레이아웃 ────────────────
left, right = st.columns([1.12, 0.88], gap="large")

# ──────────────── 🗺️ 안전 지도 ────────────────
with left:
    st.markdown("""
    <div class="sticker">
        <div style="font-size:2rem;">🗺️ 🌼</div>
        <h3>나의 안전 지도</h3>
        <div class="mini-caption">
        우리 탐험대의 안전 구역을 확인해 봐요!
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 🌳 놀이터 위치")
        a, b = st.columns(2)

        with a:
            park_lat = st.number_input(
                "놀이터 위도",
                value=37.5665,
                format="%.6f",
            )

        with b:
            park_lon = st.number_input(
                "놀이터 경도",
                value=126.9780,
                format="%.6f",
            )

        radius = st.slider(
            "💚 안전 구역 반경",
            min_value=20,
            max_value=1000,
            value=100,
            step=10,
            format="%d m",
        )

        st.markdown("---")
        st.markdown("### 🐰 아이의 위치")

        c, d = st.columns(2)

        with c:
            child_lat = st.number_input(
                "아이 위도",
                value=37.5668,
                format="%.6f",
            )

        with d:
            child_lon = st.number_input(
                "아이 경도",
                value=126.9782,
                format="%.6f",
            )

        check = st.button(
            "🍓 안전 확인하기",
            type="primary",
            use_container_width=True,
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

        m1, m2 = st.columns(2)
        with m1:
            st.metric("📍 놀이터까지 거리", f"{dist:.0f} m")
        with m2:
            st.metric("💚 안전 구역 반경", f"{radius} m")

        if dist <= radius:
            st.markdown(f"""
            <div class="safe">
                <div class="big-emoji">🌼 🐰 🌼</div>
                <h3>안전 구역 안이에요!</h3>
                놀이터 중심에서 약 <b>{dist:.0f}m</b> 떨어져 있어요.<br>
                오늘도 즐겁게 탐험해 봐요 ♡
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="danger">
                <div class="big-emoji">🚨 🍓 🚨</div>
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

# ──────────────── 💌 도움 요청 · 마이크 ────────────────
with right:
    st.markdown("""
    <div class="sticker">
        <div style="font-size:2rem;">💌 🧸</div>
        <h3>도움 요청 우체통</h3>
        <div class="mini-caption">
        혼자 해결하기 어려울 땐 믿을 수 있는 어른에게 알려요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if mode == "🐰 아이 모드":
        st.markdown("""
        <div class="danger">
            <div class="big-emoji">🧸 💗</div>
            <h3>도움이 필요하나요?</h3>
            아래 버튼으로 도움 요청을 등록할 수 있어요.
        </div>
        """, unsafe_allow_html=True)

        st.session_state.help_message = st.text_area(
            "💌 전달할 메시지",
            value=st.session_state.help_message,
            max_chars=250,
            placeholder="예: 보호자를 찾고 있어요.",
        )

        if st.button(
            "🆘 도움 요청하기",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.help_requested = True
            st.session_state.help_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            st.rerun()

        if st.session_state.help_requested:
            st.markdown(f"""
            <div class="danger">
                <h3>💌 요청이 등록됐어요!</h3>
                <p>🕒 {st.session_state.help_time}</p>
                <p>📝 {st.session_state.help_message}</p>
            </div>
            """, unsafe_allow_html=True)

            st.warning(
                "이 요청은 현재 앱 화면에 표시돼요. "
                "다른 휴대전화로 자동 전송되지는 않아요."
            )

            if st.button("확인 완료 ♡", use_container_width=True):
                st.session_state.help_requested = False
                st.session_state.help_time = ""
                st.rerun()

        st.markdown("---")
        st.markdown("""
        <div class="sticker">
            <div style="font-size:2rem;">🎤 🎧</div>
            <h3>소리 녹음 다이어리</h3>
            <div class="mini-caption">
            직접 녹음을 시작하고, 녹음한 소리를 이 화면에서 확인해요.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info(
            "마이크는 직접 시작해야 해요. "
            "녹음하기 전에 주변 사람에게 알리고 동의를 받아 주세요."
        )

        try:
            audio = st.audio_input(
                "🎙️ 녹음 시작하기",
                sample_rate=16000,
                key="child_audio",
            )

            if audio is not None:
                st.success("🌷 녹음이 완료됐어요!")
                st.audio(audio, format="audio/wav")
                st.caption(
                    "이 녹음은 이 화면에서 재생할 수 있어요. "
                    "보호자에게 자동 전송되지는 않아요."
                )
        except Exception:
            st.warning(
                "마이크 입력을 지원하지 않는 Streamlit 버전일 수 있어요. "
                "requirements.txt에서 Streamlit 버전을 확인해 주세요."
            )

    else:
        st.markdown("""
        <div class="safe">
            <div class="big-emoji">💗 🏡 💗</div>
            <h3>보호자 안전 수첩</h3>
            아이의 안전 구역과 등록된 도움 요청 상태를 확인해요.
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.help_requested:
            st.markdown(f"""
            <div class="danger">
                <h3>🚨 도움 요청 상태</h3>
                <p>🕒 {st.session_state.help_time}</p>
                <p>📝 {st.session_state.help_message}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("현재 등록된 도움 요청이 없어요. 🌷")

        st.markdown("""
        <div class="note">
            <b>🎧 주변 소리 기능 안내</b><br>
            아이 기기에서 직접 녹음한 소리는 현재 그 화면에서만 확인할 수 있어요.
            보호자 기기에서 듣는 기능은 별도의 기기 연결이 필요해요.
        </div>
        """, unsafe_allow_html=True)

# ──────────────── 🌷 하단 장식 ────────────────
st.markdown("---")
st.markdown("""
<div class="footer">
    <div style="font-size:2.5rem;">🍓 🐰 🌷 🎀 🧸</div>
    <div class="footer-title">오늘도 무사히, 행복하게!</div>
    <p style="color:#9b7180;">
    안심 탐험대와 함께하는 작은 모험 ♡
    </p>
    <div style="color:#bb8a98;font-size:.8rem;">
    ✧ 학습용 시제품 · 안전한 탐험을 위한 작은 프로젝트 ✧
    </div>
</div>
""", unsafe_allow_html=True)
