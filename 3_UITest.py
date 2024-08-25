import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates

# 한글 폰트 설정
# font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'  # MacOS의 경우
# fontprop = fm.FontProperties(fname=font_path)
# plt.rcParams['font.family'] = fontprop.get_name()

# CSV 파일 읽기
df = pd.read_csv('weather_Korean.csv', encoding='utf-8-sig')

# '일시' 열을 datetime 형식으로 변환
df['일시'] = pd.to_datetime(df['일시'])

# 지점명 리스트 생성
stations = df['지점명'].unique()

# 선택 가능한 항목 리스트 생성 (일강수량 이외의 모든 항목)
columns = df.columns.tolist()
columns.remove('지점명')
columns.remove('일시')

# Streamlit UI 구성
st.title('기상 데이터 그래프')
selected_station = st.selectbox('지점명을 선택하세요:', stations)
selected_column = st.selectbox('항목을 선택하세요:', columns)

# 선택된 지점명의 데이터 필터링
filtered_df = df[df['지점명'] == selected_station]

# 결측값 보간
filtered_df[selected_column] = filtered_df[selected_column].interpolate()

# 선택된 항목의 라인 그래프 그리기
fig, ax = plt.subplots()
ax.plot(filtered_df['일시'], filtered_df[selected_column])
ax.set_xlabel('일시')
ax.set_ylabel(selected_column)
ax.set_title(f'{selected_station}의 {selected_column}')

# x축 날짜 값을 1달 간격으로 표시
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# x축 레이블 회전
plt.xticks(rotation=45)

# Streamlit에 그래프 표시
st.pyplot(fig)
