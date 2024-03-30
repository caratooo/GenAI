// Event listener for html page load (this function is called when the html page is loaded)
document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById("audioFile");
    if (fileInput) {
        // Event listener for file input change
        // (whenever a change is made to "audioFile" from the html, the function "handleFileSelect" is called)
        fileInput.addEventListener("change", handleFileSelect);
    } else {
        console.error("Element with ID 'audioFile' not found.");
    }
});


// handle file selection
function handleFileSelect(event) {
    const fileInput = document.getElementById("audioFile");
    if (!fileInput) {
        console.error("Element with ID 'audioFile' not found.");
        return;
    }
    const file = event.target.files[0]; // Get the selected file

    //print the file name to the console for now
    console.log("Selected audio file:", file);

    
    
    
}
