document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("upload-form").addEventListener("submit", function(event) {
        event.preventDefault();
        var formData = new FormData(this);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Display transcribed text
            document.getElementById("result-container").innerHTML = `
                <h2>Transcribed Text:</h2>
                <p>${data.transcribed_text}</p>
                <h2>Paraphrased Text:</h2>
                <p>${data.paraphrased_result}</p>
                <h2>Summarized Text:</h2>
                <p>${data.summarized_result}</p>
            `;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});

