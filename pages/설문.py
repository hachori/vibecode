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

# --- 3. 웹 앱 UI 구성 ---
# 메인 제목을 표시합니다.
st.title("📝 지식정보처리 역량 진단 설문")

# 설문에 대한 안내 문구를 표시합니다.
st.markdown("---")
st.markdown("#### 각 문장을 읽고 자신을 가장 잘 나타낸다고 생각하는 번호를 선택해주세요.")
st.markdown("---")

# 'st.form'을 사용하여 모든 질문을 하나의 폼으로 묶습니다.
# 이렇게 하면 '제출하기' 버튼을 누를 때 모든 응답이 한 번에 처리됩니다.
with st.form("survey_form"):
    # 응답을 저장할 딕셔너리를 초기화합니다.
    responses = {}

    # 정의된 질문 리스트를 순회하며 각 질문에 대한 라디오 버튼을 생성합니다.
    for i, question in enumerate(questions):
        # st.radio를 사용하여 각 질문 항목을 만듭니다.
        # key를 고유하게 설정하여 각 질문의 응답을 구분합니다.
        # horizontal=True 옵션으로 버튼을 가로로 배열하여 공간을 효율적으로 사용합니다.
        responses[f"Q{i+1}"] = st.radio(
            label=question,
            options=options,
            index=2,  # 기본 선택값을 '③ 보통이다'로 설정합니다.
            horizontal=True
        )

    # 폼 내부에 제출 버튼을 생성합니다.
    submitted = st.form_submit_button("✅ 결과 확인하기")

# --- 4. 결과 처리 및 표시 ---
# '결과 확인하기' 버튼이 눌렸을 때 아래 로직을 실행합니다.
if submitted:
    st.success("설문에 참여해주셔서 감사합니다!")
    st.markdown("---")
    st.subheader("📊 나의 응답 결과")

    # 응답 결과를 깔끔하게 보여주기 위해 pandas 데이터프레임을 사용합니다.
    result_data = {
        "문항 번호": [f"{i+1}번" for i in range(len(questions))],
        "나의 응답": [responses[f"Q{i+1}"] for i in range(len(questions))],
        "점수": [score_map[responses[f"Q{i+1}"]] for i in range(len(questions))]
    }

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

