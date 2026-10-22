import streamlit as st 
st.title('보호자 알림 페이지')
st.write('아이가 지정한 위치에서 벗어나면 보호자에게 알림이 가는 기능')

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. 페이지 및 브라우저 탭 설정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="보호자 알림",
    page_icon="🚨",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. 커스텀 CSS (이미지의 스케치 UI/손그림 스타일 완벽 반영)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }

    /* 전체 배경 */
    .stApp {
        background-color: #dbeafe !important;
        background-image: radial-gradient(#93c5fd 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* 카드 박스 (손그림/스케치 스타일) */
    .sketch-card {
        background-color: #ffffff;
        border: 2px solid #2b374e;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 2px 3px 0px #2b374e;
    }

    /* 카드 헤더 제목 */
    .card-header {
        font-size: 15px;
        font-weight: 800;
        color: #1e293b;
        border-bottom: 2px solid #cbd5e1;
        padding-bottom: 6px;
        margin-bottom: 10px;
    }

    /* 메인 상단 헤더 */
    .top-header {
        background-color: #ffffff;
        border: 2px solid #2b374e;
        border-radius: 14px;
        padding: 12px;
        text-align: center;
        box-shadow: 3px 3px 0px #2b374e;
        margin-bottom: 16px;
    }

    .top-header h1 {
        color: #0f172a;
        font-size: 28px;
        font-weight: 900;
        margin: 0;
        letter-spacing: -0.5px;
    }

    /* 초록색 상태 바 */
    .status-bar-green {
        background-color: #22c55e;
        color: white;
        border: 2px solid #15803d;
        border-radius: 10px;
        padding: 6px 12px;
        text-align: center;
        font-size: 13px;
        font-weight: bold;
        margin-bottom: 12px;
    }

    /* 안전 뱃지 */
    .badge-safe {
        background-color: #bbf7d0;
        color: #166534;
        border: 2px solid #22c55e;
        padding: 4px 18px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
    }

    /* 수신된 알림 미리보기 (스마트폰 팝업 스타일) */
    .phone-preview {
        background-color: #ffffff;
        border: 2px solid #334155;
        border-radius: 14px;
        padding: 12px;
        box-shadow: 2px 2px 0px #334155;
    }

    .phone-btn-red {
        background-color: #ef4444;
        color: white;
        border: 1px solid #b91c1c;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
        font-weight: bold;
        cursor: pointer;
    }

    .phone-btn-yellow {
        background-color: #facc15;
        color: #451a03;
        border: 1px solid #ca8a04;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
        font-weight: bold;
        cursor: pointer;
    }

    /* 하단 푸터 */
    .footer-bar {
        background-color: #1e293b;
        color: #cbd5e1;
        padding: 10px 20px;
        border-radius: 6px;
        font-size: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. 세션 상태 (알림 기록)
# -----------------------------------------------------------------------------
if "notification_logs" not in st.session_state:
    st.session_state.notification_logs = [
        {"시간": "2024-3:38", "유형": "긴급", "수신 보호자": "엄마", "상태": "성공"},
        {"시간": "2024-3:25", "유형": "등교", "수신 보호자": "엄마", "상태": "아빠"},
        {"시간": "2024-3:29", "유형": "등교", "수신 보호자": "엄마", "상태": "아빠"},
        {"시간": "2024-3:29", "유형": "등교", "수신 보호자": "엄마", "상태": "아빠"},
        {"시간": "2024-3:38", "유형": "하교", "수신 보호자": "엄마", "상태": "아빠"},
        {"시간": "2024-11:30", "유형": "하교", "수신 보호자": "엄마", "상태": "아빠"}
    ]

# -----------------------------------------------------------------------------
# 4. 상단 헤더
# -----------------------------------------------------------------------------
st.markdown("""
<div class="top-header">
    <h1>보호자 긴급 알림 시스템 (어린이용)</h1>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. 메인 3열 구성 (이미지 레이아웃과 동일)
# -----------------------------------------------------------------------------
left_col, center_col, right_col = st.columns([1, 2.1, 1.1])

# ==========================================
# [좌측 컬럼] 보호대상자 정보 / 일접시간 상태 / 최근 활동 로그 / 긴급 연락처
# ==========================================
with left_col:
    # 1. 보호대상자 정보
    st.markdown("""
    <div class="sketch-card">
        <div class="card-header">보호대상자 정보</div>
        <div style="text-align: center; margin: 10px 0;">
            <h2 style="margin:0; font-size: 22px; color:#0f172a; font-weight:800;">박민수 (어린이, 7세)</h2>
            <div style="margin-top: 8px;">
                <span class="badge-safe">안전 (Safe)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 일접시간 상태
    st.markdown("""
    <div class="sketch-card">
        <div class="card-header">일접시간 상태</div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="color:#22c55e; font-size:16px;">🟢</span>
            <span style="font-weight:bold; color:#166534; font-size:14px;">실시간 요전티</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. 최근 활동 로그
    st.markdown("""
    <div class="sketch-card">
        <div class="card-header">최근 활동 로그</div>
        <div style="font-size:13px; line-height:1.9; color:#334155;">
            <div><b>오후 2:35</b> 등교 확인 (박민수)</div>
            <div><b>오후 2:39</b> 수업 중 (정상 상태)</div>
            <div><b>오전 11:30</b> 하고 예정</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. 긴급 연락처 관리
    st.markdown("""
    <div class="sketch-card">
        <div class="card-header">긴급 연락처 관리</div>
        <div style="font-size:13px; color:#334155; line-height:2.0;">
            <div>🧑‍💼 010-XXXX-XXXX</div>
            <div>🧑‍💼 010-YYXX-XXXX</div>
            <div>🧑‍💼 010-YYYY-XXXX</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# [중앙 컬럼] 모니터링 상태 / 긴급 알림 전송 / GPS 지도
# ==========================================
with center_col:
    # 실시간 모니터링 상태 바
    st.markdown("""
    <div class="status-bar-green">
        실시간 모니터링 및 맟춤아장으로 관웅확입니다.
    </div>
    """, unsafe_allow_html=True)

    # 긴급 알림 전송 카드
    with st.container():
        st.markdown("""
        <div class="sketch-card">
            <div style="text-align:center; font-size:20px; font-weight:900; margin-bottom:12px; color:#0f172a;">
                보호자 긴급 알림 전송
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.text_input("보호자 연락처 (전화번호)", value="010-XXXX-XXXX", key="p_num1")
        with c2:
            st.text_input(" ", value="010-YYYY-YYYY", key="p_num2")

        st.text_input("알림 메시지", value="도움이 필요해요! 위치를 확인해 주세요. 엄마, 어디에요? | 배고파요!", key="alert_msg")

        # 빨간색 전송 버튼
        if st.button("🚨 보호자 긴급 알림 전송 🚨", use_container_width=True, type="primary"):
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.notification_logs.insert(0, {
                "시간": now_time,
                "유형": "긴급",
                "수신 보호자": "엄마",
                "상태": "성공"
            })
            st.success("🚨 보호자에게 긴급 알림 메시지가 즉시 전송되었습니다!")

        st.markdown("""
            <div style="text-align:center; font-size:12px; color:#64748b; margin-top:8px;">
                전송 대기 중...<br>
                <b>버튼을 누르면 등록된 보호자에게 즉시 SMS 및 카카오톡 알림이 전송됩니다. 허위 진승에 유의하세요.</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 실시간 GPS 위치 지도 카드
    st.markdown("""
    <div class="sketch-card">
        <div class="card-header">실시간 GPS 위치 지도</div>
    """, unsafe_allow_html=True)

    # 서광초등학교 근처 좌표
    school_lat, school_lon = 37.5550, 126.9370
    m = folium.Map(location=[school_lat, school_lon], zoom_start=16, tiles="OpenStreetMap")

    # 위치 마커
    folium.Marker(
        location=[school_lat, school_lon],
        popup="현재 위치 (박민수)",
        tooltip="현재 위치 (박민수)",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    st_folium(m, width="100%", height=260)
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# [우측 컬럼] 최근 알림 기록 / 수신된 알림 예시
# ==========================================
with right_col:
    # 1. 최근 알림 기록
    st.markdown("""
    <div class="sketch-card">
        <div class="card-header">최근 알림 기록</div>
    """, unsafe_allow_html=True)

    df_logs = pd.DataFrame(st.session_state.notification_logs)
    st.dataframe(
        df_logs,
        use_container_width=True,
        height=210,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 수신된 알림 예시
    st.markdown("""
    <div class="sketch-card">
        <div class="card-header">수신된 알림 예시</div>
        <div class="phone-preview">
            <div style="font-weight:bold; font-size:15px; color:#0f172a; margin-bottom:6px;">박민수 어린이</div>
            <div style="font-size:12px; color:#475569; line-height:1.5;">
                <b>박민수 어린이</b>에게서 긴급 알림을 보냈습니다.<br>
                <span style="color:#64748b;">(예시: 도움이 필요해요! 위치를 확인해 주세요. | 오후 2:35)</span>
            </div>
            <div style="margin-top:12px; display:flex; gap:6px;">
                <button class="phone-btn-red">위치 확인</button>
                <button class="phone-btn-yellow">전화하기</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. 하단 푸터 영역
# -----------------------------------------------------------------------------
st.markdown("""
<div class="footer-bar">
    <div>Copyright © 2024 CareNet. All rights reserved.</div>
    <div>고객센터 : 1588-XXXX</div>
</div>
""", unsafe_allow_html=True)

     
