document.addEventListener("DOMContentLoaded", function () {
    const inputText = document.getElementById("inputText");
    const submitButton = document.getElementById("submitButton");
    const responseContainer = document.getElementById("responseContainer");
    // Get references to the HTML elements
    const resultTextBox = document.getElementById('resultTextBox');
    const fetchDataButton = document.getElementById('fetchDataButton');
    // Data from the backend
    
    
// Add an event listener to the button
    fetchDataButton.addEventListener('click', () => {

        const inputValue = inputText.value;
        
        // Clear previous responses
        responseContainer.innerHTML = "";

        // Send a GET request to your backend (you should replace the URL with your actual backend endpoint)
        fetch(`http://127.0.0.1:5000/result?input=${inputValue}`)
            .then(response => {
                console.log(response);
                return response.json();
            })
            .then(data => {
                // Display the response in the responseContainer
               
                let stockData = [];
                const currentDate = new Date();
                for (let i = 0; i < 120; i++) {
                    // Calculate the Date.UTC value for the current day in the loop
                    const futureDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() + i);
                    const utcValue = [Date.UTC(futureDate.getUTCFullYear(), futureDate.getUTCMonth(), futureDate.getUTCDate()),parseInt(data[i])];
                  
                    // Push the UTC value to the array
                    stockData.push(utcValue);
                  }
                
                console.log(stockData)
                Highcharts.stockChart('stockChart', {
                    rangeSelector: {
                        selected: 1
                    },
                    title: {
                        text: 'Stock Price Chart'
                    },
                    series: [{
                        name: 'Stock Price',
                        data: stockData,
                        tooltip: {
                            valueDecimals: 2
                        }
                    }]
                });

            })
            .catch(error => {
                console.error("Error:", error);
                responseContainer.textContent = "Error occurred while sending the request.";
            });
    });

    submitButton.addEventListener("click", function () {
        const inputValue = inputText.value;
        
        // Clear previous responses
        responseContainer.innerHTML = "";

        // Send a GET request to your backend (you should replace the URL with your actual backend endpoint)
        fetch(`http://127.0.0.1:5000/predict?input=${inputValue}`)
            .then(response => response.json())
            .then(data => {
                // Display the response in the responseContainer
                responseContainer.textContent = `Response from backend: ${data.message}`;
            })
            .catch(error => {
                console.error("Error:", error);
                responseContainer.textContent = "Error occurred while sending the request.";
            });
    });
    //drawing the chart
});
