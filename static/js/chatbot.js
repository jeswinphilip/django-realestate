async function sendMessage() {
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;

    displayMessage(userMessage, 'user');

    try {
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage })
        });

        // Important: Parse the response
        const data = await response.json();

        // Check for errors in the response
        if (data.error) {
            displayMessage(data.error, 'error');
            console.error('Chatbot error:', data.error);
        } else {
            displayMessage(data.message, 'bot');
        }
    } catch (error) {
        console.error('Network or parsing error:', error);
        displayMessage('Network error. Please check your connection.', 'error');
    }

    chatInput.value = '';
}