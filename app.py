import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime
import random

# NanumGothic 폰트 파일 경로 설정
font_path = 'NanumGothic.TTF'

# 폰트 설정
fontprop = fm.FontProperties(fname=font_path)
plt.rc('font', family=fontprop.get_name())


# 엑셀 파일 로드
file_path = './safety_savelight_data.xlsx'
source_data = pd.read_excel(file_path, sheet_name='weekly')
info_data = pd.read_excel(file_path, sheet_name='raw_data')

# 날짜 형식 변환
source_data['시작 일자'] = pd.to_datetime(source_data['시작 일자'])
source_data['종료 일자'] = pd.to_datetime(source_data['종료 일자'])

# Streamlit 사용자 입력: 날짜 선택
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #4CAF50;
        font-size: 36px;
        font-weight: bold;
        margin-top: 20px;
    }
    .subtitle {
        text-align: center;
        color: #FFC107;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .description {
        text-align: center;
        font-size: 18px;
        margin-bottom: 20px;
        color: #333;
    }
    .prediction {
        text-align: center;
        font-size: 20px;
        margin-top: 20px;
        font-weight: bold;
    }
    .signal-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .signal {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        padding: 20px;
        border-radius: 12px;
        display: inline-block;
        width: 200px;
    }
    .signal-green {
        color: green;
        background-color: #e8f5e9;
    }
    .signal-orange {
        color: orange;
        background-color: #fffde7;
    }
    .signal-red {
        color: red;
        background-color: #ffebee;
    }
    .quote {
        text-align: center;
        font-size: 24px;
        margin-top: 20px;
        font-weight: bold;
        padding: 20px;
        border-radius: 12px;
        color: #000;
        background-color: #f5f5f5;
        border: 2px solid #ccc;
    }
    .quote::before {
        content: '“';
        font-size: 36px;
        color: #ccc;
        vertical-align: middle;
    }
    .quote::after {
        content: '”';
        font-size: 36px;
        color: #ccc;
        vertical-align: middle;
    }
    </style>
    <div class="title">학교 안전 사고 예측 서비스</div>
    <div class="subtitle">웹 안전 수호등</div>
    <div class="description">기본적으로 오늘 날짜로 되어 있습니다.<br>필요한 경우, 원하는 날짜를 선택하세요.</div>
    """,
    unsafe_allow_html=True
)

date_input = st.date_input("날짜를 선택하세요", datetime.now())

# 선택된 날짜와 주차 정보 확인
current_date = pd.to_datetime(date_input)

week_info = source_data[(source_data['시작 일자'] <= current_date) & (source_data['종료 일자'] >= current_date)]
if not week_info.empty:
    current_week_number = week_info.iloc[0]['주차']
    st.success(f"선택한 날짜 ({current_date.date()})는 {current_week_number}입니다.")
else:
    st.error("해당 날짜에 대한 주차 정보를 찾을 수 없습니다.")
    current_week_number = None

# info.xlsx에서 데이터 준비
years = ['2019학년도', '2020학년도', '2021학년도', '2022학년도', '2023학년도']
norm_years = ['2019정규', '2020정규', '2021정규', '2022정규', '2023정규']

# 안전, 주의, 위험별 명언 목록
safety_quotes = [
    "안전은 모든 일의 시작이다.", "사고는 예방할 수 있다.", "안전은 습관이 되어야 한다.", 
    "위험을 예방하는 것이 가장 좋은 치료다.", "안전은 최우선이다.", "주위의 안전을 지키자.", 
    "안전은 모든 일의 기초이다.", "작은 조치가 큰 변화를 만든다.", "안전은 우리가 스스로 만들어 가는 것이다.", 
    "안전은 모든 것이 정상일 때도 기억해야 한다."
]
caution_quotes = [
    "주의는 위험을 감소시킨다.", "주의는 예방의 첫 걸음이다.", "자신과 타인을 보호하는 것이 주의이다.", 
    "주의 깊은 관찰이 사고를 막는다.", "작은 주의가 큰 문제를 예방한다.", "주의는 성과의 밑거름이다.", 
    "주의를 기울여 사고를 방지하자.", "경계는 항상 필요하다.", "주의는 절대 과잉이 아니다.", 
    "위험 요소를 발견하고 대처하자."
]
danger_quotes = [
    "위험은 준비가 부족할 때 발생한다.", "위험을 감지하고 대처하는 것이 중요하다.", 
    "위험은 즉시 조치를 취해야 한다.", "위험을 간과하면 큰 피해를 입을 수 있다.", 
    "위험한 상황에서는 냉정함이 필요하다.", "위험은 미리 예측하고 준비해야 한다.", 
    "위험에 대한 경각심을 갖자.", "위험은 항상 대비가 필요하다.", 
    "위험을 무시하면 큰 문제가 생길 수 있다.", "위험에 대해 항상 경각심을 갖자."
]

def get_random_quote(signal):
    if signal == 'signal-green':
        return random.choice(safety_quotes)
    elif signal == 'signal-orange':
        return random.choice(caution_quotes)
    elif signal == 'signal-red':
        return random.choice(danger_quotes)
    return ""

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

        # 신호등 색상 결정
        if probability < 0.3:
            signal_class = 'signal-green'
            message = '안전'
        elif probability < 0.7:
            signal_class = 'signal-orange'
            message = '주의'
        else:
            signal_class = 'signal-red'
            message = '위험'

        # 시각화
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(years, current_week_data, color='skyblue', edgecolor='black')

        # 포인트 위에 정수 값 레이블 달기
        for i, val in enumerate(current_week_data):
            ax.text(i, val + 0.05, f'{int(val)}', ha='center', va='bottom', fontsize=12,
                    bbox=dict(facecolor='white', alpha=0.6, edgecolor='blue', boxstyle='round,pad=0.5'))

        ax.set_xlabel('학년도', fontsize=14, FontProperties=fontprop)
        ax.set_ylabel('사고 건수', fontsize=14, FontProperties=fontprop)
        ax.set_title(f'{current_week_number} 각 학년도 사고 건수', fontsize=16, FontProperties=fontprop)
        st.pyplot(fig)

        # 2024학년도 예측 결과 및 신호등 색상 표시
        st.markdown(f"<div class='prediction'>2024학년도 {current_week_number}의 예측 학교 안전 사고 발생 확률은 {probability_percentage:.2f}%입니다.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='signal-container'><div class='signal {signal_class}'>● {message}</div></div>", unsafe_allow_html=True)

        # 랜덤 명언 표시
        quote = get_random_quote(signal_class)
        st.markdown(f"<div class='quote'>{quote}</div>", unsafe_allow_html=True)


    else:
        st.error("해당 주차에 대한 데이터가 없습니다.")
else:
    st.error("주차 정보를 찾을 수 없습니다.")
