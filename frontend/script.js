
const form = document.getElementById("profileForm");
const message = document.getElementById("message");
const result = document.getElementById("result");
const analyzeButton = document.getElementById("analyzeButton");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    message.textContent = "";
    result.hidden = true;
    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";

    const profile = {
        username: document.getElementById("username").value.trim(),
        bio: document.getElementById("bio").value.trim(),
        followers: Number(document.getElementById("followers").value),
        following: Number(document.getElementById("following").value),
        posts: Number(document.getElementById("posts").value),
        account_age_days: Number(document.getElementById("age").value)
    };

    if (!profile.bio) {
        message.textContent = "Please enter the profile bio.";
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze Profile";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(profile)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Prediction failed.");
        }

        const predictionElement = document.getElementById("prediction");
        const confidenceElement = document.getElementById("confidence");
        const noticeElement = document.getElementById("notice");

        predictionElement.textContent =
            data.prediction === "fake"
                ? "Likely Fake Profile"
                : "Likely Genuine Profile";

        confidenceElement.textContent =
            data.confidence === null
                ? "Unavailable"
                : `${data.confidence}%`;

        noticeElement.textContent = data.notice;

        result.hidden = false;

    } catch (error) {
        message.textContent =
            "Could not connect to the prediction server. Make sure Flask is running. " +
            error.message;
    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze Profile";
    }
});