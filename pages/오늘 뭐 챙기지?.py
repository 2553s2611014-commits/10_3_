
import streamlit as st
import json
from pathlib import Path
from datetime import date

# ----------------------------------
# 기본 설정
# ----------------------------------
st.set_page_config(
    page_title="스쿨백 | 시간표 준비물 알리미",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

SUBJECT_ICONS = {
    "국어": "📖",
    "수학": "📐",
    "영어": "🌎",
    "과학": "🔬",
    "사회": "🌏",
    "체육": "⚽",
    "음악": "🎵",
    "미술": "🎨",
    "실과": "🧵",
    "도덕": "🤝",
    "창체": "💡",
}

# ----------------------------------
# 디자인
# ----------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #F4F7FF 0%, #F9FAFC 100%);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #EEF2FF;
        border-right: 1px solid #E0E7FF;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #526DE5, #8197F8);
        padding: 30px;
        border-radius: 24px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(82,109,229,0.16);
    }

    .hero h1 {
        color: white;
        font-size: 2rem;
        margin: 0 0 10px 0;
    }

    .hero p {
        color: #F0F3FF;
        margin: 0;
        font-size: 1rem;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 750;
        color: #24345A;
        margin: 22px 0 12px 0;
    }

    .subject-card {
        background: white;
        border: 1px solid #E7EBF5;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 10px;
        box-shadow: 0 3px 12px rgba(30,50,100,0.035);
    }

    .subject-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #283657;
    }

    .subject-detail {
        color: #69758D;
        font-size: 0.9rem;
        margin-top: 7px;
    }

    .small-label {
        color: #69758D;
        font-size: 0.9rem;
    }

    div.stButton > button {
        border-radius: 12px;
        min-height: 42px;
        font-weight: 650;
        border: 1px solid #DCE3F4;
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="primary"] {
        background: #526DE5;
        border-color: #526DE5;
        color: white;
    }

    div.stButton > button:hover {
        border-color: #526DE5;
        color: #526DE5;
    }

    div.stButton > button[kind="primary"]:hover {
        color: white;
        background: #4059CD;
    }

    [data-testid="stMetric"] {
        background: white;
        padding: 18px;
        border: 1px solid #E7EBF5;
        border-radius: 16px;
    }

    [data-testid="stExpander"] {
        background: white;
        border-radius: 14px;
        border: 1px solid #E5EAF5;
    }

    [data-testid="stProgressBar"] > div > div {
        background: #526DE5;
    }

    h1, h2, h3 {
        color: #24345A;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# 데이터 불러오기 / 저장하기
# ----------------------------------
def load_data():
    if DATA_FILE.exists():
        try:
            saved = json.loads(DATA_FILE.read_text(encoding="utf-8"))

            if not isinstance(saved, dict):
                raise ValueError("저장 데이터 형식이 올바르지 않습니다.")

            subjects = saved.get("subjects", {})
            timetable = saved.get("timetable", {})

            if not isinstance(subjects, dict):
                subjects = {}

            if not isinstance(timetable, dict):
                timetable = {}

            clean_subjects = dict(DEFAULT_SUBJECTS)

            for name, items in subjects.items():
                if isinstance(name, str) and isinstance(items, list):
                    clean_subjects[name] = [
                        str(item).strip()
                        for item in items
                        if str(item).strip()
                    ]

            clean_timetable = {}

            for day in DAYS:
                lessons = timetable.get(day, [])
                if not isinstance(lessons, list):
                    lessons = []

                clean_timetable[day] = [
                    subject for subject in lessons
                    if subject in clean_subjects
                ][:10]

            return {
                "subjects": clean_subjects,
                "timetable": clean_timetable
            }

        except (json.JSONDecodeError, OSError, ValueError):
            st.warning(
                "저장 파일을 읽지 못해 기본 데이터를 불러왔어요."
            )

    return {
        "subjects": dict(DEFAULT_SUBJECTS),
        "timetable": {day: [] for day in DAYS}
    }


def save_data(data):
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


if "school_data" not in st.session_state:
    st.session_state.school_data = load_data()

if "checked_items" not in st.session_state:
    st.session_state.checked_items = {}

data = st.session_state.school_data

# 새 기본 과목과 요일 반영
for subject, items in DEFAULT_SUBJECTS.items():
    data["subjects"].setdefault(subject, items)

for day in DAYS:
    data["timetable"].setdefault(day, [])

# ----------------------------------
# 사이드바
# ----------------------------------
with st.sidebar:
    st.markdown("## 🎒 스쿨백")
    st.caption("나의 스마트 학교생활 도우미")
    st.divider()

    menu = st.radio(
        "메뉴",
        [
            "🏠  오늘의 준비물",
            "📅  시간표 설정",
            "📝  준비물 관리",
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("### ✨ 이용 안내")
    st.caption("1. 시간표를 먼저 등록해요.")
    st.caption("2. 과목별 준비물을 확인해요.")
    st.caption("3. 준비물을 체크하고 완료해요.")

    st.divider()
    st.caption("나의 준비를 도와주는 스쿨백")

# ----------------------------------
# 홈: 오늘의 준비물
# ----------------------------------
if menu == "🏠  오늘의 준비물":
    today = date.today()

    st.markdown(f"""
    <div class="hero">
        <h1>🎒 오늘도 준비 완료!</h1>
        <p>시간표를 확인하고 필요한 준비물을 하나씩 챙겨 보세요.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown(
            f"### 📆 {today.strftime('%Y년 %m월 %d일')}"
        )

    with c2:
        if today.weekday() < 5:
            default_index = today.weekday()
        else:
            default_index = 0

        selected_day = st.selectbox(
            "확인할 요일",
            DAYS,
            index=default_index
        )

    lessons = data["timetable"].get(selected_day, [])
    all_items = []

    for subject in lessons:
        for item in data["subjects"].get(subject, []):
            if item not in all_items:
                all_items.append(item)

    check_key = f"{today.isoformat()}_{selected_day}"

    completed = sum(
        st.session_state.checked_items.get(
            f"{check_key}_{item}", False
        )
        for item in all_items
    )

    m1, m2, m3 = st.columns(3)

    m1.metric("📚 오늘의 수업", f"{len(lessons)}교시")
    m2.metric("🎒 준비물 종류", f"{len(all_items)}개")
    m3.metric("✅ 준비 완료", f"{completed}/{len(all_items)}개")

    st.markdown(
        '<div class="section-title">📚 오늘의 시간표</div>',
        unsafe_allow_html=True
    )

    if lessons:
        columns = st.columns(min(len(lessons), 3))

        for i, subject in enumerate(lessons):
            with columns[i % len(columns)]:
                icon = SUBJECT_ICONS.get(subject, "📘")

                st.markdown(f"""
                <div class="subject-card">
                    <div class="small-label">{i + 1}교시</div>
                    <div class="subject-name">
                        {icon} {subject}
                    </div>
                    <div class="subject-detail">
                        준비물 {len(data["subjects"].get(subject, []))}개
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info(
            "아직 시간표가 없어요. '시간표 설정' 메뉴에서 "
            "수업을 등록해 주세요."
        )

    st.markdown(
        '<div class="section-title">🎒 준비물 체크리스트</div>',
        unsafe_allow_html=True
    )

    if all_items:
        st.progress(
            completed / len(all_items),
            text=f"준비 진행률 · {completed}/{len(all_items)}개 완료"
        )

        left, right = st.columns([3, 1])

        with left:
            st.caption("챙긴 준비물에 체크 표시를 해 주세요.")

        with right:
            if st.button("🔄 체크 초기화", use_container_width=True):
                for item in all_items:
                    st.session_state.checked_items[
                        f"{check_key}_{item}"
                    ] = False
                st.rerun()

        for item in all_items:
            key = f"{check_key}_{item}"

            st.checkbox(
                f"🎒  {item}",
                value=st.session_state.checked_items.get(key, False),
                key=key
            )

            st.session_state.checked_items[key] = st.session_state[key]

        completed = sum(
            st.session_state.checked_items.get(
                f"{check_key}_{item}", False
            )
            for item in all_items
        )

        st.progress(
            completed / len(all_items),
            text=f"현재 준비 상태 · {completed}/{len(all_items)}개 완료"
        )

        if completed == len(all_items):
            st.success("🎉 모든 준비물을 챙겼어요! 오늘도 힘내세요!")
        else:
            st.info(
                f"아직 {len(all_items) - completed}개 준비물이 남아 있어요."
            )
    else:
        st.info("시간표와 과목별 준비물을 등록하면 여기에 표시돼요.")

# ----------------------------------
# 시간표 설정
# ----------------------------------
elif menu == "📅  시간표 설정":
    st.markdown("""
    <div class="hero">
        <h1>📅 나의 주간 시간표</h1>
        <p>요일별 수업과 교시를 설정하고 저장하세요.</p>
    </div>
    """, unsafe_allow_html=True)

    subject_names = list(data["subjects"].keys())

    if not subject_names:
        st.warning("먼저 과목을 등록해 주세요.")
        st.stop()

    for day in DAYS:
        with st.expander(
            f"📘 {day}",
            expanded=(day == "월요일")
        ):
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
                    f"{i + 1}교시 과목",
                    subject_names,
                    index=subject_names.index(previous),
                    key=f"lesson_{day}_{i}"
                )

                new_lessons.append(selected)

            data["timetable"][day] = new_lessons

            if new_lessons:
                st.caption(
                    " · ".join(
                        f"{i + 1}교시 {subject}"
                        for i, subject in enumerate(new_lessons)
                    )
                )
            else:
                st.caption("등록된 수업이 없어요.")

    if st.button(
        "💾 시간표 저장하기",
        type="primary",
        use_container_width=True
    ):
        try:
            save_data(data)
            st.success("시간표를 저장했어요!")
        except OSError:
            st.error(
                "파일을 저장하지 못했어요. 실행 환경의 파일 쓰기 권한을 확인해 주세요."
            )

# ----------------------------------
# 과목별 준비물 관리
# ----------------------------------
elif menu == "📝  준비물 관리":
    st.markdown("""
    <div class="hero">
        <h1>📝 과목별 준비물 관리</h1>
        <p>과목마다 필요한 물건을 등록하고 나에게 맞게 수정하세요.</p>
    </div>
    """, unsafe_allow_html=True)

    subject_names = list(data["subjects"].keys())

    selected_subject = st.selectbox(
        "과목 선택",
        subject_names,
        format_func=lambda s: f"{SUBJECT_ICONS.get(s, '📘')} {s}"
    )

    current_items = data["subjects"].get(selected_subject, [])

    st.markdown(
        f"### {SUBJECT_ICONS.get(selected_subject, '📘')} "
        f"{selected_subject} 준비물"
    )

    st.caption(
        "준비물은 쉼표로 구분해 입력하세요. "
        "줄바꿈으로 구분해도 돼요."
    )

    item_text = st.text_area(
        "준비물 목록",
        value=", ".join(current_items),
        height=160,
        placeholder="예: 교과서, 공책, 필통, 자",
        key=f"items_editor_{selected_subject}"
    )

    st.caption(f"현재 등록된 준비물: {len(current_items)}개")

    if st.button(
        "💾 준비물 저장하기",
        type="primary",
        use_container_width=True
    ):
        items = [
            item.strip()
            for item in item_text.replace("\n", ",").split(",")
            if item.strip()
        ]

        data["subjects"][selected_subject] = list(dict.fromkeys(items))

        try:
            save_data(data)
            st.success(f"{selected_subject} 준비물을 저장했어요!")
            st.rerun()
        except OSError:
            st.error(
                "파일을 저장하지 못했어요. 실행 환경의 파일 쓰기 권한을 확인해 주세요."
            )

    st.divider()
    st.markdown("### 📦 등록된 준비물 미리 보기")

    saved_items = data["subjects"].get(selected_subject, [])

    if saved_items:
        preview_columns = st.columns(2)

        for i, item in enumerate(saved_items):
            with preview_columns[i % 2]:
                st.markdown(
                    f'<div class="subject-card">🎒 {item}</div>',
                    unsafe_allow_html=True
                )
    else:
        st.info("등록된 준비물이 없어요. 위에서 준비물을 추가해 주세요.")

# ----------------------------------
# 하단 안내
# ----------------------------------
st.divider()
st.caption(
    "🎒 스쿨백 · 시간표와 준비물을 간편하게 관리하는 나만의 학교생활 도우미"
)
