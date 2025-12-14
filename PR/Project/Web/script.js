document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("uploadForm");
    const dataFileInput = document.getElementById("dataFile");
    const periodSelect = document.getElementById("period");
    const uploadStatus = document.getElementById("uploadStatus");

    const runPredictionBtn = document.getElementById("runPredictionBtn");
    const predictionStatus = document.getElementById("predictionStatus");

    const summaryBlock = document.getElementById("summary");
    const predictionTableBody = document.querySelector("#predictionTable tbody");
    const chartArea = document.getElementById("chartArea");
    const distributionChart = document.getElementById("distributionChart");

    const tableSortProbDescBtn = document.getElementById("tableSortProbDesc");
    const tableSortProbAscBtn = document.getElementById("tableSortProbAsc");
    const chartSortProbDescBtn = document.getElementById("chartSortProbDesc");
    const chartSortProbAscBtn = document.getElementById("chartSortProbAsc");

    let predictionData = [];
    let tableSort = "prob-desc";  
    let chartSort = "prob-desc";   

    uploadForm.addEventListener("submit", (e) => {
        e.preventDefault();

        const file = dataFileInput.files[0];
        if (!file) {
            uploadStatus.textContent = "Будь ласка, оберіть файл з даними.";
            uploadStatus.className = "status error";
            return;
        }

        const formData = new FormData(uploadForm);

        uploadStatus.textContent = "Завантаження файлу...";
        uploadStatus.className = "status";

        fetch("upload.php", {
            method: "POST",
            body: formData
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    uploadStatus.textContent = data.message;
                    uploadStatus.className = "status ok";
                    runPredictionBtn.disabled = false;
                } else {
                    uploadStatus.textContent = data.message || "Сталася помилка під час завантаження.";
                    uploadStatus.className = "status error";
                }
            })
            .catch(err => {
                console.error(err);
                uploadStatus.textContent = "Помилка з’єднання з сервером.";
                uploadStatus.className = "status error";
            });
    });

    runPredictionBtn.addEventListener("click", () => {
        const period = periodSelect.value || "all";

        predictionStatus.textContent = "Виконується прогноз...";
        predictionStatus.className = "status";

        fetch("predict.php?period=" + encodeURIComponent(period))
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    predictionStatus.textContent = data.message || "Не вдалося отримати прогноз.";
                    predictionStatus.className = "status error";
                    return;
                }

                predictionStatus.textContent = data.message;
                predictionStatus.className = "status ok";

                predictionData = Array.isArray(data.data) ? data.data : [];

                renderSummary(data.summary);
                renderTable(predictionData);
                renderChart(predictionData);
                renderDistribution(predictionData);
            })
            .catch(err => {
                console.error(err);
                predictionStatus.textContent = "Помилка з’єднання з сервером.";
                predictionStatus.className = "status error";
            });
    });

    if (tableSortProbDescBtn) {
        tableSortProbDescBtn.addEventListener("click", () => {
            tableSort = "prob-desc";
            if (predictionData.length) renderTable(predictionData);
        });
    }

    if (tableSortProbAscBtn) {
        tableSortProbAscBtn.addEventListener("click", () => {
            tableSort = "prob-asc";
            if (predictionData.length) renderTable(predictionData);
        });
    }

    if (chartSortProbDescBtn) {
        chartSortProbDescBtn.addEventListener("click", () => {
            chartSort = "prob-desc";
            if (predictionData.length) renderChart(predictionData);
        });
    }

    if (chartSortProbAscBtn) {
        chartSortProbAscBtn.addEventListener("click", () => {
            chartSort = "prob-asc";
            if (predictionData.length) renderChart(predictionData);
        });
    }

    function renderSummary(summary) {
        summaryBlock.innerHTML = "";

        if (!summary) return;

        const items = [
            `Кількість клієнтів у вибірці: <b>${summary.totalClients}</b>`,
            `Клієнтів з високою ймовірністю повернення (≥ 0.7): <b>${summary.highProbabilityClients}</b>`,
            `Середня ймовірність повернення: <b>${summary.averageProbability}</b>`
        ];

        items.forEach(text => {
            const el = document.createElement("div");
            el.className = "summary-item";
            el.innerHTML = text;
            summaryBlock.appendChild(el);
        });
    }

    function renderTable(data) {
        predictionTableBody.innerHTML = "";
        if (!Array.isArray(data) || !data.length) return;

        const sorted = [...data].sort((a, b) => {
            if (tableSort === "prob-asc") {
                return a.probability - b.probability;
            }
            return b.probability - a.probability;
        });

        sorted.forEach(client => {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${client.id}</td>
                <td>${client.name}</td>
                <td>${(client.probability * 100).toFixed(1)}%</td>
                <td>${client.recommended}</td>
                <td>${client.comment}</td>
            `;

            predictionTableBody.appendChild(tr);
        });
    }

    function renderChart(data) {
        chartArea.innerHTML = "";
        if (!Array.isArray(data) || !data.length) return;

        const sorted = [...data].sort((a, b) => {
            if (chartSort === "prob-asc") {
                return a.probability - b.probability;
            }
            return b.probability - a.probability;
        });

        const limited = sorted.slice(0, 20);

        limited.forEach(client => {
            const row = document.createElement("div");
            row.className = "chart-row";

            const label = document.createElement("div");
            label.className = "chart-label";
            label.textContent = client.name;

            const bar = document.createElement("div");
            bar.className = "chart-bar";

            const fill = document.createElement("div");
            fill.className = "chart-bar-fill";
            fill.style.width = (client.probability * 100).toFixed(0) + "%";

            bar.appendChild(fill);
            row.appendChild(label);
            row.appendChild(bar);
            chartArea.appendChild(row);
        });
    }

    function renderDistribution(data) {
        distributionChart.innerHTML = "";
        if (!Array.isArray(data) || !data.length) return;

        let low = 0;   // < 0.5
        let mid = 0;   // 0.5–0.8
        let high = 0;  // >= 0.8

        data.forEach(c => {
            const p = c.probability;
            if (p < 0.5) low++;
            else if (p < 0.8) mid++;
            else high++;
        });

        const total = data.length || 1;

        const groups = [
            { label: "Низька (p < 0.5)", count: low },
            { label: "Середня (0.5 ≤ p < 0.8)", count: mid },
            { label: "Висока (p ≥ 0.8)", count: high }
        ];

        groups.forEach(g => {
            const percent = (g.count / total) * 100;

            const row = document.createElement("div");
            row.className = "dist-row";

            const header = document.createElement("div");
            header.className = "dist-header";

            const lbl = document.createElement("div");
            lbl.className = "dist-label";
            lbl.textContent = g.label;

            const val = document.createElement("div");
            val.className = "dist-value";
            val.textContent = `${g.count} клієнтів (${percent.toFixed(1)}%)`;

            header.appendChild(lbl);
            header.appendChild(val);

            const bar = document.createElement("div");
            bar.className = "dist-bar";

            const fill = document.createElement("div");
            fill.className = "dist-bar-fill";
            fill.style.width = `${percent.toFixed(1)}%`;

            bar.appendChild(fill);

            row.appendChild(header);
            row.appendChild(bar);

            distributionChart.appendChild(row);
        });
    }
});
