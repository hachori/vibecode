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

# 20문항 MBTI 검사 질문 리스트
# 각 질문은 id, 지표(dichotomy), 질문 내용(text), 선택지(options)로 구성
# options: { "사용자에게 보여질 텍스트": "실제 값 (E/I, S/N, T/F, J/P 중 하나)" }
detailed_questions = [
    # E/I (외향/내향)
    {"id": "EI1", "dichotomy": "EI", "text": "1. 나는 주로...", "options": {"다른 사람들과 어울리며 에너지를 얻는다 🎉": "E", "혼자만의 시간을 통해 에너지를 충전한다 🔋": "I"}},
    {"id": "EI2", "dichotomy": "EI", "text": "2. 주말 계획을 세울 때...", "options": {"친구들과의 약속이나 모임을 먼저 생각한다 🥳": "E", "조용히 집에서 쉬거나 개인적인 활동을 선호한다 📚": "I"}},
    {"id": "EI3", "dichotomy": "EI", "text": "3. 처음 만나는 사람이 많은 자리에서 나는...", "options": {"먼저 다가가 말을 걸고 쉽게 어울린다 🗣️": "E", "다른 사람이 다가와 주기를 기다리거나 조용히 관찰한다 👤": "I"}},
    {"id": "EI4", "dichotomy": "EI", "text": "4. 고민이 생겼을 때...", "options": {"다른 사람에게 이야기하며 생각을 정리한다 💬": "E", "혼자 조용히 생각하며 해결책을 찾는다 🤔": "I"}},
    {"id": "EI5", "dichotomy": "EI", "text": "5. 단체 활동을 할 때...", "options": {"주도적으로 의견을 내고 사람들을 이끄는 편이다 📢": "E", "조용히 맡은 역할을 수행하거나 뒤에서 지원하는 편이다 🌿": "I"}},

    # S/N (감각/직관)
    {"id": "SN1", "dichotomy": "SN", "text": "6. 정보를 받아들일 때 나는...", "options": {"현재 실제로 보고 듣는 구체적인 사실에 집중한다 👀": "S", "이면의 의미, 패턴, 가능성을 더 생각한다 💭": "N"}},
    {"id": "SN2", "dichotomy": "SN", "text": "7. 새로운 것을 배울 때...", "options": {"실제 경험이나 실습을 통해 배우는 것을 선호한다 🛠️": "S", "이론이나 개념을 먼저 이해하고 전체적인 그림을 그린다 🗺️": "N"}},
    {"id": "SN3", "dichotomy": "SN", "text": "8. 대화할 때 나는...", "options": {"사실적이고 현실적인 주제를 주로 이야기한다 📌": "S", "추상적이거나 미래지향적인 아이디어를 나누는 것을 즐긴다 ✨": "N"}},
    {"id": "SN4", "dichotomy": "SN", "text": "9. 길을 찾을 때...", "options": {"지도나 내비게이션의 단계별 지시를 따른다 🧭": "S", "전체적인 방향 감각이나 직감에 의존하는 편이다 🌌": "N"}},
    {"id": "SN5", "dichotomy": "SN", "text": "10. 일을 설명할 때...", "options": {"구체적인 예시와 세부 사항을 들어 설명한다 📋": "S", "비유나 큰 그림을 통해 전체적인 개념을 전달한다 🖼️": "N"}},

    # T/F (사고/감정)
    {"id": "TF1", "dichotomy": "TF", "text": "11. 결정을 내릴 때 주로...", "options": {"논리적이고 객관적인 분석을 중요하게 생각한다 🧠": "T", "다른 사람들과의 관계나 감정, 가치를 고려한다 ❤️": "F"}},
    {"id": "TF2", "dichotomy": "TF", "text": "12. 친구가 고민을 털어놓을 때...", "options": {"문제의 원인을 분석하고 해결책을 제시하려 한다 💡": "T", "먼저 공감하고 위로하며 감정을 다독인다 🤗": "F"}},
    {"id": "TF3", "dichotomy": "TF", "text": "13. 비판을 받거나 논쟁이 생겼을 때...", "options": {"감정보다는 사실 관계와 논리에 집중한다 ⚖️": "T", "감정적으로 상처를 받거나 상대방의 기분을 신경 쓴다 😥": "F"}},
    {"id": "TF4", "dichotomy": "TF", "text": "14. 칭찬이나 인정을 받을 때 중요한 것은...", "options": {"나의 능력이나 성과에 대한 객관적인 평가 🏆": "T", "나를 향한 따뜻한 마음과 진심어린 격려 😊": "F"}},
    {"id": "TF5", "dichotomy": "TF", "text": "15. 다른 사람의 부탁을 받았을 때...", "options": {"합리적인지, 내가 할 수 있는 일인지 먼저 판단한다 🧐": "T", "거절하면 상대방이 실망할까 봐 마음이 쓰인다 💌": "F"}},

    # J/P (판단/인식)
    {"id": "JP1", "dichotomy": "JP", "text": "16. 나는 생활할 때...", "options": {"계획을 세우고 체계적으로 일을 처리하는 것을 좋아한다 📅": "J", "상황에 맞춰 즉흥적이고 유연하게 대처하는 것을 선호한다 🤸": "P"}},
    {"id": "JP2", "dichotomy": "JP", "text": "17. 여행을 갈 때...", "options": {"미리 일정을 짜고 숙소와 교통편을 예약한다 ✈️": "J", "대략적인 계획만 세우거나 가서 결정하는 편이다 🗺️🎒": "P"}},
    {"id": "JP3", "dichotomy": "JP", "text": "18. 마감 기한이 있는 일은...", "options": {"미리미리 시작해서 여유롭게 끝내는 편이다 ✅": "J", "마감 직전에 집중해서 해치우는 경향이 있다 🔥": "P"}},
    {"id": "JP4", "dichotomy": "JP", "text": "19. 나의 책상이나 방은 보통...", "options": {"잘 정돈되어 있고 물건들이 제자리에 있다 🧹": "J", "다소 어수선하지만 어디에 뭐가 있는지는 안다 📚🎨": "P"}},
    {"id": "JP5", "dichotomy": "JP", "text": "20. 갑작스러운 변화나 새로운 상황에 대해...", "options": {"예측 불가능한 상황에 스트레스를 받고 기존 계획을 고수하려 한다 🚧": "J", "새로운 가능성으로 보고 흥미를 느끼며 잘 적응한다 🌊": "P"}}
]


