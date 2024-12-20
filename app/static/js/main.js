// app/static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    const analysisForm = document.getElementById('analysisForm');
    const analyzeButton = document.getElementById('analyzeButton');
    const loadingMessage = document.getElementById('loadingMessage');
    const errorMessage = document.getElementById('errorMessage');

    if (analysisForm) {
        analysisForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Form submitted once'); // Add this log
            
            try {
                // Disable button and show loading message
                analyzeButton.disabled = true;
                loadingMessage.style.display = 'block';
                errorMessage.style.display = 'none';
                
                // Get form data
                const endDate = document.getElementById('endDate').value;
                const formData = {
                    ticker: document.getElementById('ticker').value,
                    endDate: endDate || null,  // Send null if date is empty
                    lookbackDays: document.getElementById('lookbackDays').value,
                    crossoverDays: document.getElementById('crossoverDays').value
                };
                
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
                    if (newWindow) {
                        newWindow.document.write(data.html);
                        newWindow.document.close();
                    } else {
                        throw new Error('Please allow pop-ups for this site to view the analysis');
                    }
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
    }

    // Initialize date input with today's date
    const endDateInput = document.getElementById('endDate');
    if (endDateInput) {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        endDateInput.value = `${yyyy}-${mm}-${dd}`;
    }

    // Add input validation
    const tickerInput = document.getElementById('ticker');
    if (tickerInput) {
        tickerInput.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    }

    const numericalInputs = ['lookbackDays', 'crossoverDays'];
    numericalInputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) {
            input.addEventListener('input', function() {
                const value = parseInt(this.value);
                if (value < 1) {
                    this.value = 1;
                }
            });
        }
    });
});