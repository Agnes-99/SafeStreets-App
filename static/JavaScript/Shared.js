document.addEventListener("DOMContentLoaded", () => {
    const hamburgerMenu = document.getElementById("hamburger-menu");
    const sidebarMenu = document.querySelector(".sidebar-menu");
    const closeButton = document.querySelector(".close-button");

    hamburgerMenu.addEventListener("click", () => {
       sidebarMenu.classList.toggle("show");
    });

    closeButton.addEventListener("click",()=>{
        sidebarMenu.classList.remove("show");
    });
});
