// 15 Test Questions
const questions = [
  // E vs I (1~4)
  {
    category: "에너지 방향 (E / I)",
    dimension: "EI",
    text: "주말이나 휴일이 찾아왔을 때, 에너지를 얻는 나의 방식은?",
    options: [
      { label: "친구들을 만나거나 야외 활동을 하며 사람들과 소통하기", value: "E" },
      { label: "집에서 혼자 조용히 휴식을 취하며 나만의 취미 즐기기", value: "I" }
    ]
  },
  {
    category: "에너지 방향 (E / I)",
    dimension: "EI",
    text: "새로운 사람들과 함께하는 모임에 초대받았을 때 나의 감정은?",
    options: [
      { label: "새로운 인연을 만날 생각에 흥미롭고 기대되는 편이다", value: "E" },
      { label: "약간의 부담을 느끼며 편한 지인과의 자리를 더 선호한다", value: "I" }
    ]
  },
  {
    category: "에너지 방향 (E / I)",
    dimension: "EI",
    text: "어려운 문제나 스트레스가 생겼을 때 나의 대처 방식은?",
    options: [
      { label: "친구나 동료에게 이야기하며 대화를 통해 털어내는 편이다", value: "E" },
      { label: "혼자 차분히 생각을 정리한 후 해결책을 찾는 편이다", value: "I" }
    ]
  },
  {
    category: "에너지 방향 (E / I)",
    dimension: "EI",
    text: "평소 하루 일과가 끝난 후 편안함을 느끼는 시간은?",
    options: [
      { label: "지인들과 가볍게 저녁을 먹거나 통화로 일상을 나눌 때", value: "E" },
      { label: "방해받지 않고 조용히 음악을 듣거나 독서를 즐길 때", value: "I" }
    ]
  },

  // S vs N (5~8)
  {
    category: "인식 방식 (S / N)",
    dimension: "SN",
    text: "새로운 일을 시작하거나 정보를 접할 때 내가 먼저 주목하는 것은?",
    options: [
      { label: "눈앞의 구체적인 사실, 현재의 상황과 실제 경험", value: "S" },
      { label: "전체적인 맥락, 미래의 가능성과 숨겨진 아이디어", value: "N" }
    ]
  },
  {
    category: "인식 방식 (S / N)",
    dimension: "SN",
    text: "여행 계획을 세울 때 내가 더 관심 갖는 부분은?",
    options: [
      { label: "방문할 식당의 메뉴, 교통편, 숙소의 구체적 위치와 시설", value: "S" },
      { label: "여행지에서 느낄 분위기, 색다른 테마와 영감을 주는 경험", value: "N" }
    ]
  },
  {
    category: "인식 방식 (S / N)",
    dimension: "SN",
    text: "영화나 책을 감상할 때 내가 더 매력을 느끼는 요소는?",
    options: [
      { label: "현실감 넘치는 묘사와 개연성 있는 탄탄한 스토리", value: "S" },
      { label: "독창적인 세계관과 상상력을 자극하는 은유 및 복선", value: "N" }
    ]
  },
  {
    category: "인식 방식 (S / N)",
    dimension: "SN",
    text: "대화를 나눌 때 주로 편하게 느껴지는 주제는?",
    options: [
      { label: "실제로 겪은 일상 이야기나 최근 일어난 현실적인 이슈", value: "S" },
      { label: "'만약에 이렇다면?' 같은 상상이나 철학적/미래적 담론", value: "N" }
    ]
  },

  // T vs F (9~11)
  {
    category: "판단 기준 (T / F)",
    dimension: "TF",
    text: "친구가 힘든 고민을 털어놓을 때 나의 첫 반응에 가까운 것은?",
    options: [
      { label: "상황을 분석하고 현실적인 해결 방법이나 대안을 찾아본다", value: "T" },
      { label: "친구의 감정에 먼저 공감하고 마음을 위로해준다", value: "F" }
    ]
  },
  {
    category: "판단 기준 (T / F)",
    dimension: "TF",
    text: "중요한 결정을 내릴 때 내가 더 중요하게 생각하는 기준은?",
    options: [
      { label: "논리적 인과관계, 객관적 사실과 효율성", value: "T" },
      { label: "관련된 사람들의 마음, 조화로운 관계와 가치관", value: "F" }
    ]
  },
  {
    category: "판단 기준 (T / F)",
    dimension: "TF",
    text: "누군가에게 피드백을 전달해야 할 때 나의 스타일은?",
    options: [
      { label: "명확하고 솔직하게 개선점을 직관적으로 알려준다", value: "T" },
      { label: "상대방의 기분이 상하지 않도록 부드럽고 배려 있게 전한다", value: "F" }
    ]
  },

  // J vs P (12~15)
  {
    category: "생활 양식 (J / P)",
    dimension: "JP",
    text: "주말이나 휴가를 보낼 때 나의 스타일은?",
    options: [
      { label: "시간대별 일정이나 동선을 미리 계획해두는 편이다", value: "J" },
      { label: "그날의 기분과 날씨에 맞춰 유연하게 즉흥적으로 움직인다", value: "P" }
    ]
  },
  {
    category: "생활 양식 (J / P)",
    dimension: "JP",
    text: "과제나 업무 마감 기한이 주어졌을 때 나의 일 처리 방식은?",
    options: [
      { label: "미리 마감일 전까지 분량을 나누어 계획적으로 완료한다", value: "J" },
      { label: "마감이 임박했을 때 집중력이 극대화되어 빠르게 처리한다", value: "P" }
    ]
  },
  {
    category: "생활 양식 (J / P)",
    dimension: "JP",
    text: "나의 작업 공간이나 방 정리 상태는 보통 어떤 편인가요?",
    options: [
      { label: "물건들이 제자리에 정돈되어 있어야 마음이 편안하다", value: "J" },
      { label: "약간 어질러져 있어도 내가 찾는 위치만 알면 편안하다", value: "P" }
    ]
  },
  {
    category: "생활 양식 (J / P)",
    dimension: "JP",
    text: "예상치 못한 갑작스러운 일정 변경이 생겼을 때 나의 반응은?",
    options: [
      { label: "계획이 틀어져 다소 혼란스럽고 당황스럽다", value: "J" },
      { label: "'그럴 수도 있지' 하며 상황에 맞게 쉽게 적응한다", value: "P" }
    ]
  }
];

