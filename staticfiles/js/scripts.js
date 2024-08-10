const icon = document.getElementById("icons");
const body = document.body;

// Check if light mode preference is stored in local storage
const isLightMode = localStorage.getItem("lightMode") === "true";

// Set initial light mode state based on local storage or default
if (isLightMode) {
  body.classList.add("lightmode");
}

icon.onclick = function () {
  // Toggle the "lightmode" class on the body
  body.classList.toggle("lightmode");

  // Update local storage with the current light mode state
  localStorage.setItem(
    "lightMode",
    body.classList.contains("lightmode") ? "true" : "false"
  );
};

function OpenSidebar(){
    const  sidebar=document.querySelector(".sidebar");
    sidebar.style.display = "flex"
}
function CloseSidebar(){
    const  sidebar=document.querySelector(".sidebar");
    sidebar.style.display = "none"
}

const hover = document.querySelector(".hover");

function display() {
  hover.style.display = "flex";
}

function noDisplay() {
  hover.style.display = "none";
}

let counter = 0;

const clap = document.querySelector(".clap");

clap.addEventListener("click", () => {
  const count = counter++;
  document.querySelector(".clap span").innerHTML = count;
});

