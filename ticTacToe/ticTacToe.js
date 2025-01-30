let x = document.querySelectorAll(".box");
let z =0;
let count =0;
const arr = 
    [[0,1,2],
     [3,4,5],
     [6,7,8],
     [0,3,6],
     [1,4,7],
     [2,5,8],
     [0,4,8],
     [2,4,6]];
let resetAnna = ()=>{
    location.reload();
}
changeAnna = (evt) => {
    let attr = evt.target.getAttribute("class");
    attrArr = attr.split(" ");
    console.log(attrArr[1]);
    let sd = "."+attrArr[1];
    let theBox = document.querySelector(sd);
    if(count%2 == 0){
        theBox.style.color = "pink";
        theBox.innerText = "X";
        count++;
    }else{
        theBox.innerText = "O";
        count++;
    }
    theBox.disabled = true;
    checker(arr,count);
};
checker = (arr,count) => {
    let allBoxes = document.querySelectorAll(".box")
    arr.forEach(element => {
        let startBtw = allBoxes[element[0]].innerText;
        let midBtw = allBoxes[element[1]].innerText;
        let lastBtw = allBoxes[element[2]].innerText;

        if((startBtw != "" && midBtw != "" && lastBtw != "") || (count == 9)){
            if((startBtw === midBtw && midBtw === lastBtw) || (count == 9)){
                document.querySelector(".container").classList.toggle("visible");
                document.querySelector(".troopButton").classList.toggle("visible");
                let winningShow = document.createElement("button");
                if(count != 9){
                    winningShow.innerText = `Winner is ${startBtw}!!`;
                }else{
                    if(startBtw === midBtw && midBtw === lastBtw)
                        winningShow.innerText = `Winner is ${startBtw}!!`;
                    else
                        winningShow.innerText = `The Match is Tie!!`;
                }
                count++;
                winningShow.setAttribute("class","box")
                winningShow.style.width = "60vmin";
                winningShow.style.height = "60vmin";
                document.querySelector("h5").after(winningShow);
                let playAgain = document.createElement("p");
                playAgain.innerText = "\npress here to \nplay again";
                winningShow.append(playAgain);
                winningShow.addEventListener("click",resetAnna);
            }
        }
    });
};

for(i of x){
    i.classList.add(`btw${z}`);
    z++;
    i.addEventListener("click",changeAnna);
}

let resetButton = document.createElement("button");

resetButton.setAttribute("class","troopButton");
resetButton.innerText = "Reset";
resetButton.addEventListener("click",resetAnna);



document.querySelector(".container").after(resetButton);