let currentQuestionIndex = 0;
const answers = [];

// DOM Elements
const quizSection = document.getElementById("quiz-section");
const loadingSection = document.getElementById("loading-section");
const resultSection = document.getElementById("result-section");
const questionIndicator = document.getElementById("question-indicator");
const progressPercent = document.getElementById("progress-percent");
const progressBarFill = document.getElementById("progress-bar-fill");
const questionCategory = document.getElementById("question-category");
const questionText = document.getElementById("question-text");
const optionsContainer = document.getElementById("options-container");
const prevBtn = document.getElementById("prev-btn");
const errorBanner = document.getElementById("error-message");
const restartBtn = document.getElementById("restart-btn");
const copyBtn = document.getElementById("copy-btn");
const toast = document.getElementById("toast");

function initQuiz() {
  currentQuestionIndex = 0;
  answers.length = 0;
  quizSection.style.display = "block";
  loadingSection.style.display = "none";
  resultSection.style.display = "none";
  errorBanner.style.display = "none";
  renderQuestion();
}

function renderQuestion() {
  const q = questions[currentQuestionIndex];
  const total = questions.length;
  const currentNum = currentQuestionIndex + 1;
  const percent = Math.round((currentNum / total) * 100);

  questionIndicator.textContent = `질문 ${currentNum} / ${total}`;
  progressPercent.textContent = `${percent}%`;
  progressBarFill.style.width = `${percent}%`;

  questionCategory.textContent = q.category;
  questionText.textContent = q.text;

  prevBtn.style.visibility = currentQuestionIndex > 0 ? "visible" : "hidden";

  optionsContainer.innerHTML = "";
  q.options.forEach((opt) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    btn.textContent = opt.label;
    btn.addEventListener("click", () => handleSelectOption(opt.value));
    optionsContainer.appendChild(btn);
  });
}

function handleSelectOption(val) {
  answers[currentQuestionIndex] = val;
  if (currentQuestionIndex < questions.length - 1) {
    currentQuestionIndex++;
    renderQuestion();
  } else {
    finishQuiz();
  }
}

prevBtn.addEventListener("click", () => {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    renderQuestion();
  }
});

