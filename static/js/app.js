// DOM Elements
const formSection = document.getElementById("form-section");
const loadingSection = document.getElementById("loading-section");
const resultSection = document.getElementById("result-section");
const restaurantForm = document.getElementById("restaurant-form");
const errorBanner = document.getElementById("error-message");
const restartBtn = document.getElementById("restart-btn");
const copyBtn = document.getElementById("copy-btn");
const toast = document.getElementById("toast");

// Form submit handler
restaurantForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const location = document.getElementById("location").value.trim();
  const operating_hours = document.getElementById("operating_hours").value.trim();
  const avg_price = document.getElementById("avg_price").value.trim();
  const best_menu = document.getElementById("best_menu").value.trim();
  const avg_waiting = document.getElementById("avg_waiting").value.trim();
  const representative_menus = document.getElementById("representative_menus").value.trim();

  // Frontend validation
  if (!location || !avg_price || !best_menu || !avg_waiting || !representative_menus) {
    showError("모든 필수 입력값(*)을 입력해 주세요.");
    return;
  }

  formSection.style.display = "none";
  loadingSection.style.display = "block";
  resultSection.style.display = "none";
  errorBanner.style.display = "none";

  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        location,
        operating_hours,
        avg_price,
        best_menu,
        avg_waiting,
        representative_menus
      })
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.message || "추천 정보를 불러오지 못했습니다.");
    }

    renderResult(data.result);
  } catch (err) {
    loadingSection.style.display = "none";
    formSection.style.display = "block";
    showError(err.message || "서버 통신 중 문제가 발생했습니다.");
  }
});

function renderResult(result) {
  loadingSection.style.display = "none";
  resultSection.style.display = "block";

  document.getElementById("result-name").textContent = result.restaurant_name || "추천 맛집";

  // 필수 출력 항목 6가지 바인딩
  document.getElementById("res-open-time").textContent = result.open_time || "가게 사정으로 인한 휴무";
  document.getElementById("res-break-time").textContent = result.break_time || "가게 사정으로 인한 휴무";
  document.getElementById("res-eating-tips").textContent = result.eating_tips || "";
  document.getElementById("res-directions").textContent = result.directions || "";
  document.getElementById("res-review").textContent = result.review || "";
  document.getElementById("res-precautions").textContent = result.precautions || "";

  // Serper Search Results
  const serperContainer = document.getElementById("serper-container");
  const serperList = document.getElementById("serper-list");
  serperList.innerHTML = "";

  if (result.real_time_info && result.real_time_info.length > 0) {
    serperContainer.style.display = "block";
    result.real_time_info.forEach((item) => {
      const div = document.createElement("div");
      div.className = "serper-item";
      div.innerHTML = `
        <a href="${item.link}" target="_blank" rel="noopener noreferrer" class="serper-link">🔗 ${escapeHtml(item.title)}</a>
        <p class="serper-snippet">${escapeHtml(item.snippet)}</p>
      `;
      serperList.appendChild(div);
    });
  } else {
    serperContainer.style.display = "none";
  }

  // Scroll to top of results
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showError(msg) {
  errorBanner.textContent = `⚠️ 오류: ${msg}`;
  errorBanner.style.display = "block";
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

restartBtn.addEventListener("click", () => {
  resultSection.style.display = "none";
  formSection.style.display = "block";
  window.scrollTo({ top: 0, behavior: "smooth" });
});

copyBtn.addEventListener("click", async () => {
  try {
    const textToCopy = `[추천 맛집: ${document.getElementById("result-name").textContent}]
- 오픈시간: ${document.getElementById("res-open-time").textContent}
- 브레이크타임: ${document.getElementById("res-break-time").textContent}
- 맛있게 먹는 방법: ${document.getElementById("res-eating-tips").textContent}
- 오는길: ${document.getElementById("res-directions").textContent}
- 리뷰: ${document.getElementById("res-review").textContent}
- 주의사항: ${document.getElementById("res-precautions").textContent}`;

    await navigator.clipboard.writeText(textToCopy);
    toast.style.display = "block";
    setTimeout(() => {
      toast.style.display = "none";
    }, 2500);
  } catch (err) {
    showError("복사에 실패했습니다.");
  }
});
