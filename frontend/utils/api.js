// API Functions

const analyzeSentiment = async (text) => {
    if (!text.trim()) {
        throw new Error('Please enter some text to analyze');
    }

    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text.trim() }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;

    } catch (err) {
        if (err.name === 'TypeError' && err.message.includes('Failed to fetch')) {
            throw new Error('Cannot connect to the FastAPI server. Make sure it\'s running on http://localhost:8000 and CORS is enabled.');
        }
        throw err;
    }
};