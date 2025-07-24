import streamlit as st
import pandas as pd

# --- 1. 페이지 기본 설정 ---
# 웹 페이지의 제목, 아이콘, 레이아웃을 설정합니다.
st.set_page_config(
    page_title="지식정보처리 역량 진단",
    page_icon="📝",
    layout="centered",
)

# --- 2. 설문 데이터 정의 ---
# 이미지에 명시된 설문 문항들을 리스트로 정의합니다.
questions = [
    "1. 과제를 해결하는 데 도움이 될 만한 자료(예: 인터넷 사이트, 책 등)나 사람들을 잘 알고 있다.",
    "2. 여러 자료들 중에서 가장 도움이 되는 것을 먼저 살펴본다.",
    "3. 필요할 때 손쉽게 찾을 수 있도록 자료를 정리해 둔다.",
    "4. 자료들을 사용하기 쉽게 내 방식대로 모아서나 순서를 바꾼다.",
    "5. 글을 그림으로 표현하거나, 그림을 글로 설명하는 식으로 새롭고 쓸모 있는 자료들을 만든다.",
    "6. 컴퓨터와 인터넷을 활용하여 다양한 정보를 얻을 수 있다.",
    "7. 컴퓨터나 인터넷 상의 다양한 자료(예: 강의·강연 동영상, 웹문서 파일 등)를 활용하여 학습할 수 있다.",
    "8. 내가 가지고 있는 정보를 SNS(예: 카카오톡, 페이스북 등)나 블로그 등을 통해 공유할 수 있다.",
    "9. 컴퓨터 프로그램(예: 워드, 파워포인트, 엑셀, 포토샵 등)을 이용해서 문서·그림·동영상 등을 만들거나 편집할 수 있다."
]

# 리커트 척도 응답 선택지를 리스트로 정의합니다.
options = [
    "① 전혀 그렇지 않다",
    "② 그렇지 않다",
    "③ 보통이다",
    "④ 그렇다",
    "⑤ 매우 그렇다"
]

# 점수 계산을 위해 각 응답에 해당하는 점수를 매핑하는 딕셔너리를 만듭니다.
score_map = {option: i + 1 for i, option in enumerate(options)}

# --- 3. 세션 상태 초기화 ---
# 현재 질문 인덱스와 응답을 저장할 세션 상태 변수를 초기화합니다.
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- 4. 웹 앱 UI 구성 ---
# 메인 제목을 표시합니다.
st.title("📝 지식정보처리 역량 진단 설문")

# 설문에 대한 안내 문구를 표시합니다.
st.markdown("---")
st.markdown("#### 각 문장을 읽고 자신을 가장 잘 나타낸다고 생각하는 번호를 선택해주세요.")
st.markdown("---")

# 모든 질문을 완료하지 않았을 때만 질문을 표시합니다.
if not st.session_state.submitted:
    current_index = st.session_state.current_question_index
    
    if current_index < len(questions):
        # 현재 질문을 가져옵니다.
        current_question = questions[current_index]
        question_key = f"Q{current_index + 1}"

        st.subheader(f"문항 {current_index + 1} / {len(questions)}")

        # 'st.form'을 사용하여 각 질문을 하나의 폼으로 묶습니다.
        with st.form(key=f"question_form_{current_index}"):
            # st.radio를 사용하여 현재 질문 항목을 만듭니다.
            # 이전에 응답한 값이 있다면 기본값으로 설정합니다.
            default_index = options.index(st.session_state.responses.get(question_key, "③ 보통이다"))
            
            selected_option = st.radio(
                label=current_question,
                options=options,
                index=default_index,
                horizontal=True,
                key=f"radio_{question_key}" # 라디오 버튼의 고유 키
            )
            
            col1, col2 = st.columns([1, 1])

            with col1:
                # 이전 버튼 (첫 번째 질문이 아닐 때만 표시)
                if current_index > 0:
                    if st.form_submit_button("◀️ 이전"):
                        st.session_state.responses[question_key] = selected_option # 현재 응답 저장
                        st.session_state.current_question_index -= 1
                        st.rerun() # 페이지 새로고침하여 이전 질문 표시
            
            with col2:
                # 다음 또는 결과 확인 버튼
                if current_index < len(questions) - 1:
                    if st.form_submit_button("다음 ▶️"):
                        st.session_state.responses[question_key] = selected_option # 현재 응답 저장
                        st.session_state.current_question_index += 1
                        st.rerun() # 페이지 새로고침하여 다음 질문 표시
                else:
                    # 마지막 질문일 경우 '결과 확인하기' 버튼 표시
                    if st.form_submit_button("✅ 결과 확인하기"):
                        st.session_state.responses[question_key] = selected_option # 마지막 응답 저장
                        st.session_state.submitted = True
                        st.rerun() # 페이지 새로고침하여 결과 표시
    else:
        # 모든 질문이 완료되었지만, submitted 상태가 False일 경우 (예외 처리)
        st.session_state.submitted = True
        st.rerun()

# --- 5. 결과 처리 및 표시 ---
# '결과 확인하기' 버튼이 눌렸거나 모든 질문이 완료되었을 때 아래 로직을 실행합니다.
if st.session_state.submitted:
    st.success("설문에 참여해주셔서 감사합니다!")
    st.markdown("---")
    st.subheader("📊 나의 응답 결과")

    # 응답 결과를 깔끔하게 보여주기 위해 pandas 데이터프레임을 사용합니다.
    result_data = {
        "문항 번호": [],
        "나의 응답": [],
        "점수": []
    }

    # 세션 상태에 저장된 응답을 기반으로 데이터프레임을 생성합니다.
    for i in range(len(questions)):
        q_key = f"Q{i+1}"
        if q_key in st.session_state.responses:
            response_text = st.session_state.responses[q_key]
            result_data["문항 번호"].append(f"{i+1}번")
            result_data["나의 응답"].append(response_text)
            result_data["점수"].append(score_map[response_text])

    # 데이터프레임 생성
    df = pd.DataFrame(result_data)

    # 인덱스를 숨기고 데이터프레임을 표 형태로 화면에 표시합니다.
    st.dataframe(df.set_index("문항 번호"), use_container_width=True)

    # 총점 계산
    total_score = df['점수'].sum()
    max_score = len(questions) * 5

    # 총점과 백분율을 계산하여 시각적으로 강조해서 보여줍니다.
    st.markdown("---")
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 10px; background-color: #f0f2f6;">
        <h3 style='text-align: center; color: #1E90FF;'>
            총점: <span style='font-size: 1.5em;'>{total_score}</span> / {max_score} 점
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # 간단한 결과 해석을 제공합니다.
    st.info("""
    **결과 해석 Tip:**
    - 점수가 높을수록 지식정보를 처리하고 활용하는 역량이 높다고 볼 수 있습니다.
    - 낮은 점수를 받은 문항을 확인하여 해당 역량을 보완하기 위한 계획을 세워볼 수 있습니다.
    """)

    # 설문 다시 시작 버튼
    if st.button("설문 다시 시작하기"):
        st.session_state.current_question_index = 0
        st.session_state.responses = {}
        st.session_state.submitted = False
        st.rerun()
