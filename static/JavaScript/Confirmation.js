function loadConfirmationData() {
    // Retrieve the report data from localStorage
    const reportData = JSON.parse(localStorage.getItem("reportData"));
    const latitude = localStorage.getItem("Latitude");
    const longitude = localStorage.getItem("Longitude");

    if (reportData) {
        // Populate the report details
        document.getElementById("crime_type").innerText = reportData.crime_type || "N/A";
        document.getElementById("crime-date").innerText = reportData.crime_date || "N/A";
        document.getElementById("description").innerText = reportData.description || "N/A";
        document.getElementById("location").innerText = `Latitude: ${latitude || "N/A"}, Longitude: ${longitude || "N/A"}`;

        const imageContainer = document.getElementById("images");
        const videoContainer = document.getElementById("videos");

        
        // Display images
         imageContainer.innerHTML = '';
        if (reportData["images[]"] && Array.isArray(reportData["images[]"]) && reportData["images[]"].length > 0) {
            reportData["images[]"].forEach(src => {
                console.log(reportData["images[]"], src)
                let img = document.createElement("img");
                img.src = src; 
                img.style.maxWidth = "300px";  
                img.style.maxHeight = "200px"; 
                img.style.margin = "5px"; 
                imageContainer.appendChild(img);
            });
        } else {
            imageContainer.innerText = "No images available.";
        }

        // Display videos
         videoContainer.innerHTML = '';
        if (reportData["videos[]"] && Array.isArray(reportData["videos[]"]) && reportData["videos[]"].length > 0) {
            reportData["videos[]"].forEach(src => {
                let video = document.createElement("video");
                video.src = src; 
                video.controls = true;
                video.style.maxWidth = "300px";
                video.style.maxHeight = "200px"; 
                video.style.margin = "5px";
                videoContainer.appendChild(video);
            });
        } else {
            videoContainer.innerText = "No videos available.";
        }
    } else {
      
        alert('No report data found.');
        window.location.href = "http://127.0.0.1.5000/report";
     }
}


window.onload = loadConfirmationData;

var submitReportUrl = "{{ url_for('auth.submit_report') }}";
var csrfToken = "{{ csrf_token() }}";
var finalPageUrl ="{{url_for('auth.final')}}";

function confirmReport() {
    const reportData = JSON.parse(localStorage.getItem('reportData'));

    if (reportData) {
       
        const requestData={
            ...reportData,
            latitude: localStorage.getItem('Latitude'),
            longitude: localStorage.getItem('Longitude')
    };

    //Fetch request

    fetch("http://127.0.0.1:5000/submit_report",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": csrfToken
        } ,
        body:JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data =>{
        if(data.success){
            localStorage.removeItem("reportData");
            window.location ="http://127.0.0.1:5000/final?report_id="+ data.report_id;
        }else{
            alert("Failed to submit report: "+data.message);
        }
    })
    .catch(error =>{
        console.error("Error: ",error);
        alert("An error occured. Please try again.");
    });
}else{
    alert("No report data available.");
 }
}

document.addEventListener('DOMContentLoaded', loadConfirmationData);