function calculateMBTI() {
  const counts = { E: 0, I: 0, S: 0, N: 0, T: 0, F: 0, J: 0, P: 0 };
  answers.forEach((ans) => {
    if (counts[ans] !== undefined) {
      counts[ans]++;
    }
  });

  const totalEI = counts.E + counts.I || 1;
  const totalSN = counts.S + counts.N || 1;
  const totalTF = counts.T + counts.F || 1;
  const totalJP = counts.J + counts.P || 1;

  const ratios = {
    E: Math.round((counts.E / totalEI) * 100),
    I: Math.round((counts.I / totalEI) * 100),
    S: Math.round((counts.S / totalSN) * 100),
    N: Math.round((counts.N / totalSN) * 100),
    T: Math.round((counts.T / totalTF) * 100),
    F: Math.round((counts.F / totalTF) * 100),
    J: Math.round((counts.J / totalJP) * 100),
    P: Math.round((counts.P / totalJP) * 100)
  };

  const mbti = [
    ratios.E >= ratios.I ? "E" : "I",
    ratios.S >= ratios.N ? "S" : "N",
    ratios.T >= ratios.F ? "T" : "F",
    ratios.J >= ratios.P ? "J" : "P"
  ].join("");

  return { mbti, ratios };
}

async function finishQuiz() {
  quizSection.style.display = "none";
  loadingSection.style.display = "block";
  errorBanner.style.display = "none";

  const { mbti, ratios } = calculateMBTI();

  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mbti, ratios })
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.message || "추천 정보를 가져오지 못했습니다.");
    }

    renderResult(data);
  } catch (err) {
    loadingSection.style.display = "none";
    quizSection.style.display = "block";
    showError(err.message || "서버 통신 중 문제가 발생했습니다.");
  }
}

function renderResult(data) {
  loadingSection.style.display = "none";
  resultSection.style.display = "block";

  const { mbti, ratios, result } = data;

  // Header & Summary
  document.getElementById("result-mbti").textContent = mbti;
  document.getElementById("result-summary").textContent = result.summary || "";

  // Ratios visualizer
  const dims = [
    ["E", "I"],
    ["S", "N"],
    ["T", "F"],
    ["J", "P"]
  ];
  dims.forEach(([k1, k2]) => {
    document.getElementById(`ratio-${k1}`).textContent = `${ratios[k1]}%`;
    document.getElementById(`ratio-${k2}`).textContent = `${ratios[k2]}%`;
    document.getElementById(`bar-${k1}`).style.width = `${ratios[k1]}%`;
    document.getElementById(`bar-${k2}`).style.width = `${ratios[k2]}%`;
  });

  // Activities
  const actContainer = document.getElementById("activities-container");
  actContainer.innerHTML = "";
  (result.activities || []).forEach((act) => {
    const card = document.createElement("div");
    card.className = "activity-card";

    let realTimeHtml = "";
    if (act.real_time_info && act.real_time_info.length > 0) {
      const items = act.real_time_info
        .map(
          (item) => `
        <div class="serper-item">
          <a href="${item.link}" target="_blank" rel="noopener noreferrer" class="serper-link">🔗 ${escapeHtml(item.title)}</a>
          <p class="serper-snippet">${escapeHtml(item.snippet)}</p>
        </div>
      `
        )
        .join("");

      realTimeHtml = `
        <div class="serper-info-box">
          <span class="serper-badge">실시간 검색 추천 정보</span>
          ${items}
        </div>
      `;
    }

    card.innerHTML = `
      <h4 class="activity-title">${escapeHtml(act.title)}</h4>
      <p class="activity-reason">${escapeHtml(act.reason)}</p>
      ${realTimeHtml}
    `;
    actContainer.appendChild(card);
  });

  // Celebrities
  const celebContainer = document.getElementById("celebrities-container");
  celebContainer.innerHTML = "";
  (result.celebrities || []).forEach((c) => {
    const card = document.createElement("div");
    card.className = "celebrity-card";
    card.innerHTML = `
      <h4 class="celebrity-name">${escapeHtml(c.name)}</h4>
      <p class="celebrity-desc">${escapeHtml(c.description)}</p>
    `;
    celebContainer.appendChild(card);
  });
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
  initQuiz();
});

copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(window.location.href);
    toast.style.display = "block";
    setTimeout(() => {
      toast.style.display = "none";
    }, 2500);
  } catch (err) {
    showError("링크 복사에 실패했습니다.");
  }
});

// Start on page load
initQuiz();
