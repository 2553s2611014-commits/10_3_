
import math
from datetime import datetime

import pandas as pd
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="안심 탐험대 🍓",
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 다이어리 디자인 CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --pink: #f3a6bd;
    --dark-pink: #cf6f91;
    --cream: #fffaf0;
    --green: #b9d7a8;
    --ink: #62505a;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 5%, #ffe4ec 0%, transparent 30%),
        radial-gradient(ellipse at 90% 70%, #eaf3dd 0%, transparent 28%),
        #fffaf2;
    color: var(--ink);
    font-family: 'Nunito', sans-serif;
}

h1, h2, h3, h4, p, label, span, div {
    font-family: 'Nunito', sans-serif;
}

h1, h2, h3 {
    color: #9c5874;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #fff0f4;
    border-right: 2px dashed #efb5c8;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Jua', sans-serif;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 30px 28px;
    border: 3px solid white;
    border-radius: 28px;
    background: linear-gradient(125deg, #f8c7d6, #fff0cb 58%, #d8e9c9);
    box-shadow: 0 8px 0 #edc4cf, 0 12px 24px #d8a9b522;
    margin-bottom: 24px;
}

.hero::after {
    content: "🍓  ✿  ♡  ✦";
    position: absolute;
    right: 22px;
    top: 16px;
    font-size: 24px;
    transform: rotate(8deg);
}

.hero h1 {
    font-family: 'Jua', sans-serif;
    font-size: clamp(30px, 4vw, 48px);
    margin: 0;
    color: #96536e;
    letter-spacing: 1px;
}

.hero p {
    margin: 10px 0 0;
    font-size: 15px;
    color: #765d68;
}

.tape {
    display: inline-block;
    padding: 6px 14px;
    background: #fff9dc;
    border: 1px dashed #e7bb88;
    color: #a66c6c;
    border-radius: 5px;
    transform: rotate(-2deg);
    font-size: 12px;
    font-weight: 800;
    margin-bottom: 12px;
}

.section-title {
    font-family: 'Jua', sans-serif;
    font-size: 23px;
    color: #a25c78;
    margin: 6px 0 14px;
}

.diary {
    position: relative;
    background-color: #fffdf8;
    background-image: repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 31px,
        #e9dce4 32px,
        transparent 33px
    );
    border: 1px solid #efd6df;
    border-radius: 18px;
    padding: 22px 20px 22px 36px;
    box-shadow: 4px 5px 0 #f0d5df;
    margin-bottom: 20px;
    overflow: hidden;
}

.diary::before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 22px;
    border-left: 2px solid #efa6b9;
}

.diary h3 {
    font-family: 'Jua', sans-serif;
    margin-top: 0;
}

.sticker {
    display: inline-block;
    background: #ffe0e9;
    color: #a65376;
    padding: 7px 12px;
    border: 1px solid #f2b4c8;
    border-radius: 12px 5px 12px 5px;
    transform: rotate(-2deg);
    font-size: 12px;
    font-weight: 800;
    margin-bottom: 10px;
}

.paper-card {
    background: #fffdf8;
    border: 2px dashed #eac0cf;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 6px 0 #f2dce4;
    margin-bottom: 18px;
}

.green-card {
    background: #f5faee;
    border-color: #c7ddb9;
    box-shadow: 0 6px 0 #e0ebd5;
}

.pink-card {
    background: #fff0f4;
}

.metric {
    background: #fffdf9;
    border: 2px solid #f0d1dc;
    border-radius: 18px;
    padding: 16px 12px;
    text-align: center;
    box-shadow: 0 4px 0 #f5e2e8;
    min-height: 95px;
}

.metric-label {
    font-size: 12px;
    color: #987783;
    font-weight: 800;
}

.metric-value {
    font-family: 'Jua', sans-serif;
    font-size: 25px;
    color: #a65e7b;
    margin-top: 6px;
    overflow-wrap: anywhere;
}

.safe-banner {
    background: #eef7e7;
    border: 2px solid #b9d7a8;
    border-radius: 18px;
    padding: 18px;
    color: #55784a;
    font-weight: 800;
    margin: 12px 0;
}

.danger-banner {
    background: #fff0f1;
    border: 2px solid #e99aab;
    border-radius: 18px;
    padding: 18px;
    color: #b33f5b;
    font-weight: 800;
    margin: 12px 0;
}

.small-note {
    font-size: 12px;
    color: #997d87;
}

.stButton > button {
    border-radius: 14px;
    border: 1px solid #e8b2c4;
    background: #f5bfd0;
    color: #78445a;
    font-weight: 800;
    min-height: 44px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #eea9c0;
    border-color: #d889a6;
    color: #68364c;
    transform: translateY(-2px);
}

.stTextArea textarea,
.stTextInput input,
.stNumberInput input {
    background: #fffdf9;
    border-color: #e8c7d3;
    border-radius: 12px;
}

