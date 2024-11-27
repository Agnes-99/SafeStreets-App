

//---------------------------------------Geo Tag-----------------------------
let locationButton = document.getElementById("location-button");
let geoError =document.getElementById("geo-error");
let locationDisplay = document.getElementById("location-display");
let mapHolder = document.getElementById("map-holder");

function getLocation(){
	geoError.innerHTML ='';
	locationDisplay.innerHTML ='';

	if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition(showCoordinates, showError);
	}
	else{
		geoError.innerHTML = "Geoolocation is not supported by this browser.";
	}
}

function showCoordinates(position){
	locationDisplay.innerHTML = "Latitude: "+ position.coords.latitude + 
	"<br>Longitude: "+ position.coords.longitude;
    
    console.log("locations added to the local storage");
	showPosition(position);
    localStorage.setItem("Latitude", position.coords.latitude);
    localStorage.setItem("Longitude",position.coords.longitude); 
} 

function showError(error){
	switch(error.code){
	case error.PERMISSION_DENIED:
		geoError.innerHTML = "User denied the request for Geolocation.";
		break;
	case error.POSITION_UNAVAILABLE:
		geoError.innerHTML = "Location information is unavailable."
		break;
	case error.TIMEOUT:
		geoError.innerHTML = "The request to get user location timed out.";
		break;
	case error.UNKNOWN_ERROR:
		geoError.innerHTML = "An unknown error occured.";
		break;
	default:
		geoError.innerHTML = "An unexpected error occured";
		break;
	}
}

function showPosition(position){
      let lat = position.coords.latitude;
      let lon = position.coords.longitude
	  let latlon = lat+","+lon;

    
	 let img_url = "https://maps.googleapis.com/maps/api/staticmap?center=" +
     latlon + "GOOGLE MAPS AP KEY";
     
     let img = new Image();
    img.onload = function() {
    	showLoader();

        mapHolder.innerHTML = ''; 
        mapHolder.appendChild(img);
        hideLoader();
    };
    img.src = img_url;
}

function showLoader() {
        let loader = mapHolder.querySelector('.loader');
        if (loader) {
            loader.style.display ="block";
        }
    }

function hideLoader() {
     let loader = document.querySelector('.loader');
     if (loader) {
        loader.style.display = 'none';
    }
}

//--------------------------------Submit form--------------------*/
    

   async function submitReport() {
    const form = document.getElementById("report-form");
    const formData = new FormData(form);
    const reportData = {};

    // Helper function to convert files to base64
    function convertFileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = () => reject(new Error('Error reading file'));
            reader.readAsDataURL(file);
        });
    }

    // Handle file inputs and convert to base64
    const processFiles = async (key) => {
        const files = formData.getAll(key);
        const filePromises = files.map(file => convertFileToBase64(file));
        return Promise.all(filePromises);
    };

   
    for (let [key, value] of formData.entries()) {
        if (key === "images[]" || key === "videos[]") {
            // Convert files to base64
            try {
                reportData[key] = await processFiles(key);
            } catch (error) {
                console.error('Error converting files to base64:', error);
                reportData[key] = []; 
            }
        } else {
            
            reportData[key] = value;
        }
    }

    reportData.latitude = localStorage.getItem("latitude") || "N/A";
    reportData.longitude = localStorage.getItem("longitude") || "N/A";

    localStorage.setItem("reportData", JSON.stringify(reportData));

    window.location.href = confirmationUrl; 
}

