import streamlit as st
from datetime import date
from collections import Counter
from deep_translator import GoogleTranslator
import re
import os

st.title("나만의 일기 앱 (한/영 2분할)")

# 날짜 선택
selected_date = st.date_input("날짜 선택", date.today())

# 파일 경로
filename = f"diary_{selected_date}.txt"

# 불러오기 (파일이 있으면 내용 읽기)
loaded_korean = ""
loaded_english = ""
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    # 간단하게 국문/영문 분리
    parts = content.split("영문 일기:\n")
    if len(parts) == 2:
        kor_part = parts[0].replace("국문 일기:\n", "").strip()
        eng_part = parts[1].strip()
        loaded_korean = kor_part
        loaded_english = eng_part

# 위쪽: 국문 일기
st.subheader("국문 일기")
korean_text = st.text_area("오늘의 일기 (한글)", value=loaded_korean, height=200)

# 키워드 추출 함수 (5개 고정)
def extract_keywords(text):
    words = re.findall(r"[가-힣]+", text)
    words = [w for w in words if len(w) > 1]
    counter = Counter(words)
    return [w for w, _ in counter.most_common(5)]

keywords_en = []
if korean_text.strip():
    keywords_ko = extract_keywords(korean_text)
    for kw in keywords_ko:
        translated = GoogleTranslator(source='ko', target='en').translate(kw)
        keywords_en.append(translated)

# 아래쪽: 영문 일기
st.subheader("영문 일기")
if keywords_en:
    st.info("추천 키워드 (영문): " + ", ".join(keywords_en))

english_text = st.text_area("Today's Diary (English)", value=loaded_english, height=200)

# 저장 버튼
if st.button("저장"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("국문 일기:\n")
        f.write(korean_text + "\n\n")
        f.write("영문 일기:\n")
        f.write(english_text)
    st.success(f"{filename} 에 저장되었습니다!")
