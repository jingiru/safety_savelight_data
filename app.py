import streamlit as st
from datetime import datetime
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from sklearn.linear_model import LinearRegression
from PIL import Image
from io import BytesIO
import base64
import os
import pytz

# NanumGothic 폰트 파일 경로 설정
font_path = os.path.join(os.getcwd(), 'NanumGothic.TTF')

# 폰트 설정
fontprop = fm.FontProperties(fname=font_path)

# 엑셀 파일 로드
file_path = './safety_savelight_data.xlsx'
source_data = pd.read_excel(file_path, sheet_name='weekly')
info_data = pd.read_excel(file_path, sheet_name='raw_data')

# 날짜 형식 변환
source_data['시작 일자'] = pd.to_datetime(source_data['시작 일자'])
source_data['종료 일자'] = pd.to_datetime(source_data['종료 일자'])


# 한국 시간으로 현재 날짜를 가져오기
tz = pytz.timezone('Asia/Seoul')
current_time_kst = datetime.now(tz)


# Streamlit 사용자 입력: 날짜 선택
st.markdown(
    """
    <style>
    .title-container {
        text-align: center;
        margin-top: 20px;
        padding: 20px;
        background-color: #f4f4f9;
        color: #333;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .title {
        font-size: 42px;
        font-weight: 600;
        margin: 0;
        color: #2c3e50;
    }
    .subtitle {
        text-align: center;
        font-size: 24px;
        font-weight: 500;
        margin-top: 5px;
        color: #7f8c8d;
    }
    .description {
        text-align: center;
        font-size: 18px;
        margin-top: 10px;
        color: #7f8c8d;
    }
    .prediction {
        text-align: center;
        font-size: 20px;
        margin-top: 20px;
        font-weight: bold;
    }
    .signal-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
    }
    .signal {
        text-align: center;
        font-size: 25px;
        font-weight: bold;
        padding: 10px;
        border-radius: 15px;
        display: inline-block;
        width: 200px;
        margin-bottom: 20px;
    }
    .signal-green {
        color: #2ecc71;
        background-color: #e8f5e9;
    }
    .signal-orange {
        color: #f39c12;
        background-color: #fffde7;
    }
    .signal-red {
        color: #e74c3c;
        background-color: #ffebee;
    }
    .quote-container {
    text-align: center;
    margin-top: 20px;
    padding: 1px;
    border-radius: 10px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    }

    .quote {
        text-align: center;
        font-size: 16px;
        margin: 0; /* 상자 안쪽 여백 제거 */
        font-weight: bold;
        color: #333;
        background-color: #f9f9f9;
    }

    .quote::before {
        content: '“';
        font-size: 30px;
        color: #aaa;
        vertical-align: middle;
    }

    .quote::after {
        content: '”';
        font-size: 30px;
        color: #aaa;
        vertical-align: middle;
    }

    .quote-author {
        font-size: 14px;
        font-style: italic;
        color: #555;
        margin-top: -10px;
        margin-bottom: 5px;
    }
    hr {
        margin: 30px 0;
        border: 0;
        border-top: 2px solid #ddd;
        width: 100%;
        align-self: center;
    }
    </style>
    <div class="title-container">
        <div class="title">[ 학교 안전 수호등 ]</div>
        <div class="subtitle">2024학년도 학교 안전 사고 예측 서비스</div>
    </div>
    <hr>
    <div class="description">기본적으로 오늘 날짜입니다.<br>필요한 경우, 원하는 날짜를 선택하세요.</div>
    """,
    unsafe_allow_html=True
)

# 날짜 범위 설정
min_date = datetime(2024, 3, 4)
max_date = datetime(2025, 2, 28)
 
st.subheader(":date:")
date_input = st.date_input("날짜를 선택하세요. 2024학년도의 날짜(2024.03.04~2025.02.28.)만 선택 가능", current_time_kst, min_value=min_date, max_value=max_date)

