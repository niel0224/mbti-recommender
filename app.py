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
logger = logging.getLogger("restaurant_recommender")

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
    Search real-world restaurant information using Serper.dev API
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


def search_serper_images(query: str, num_results: int = 4):
    """
    Search actual real-world photos of the specified dish.
    Uses Serper Images API if configured, otherwise performs a live web image search
    to fetch authentic photos of the exact searched food.
    """
    # 1. Try Serper.dev API if key is valid
    if SERPER_API_KEY and SERPER_API_KEY != "your_serper_api_key_here":
        url = "https://google.serper.dev/images"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "q": f"{query} 음식",
            "gl": "kr",
            "hl": "ko",
            "num": num_results
        }
        try:
            logger.info(f"Serper Images Request: Query='{query}'")
            resp = requests.post(url, headers=headers, json=payload, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                images = data.get("images", [])
                image_list = []
                for img in images[:num_results]:
                    img_url = img.get("imageUrl")
                    if img_url and img_url.startswith("http"):
                        image_list.append({
                            "title": img.get("title", query),
                            "imageUrl": img_url,
                            "source": img.get("source", "웹 검색")
                        })
                if len(image_list) >= 2:
                    return image_list
        except Exception as e:
            logger.error(f"Serper image search failed: {str(e)}")

    # 2. Live Web Food Image Search (Scrapes actual live food photos for the exact query)
    try:
        import urllib.parse
        import re
        encoded = urllib.parse.quote(f"{query} 맛집")
        scrape_url = f"https://search.daum.net/search?w=img&q={encoded}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        logger.info(f"Live Web Food Image Search for '{query}'")
        resp = requests.get(scrape_url, headers=headers, timeout=5)
        if resp.status_code == 200:
            pattern = r'https://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)'
            matches = re.findall(pattern, resp.text)
            excluded = ["daum_og", "favicon", "static", "icon", "logo", "profile", "thumb/200x"]
            real_images = []
            for m in matches:
                clean_url = m.replace("&amp;", "&")
                if any(x in clean_url for x in excluded):
                    continue
                if clean_url not in [img["imageUrl"] for img in real_images]:
                    real_images.append({
                        "title": f"실제 검색된 '{query}' 사진",
                        "imageUrl": clean_url,
                        "source": "실시간 웹 이미지 검색"
                    })
                if len(real_images) >= num_results:
                    break
            if real_images:
                return real_images
    except Exception as e:
        logger.error(f"Live web food image search failed: {str(e)}")

    # 3. Fallback only if no network results found
    return [
        {"title": f"'{query}' 사진", "imageUrl": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=80", "source": "웹 검색"},
        {"title": f"'{query}' 사진", "imageUrl": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&auto=format&fit=crop&q=80", "source": "웹 검색"}
    ][:num_results]


def generate_restaurant_recommendation(location, operating_hours, avg_price, best_menu, avg_waiting, representative_menus):
    """
    Generate restaurant details using Gemini API with realistic open/break times based on inputs.
    """
    system_instruction = (
        "당신은 신뢰할 수 있고 친절한 전문 맛집 큐레이터 AI입니다.\n"
        "사용자가 입력한 정보와 해당 지역/메뉴의 특성을 고려하여 사실적이고 유용한 맛집 추천 정보를 제공합니다.\n"
        "응답은 반드시 유효한 JSON 형식이어야 하며 마크다운 코드블록 없이 순수 JSON 문자열만 반환하세요."
    )

    prompt = f"""
다음은 사용자가 입력한 맛집 추천 기준 및 정보입니다:
- 맛집 위치: {location}
- 가게의 운영시간(사용자 입력): {operating_hours}
- 메뉴들의 평균가격: {avg_price}
- 제일 평이 좋은 메뉴: {best_menu}
- 평균 웨이팅 시간: {avg_waiting}
- 맛집들의 대표 메뉴: {representative_menus}

위 정보를 바탕으로 아래 구조의 JSON 데이터를 생성해 주세요:
{{
  "restaurant_name": "추천 맛집 상호명 또는 테마명 (예: {location} 인기 맛집)",
  "open_time": "사용자가 입력한 운영시간 또는 이 업종에 걸맞은 구체적 오픈시간 (예: 11:30 또는 11:00 오픈)",
  "break_time": "해당 맛집의 전형적인 브레이크타임 (예: 15:00 ~ 17:00, 브레이크타임 없음 등)",
  "eating_tips": "이곳의 대표 메뉴와 베스트 메뉴를 가장 맛있게 먹는 구체적인 방법 및 꿀조합 팁 (2~3문장)",
  "directions": "{location} 기준 대중교통 및 도보로 찾아오는 길 안내 (상세하고 친절하게)",
  "review": "방문객들의 실제 만족 포인트와 솔직한 분위기 총평 리뷰 (3문장 내외)",
  "precautions": "웨이팅({avg_waiting}), 재료 소진, 주차, 예약 등 방문 시 주의해야 할 핵심 주의사항 (2~3가지)",
  "search_keyword": "{location} {best_menu} 맛집"
}}
"""

    if not gemini_client:
        logger.info("Using rich mock response because GEMINI_API_KEY is not set.")
        return get_fallback_restaurant(location, operating_hours, avg_price, best_menu, avg_waiting, representative_menus)

    try:
        logger.info(f"Gemini API Request for Restaurant at {location}")
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
        return get_fallback_restaurant(location, operating_hours, avg_price, best_menu, avg_waiting, representative_menus)


def get_fallback_restaurant(location, operating_hours, avg_price, best_menu, avg_waiting, representative_menus):
    """Fallback restaurant recommendation with realistic open/break time"""
    open_time_val = operating_hours if operating_hours and operating_hours != "별도 문의 필요" else "11:30 (매일 11:30 ~ 21:30)"
    return {
        "restaurant_name": f"{location} 추천 명품 맛집",
        "open_time": open_time_val,
        "break_time": "15:00 ~ 17:00 (주말 브레이크타임 없음)",
        "eating_tips": f"가장 평이 좋은 '{best_menu}'는 특제 소스를 곁들여 첫 입을 드셔보신 후, 함께 나오는 반찬과 조합해 드시면 감칠맛이 극대화됩니다. 대표 메뉴인 {representative_menus}와 번갈아 맛보시면 물리지 않고 풍성한 식사를 즐기실 수 있습니다.",
        "directions": f"{location} 인근 지하철역 또는 버스 정류장에서 도보 5~7분 거리에 위치해 있습니다. 메인 먹자골목 중심 교차로에서 우측 골목으로 진입하시면 쉽게 찾으실 수 있습니다.",
        "review": f"평균 가격대({avg_price}) 대비 음식의 정갈함과 신선도가 탁월하여 현지인과 방문객 모두에게 찬사를 받는 곳입니다. 정갈한 인테리어와 친절한 응대로 기분 좋은 식사 경험을 선사합니다.",
        "precautions": f"평균 웨이팅 시간이 약 {avg_waiting} 내외로 소요될 수 있으므로 피크 시간대에는 여유를 갖고 방문하세요. 또한 주차 공간이 협소할 수 있어 대중교통 이용을 권장하며, 재료 조기 소진 시 조기 마감될 수 있습니다.",
        "search_keyword": f"{location} {best_menu} 맛집"
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

        # Input extraction
        location = data.get("location", "").strip()
        operating_hours = data.get("operating_hours", "").strip() or "별도 문의 필요"
        avg_price = data.get("avg_price", "").strip()
        best_menu = data.get("best_menu", "").strip()
        avg_waiting = data.get("avg_waiting", "").strip()
        representative_menus = data.get("representative_menus", "").strip()

        # Input validation
        if not location:
            return jsonify({"success": False, "message": "맛집 위치를 입력해 주세요."}), 400
        if not avg_price:
            return jsonify({"success": False, "message": "메뉴들의 평균가격을 입력해 주세요."}), 400
        if not best_menu:
            return jsonify({"success": False, "message": "제일 평이 좋은 메뉴를 입력해 주세요."}), 400
        if not avg_waiting:
            return jsonify({"success": False, "message": "평균 웨이팅 시간을 입력해 주세요."}), 400
        if not representative_menus:
            return jsonify({"success": False, "message": "맛집들의 대표 메뉴를 입력해 주세요."}), 400

        logger.info(f"POST /recommend received: Location='{location}', Best='{best_menu}', Price='{avg_price}'")

        # 1. Gemini Content Generation
        result_data = generate_restaurant_recommendation(
            location, operating_hours, avg_price, best_menu, avg_waiting, representative_menus
        )

        # 2. Serper Search for live info
        search_kw = result_data.get("search_keyword") or f"{location} {best_menu} 맛집"
        real_time_info = search_serper(search_kw, num_results=3)
        result_data["real_time_info"] = real_time_info

        # 3. Image Search for best_menu
        best_menu_images = search_serper_images(f"{location} {best_menu}", num_results=4)
        result_data["best_menu"] = best_menu
        result_data["best_menu_images"] = best_menu_images

        logger.info("Restaurant recommendation successfully created.")
        return jsonify({
            "success": True,
            "result": result_data
        })

    except Exception as e:
        logger.error(f"Error processing /recommend: {str(e)}", exc_info=True)
        return jsonify({"success": False, "message": "맛집 추천을 생성하는 도중 오류가 발생했습니다."}), 500


if __name__ == "__main__":
    logger.info("Starting Restaurant Recommender Flask Server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
