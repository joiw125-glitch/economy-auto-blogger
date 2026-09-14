import os
import requests
from google import genai

# 환경 변수에서 키 불러오기
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def generate_economy_content():
client = genai.Client(api_key=GEMINI_API_KEY)

prompt = """
당신은 5060 중장년층과 직장인을 타깃으로 하는 전문 경제/재테크 블로그 라이터이자, SEO 콘텐츠 디자이너입니다.
오늘 날짜 기준으로 최근 대중에게 화제가 되었거나 이슈가 된 경제 뉴스, 금리, 물가, 부동산, 또는 생활 재테크 정보 중 하나를 선정하고, 아래 지침에 맞춰 블로그 포스팅을 작성해 주세요.

[Part 1. HTML 태그 구조 지침]
- 티스토리 HTML 에디터에 바로 붙여넣을 수 있도록, 반드시 **HTML 태그(`<h3>`, `<h4>`, `<p>`, `<ul>`, `<li>`, `<strong>` 등)**를 사용하여 가독성 있게 작성하세요.
- 글의 대제목(단락 제목)은 반드시 `<h3>` 태그를 사용하세요.
- 세부 소제목이나 항목 제목은 반드시 `<h4>` 태그를 사용하세요.

글의 흐름은 반드시 아래 6가지 구조를 따르세요:
1. [도입부]: 최근 경제 이슈 발생 배경과 독자들의 일상에 미치는 영향 설명.
2. [핵심 배경 및 원인]: 이 이슈가 왜 나타났는지 이해하기 쉽게 3가지로 설명.
3. [내 자산/생활에 미치는 영향]: 독자들이 실질적으로 알아야 할 손익이나 변화 포인트.
4. [대응 전략 및 실천 팁]: 지금 시점에서 개인이 취해야 할 현명한 대처 방법.
5. [전문가 조언 및 주의사항]: 섣부른 투자나 무리한 행동을 경계하는 조언.
6. [마치며]: 전체 요약 및 따뜻한 응원의 메시지.

[Part 2. 쿠팡 파트너스 및 추천제품 지침]
- **[중요]** 본문 맨 상단(제목 바로 아래, 도입부 시작 전)에 아래 공정고시 문구를 HTML로 반드시 배치해 주세요.
<p style="font-size: 13px; color: #555; margin-bottom: 20px;"><em>"이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."</em></p>
- [태그] 윗부분에 **[쿠팡 추천제품]** 항목을 만들어, 경제/재테크 관련 도서나 가계부, 혹은 실생활 유용 상품을 1개 추천해 주세요.

[Part 3. Tone & Writing Style]
- 어조: 신뢰감 있으면서도 친절하고 이해하기 쉬운 구어체 (~입니다, ~습니다).
- 객관성: "무조건 오른다/떨어진다"는 단정적 표현 대신 "가능성이 높습니다", "대비가 필요합니다" 표현 사용.

[Output Format (출력 양식)]
반드시 아래 양식에 맞춰 출력해 주세요:

[제목]: (시선을 사로잡는 경제 블로그 제목 작성)

[HTML 본문]:
(상단 공정고시 문구가 포함되고, <h3>와 <h4> 태그가 적용된 전체 HTML 본문 작성)

[쿠팡 추천제품]: 
- 추천 상품명: (예: 돈의 속성 (도서) / 가계부 등)

[태그]: 
#경제이슈 #재테크 #생활경제 #연관키워드 ... (10~15개의 해시태그)

[썸네일 문구 및 프롬프트]:
- 메인 타이틀: (핵심 키워드 중심의 직관적이고 굵은 텍스트)
- 서브 타이틀: (한눈에 들어오는 부제목 또는 경고/알림 문구)
- 이미지 생성 프롬프트: (신뢰감을 주는 금융/경제 스타일 배경에 중앙/하단에 선명한 한국어 텍스트 레이아웃이 적용된 썸네일 생성을 위한 영문 프롬프트)
"""

response = client.models.generate_content(
model="gemini-3.6-flash",
contents=prompt,
)
return response.text

def send_to_telegram(message):
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

payload = {
"chat_id": TELEGRAM_CHAT_ID,
"text": message,
"parse_mode": "HTML"
}

response = requests.post(url, json=payload)
if response.status_code == 200:
print("텔레그램으로 경제 글 전송 성공!")
else:
print(f"전송 실패: {response.text}")

if __name__ == "__main__":
print("AI가 오늘의 경제 이슈를 검색하고 글을 작성 중입니다...")
blog_post = generate_economy_content()
send_to_telegram(blog_post)
