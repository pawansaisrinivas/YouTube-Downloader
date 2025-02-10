function fetchFormats() {
    const videoURL = document.getElementById("videoURL").value;
    const statusElement = document.getElementById("status");
    const qualitySelect = document.getElementById("quality");

    if (!videoURL) {
        alert("Please enter a valid YouTube URL!");
        return;
    }

    statusElement.innerText = "Fetching available formats...";
    
    fetch("https://youtube-downloader-1-apnw.onrender.com/formats", {  // ✅ Updated URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: videoURL })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            statusElement.innerText = "Error: " + data.error;
            return;
        }

        // ✅ Clear previous options
        qualitySelect.innerHTML = "";

        // ✅ Populate dropdown with unique formats
        data.formats.forEach(format => {
            let option = document.createElement("option");
            option.value = format.format_id;
            option.textContent = format.resolution;
            qualitySelect.appendChild(option);
        });

        document.getElementById("qualitySelection").style.display = "block";
        statusElement.innerText = "Select a quality and click download.";
    })
    .catch(error => {
        statusElement.innerText = "Something went wrong!";
        console.error(error);
    });
}

function downloadVideo() {
    const videoURL = document.getElementById("videoURL").value;
    const formatID = document.getElementById("quality").value;
    const statusElement = document.getElementById("status");

    if (!videoURL || !formatID) {
        alert("Please select a quality before downloading!");
        return;
    }

    statusElement.innerText = "Downloading video, please wait...";

    fetch("https://youtube-downloader-1-apnw.onrender.com/download", {  // ✅ Updated URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: videoURL, format_id: formatID })
    })
    .then(response => response.json())
    .then(data => {
        if (data.download_link) {
            statusElement.innerHTML = 
                `<a href="${data.download_link}" download onclick="celebrate()">Click here to download</a>`;
        } else {
            statusElement.innerText = "Error: " + data.error;
        }
    })
    .catch(error => {
        statusElement.innerText = "Something went wrong!";
        console.error(error);
    });
}

// 🎉 Confetti Celebration Effect
function celebrate() {
    for (let i = 0; i < 50; i++) {
        createConfetti();
    }

    // 🎊 Show Congratulations Message
    document.getElementById("congratulations").style.display = "block";

    setTimeout(() => {
        location.reload();
    }, 5000); // Refresh after 5 seconds
}

// 🎊 Create Confetti Particles
function createConfetti() {
    const confetti = document.createElement("div");
    confetti.classList.add("confetti");
    confetti.style.left = `${Math.random() * 100}vw`;
    confetti.style.backgroundColor = randomColor();
    confetti.style.animationDuration = `${Math.random() * 2 + 2}s`;

    document.body.appendChild(confetti);

    setTimeout(() => {
        confetti.remove();
    }, 3000);
}

// 🌈 Random Color Generator for Confetti
function randomColor() {
    const colors = ["#ff4757", "#2ed573", "#1e90ff", "#ff6b81", "#ffa502", "#7bed9f"];
    return colors[Math.floor(Math.random() * colors.length)];
}
