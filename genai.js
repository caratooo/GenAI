document.getElementById('capture').onclick = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (enhancer) {
            let frame = enhancer.getFrameFromVideo(stream);

            let width = screen.availWidth;
            let height = screen.availHeight;
            let popW = 640, popH = 480; // Adjust dimensions as needed
            let left = (width - popW) / 2;
            let top = (height - popH) / 2;

            popWindow = window.open('', 'popup', 'width=' + popW + ',height=' + popH +
                ',top=' + top + ',left=' + left + ', scrollbars=yes');

            popWindow.document.body.appendChild(frame.canvas);
        }
    } catch (error) {
        console.error('Error accessing camera:', error);
        // Handle error (e.g., display a message to the user)
    }
};
