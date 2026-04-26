document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("fortune-form");
    const submitBtn = document.getElementById("submit-btn");
    const btnText = submitBtn.querySelector(".btn-text");
    const btnSpinner = document.getElementById("btn-spinner");
    const loading = document.getElementById("loading");
    const resultCards = document.getElementById("result-cards");
    const errorCard = document.getElementById("error-card");
    const errorText = document.getElementById("error-text");
    const emptyState = document.getElementById("empty-state");
    const questionEl = document.getElementById("question");
    const charNum = document.getElementById("char-num");

    // Character counter
    questionEl.addEventListener("input", () => {
        charNum.textContent = questionEl.value.length;
    });

    // Form submit
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Clear previous errors
        clearErrors();

        // Validate
        const name = document.getElementById("name").value.trim();
        const birthDate = document.getElementById("birth_date").value;
        const gender = form.querySelector("input[name='gender']:checked")?.value;
        const question = document.getElementById("question").value.trim() || null;
        const model = document.getElementById("model").value;

        let hasError = false;

        if (!name) {
            showError("name-error", "请输入姓名");
            document.getElementById("name").classList.add("error");
            hasError = true;
        }
        if (!birthDate) {
            showError("date-error", "请选择出生日期");
            document.getElementById("birth_date").classList.add("error");
            hasError = true;
        }

        if (hasError) return;

        // Show loading
        setLoading(true);

        try {
            const response = await fetch("/api/fortune", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, birth_date: birthDate, gender, question, model }),
            });

            if (!response.ok) {
                const errData = await response.json();
                const detail = errData.detail;
                if (Array.isArray(detail)) {
                    detail.forEach((d) => {
                        if (d.loc.includes("name")) showError("name-error", d.msg);
                        if (d.loc.includes("birth_date")) showError("date-error", d.msg);
                    });
                } else if (typeof detail === "string") {
                    throw new Error(detail);
                } else {
                    throw new Error("请求失败，请检查输入信息");
                }
                setLoading(false);
                return;
            }

            const data = await response.json();
            renderResult(data);
        } catch (err) {
            setLoading(false);
            showErrorCard(err.message || "网络连接失败，请稍后重试");
        }
    });

    // Retry button
    document.getElementById("btn-retry").addEventListener("click", () => {
        errorCard.classList.add("hidden");
        emptyState.classList.remove("hidden");
    });

    function setLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            btnText.classList.add("hidden");
            btnSpinner.classList.remove("hidden");
            resultCards.classList.add("hidden");
            errorCard.classList.add("hidden");
            emptyState.classList.add("hidden");
            loading.classList.remove("hidden");
        } else {
            submitBtn.disabled = false;
            btnText.classList.remove("hidden");
            btnSpinner.classList.add("hidden");
            loading.classList.add("hidden");
        }
    }

    function renderResult(data) {
        setLoading(false);

        // Badges
        document.getElementById("badge-zodiac").textContent = `生肖：${data.zodiac}`;
        document.getElementById("badge-element").textContent = `五行：${data.element}`;

        const categoryBadge = document.getElementById("badge-category");
        categoryBadge.textContent = data.fortune_category;
        categoryBadge.className = "badge badge-category";
        if (data.fortune_category.includes("大吉") || data.fortune_category.includes("吉") && !data.fortune_category.includes("凶")) {
            categoryBadge.classList.add("great");
        } else if (data.fortune_category.includes("吉")) {
            categoryBadge.classList.add("good");
        } else if (data.fortune_category.includes("平")) {
            categoryBadge.classList.add("ok");
        } else {
            categoryBadge.classList.add("bad");
        }

        // Score bar (animate)
        const scoreBar = document.getElementById("score-bar");
        document.getElementById("score-value").textContent = data.fortune_score;
        setTimeout(() => {
            scoreBar.style.width = `${data.fortune_score}%`;
        }, 100);

        // Reading
        document.getElementById("reading-text").textContent = data.reading;

        // Model info
        const modelLabel = data.model_used === "rule_based" ? "离线模式（规则引擎）" : `AI 模型：${data.model_used}`;
        document.getElementById("model-info").textContent = `生成时间：${data.generated_at} · ${modelLabel}`;

        resultCards.classList.remove("hidden");
    }

    function showErrorCard(msg) {
        errorText.textContent = msg;
        errorCard.classList.remove("hidden");
        emptyState.classList.add("hidden");
    }

    function showError(id, msg) {
        document.getElementById(id).textContent = msg;
    }

    function clearErrors() {
        document.querySelectorAll(".error-msg").forEach((el) => (el.textContent = ""));
        document.querySelectorAll(".form-group input.error, .form-group textarea.error").forEach((el) => {
            el.classList.remove("error");
        });
    }
});
