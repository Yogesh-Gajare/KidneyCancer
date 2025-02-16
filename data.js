// // Capture the form submission
// document.getElementById("predict-btn").addEventListener("click", function(event) {
//     event.preventDefault();  // Prevent form submission

//     // Get values from the form
//     const age = document.getElementById("age").value;
//     const bloodPressure = document.getElementById("blood_pressure").value;
//     const albumin = document.getElementById("albumin").value;
//     const sugar = document.getElementById("sugar").value;
//     const redBloodCells = document.getElementById("red_blood_cells").value;
//     const pusCell = document.getElementById("pus_cell").value;
//     const bacteria = document.getElementById("bacteria").value;
//     const bloodGlucose = document.getElementById("blood_glucose").value;
//     const serumCreatinine = document.getElementById("serum_creatinine").value;
//     const potassium = document.getElementById("potassium").value;
//     const anaemia = document.getElementById("anaemia").value;

//     // Create an object to store the form data
//     const formData = {
//         age,
//         bloodPressure,
//         albumin,
//         sugar,
//         redBloodCells,
//         pusCell,
//         bacteria,
//         bloodGlucose,
//         serumCreatinine,
//         potassium,
//         anaemia
//     };

//     // Store the form data in localStorage
//     localStorage.setItem("formData", JSON.stringify(formData));

//     // Redirect to the prediction page
//     window.location.href = "annpredict.html";
// });


document.addEventListener("DOMContentLoaded", () => {
    // Check if we're on the prediction page
    const predictionForm = document.getElementById("prediction-form");
    if (predictionForm) {
        // On the prediction page, fetch data from localStorage
        const formData = JSON.parse(localStorage.getItem("formData"));

        if (formData) {
            // Pre-fill the form fields with data from localStorage
            document.getElementById("age").value = formData.age;
            document.getElementById("blood_pressure").value = formData.bloodPressure;
            document.getElementById("albumin").value = formData.albumin;
            document.getElementById("sugar").value = formData.sugar;
            document.getElementById("red_blood_cells").value = formData.redBloodCells;
            document.getElementById("pus_cell").value = formData.pusCell;
            document.getElementById("bacteria").value = formData.bacteria;
            document.getElementById("blood_glucose").value = formData.bloodGlucose;
            document.getElementById("serum_creatinine").value = formData.serumCreatinine;
            document.getElementById("potassium").value = formData.potassium;
            document.getElementById("anaemia").value = formData.anaemia;
        }

        // Handle form submission for prediction
        predictionForm.addEventListener("submit", async (event) => {
            event.preventDefault(); // Prevent form submission

            // Collect input values from the form
            const formData = {
                age: document.getElementById("age").value,
                blood_pressure: document.getElementById("blood_pressure").value,
                albumin: document.getElementById("albumin").value,
                sugar: document.getElementById("sugar").value,
                red_blood_cells: document.getElementById("red_blood_cells").value,
                pus_cell: document.getElementById("pus_cell").value,
                bacteria: document.getElementById("bacteria").value,
                blood_glucose: document.getElementById("blood_glucose").value,
                serum_creatinine: document.getElementById("serum_creatinine").value,
                potassium: document.getElementById("potassium").value,
                anaemia: document.getElementById("anaemia").value
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                // Display the result
                document.getElementById("prediction-result").innerHTML = `
                    <h3>Prediction Result: ${result.prediction}</h3>
                `;
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    // Handle "Predict" button click to store data in localStorage and redirect
    const predictButton = document.getElementById("predict-btn");
    if (predictButton) {
        predictButton.addEventListener("click", function(event) {
            event.preventDefault();  // Prevent form submission

            // Get values from the form
            const age = document.getElementById("age").value;
            const bloodPressure = document.getElementById("blood_pressure").value;
            const albumin = document.getElementById("albumin").value;
            const sugar = document.getElementById("sugar").value;
            const redBloodCells = document.getElementById("red_blood_cells").value;
            const pusCell = document.getElementById("pus_cell").value;
            const bacteria = document.getElementById("bacteria").value;
            const bloodGlucose = document.getElementById("blood_glucose").value;
            const serumCreatinine = document.getElementById("serum_creatinine").value;
            const potassium = document.getElementById("potassium").value;
            const anaemia = document.getElementById("anaemia").value;

            // Create an object to store the form data
            const formData = {
                age,
                bloodPressure,
                albumin,
                sugar,
                redBloodCells,
                pusCell,
                bacteria,
                bloodGlucose,
                serumCreatinine,
                potassium,
                anaemia
            };

            // Store the form data in localStorage
            localStorage.setItem("formData", JSON.stringify(formData));

            // Redirect to the prediction page
            window.location.href = "annpredict.html";
        });
    }
});
