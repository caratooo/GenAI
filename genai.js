// Event listener for file input change
// (whenever a change is made to "audioFile" from the html, the function "handleFileSelect" is called)
document.getElementById("audioFile").addEventListener("change", handleFileSelect);


// handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0]; // Get the selected file
    
    //print the file name to the console for now
    console.log("Selected audio file:", file);
    
    
}
