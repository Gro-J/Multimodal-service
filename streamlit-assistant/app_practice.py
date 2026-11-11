# ============================================================
# app_practice.py - [실습] OpenAI 없이 CLIP 만으로 사진을 찾는 앱 (돈이 안 들어요!)
# ============================================================
import streamlit as st
import fashion_rag_core as core

st.set_page_config(page_title="FashionRAG 실습", layout="wide")   # 꼭 제일 먼저!
st.title("실습: 패션 이미지 검색기")


@st.cache_resource(show_spinner="CLIP 모델 로딩 중...")   # 무거운 CLIP 은 냉장고에 한 번만
def load_collection():
    return core.get_collection()

collection = load_collection()

# [실습 1] 옆 서랍에 미끄럼 막대(슬라이더) 만들기
#   막대를 움직이면 → 파일이 1줄부터 다시 실행되고 → n 에 새 숫자가 들어가요
with st.sidebar:
    # 실습 1 완료: 가장 작게 1, 가장 크게 6, 처음 값 3
    n = st.slider("검색할 이미지 수", min_value=1, max_value=6, value=3)
    st.caption(f"DB 이미지 수: {collection.count()}장")

# [실습 2] 사물함(session_state)에 '검색 기록장' 만들기 - 다시 실행돼도 기록이 남아요
if "searches" not in st.session_state:             # 처음 한 번만 빈 기록장을 만들어요
    st.session_state.searches = []

query = st.text_input("영어 검색어를 입력하세요 (예: a red dress)")
if query:                                           # 뭔가 입력했다면
    results = core.query_db(collection, query, n_results=n)   # n 장 찾기
    cols = st.columns(n)                            # n 칸으로 가로 나누기
    for col, pid, uri, dist in zip(cols, results["ids"][0], results["uris"][0], results["distances"][0]):
        # [실습 3] 사진 아래 글(caption)에 이름표 pid 와 거리 dist(소수점 3자리) 표시
        #   예: image_0012 (거리 0.812)
        col.image(uri, caption=f"{pid} (거리 {dist:.3f})", width=200)
    if query not in st.session_state.searches:      # 같은 검색어는 두 번 적지 않기
        st.session_state.searches.append(query)     # 기록장 맨 뒤에 적기

st.subheader("검색 기록")
for q in st.session_state.searches:
    st.write("-", q)
