import streamlit as st

# MBTI 유형별 추천 직업 데이터 (이전과 동일)
mbti_jobs = {
    "INTJ": ["🤔 전략가", "🧑‍🔬 과학자", "💻 시스템 분석가", "🏛️ 건축가", "⚖️ 변호사"],
    "INTP": ["💡 아이디어뱅크", "🤔 철학자", "👨‍🏫 교수", "💻 프로그래머", "✍️ 작가"],
    "ENTJ": ["🧑‍✈️ 통솔자", "🚀 경영 컨설턴트", "🤵 CEO", "👨‍⚖️ 판사", "🕴️ 정치인"],
    "ENTP": ["🗣️ 토론가", "📢 발명가", "벤처 사업가", "👨‍💼 마케터", "🎬 영화감독"],
    "INFJ": ["🧑‍⚕️ 상담사", "✍️ 작가", "🧑‍🎨 예술가", "👨‍🏫 교사", "🤝 사회복지사"],
    "INFP": ["🧘 중재자", "✍️ 시인/소설가", "🧑‍🎨 그래픽 디자이너", "📚 사서", "🧠 심리학자"],
    "ENFJ": ["👨‍🏫 선도자", "🤝 사회복지사", "🗣️ HR 전문가", "👨‍💼 컨설턴트", "🌍 외교관"],
    "ENFP": ["🥳 활동가", "🧑‍🎨 배우", "✍️ 카피라이터", "🎤 언론인", "🎉 이벤트 플래너"],
    "ISTJ": ["꼼꼼한 행정가", "👮 회계사", "💻 데이터 분석가", "🧑‍🔧 엔지니어", "👨‍✈️ 파일럿"],
    "ISFJ": ["🧑‍⚕️ 간호사", "👨‍🏫 초등학교 교사", "🎨 인테리어 디자이너", "🧑‍🍳 요리사", "🤝 고객 서비스 담당자"],
    "ESTJ": ["🏢 관리자", "👮 경찰관", "🧑‍🏭 감독관", "👨‍💼 영업 관리자", "💰 은행원"],
    "ESFJ": ["🤝 사교적인 외교관", "🧑‍🏫 교사", "🧑‍⚕️ 의사", "🏨 호텔 매니저", "🥰 홍보 전문가"],
    "ISTP": ["🛠️ 만능재주꾼", "🧑‍🚒 소방관", "🧑‍✈️ 조종사", "💻 네트워크 엔지니어", "🏃 운동선수"],
    "ISFP": ["🧑‍🎨 예술가", "🎶 음악가", "🏞️ 조경사", "🐾 수의사", "📸 사진작가"],
    "ESTP": ["🎲 사업가", "🧑‍🚒 구조대원", "👨‍💼 영업사원", "📢 MC", "🎭 연기자"],
    "ESFP": ["🎤 연예인", "🧑‍🎨 디자이너", "🎉 파티 플래너", "🧑‍🏫 유치원 교사", "✈️ 승무원"]
}

# 간이 MBTI 검사 질문
questions = {
    "EI": {
        "question": "🤔 나는 주로...",
        "options": {"E": "다른 사람들과 어울리며 에너지를 얻는다 🎉", "I": "혼자만의 시간을 통해 에너지를 충전한다 🔋"},
        "values": {"다른 사람들과 어울리며 에너지를 얻는다 🎉": "E", "혼자만의 시간을 통해 에너지를 충전한다 🔋": "I"}
    },
    "SN": {
        "question": "🌳 정보를 받아들일 때 나는...",
        "options": {"S": "현재 실제로 보고 듣는 것에 집중한다 👀", "N": "이면의 의미나 가능성을 더 생각한다 🤔"},
        "values": {"현재 실제로 보고 듣는 것에 집중한다 👀": "S", "이면의 의미나 가능성을 더 생각한다 🤔": "N"}
    },
    "TF": {
        "question": "❤️ 결정을 내릴 때 주로...",
        "options": {"T": "논리적이고 객관적인 분석을 중요하게 생각한다 🧠", "F": "다른 사람들과의 관계나 감정을 고려한다 🥰"},
        "values": {"논리적이고 객관적인 분석을 중요하게 생각한다 🧠": "T", "다른 사람들과의 관계나 감정을 고려한다 🥰": "F"}
    },
    "JP": {
        "question": "📅 나는 생활할 때...",
        "options": {"J": "계획을 세우고 체계적으로 진행하는 것을 좋아한다 ✅", "P": "상황에 맞춰 유연하게 대처하는 것을 선호한다 🤸"},
        "values": {"계획을 세우고 체계적으로 진행하는 것을 좋아한다 ✅": "J", "상황에 맞춰 유연하게 대처하는 것을 선호한다 🤸": "P"}
    }
}

# 앱 상태 초기화 (세션 상태 사용)
if 'mbti_result' not in st.session_state:
    st.session_state.mbti_result = None
if 'test_taken' not in st.session_state:
    st.session_state.test_taken = False
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# 웹앱 제목 설정
st.title("🌟 MBTI 간이검사 & 추천 직업 찾기 🌟")

if not st.session_state.test_taken:
    st.header("📝 간이 MBTI 검사")
    st.write("아래 질문에 답변하고 당신의 MBTI 유형을 알아보세요! 👇")

    for key, q_data in questions.items():
        answer = st.radio(q_data["question"], list(q_data["options"].values()), key=f"q_{key}")
        st.session_state.answers[key] = q_data["values"][answer]

    if st.button("✔️ 결과 보기!"):
        result = ""
        result += st.session_state.answers["EI"]
        result += st.session_state.answers["SN"]
        result += st.session_state.answers["TF"]
        result += st.session_state.answers["JP"]
        st.session_state.mbti_result = result
        st.session_state.test_taken = True
        st.rerun() # 페이지를 새로고침하여 결과 표시 부분으로 넘어감

else:
    # MBTI 결과 및 직업 추천 표시
    selected_mbti = st.session_state.mbti_result
    st.header(f"🥳 당신의 MBTI는 **{selected_mbti}** 입니다!")

    if selected_mbti in mbti_jobs:
        st.subheader(f"🎉 {selected_mbti} 유형에게 추천하는 직업들이에요! 🎉")
        jobs = mbti_jobs[selected_mbti]
        for job in jobs:
            st.markdown(f"- {job}")
        st.balloons() # 결과 표시 시 풍선 효과! 🎈
    else:
        st.error("앗! 해당 MBTI 유형에 대한 직업 정보가 아직 준비되지 않았어요. 😥")

    if st.button("🔄 다시 검사하기"):
        # 상태 초기화
        st.session_state.mbti_result = None
        st.session_state.test_taken = False
        st.session_state.answers = {}
        st.rerun()


st.sidebar.header("ℹ️ 앱 정보")
st.sidebar.info(
    "이 앱은 간이 MBTI 검사를 통해 성격 유형을 알아보고, "
    "해당 유형에 맞는 추천 직업을 제공하여 진로 탐색에 도움을 주기 위해 만들어졌습니다. "
    "MBTI는 성격 선호도를 나타내는 지표이며, 직업 선택은 개인의 흥미, 역량, 가치관 등 다양한 요소를 고려해야 합니다. "
    "재미로 참고해주세요! 😊"
)
