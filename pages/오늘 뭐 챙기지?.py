import streamlit as st
import json
from pathlib import Path
from datetime import date

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="시간표 준비물 알리미",
    page_icon="🎒",
    layout="centered"
)

st.title("🎒 시간표 준비물 알리미")
st.caption("오늘의 수업을 확인하고 준비물을 빠짐없이 챙겨요!")

DATA_FILE = Path("school_data.json")

DEFAULT_SUBJECTS = {
    "국어": ["국어 교과서", "국어 공책", "필통"],
    "수학": ["수학 교과서", "수학 공책", "필통"],
    "영어": ["영어 교과서", "영어 공책", "필통"],
    "과학": ["과학 교과서", "과학 공책", "필통"],
    "사회": ["사회 교과서", "사회 공책", "필통"],
    "체육": ["체육복", "운동화", "물통"],
    "음악": ["음악 교과서"],
    "미술": ["미술 교과서", "색연필"],
    "실과": ["실과 교과서"],
    "도덕": ["도덕 교과서"],
    "창체": ["필통"],
}

DAYS = ["월요일", "화요일", "수요일", "목요일", "금요일"]


def load_data():
    """저장된 데이터를 불러옵니다."""
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "subjects": DEFAULT_SUBJECTS,
        "timetable": {day: [] for day in DAYS}
    }


def save_data(data):
    """시간표와 준비물 설정을 저장합니다."""
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


if "school_data" not in st.session_state:
    st.session_state.school_data = load_data()

data = st.session_state.school_data

if "checked_items" not in st.session_state:
    st.session_state.checked_items = {}

# 기존 저장 파일에 새 기본 과목이 없으면 추가
for subject, items in DEFAULT_SUBJECTS.items():
    data["subjects"].setdefault(subject, items)

for day in DAYS:
    data["timetable"].setdefault(day, [])

# -----------------------------
# 사이드바 메뉴
# -----------------------------
menu = st.sidebar.radio(
    "메뉴",
    ["🏠 오늘의 준비물", "📅 시간표 설정", "📝 과목별 준비물 설정"]
)

# -----------------------------
# 오늘의 준비물
# -----------------------------
if menu == "🏠 오늘의 준비물":
    today = date.today()
    st.subheader(f"📆 {today.strftime('%Y년 %m월 %d일')}")

    # 주말이면 다음 주 월요일을 자동 선택하지 않고
    # 사용자가 평일을 직접 선택하도록 합니다.
    if today.weekday() < 5:
        default_day = DAYS[today.weekday()]
    else:
        default_day = DAYS[0]

    selected_day = st.selectbox(
        "어느 날의 준비물을 확인할까요?",
        DAYS,
        index=DAYS.index(default_day)
    )

    lessons = data["timetable"].get(selected_day, [])

    if not lessons:
        st.info("아직 등록된 시간표가 없어요. '시간표 설정'에서 수업을 등록해 주세요.")

    else:
        st.write(f"### 📚 {selected_day} 수업")

        all_items = []

        for period, subject in enumerate(lessons, start=1):
            st.write(f"**{period}교시 · {subject}**")

            items = data["subjects"].get(subject, [])

            if items:
                for item in items:
                    if item not in all_items:
                        all_items.append(item)
            else:
                st.caption("등록된 준비물이 없어요.")

        st.divider()
        st.subheader("🎒 오늘 챙길 준비물")
        st.caption("준비물을 체크하면 완료 여부를 확인할 수 있어요.")

        if all_items:
            check_key = f"{today.isoformat()}_{selected_day}"

            for item in all_items:
                key = f"{check_key}_{item}"
                checked = st.checkbox(
                    item,
                    value=st.session_state.checked_items.get(key, False),
                    key=key
                )
                st.session_state.checked_items[key] = checked

            completed = sum(
                st.session_state.checked_items.get(
                    f"{check_key}_{item}", False
                )
                for item in all_items
            )

            st.progress(completed / len(all_items))
            st.write(f"준비 완료: {completed}/{len(all_items)}개")

            if completed == len(all_items):
                st.success("모든 준비물을 챙겼어요! 좋은 하루 보내세요 😊")

            if st.button("체크리스트 초기화"):
                for item in all_items:
                    st.session_state.checked_items[
                        f"{check_key}_{item}"
                    ] = False
                st.rerun()

        else:
            st.warning("이 수업에 등록된 준비물이 없습니다.")

# -----------------------------
# 시간표 설정
# -----------------------------
elif menu == "📅 시간표 설정":
    st.subheader("📅 주간 시간표 설정")
    st.write("요일별로 수업 과목을 교시 순서대로 선택하세요.")

    subject_names = list(data["subjects"].keys())

    for day in DAYS:
        with st.expander(day, expanded=(day == "월요일")):
            current_lessons = data["timetable"].get(day, [])

            count = st.number_input(
                f"{day} 수업 교시 수",
                min_value=0,
                max_value=10,
                value=len(current_lessons),
                step=1,
                key=f"count_{day}"
            )

            new_lessons = []

            for i in range(int(count)):
                previous = (
                    current_lessons[i]
                    if i < len(current_lessons)
                    and current_lessons[i] in subject_names
                    else subject_names[0]
                )

                selected = st.selectbox(
                    f"{i + 1}교시",
                    subject_names,
                    index=subject_names.index(previous),
                    key=f"lesson_{day}_{i}"
                )
                new_lessons.append(selected)

            data["timetable"][day] = new_lessons

    if st.button("💾 시간표 저장", type="primary"):
        save_data(data)
        st.success("시간표를 저장했어요!")

# -----------------------------
# 과목별 준비물 설정
# -----------------------------
elif menu == "📝 과목별 준비물 설정":
    st.subheader("📝 과목별 준비물 설정")
    st.write("과목마다 필요한 준비물을 쉼표(,)로 구분해 입력하세요.")

    subject_names = list(data["subjects"].keys())

    selected_subject = st.selectbox(
        "과목 선택",
        subject_names
    )

    current_items = data["subjects"].get(selected_subject, [])

    item_text = st.text_area(
        "준비물 목록",
        value=", ".join(current_items),
        height=120,
        help="예: 수학 교과서, 수학 공책, 자"
    )

    if st.button("💾 준비물 저장", type="primary"):
        items = [
            item.strip()
            for item in item_text.replace("\n", ",").split(",")
            if item.strip()
        ]

        
        data["subjects"][selected_subject] = list(dict.fromkeys(items))
        save_data(data)
        st.success(f"{selected_subject} 준비물을 저장했어요!")
        st.rerun()