# 앱 상태 초기화
if 'mbti_result' not in st.session_state:
    st.session_state.mbti_result = None
if 'test_taken' not in st.session_state:
    st.session_state.test_taken = False
if 'answers' not in st.session_state:
    st.session_state.answers = {q["id"]: None for q in detailed_questions} # 각 질문 ID별 답변 저장

# 웹앱 제목 설정
st.title("🌟 MBTI 정밀검사 & 추천 직업 찾기 🌟")

if not st.session_state.test_taken:
    st.header("📝 MBTI 정밀 검사 (20문항)")
    st.write("아래 20가지 질문에 답변하고 당신의 MBTI 유형을 자세히 알아보세요! 👇")

    with st.form(key="mbti_form"):
        for q in detailed_questions:
            # 각 질문의 선택지 텍스트 리스트 생성
            option_texts = list(q["options"].keys())
            # 사용자의 선택을 라디오 버튼으로 받음
            user_choice_text = st.radio(q["text"], option_texts, key=q["id"], horizontal=True)
            # 사용자가 선택한 텍스트에 해당하는 실제 값(E/I, S/N 등)을 저장
            st.session_state.answers[q["id"]] = q["options"][user_choice_text]
            st.markdown("---") # 질문 사이에 구분선 추가

        submit_button = st.form_submit_button(label="✔️ 최종 결과 보기!")

    if submit_button:
        scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        for q_id, answer_value in st.session_state.answers.items():
            if answer_value: # 답변이 있는 경우에만 점수 계산
                scores[answer_value] += 1
        
        # MBTI 결과 계산
        mbti_type = ""
        mbti_type += "E" if scores["E"] > scores["I"] else "I"
        mbti_type += "S" if scores["S"] > scores["N"] else "N"
        mbti_type += "T" if scores["T"] > scores["F"] else "F"
        mbti_type += "J" if scores["J"] > scores["P"] else "P"
        
        st.session_state.mbti_result = mbti_type
        st.session_state.test_taken = True
        st.rerun()

else:
    # MBTI 결과 및 직업 추천 표시
    selected_mbti = st.session_state.mbti_result
    st.header(f"🥳 당신의 MBTI는 **{selected_mbti}** 입니다!")

    if selected_mbti in mbti_jobs:
        st.subheader(f"🎉 {selected_mbti} 유형에게 추천하는 직업들이에요! 🎉")
        jobs = mbti_jobs[selected_mbti]
        for job in jobs:
            st.markdown(f"- {job}")
        st.balloons()
    else:
        st.error("앗! 해당 MBTI 유형에 대한 직업 정보가 아직 준비되지 않았어요. 😥")

    if st.button("🔄 다시 검사하기"):
        st.session_state.mbti_result = None
        st.session_state.test_taken = False
        st.session_state.answers = {q["id"]: None for q in detailed_questions}
        st.rerun()

st.sidebar.header("ℹ️ 앱 정보")
st.sidebar.info(
    "이 앱은 20문항 MBTI 검사를 통해 성격 유형을 알아보고, "
    "해당 유형에 맞는 추천 직업을 제공하여 진로 탐색에 도움을 주기 위해 만들어졌습니다. "
    "MBTI는 성격 선호도를 나타내는 지표이며, 직업 선택은 개인의 흥미, 역량, 가치관 등 다양한 요소를 고려해야 합니다. "
    "재미로 참고해주세요! 😊"
)
