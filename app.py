import os
import json
import logging
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)
logger = logging.getLogger("mbti_recommender")

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Initialize Gemini Client if key exists
gemini_client = None
if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
else:
    logger.warning("GEMINI_API_KEY is not set or using placeholder.")


def search_serper(query: str, num_results: int = 3):
    """
    Search real-world information using Serper.dev API
    """
    if not SERPER_API_KEY or SERPER_API_KEY == "your_serper_api_key_here":
        logger.warning("SERPER_API_KEY is not configured. Returning fallback search items.")
        return []

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "gl": "kr",
        "hl": "ko",
        "num": num_results
    }

    try:
        logger.info(f"Serper API Request: Query='{query}'")
        resp = requests.post(url, headers=headers, json=payload, timeout=6)
        if resp.status_code == 200:
            data = resp.json()
            organic = data.get("organic", [])
            results = []
            for item in organic[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", "#"),
                    "snippet": item.get("snippet", "")
                })
            return results
        else:
            logger.error(f"Serper API HTTP Error {resp.status_code}: {resp.text}")
            return []
    except Exception as e:
        logger.error(f"Serper search failed: {str(e)}")
        return []


def generate_gemini_recommendations(mbti_type: str, ratios: dict):
    """
    Generate tailored activity recommendations and celebrities using Gemini API.
    Adheres strictly to cautious, flexible MBTI guidelines.
    """
    system_instruction = (
        "당신은 따뜻하고 신중한 성향 분석 및 라이프스타일 큐레이터입니다.\n"
        "[MBTI 사용 주의사항]\n"
        "1. MBTI는 참고용 성향 정보로만 활용하며 사용자의 성격이나 행동을 절대 단정 짓지 마세요.\n"
        "2. 어조는 항상 '~하는 경향이 있을 수 있습니다', '~한 활동을 즐기실 가능성이 높습니다'와 같이 유연하고 부드럽게 서술하세요.\n"
        "3. 응답은 반드시 유효한 JSON 형식이어야 합니다. 마크다운 코드블록(```json) 없이 순수 JSON 문자열만 반환하세요."
    )

    prompt = f"""
다음은 사용자의 설문 기반 성향 진단 결과입니다:
- MBTI 유형: {mbti_type}
- 성향 비율: E {ratios.get('E', 50)}% / I {ratios.get('I', 50)}%, S {ratios.get('S', 50)}% / N {ratios.get('N', 50)}%, T {ratios.get('T', 50)}% / F {ratios.get('F', 50)}%, J {ratios.get('J', 50)}% / P {ratios.get('P', 50)}%

위 정보를 바탕으로 아래 구조의 JSON 데이터를 생성해 주세요:
{{
  "summary": "{mbti_type} 성향을 가진 분들의 유연한 성향 요약 (2-3문장, 부드러운 어조)",
  "activities": [
    {{
      "title": "활동 이름 (예: 조용한 북카페 탐방, 러닝 크루 참여 등)",
      "reason": "해당 성향 분들이 이 활동에서 편안함이나 즐거움을 느끼기 쉬운 이유 (~할 가능성이 있습니다 체)",
      "search_keyword": "네이버나 구글에서 실제 장소나 모임을 찾기 좋은 한국어 검색 키워드 (예: 서울 조용한 북카페 추천)"
    }}
  ],
  "celebrities": [
    {{
      "name": "유명인 또는 친숙한 캐릭터 이름",
      "description": "이 유형의 매력적인 특성을 잘 보여주는 부분 소개 (~하는 모습으로 사랑받는 경향이 있습니다 체)"
    }}
  ]
}}

요구 조건:
1. activities는 3개~4개 포함해 주세요.
2. celebrities는 2명~3명 포함해 주세요.
3. 각 활동의 search_keyword는 구체적인 검색이 가능한 단어여야 합니다.
"""

    if not gemini_client:
        logger.info("Using rich mock response because GEMINI_API_KEY is not set.")
        return get_fallback_recommendations(mbti_type, ratios)

    try:
        logger.info(f"Gemini API Request for MBTI: {mbti_type}")
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.7
            )
        )
        data = json.loads(response.text)
        return data
    except Exception as e:
        logger.error(f"Gemini API generation failed: {str(e)}")
        return get_fallback_recommendations(mbti_type, ratios)