# 선택된 날짜와 주차 정보 확인
current_date = pd.to_datetime(date_input)

week_info = source_data[(source_data['시작 일자'] <= current_date) & (source_data['종료 일자'] >= current_date)]
if not week_info.empty:
    current_week_number = week_info.iloc[0]['주차']
    st.success(f"선택한 날짜 ({current_date.date()})는 2024학년도의 {current_week_number}입니다.")
else:
    st.error("해당 날짜에 대한 주차 정보를 찾을 수 없습니다.")
    current_week_number = None

# info.xlsx에서 데이터 준비
years = ['2019학년도', '2020학년도', '2021학년도', '2022학년도', '2023학년도']
norm_years = ['2019정규', '2020정규', '2021정규', '2022정규', '2023정규']

# 통합 명언 목록
quotes = [
    ("위험은 자신이 무엇을 하는지 모르는데서 온다", "워렌 버핏"),
    ("위험을 피하려면 항상 최악의 상태를 대비해두어야 한다", "그라시야"),
    ("미리 예견한 위험은 반쯤 피한 것이나 다름없다", "토마스 풀러"),
    ("오직 하나만 생각할 때, 그것보다 위험한 것은 없다", "알랭"),
    ("당신이 단 한 가지의 생각을 가지고 있을 때가 가장 위험하다", "에밀 사르티에"),
    ("안전은 자연스럽게 일어나는 것이 아니라 노력을 기울여 만들어진 것이다", "마크 트웨인"),
    ("안전은 발명이 아닌 태도이다", "스페인 속담"),
    ("안전은 성공의 열쇠이다", "폴 마르네프"),
    ("안전은 모든 자유 중 가장 중요한 것이다", "피델 카스트로"),
    ("안전은 운의 문제가 아니라 예방의 문제다", "포르투갈 속담"),
    ("안전은 성고을 위한 열쇠입니다", "지그 지글러"),
    ("안전은 세심한 주의의 결과이다", "헤로도트"),
    ("안전은 지식, 사고, 의지에서 발생해야 하는 것입니다", "루크레티오스 스루스러"),
    ("안전은 항상 당신의 손에 있습니다", "시세로"),
    ("위험은 사람들이 최선의 일을 하도록 만드는 조건이다", "존 A. 록펠러"),
    ("안전은 사람들이 하루 일을 마칠 수 있을 만큼만 충분히 많이 아는 것이다", "노맨 애글"),
    ("안전은 우리가 지키지 않으면 안 되는 유일한 것이다", "더글러스 아덤스"),
    ("안전은 모두를 위한 것이고, 위험은 아무도 위한 것이 아니다", "미건 애리스토틀"),
    ("안전을 위해 생각하고 일하기, 그게 진정한 승리다", "나폴레옹 보나파르트"),
    ("안전은 효율적인 일의 일부이다. 그것은 동시에 삶의 일부이다", "헨리 포드"),
    ("생명을 지키기 위한 일은 언제나 허용되는 일이다", "토마스 제퍼슨"),
    ("위험을 회피하기 위해 어떤 시도도 하지 말라는 의미는 아니다. 위험을 효과적으로 관리해야 한다는 것이다", "레이닌 스톤"),
    ("잠재적 위험을 식별하고 관리하지 않으면, 그 위험은 당신에게서 자신의 권한을 빼앗아 갈 수 있다", "스티븐 스타크"),
    ("위험은 피할 수 있는 것도 있지만, 감수할 수 없는 것도 있다", "톰 클랜시"),
    ("안전은 우리가 지킬 수 있는 유일한 것이다", "아인슈타인"),
    ("안전은 우리가 무엇이든 할 수 있는 유일한 투자다", "존 F. 케네디")
]


# 명언과 저자 이름을 표시하는 함수
def show_quote_with_author(quote, author):
    st.markdown(f"""
    <div class="quote-container">
        <div class="quote">
            {quote}
        </div>
        <div class="quote-author">- {author}</div>
    </div>
    """, unsafe_allow_html=True)