div[data-baseweb="select"] > div {
    background: #fffdf9;
    border-color: #e8c7d3;
    border-radius: 12px;
}

hr {
    border-color: #efd7e0;
}

.footer {
    text-align: center;
    padding: 22px 8px;
    color: #b18193;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 거리 계산 함수
# -----------------------------
def distance_m(lat1, lon1, lat2, lon2):
    """두 좌표 사이의 거리를 미터 단위로 계산"""
    radius = 6371000

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

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "help_message" not in st.session_state:
    st.session_state.help_message = ""

if "help_requested" not in st.session_state:
    st.session_state.help_requested = False

if "help_time" not in st.session_state:
    st.session_state.help_time = ""

if "help_reset" not in st.session_state:
    st.session_state.help_reset = 0


# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.markdown("## 🍓 안심 탐험대")
    st.caption("오늘도 안전하게, 소중하게!")

    st.markdown("---")

    mode = st.radio(
        "📔 다이어리 주인",
        ["🧸 어린이 모드", "🌷 보호자 모드"],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 🎀 안전 약속")
    st.markdown("""
    - 낯선 사람을 따라가지 않기
    - 위험하면 믿을 수 있는 어른에게 알리기
    - 길을 잃으면 안전한 장소에서 도움 요청하기
    """)

    st.markdown("---")
    st.markdown(
        '<div class="small-note">오늘의 안전도 중요하지만, '
        '무엇보다 네가 소중해! 🍰</div>',
        unsafe_allow_html=True,
    )


# -----------------------------
# 상단 다이어리 표지
# -----------------------------
today = datetime.now().strftime("%Y년 %m월 %d일")

st.markdown(f"""
<div class="hero">
    <div class="tape">MY LITTLE SAFETY DIARY ✂️</div>
    <h1>🍓 안심 탐험대</h1>
    <p>오늘의 작은 모험도 안전하게 기록하기</p>
    <p>📅 {today} &nbsp; · &nbsp; 오늘도 무사히 돌아오기 프로젝트</p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# 좌표 설정
# -----------------------------
with st.expander("🗺️ 놀이터와 어린이 위치 설정하기", expanded=True):
    st.caption(
        "아래 좌표는 직접 입력하는 테스트용 정보야. "
        "실제 GPS 위치가 자동으로 들어오는 것은 아니야."
    )

    location_col1, location_col2 = st.columns(2)

    with location_col1:
        st.markdown("### 🌳 놀이터 위치")
        playground_lat = st.number_input(
            "놀이터 위도",
            value=37.5665,
            format="%.6f",
            key="play_lat",
        )
        playground_lon = st.number_input(
            "놀이터 경도",
            value=126.9780,
            format="%.6f",
            key="play_lon",
        )

    with location_col2:
        st.markdown("### 🧸 어린이 위치")
        child_lat = st.number_input(
            "어린이 위도",
            value=37.5665,
            format="%.6f",
            key="child_lat",
        )
        child_lon = st.number_input(
            "어린이 경도",
            value=126.9780,
            format="%.6f",
            key="child_lon",
        )

    safe_radius = st.slider(
        "안전 범위 설정",
        min_value=50,
        max_value=1000,
        value=200,
        step=50,
        format="%d m",
    )

    st.caption("💡 테스트할 때는 어린이 좌표를 바꾸면서 거리를 확인해 봐!")


# -----------------------------
# 현재 안전 상태 계산
# -----------------------------
distance = distance_m(
    playground_lat,
    playground_lon,
    child_lat,
    child_lon,
)

is_safe = distance <= safe_radius


# -----------------------------
# 메인 화면 배치
# 왼쪽: 안전 상태 / 지도
# 오른쪽: 도움 요청 / 음성 기록
# -----------------------------
left_col, right_col = st.columns([1.12, 0.88], gap="large")


# =============================
# 왼쪽 다이어리 페이지
# =============================
with left_col:
    st.markdown(
        '<div class="section-title">📍 오늘의 안전 기록</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sticker">TODAY CHECK ✔</div>',
                unsafe_allow_html=True)

    if is_safe:
        st.markdown("""
        <div class="safe-banner">
            🌷 안전 범위 안에 있어요!<br>
            <span style="font-size:13px;font-weight:normal">
            설정한 놀이터 범위 안에 있는 것으로 계산됐어요.
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="danger-banner">
            🎀 안전 범위를 벗어났어요!<br>
            <span style="font-size:13px;font-weight:normal">
            입력한 좌표를 다시 확인하고 어린이의 안전을 확인해 주세요.
            </span>
        </div>
        """, unsafe_allow_html=True)

    metric1, metric2 = st.columns(2)

    with metric1:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-label">📏 놀이터와 거리</div>
            <div class="metric-value">{distance:.1f} m</div>
        </div>
        """, unsafe_allow_html=True)

    with metric2:
        status_text = "안전 범위" if is_safe else "범위 밖"
        st.markdown(f"""
        <div class="metric">
            <div class="metric-label">🌱 현재 판정</div>
            <div class="metric-value">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    st.markdown("""
    <div class="diary">
        <div class="sticker">MY MAP 🗺️</div>
        <h3>오늘의 모험 지도</h3>
        <p>📌 분홍색 핀은 놀이터, 초록색 핀은 어린이 위치예요.</p>
    </div>
    """, unsafe_allow_html=True)

    map_data = pd.DataFrame({
        "lat": [playground_lat, child_lat],
        "lon": [playground_lon, child_lon],
    })

    st.map(map_data, latitude="lat", longitude="lon", size=150)

    st.markdown(
        '<div class="small-note">※ 지도는 입력한 좌표를 표시해요. '
        '실제 위치 추적 기능은 아니에요.</div>',
        unsafe_allow_html=True,
    )


# =============================
# 오른쪽 다이어리 페이지
# =============================
with right_col:
    st.markdown(
        '<div class="section-title">💌 비밀 쪽지함</div>',
        unsafe_allow_html=True,
    )

    if mode == "🧸 어린이 모드":
        st.markdown("""
        <div class="diary">
            <div class="sticker">DEAR GUARDIAN 💌</div>
            <h3>도움이 필요해요!</h3>
            <p>걱정되는 일이 있다면 믿을 수 있는 어른에게 알려 주세요.</p>
        </div>
        """, unsafe_allow_html=True)

        message = st.text_area(
            "보호자에게 남길 쪽지",
            value=st.session_state.help_message,
            placeholder="예: 길을 잘 모르겠어요. 도와주세요!",
            height=125,
            key=f"child_message_{st.session_state.help_reset}",
        )

        if st.button("💌 도움 요청 쪽지 작성하기", use_container_width=True):
            st.session_state.help_message = message.strip()
            st.session_state.help_requested = True
            st.session_state.help_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )

            if not st.session_state.help_message:
                st.session_state.help_message = "도움이 필요해요!"
            st.success("쪽지를 이 앱에 기록했어요!")

        if st.session_state.help_requested:
            st.markdown(
                f"""
                <div class="paper-card pink-card">
                    <div class="sticker">SAVED NOTE ✨</div>
                    <h3>📝 작성한 쪽지</h3>
                    <p>{st.session_state.help_message}</p>
                    <p class="small-note">
                    기록 시간: {st.session_state.help_time}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown("""
        <div class="paper-card green-card">
            <div class="sticker">VOICE MEMO 🎙️</div>
            <h3>목소리 메모</h3>
            <p>필요할 때 직접 녹음해 이 화면에서 다시 들을 수 있어요.</p>
        </div>
        """, unsafe_allow_html=True)

        audio_value = st.audio_input(
            "음성 메모 녹음하기",
            key="child_audio",
        )

        if audio_value is not None:
            st.audio(audio_value)
            st.caption(
                "녹음은 이 화면에서 재생할 수 있어요. "
                "보호자에게 자동으로 전송되지는 않아요."
            )

    else:
        st.markdown("""
        <div class="diary">
            <div class="sticker">GUARDIAN'S PAGE 🌷</div>
            <h3>보호자 확인 페이지</h3>
            <p>어린이의 안전 상태와 도움 요청 기록을 확인해 보세요.</p>
        </div>
        """, unsafe_allow_html=True)

        if is_safe:
            st.success("🌱 입력된 좌표 기준으로 안전 범위 안에 있어요.")
        else:
            st.error("📍 입력된 좌표 기준으로 안전 범위를 벗어났어요.")

        st.markdown("### 💌 도움 요청 기록")

        if st.session_state.help_requested:
            st.markdown(
                f"""
                <div class="paper-card pink-card">
                    <div class="sticker">NEW NOTE 💗</div>
                    <h3>어린이가 남긴 쪽지</h3>
                    <p>{st.session_state.help_message}</p>
                    <p class="small-note">
                    기록 시간: {st.session_state.help_time}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("☑️ 쪽지 확인 완료", use_container_width=True):
                st.session_state.help_requested = False
                st.session_state.help_message = ""
                st.session_state.help_time = ""
                st.rerun()
        else:
            st.info("아직 이 앱에 기록된 도움 요청이 없어요.")

        st.markdown("---")

        st.markdown("""
        <div class="paper-card green-card">
            <div class="sticker">SAFETY REMINDER 🌼</div>
            <h3>안전 확인 메모</h3>
            <p>실제 상황에서는 어린이에게 직접 연락하거나 가까운 믿을 수 있는 어른에게 도움을 요청하세요.</p>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------
# 하단 장식
# -----------------------------
st.markdown("---")
st.markdown("""
<div class="footer">
    🍓 안심 탐험대 · MY LITTLE SAFETY DIARY 🍓<br>
    작은 모험도 안전하게, 하루의 끝은 행복하게 ♡
</div>
""", unsafe_allow_html=True)
