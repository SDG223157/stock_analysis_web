document.getElementById('analysisForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const analyzeButton = document.getElementById('analyzeButton');
    const loadingMessage = document.getElementById('loadingMessage');
    const errorMessage = document.getElementById('errorMessage');
    
    // Get form data
    const formData = {
        ticker: document.getElementById('ticker').value,
        endDate: document.getElementById('endDate').value,
        lookbackDays: document.getElementById('lookbackDays').value,
        crossoverDays: document.getElementById('crossoverDays').value
    };
    
    try {
        // Disable button and show loading message
        analyzeButton.disabled = true;
        loadingMessage.style.display = 'block';
        errorMessage.style.display = 'none';
        
        // Send request to server
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Open result in new window
            const newWindow = window.open('');
            newWindow.document.write(data.html);
            newWindow.document.close();
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.style.display = 'block';
    } finally {
        // Re-enable button and hide loading message
        analyzeButton.disabled = false;
        loadingMessage.style.display = 'none';
    }
});