def get_fallback_recommendations(mbti_type: str, ratios: dict):
    """Fallback recommendation when API is unreachable or key not set"""
    is_e = ratios.get("E", 50) >= 50
    return {
        "summary": f"{mbti_type} 성향은 다양한 상황에서 유연하게 자신의 에너지를 발휘하는 경향이 있을 수 있습니다. 상황에 따라 새로운 아이디어를 탐색하거나 차분한 집중을 즐기실 가능성이 높습니다.",
        "activities": [
            {
                "title": "테마가 있는 원데이 클래스 참여" if is_e else "아늑하고 조용한 독립서점 탐방",
                "reason": "새로운 사람들과 자연스럽게 교류하며 활력을 얻으실 가능성이 높습니다." if is_e else "혼자만의 사색과 지적 호기심을 평온하게 채우는 경향이 있을 수 있습니다.",
                "search_keyword": "원데이 클래스 공방 추천" if is_e else "조용한 독립서점 북카페 추천"
            },
            {
                "title": "풍경이 아름다운 산책로 걷기",
                "reason": "생각을 정리하고 일상에 신선한 영감을 불어넣는 데 도움이 될 수 있습니다.",
                "search_keyword": "도심 힐링 산책로 코스"
            },
            {
                "title": "취향 중심의 소규모 팝업 전시 관람",
                "reason": "감각적이고 새로운 자극을 통해 감성을 재충전하는 시간을 가지실 가능성이 있습니다.",
                "search_keyword": "이번 주 팝업스토어 전시 일정"
            }
        ],
        "celebrities": [
            {
                "name": "대표 인물 A",
                "description": "열정적이고 진정성 있는 태도로 주위 사람들에게 긍정적인 영감을 주는 경향이 있습니다."
            },
            {
                "name": "대표 인물 B",
                "description": "자신만의 고유한 시각으로 차분하게 결과물을 완성해 나가는 매력을 보여줍니다."
            }
        ]
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        if not data:
            logger.warning("Empty request payload received.")
            return jsonify({"success": False, "message": "요청 데이터가 없습니다."}), 400

        mbti_type = data.get("mbti", "").strip().upper()
        ratios = data.get("ratios", {})

        # Validation
        valid_letters = [
            ("E", "I"),
            ("S", "N"),
            ("T", "F"),
            ("J", "P")
        ]
        if len(mbti_type) != 4:
            return jsonify({"success": False, "message": "유효하지 않은 MBTI 형식입니다 (4자리 필요)."}), 400

        for i, pair in enumerate(valid_letters):
            if mbti_type[i] not in pair:
                return jsonify({"success": False, "message": f"MBTI 지표가 잘못되었습니다: {mbti_type}"}), 400

        logger.info(f"POST /recommend received: MBTI={mbti_type}, Ratios={ratios}")

        # 1. Gemini Content Generation
        result_data = generate_gemini_recommendations(mbti_type, ratios)

        # 2. Serper Search for each activity keyword
        activities = result_data.get("activities", [])
        for act in activities:
            kw = act.get("search_keyword")
            if kw:
                act["real_time_info"] = search_serper(kw, num_results=2)
            else:
                act["real_time_info"] = []

        logger.info("Recommendation successfully generated and enriched.")
        return jsonify({
            "success": True,
            "mbti": mbti_type,
            "ratios": ratios,
            "result": result_data
        })

    except Exception as e:
        logger.error(f"Error processing /recommend: {str(e)}", exc_info=True)
        return jsonify({"success": False, "message": "추천을 생성하는 도중 서버 오류가 발생했습니다."}), 500


if __name__ == "__main__":
    logger.info("Starting MBTI Recommender Flask Server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
