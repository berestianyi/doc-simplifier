const html = document.getElementById("htmlPage");
const button = document.getElementById("toggleColorModeButton");
const sunIcon = document.getElementById("sunIcon");
const moonIcon = document.getElementById("moonIcon");

let isDarkMode = localStorage.getItem('isDarkMode') === 'true';

function applyMode() {
    if (isDarkMode) {
        html.setAttribute("data-bs-theme", "dark");
        button.setAttribute("class", "btn btn-outline-primary ms-4 me-2");
        sunIcon.style.display = "none";
        moonIcon.style.display = "inline";
    } else {
        html.setAttribute("data-bs-theme", "light");
        button.setAttribute("class", "btn btn-outline-warning ms-4 me-2");
        sunIcon.style.display = "inline";
        moonIcon.style.display = "none";
    }
}

applyMode();

button.addEventListener("click", () => {
    isDarkMode = !isDarkMode;
    localStorage.setItem('isDarkMode', isDarkMode);
    applyMode();
});