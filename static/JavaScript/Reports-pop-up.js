
document.addEventListener('DOMContentLoaded', () =>{
    const crimeTypeFilter = document.getElementById("crime-type") ;
    const locationFilter = document.getElementById("location") ;
    const searchInput = document.getElementById("search") ;
    const reportList = document.querySelector(".report-list") ;

    function filterNotifications(){
        const crimeType = crimeTypeFilter.value;
        const location = locationFilter.value.toLowerCase();

        const reports = Array.from(reportList.children);
        reports.forEach(report => {
            const title = report.querySelector(".report-title").textContent.toLowerCase();
            const address = report.querySelector(".report-address").textContent.toLowerCase();

            const matchesCrimeType = crimeType === "all" || title.includes(crimeType);
           
            const matchesLocation = !location || address.includes(location);

            if (matchesCrimeType && matchesLocation) {
                report.style.display = "";
            } 
            else {
                report.style.display = "none";
            }
       });
    }

    function searchNotifications() {
        const query = searchInput.value.toLowerCase();
        const reports = Array.from(reportList.children);

        reports.forEach(report => {
            const title = report.querySelector(".report-title").textContent.toLowerCase();
            const address = report.querySelector(".report-address").textContent.toLowerCase();
            const description = report.querySelector(".report-description").textContent.toLowerCase();

            // Check if query matches title, address, or description
            if (title.includes(query) || address.includes(query) || description.includes(query)) {
                report.style.display = "";
            } 
            else {
                report.style.display = "none";
            }
        });
    }

    crimeTypeFilter.addEventListener("change",  filterNotifications);
    locationFilter.addEventListener("input",  filterNotifications);
    searchInput.addEventListener("input", searchNotifications);
});

