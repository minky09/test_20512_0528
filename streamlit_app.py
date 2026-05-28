import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="아시아 축구선수 25/26 스탯 대시보드", layout="wide")

# 가상 데이터 생성 (실제로는 API나 DB에서 불러와야 합니다)
@st.cache_data
def load_data():
    data = {
        '선수명': ['손흥민', '이강인', '김민재', '구보 다케후사', '미토마 카오루', '황희찬'],
        '국적': ['대한민국', '대한민국', '대한민국', '일본', '일본', '대한민국'],
        '소속팀': ['토트넘 홋스퍼', '파리 생제르맹', '바이에른 뮌헨', '레알 소시에다드', '브라이튼', '울버햄튼'],
        '리그': ['프리미어리그', '리그 1', '분데스리가', '라리가', '프리미어리그', '프리미어리그'],
        '포지션': ['FW', 'MF', 'DF', 'MF', 'FW', 'FW'],
        '출장시간': [2800, 2100, 2900, 2400, 1800, 2200],
        '골': [15, 6, 2, 8, 5, 10],
        '도움': [8, 10, 1, 6, 4, 3],
        '평점': [7.4, 7.2, 7.3, 7.1, 6.9, 7.0]
    }
    return pd.DataFrame(data)

df = load_data()

# --- 사이드바 필터링 ---
st.sidebar.header("🔍 검색 및 필터")
selected_nation = st.sidebar.multiselect("국적 선택", options=df['국적'].unique(), default=df['국적'].unique())
selected_league = st.sidebar.multiselect("리그 선택", options=df['리그'].unique(), default=df['리그'].unique())
selected_position = st.sidebar.multiselect("포지션 선택", options=df['포지션'].unique(), default=df['포지션'].unique())

# 필터 적용
filtered_df = df[
    (df['국적'].isin(selected_nation)) & 
    (df['리그'].isin(selected_league)) & 
    (df['포지션'].isin(selected_position))
]

# --- 메인 화면 ---
st.title("🌏 25/26 시즌 아시아 축구선수 스탯 허브")
st.markdown("전 세계 주요 리그에서 활약하는 아시아 선수들의 활약상을 확인하세요.")

st.divider()

# 주요 스탯 요약 (KPI)
col1, col2, col3 = st.columns(3)
col1.metric("등록된 선수 수", f"{len(filtered_df)} 명")
col2.metric("총 득점", f"{filtered_df['골'].sum()} 골")
col3.metric("총 도움", f"{filtered_df['도움'].sum()} 개")

st.divider()

# 데이터 테이블 출력
st.subheader("📊 상세 스탯 테이블")
st.dataframe(filtered_df, use_container_width=True)

# 데이터 시각화 (공격 포인트)
st.subheader("📈 선수별 공격 포인트 (골+도움)")
if not filtered_df.empty:
    filtered_df['공격포인트'] = filtered_df['골'] + filtered_df['도움']
    fig = px.bar(filtered_df, x='선수명', y='공격포인트', color='국적', 
                 hover_data=['소속팀', '골', '도움'], text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("선택된 필터에 해당하는 선수가 없습니다.")