// When the page loads, get the uploaded image from localStorage
window.onload = function() {
    const imagePath = localStorage.getItem("uploadedImage");
  
    if (imagePath) {
      // Set the uploaded image as the source of the image tag
      document.getElementById('uploadedImage').src = imagePath;
    } else {
      alert("No image uploaded. Please upload an image first.");
      window.location.href = 'cnnprediction.html'; // Redirect to upload page if no image
    }
  };
  
  // Simulate prediction when the button is clicked
  document.getElementById('predictBtn').addEventListener('click', function() {
    const prediction = "Positive for Kidney Cancer"; // Example prediction result
  
    // Display the prediction result
    document.getElementById('predictionResult').style.display = "block";
    document.getElementById('predictionText').innerText = prediction;
  });
  