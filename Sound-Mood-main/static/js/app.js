async function generateSoundscape() {
    const userInput = document.getElementById('userInput').value;
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const audioPlayer = document.getElementById('audioPlayer');

    // Clear previous results
    resultDiv.textContent = '';
    errorDiv.textContent = '';
    audioPlayer.pause();

    if (!userInput.trim()) {
        errorDiv.textContent = 'Please enter how you feel!';
        return;
    }

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text: userInput })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'API request failed');
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        resultDiv.textContent = `Recommended Soundscape: ${data.theme}`;
        audioPlayer.src = `static/sounds/${data.theme}.mp3`;
        audioPlayer.play();

    } catch (error) {
        console.error('Error:', error);
        errorDiv.textContent = `Error: ${error.message}`;
        audioPlayer.src = '';
    }
}