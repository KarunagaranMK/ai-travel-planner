async function planTrip() {

    const name = document.getElementById("name").value;
    const destination = document.getElementById("destination").value;
    const days = Number(document.getElementById("days").value);
    const budget = Number(document.getElementById("budget").value);

    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const errorDiv = document.getElementById("error");

    loading.classList.remove("hidden");
    result.classList.add("hidden");
    errorDiv.classList.add("hidden");

    try {

        const response = await fetch("http://127.0.0.1:8000/plan-trip", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name,
                destination,
                days,
                budget
            })
        });

        const data = await response.json();
        loading.classList.add("hidden");

        if (data.error) {
            errorDiv.textContent = data.error;
            errorDiv.classList.remove("hidden");
            return;
        }

        renderResult(data);
        result.classList.remove("hidden");

    } catch (err) {
        loading.classList.add("hidden");
        errorDiv.textContent = "Server error. Make sure backend is running.";
        errorDiv.classList.remove("hidden");
    }
}

function renderResult(data) {

    const summary = document.getElementById("summary");
    const itineraryDiv = document.getElementById("itinerary");
    const reasoningDiv = document.getElementById("reasoning");

    summary.innerHTML = `
        <p><strong>User:</strong> ${data.user}</p>
        <p><strong>Total Cost:</strong> $${data.trip_plan.total_cost}</p>
        <p><strong>Remaining Budget:</strong> $${data.trip_plan.remaining_budget}</p>
    `;

    itineraryDiv.innerHTML = "";
    data.trip_plan.itinerary.forEach(item => {
        itineraryDiv.innerHTML += `
            <div style="margin-bottom:10px;padding:10px;background:#f5f7fa;border-radius:8px;">
                <strong>${item.destination}</strong><br>
                Days: ${item.days} <br>
                Daily Cost: $${item.daily_cost} <br>
                Temperature: ${item.temperature}°C <br>
                Total: $${item.total_cost}
            </div>
        `;
    });

    reasoningDiv.innerHTML = "";
    data.reasoning.forEach(step => {
        reasoningDiv.innerHTML += `<p>• ${step}</p>`;
    });
}