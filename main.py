import os
from dotenv import load_dotenv
from langchain_unstructured import UnstructuredLoader

load_dotenv()  # .env의 키를 메모리로 불러오기

# ───────────────────────────────────────────────
# UnstructuredLoader 설정
# ───────────────────────────────────────────────
loader = UnstructuredLoader(
    file_path="./data/sample_text.pdf",                      # 파싱할 파일 경로
    api_key=os.getenv("UNSTRUCTURED_API_KEY"),   # 신분증
    url=os.getenv("UNSTRUCTURED_API_URL"),       # 서버 주소
    partition_via_api=True,                      # ⭐ 핵심! True = 서버에서 처리
    strategy="fast",                             # fast(빠름/저렴) vs hi_res(정확/느림)
    chunking_strategy="by_title",                # 제목 단위로 문서를 잘라줌 (RAG에 유리)
    max_characters=1000,                         # 조각 하나의 최대 글자 수
)

# ───────────────────────────────────────────────
# 실행 및 결과 확인
# ───────────────────────────────────────────────
docs = loader.load()

print(f"📄 총 {len(docs)}개의 조각(chunk)으로 분리되었습니다.\n")

# 앞 3개 조각만 미리보기
for i, doc in enumerate(docs[:3]):
    print(f"--- [조각 {i+1}] ---")
    print(doc.page_content[:200])        # 내용 앞 200자
    print(f"메타데이터: {doc.metadata.get('page_number')}페이지\n")