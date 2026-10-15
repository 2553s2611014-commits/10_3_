import math
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="안심 놀이터",
    page_icon="🌳",
    layout="centered"
)

st.title("🌳 안심 놀이터")
st.write("아이의 위치를 확인하고 놀이터 안전 구역을 관리해요.")

st.info(
    "학습용 앱입니다. 아래에서 아이의 위치를 입력해 "
    "안전 구역 이탈 여부를 확인할 수 있어요."
)

st.subheader("📍 놀이터 안전 구역 설정")

park_lat = st.number_input(
    "놀이터 위도",
    value=37.5665,
    format="%.6f"
)

park_lon = st.number_input(
    "놀이터 경도",
    value=126.9780,
    format="%.6f"
)

radius = st.slider(
    "안전 구역 반경 (미터)",
    min_value=20,
    max_value=1000,
    value=100,
    step=10
)

st.divider()

st.subheader("👶 아이의 현재 위치")

child_lat = st.number_input(
    "아이의 위도",
    value=37.5668,
    format="%.6f"
)

child_lon = st.number_input(
    "아이의 경도",
    value=126.9782,
    format="%.6f"
)


# 두 위치 사이의 거리 계산
def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371000

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    return earth_radius * 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )


if st.button("📡 위치 확인하기", use_container_width=True):

    coordinates = [park_lat, park_lon, child_lat, child_lon]

    if not all(math.isfinite(x) for x in coordinates):
        st.error("올바른 위치 좌표를 입력해 주세요.")

    elif not (
        -90 <= park_lat <= 90
        and -180 <= park_lon <= 180
        and -90 <= child_lat <= 90
        and -180 <= child_lon <= 180
    ):
        st.error("위도 또는 경도의 범위가 올바르지 않아요.")

    else:
        distance = calculate_distance(
            park_lat,
            park_lon,
            child_lat,
            child_lon
        )

        st.metric(
            "놀이터 중심과의 거리",
            f"{distance:.1f} m"
        )

        if distance > radius:
            st.error(
                "🚨 안전 구역 이탈! "
                "아이의 위치를 확인해 주세요."
            )
            st.warning(
                "이 경고는 앱 화면에 표시됩니다. "
                "휴대폰 문자나 푸시 알림은 별도 설정이 필요합니다."
            )

        else:
            st.success(
                "✅ 아이가 놀이터 안전 구역 안에 있어요!"
            )

        st.subheader("🗺️ 위치 지도")

        map_data = pd.DataFrame({
            "latitude": [park_lat, child_lat],
            "longitude": [park_lon, child_lon]
        })

        st.map(
            map_data,
            latitude="latitude",
            longitude="longitude"
        )

st.divider()

st.caption(
    "안심 놀이터 | 학습용 안전 구역 확인 앱"
)
