import streamlit as st 
st.title('보호자 알림 페이지')
st.write('아이가 지정한 위치에서 벗어나면 보호자에게 알림이 가는 기능')

import streamlit as st
import folium
from streamlit_folium import st_folium
import math
from datetime import datetime
import pandas as pd
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 초기화
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="아동 안심 지오펜스 알림 시스템",
    page_icon="🚨",
    layout="wide"
)

# 세션 상태 초기화 (위험 이력 기록용)
if "alert_history" not in st.session_state:
    st.session_state.alert_history = []

# -----------------------------------------------------------------------------
# 2. 유틸리티 함수 (하버사인 거리 계산 공식)
# -----------------------------------------------------------------------------
def haversine_distance(lat1, lon1, lat2, lon2):
    """두 위도/경도 좌표 사이의 거리를 미터(m) 단위로 계산합니다."""
    R = 6371000  # 지구 반지름 (미터)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# -----------------------------------------------------------------------------
# 3. Gemini AI 대처 가이드 생성 함수
# -----------------------------------------------------------------------------
def get_ai_emergency_guide(child_name, zone_name, distance, safe_radius):
    """Gemini AI를 활용해 지오펜스 이탈 시 행동 요령을 작성합니다."""
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        return "⚠️ Gemini API 키가 설정되지 않았습니다. Secrets 설정을 확인해주세요."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        prompt = f"""
        당신은 아동 안전 전문 컨설턴트입니다.
        아래 상황 정보를 바탕으로 보호자가 즉각 취해야 할 행동 가이드라인 3가지와 당황하지 않도록 격려하는 메시지를 간결하게 작성해주세요.

        - 아이 이름: {child_name}
        - 지정 안전구역: {zone_name} (설정 반지름: {safe_radius}m)
        - 이탈 거리: 지정 구역으로부터 약 {int(distance - safe_radius)}m 추가 이탈 (총 거리 {int(distance)}m)

        응답 형식:
        1. 🚨 즉시 확인 행동 요령 3가지 (Bullet points)
        2. 📞 권장 확인 연락처 체크리스트
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI 가이드를 불러오는 중 오류가 발생했습니다: {str(e)}"

# -----------------------------------------------------------------------------
# 4. 사이드바 - 설정 메뉴
# -----------------------------------------------------------------------------
st.sidebar.title("🛡️ 안전구역 & 아이 정보 설정")

child_name = st.sidebar.text_input("아이 이름", value="김민준")
zone_name = st.sidebar.text_input("안전구역 이름", value="OO초등학교 & 학원가")

st.sidebar.subheader("📍 안전구역 중심 좌표")
center_lat = st.sidebar.number_input("중심 위도 (Latitude)", value=37.5665, format="%.6f")
center_lon = st.sidebar.number_input("중심 경도 (Longitude)", value=126.9780, format="%.6f")
safe_radius = st.sidebar.slider("안전 반지름 (미터)", min_value=50, max_value=1000, value=200, step=50)

st.sidebar.markdown("---")
st.sidebar.subheader("📱 아이 GPS 위치 시뮬레이터")
st.sidebar.caption("아이의 위치 데이터를 실시간 변경하여 이탈 상황을 테스트하세요.")
child_lat = st.sidebar.number_input("아이 현재 위도", value=37.5690, format="%.6f")
child_lon = st.sidebar.number_input("아이 현재 경도", value=126.9795, format="%.6f")

# -----------------------------------------------------------------------------
# 5. 메인 화면 구성
# -----------------------------------------------------------------------------
st.title("🚨 아이 안심 지오펜스 이탈 알림 시스템")
st.write("아이의 실시간 위치를 모니터링하고, 지정된 안전 구역을 벗어날 경우 보호자에게 즉시 경고합니다.")

# 연산: 거리 계산
distance = haversine_distance(center_lat, center_lon, child_lat, child_lon)
is_out_of_bounds = distance > safe_radius

# 대시보드 메트릭 표시
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="지정 안전 반지름", value=f"{safe_radius} m")
with col2:
    st.metric(label="현재 아이와의 거리", value=f"{int(distance)} m")
with col3:
    if is_out_of_bounds:
        st.metric(label="현재 상태", value="🚨 이탈 발생", delta=f"+{int(distance - safe_radius)}m 초과", delta_color="inverse")
    else:
        st.metric(label="현재 상태", value="✅ 안전구역 내", delta="안전함", delta_color="normal")

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. 알림 처리 및 UI 반응
# -----------------------------------------------------------------------------
if is_out_of_bounds:
    # 이탈 발생 경고 UI
    st.error(f"⚠️ [비상] **{child_name}** 아이가 지정된 안전구역(**{zone_name}**)을 벗어났습니다! (초과 거리: 약 {int(distance - safe_radius)}m)")
    
    # 비상 경고음 효과 (웹 오디오 재생)
    audio_html = """
        <audio autoplay style="display:none;">
            <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
        </audio>
    """
    st.components.v1.html(audio_html, height=0)

    # 이력에 추가 (중복 방지)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "시각": now_str,
        "이름": child_name,
        "위치": f"{child_lat:.4f}, {child_lon:.4f}",
        "거리": f"{int(distance)}m",
        "상태": "위험 (이탈)"
    }
    if not st.session_state.alert_history or st.session_state.alert_history[-1]["시각"] != now_str:
        st.session_state.alert_history.append(log_entry)

else:
    st.success(f"🟢 **{child_name}** 아이가 안전구역(**{zone_name}**) 내부에서 정상 활동 중입니다.")

# -----------------------------------------------------------------------------
# 7. 지도 시각화 & AI 가이드 탭
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["🗺️ 실시간 지도 모니터링", "🤖 Gemini 비상 대응 AI 가이드", "📜 이탈 경고 이력 로그"])

with tab1:
    st.subheader("📍 안전 구역 및 아이 위치 시각화")
    
    # Folium 지도 생성
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

    # 1. 안전구역 (원 표시)
    folium.Circle(
        location=[center_lat, center_lon],
        radius=safe_radius,
        color="green" if not is_out_of_bounds else "orange",
        fill=True,
        fill_color="green" if not is_out_of_bounds else "orange",
        fill_opacity=0.2,
        popup=f"안전구역: {zone_name} (반지름 {safe_radius}m)"
    ).add_to(m)

    # 2. 안전구역 중심 마커
    folium.Marker(
        location=[center_lat, center_lon],
        popup=f"중심점: {zone_name}",
        icon=folium.Icon(color="blue", icon="home")
    ).add_to(m)

    # 3. 아이 위치 마커
    folium.Marker(
        location=[child_lat, child_lon],
        popup=f"{child_name}의 현재 위치",
        icon=folium.Icon(color="red" if is_out_of_bounds else "green", icon="user")
    ).add_to(m)

    # Streamlit에 지도 출력
    st_folium(m, width="100%", height=450)

with tab2:
    st.subheader("🤖 AI 맞춤형 비상 대응 리포트")
    if is_out_of_bounds:
        st.warning("아이가 안전 구역을 이탈했습니다. 아래 Gemini AI가 제안하는 가이드를 참고하세요.")
        if st.button("🚨 AI 긴급 대응 가이드 생성/갱신"):
            with st.spinner("Gemini AI가 상황 분석 및 가이드를 생성 중입니다..."):
                ai_guide = get_ai_emergency_guide(child_name, zone_name, distance, safe_radius)
                st.markdown(ai_guide)
    else:
        st.info("현재 아이가 안전 구역 내에 있습니다. 이탈 시 이곳에 AI 대응 가이드가 활성화됩니다.")

with tab3:
    st.subheader("📜 위험 이탈 기록")
    if st.session_state.alert_history:
        df_history = pd.DataFrame(st.session_state.alert_history)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.write("บัน 기록된 이탈 이력이 없습니다.")

     
