let theNoButton = document.querySelectorAll("button")[1];
let theYesButton = document.querySelector("button");
let twinkle = document.createElement("h1");
twinkle.innerText = "I am Arupa and I am gonna approach Swagatika!!";
document.querySelector("h1").prepend(twinkle); 
document.querySelector("h1").innerText = document.querySelector("h1").innerText.slice(0,-1) + " Swagatika?";

moveLikeCrazy = (evt) => {
    console.log(evt.target);
    evt.target.style.position = "absolute";
    let topMove = Math.floor(Math.random() * 100);
    let leftMove = Math.floor(Math.random() * 100);
    evt.target.style.top = topMove + "vmin";
    evt.target.style.left = leftMove + "vmin";
}

theNoButton.addEventListener("mouseover",moveLikeCrazy);
theYesButton.addEventListener("click",()=>{
    // document.querySelectorAll("button").classList.toggle("visible");
    document.querySelector("h1").innerText = "Thank You for accecping me and my flaws";
})