def get_random_quote():
    quote, author = random.choice(quotes)
    return quote, author

def show_signal_and_image(signal_class, message, image_file):
    # 신호등과 이미지 함께 표시
    st.markdown(f"""
    <div class='signal-container'>
        <div style="margin-bottom: 5px; margin-top: -25px;">
            <img src="data:image/png;base64,{get_image_base64(image_file)}" alt="{message}" style="width: 430px;">
        </div>
        <div class='signal {signal_class}'>● {message}</div>
    </div>
    """, unsafe_allow_html=True)

def get_image_base64(image_file):
    with open(image_file, "rb") as img_file:
        buffered = BytesIO(img_file.read())
        base64_str = base64.b64encode(buffered.getvalue()).decode()
    return base64_str

if current_week_number:
    current_week_data = info_data[info_data['학사일정 주차'] == current_week_number][years].values.flatten()
    current_week_norm_data = info_data[info_data['학사일정 주차'] == current_week_number][norm_years].values.flatten()

    if len(current_week_data) > 0 and len(current_week_norm_data) > 0:
        # 선형 회귀 모델 학습 및 예측
        X = np.array([2019, 2020, 2021, 2022, 2023]).reshape(-1, 1)
        y = current_week_norm_data

        model = LinearRegression()
        model.fit(X, y)

        # 회귀식 계수 및 절편
        coef = model.coef_[0]
        intercept = model.intercept_

        # 2024학년도 예측
        predicted_value_2024 = model.predict(np.array([[2024]]))[0]

        # 예측값을 확률로 변환 (0에서 1 사이의 값으로 가정)
        probability = min(max(predicted_value_2024, 0), 1)
        probability_percentage = probability * 100  # 확률을 백분율로 변환

        # 신호등 색상 및 이미지 결정
        if probability < 0.3:
            signal_class = 'signal-green'
            message = '안전'
            image_file = 'green.png'
        elif probability < 0.7:
            signal_class = 'signal-orange'
            message = '주의'
            image_file = 'yellow.png'
        else:
            signal_class = 'signal-red'
            message = '위험'
            image_file = 'red.png'

        # 시각화
        fig, ax = plt.subplots(figsize=(12, 6))

        # x축 레이블에 폰트 적용
        ax.set_xticks(range(len(years)))
        ax.set_xticklabels(years, fontproperties=fontprop)

        # x축 구성
        ax.bar(years, current_week_data, color='skyblue', edgecolor='black')

        # 포인트 위에 정수 값 레이블 달기
        for i, val in enumerate(current_week_data):
            ax.text(i, val + 0.05, f'{int(val)}', ha='center', va='bottom', fontsize=12,
                    bbox=dict(facecolor='white', alpha=0.6, edgecolor='blue', boxstyle='round,pad=0.5'))

        ax.set_xlabel('학년도', fontsize=14, fontproperties=fontprop)
        ax.set_ylabel('사고 건수', fontsize=14, fontproperties=fontprop)
        
        # 2024학년도 예측 결과 및 신호등 색상 표시
        st.markdown(f"<div class='prediction'>2024학년도 {current_week_number}에 안전 사고가 발생할 확률은 {probability_percentage:.2f}%입니다.</div>", unsafe_allow_html=True)
        
        # 신호등과 이미지 표시
        show_signal_and_image(signal_class, message, image_file)

        # 랜덤 명언과 저자 이름 추출
        quote, author = get_random_quote()
        show_quote_with_author(quote, author)


        # 서브타이틀 추가 및 그래프 표시
        st.divider()
        st.markdown(f"<div class='subtitle'>{current_week_number} 각 학년도 사고 건수</div>", unsafe_allow_html=True)
        st.pyplot(fig)

    else:
        st.error("해당 주차에 대한 데이터가 없습니다.")
else:
    st.error("주차 정보를 찾을 수 없습니다.")
