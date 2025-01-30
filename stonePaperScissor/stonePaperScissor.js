
let bestOf1 = document.createElement("button");

let bestOf3 = document.createElement("button");

let bestOf5 = document.createElement("button");
let stoneGame = document.querySelectorAll("game")
stoneGame[0].append(bestOf1,bestOf3,bestOf5);

let player1Show = document.createElement("h2");
let player2Show = document.createElement("h2");
let messag = document.createElement("h2");

player1Show.innerText = "Player 1 : 0";
player2Show.innerText = "Player 2 : 0";
messag.innerText = "Message";
stoneGame[1].append(player1Show,messag,player2Show);

let resetAnna = ()=>{
    location.reload();
}

let resetBtn = document.createElement("button");
resetBtn.innerText = "Reset"
document.querySelector("container").after(resetBtn);

resetBtn.addEventListener("click",resetAnna);

let buttons = document.querySelectorAll("button");
buttons.forEach((ele,index)=>{
    ele.classList.add(`btn${index}`);
    ele.style.backgroundColor = "black";
    ele.style.color = "white";
    ele.style.fontSize = "5rem";
    ele.style.borderRadius = "10px";
    ele.style.padding = "10px";
});


bestOf1.innerText = "Best Of 1";
bestOf1.style.fontSize = "2rem";

bestOf3.innerText = "Best Of 3";
bestOf3.style.fontSize = "2rem";

bestOf5.innerText = "Best Of 5";
bestOf5.style.fontSize = "2rem";

let theLimitOutside = 0;

limiterDraws = (evt) => {
    let theLimit =  evt.target.innerText;
    theLimitOutside = theLimit[theLimit.length-1];
    evt.target.style.color = "red";
    console.log(theLimitOutside);
    bestOf1.disabled = true;
    bestOf3.disabled = true;
    bestOf5.disabled = true;
    buttons[3].disabled = false;
    buttons[4].disabled = false;
}

bestOf1.addEventListener("click",limiterDraws);
bestOf3.addEventListener("click",limiterDraws);
bestOf5.addEventListener("click",limiterDraws);

buttons[3].style.borderLeft = "10px solid red";
buttons[3].style.paddingLeft = "50px";
buttons[3].innerText = "Draw";
buttons[4].style.borderRight = "10px solid red";
buttons[4].style.paddingRight = "50px";
buttons[4].innerText = "Draw";

buttons[3].disabled = true;
buttons[4].disabled = true;

let store = new Map();

store[0] = "Stone";
store[1] = "Paper";
store[2] = "Scissor";

const resultsCompare = new Map();

resultsCompare["StonePaper"] = "player2";
resultsCompare["PaperStone"] = "player1";
resultsCompare["StoneScissor"] = "player1";
resultsCompare["ScissorStone"] = "player2";
resultsCompare["ScissorPaper"] = "player1";
resultsCompare["PaperScissor"] = "player2";

let bestOf = 0;

innerPrint = (evt) =>{
    let rand = Math.floor( Math.random() * 3);
    evt.target.innerText = store[rand];
    console.log((Number(theLimitOutside)*2)-1);


    if(bestOf < (Number(theLimitOutside)*2)-1){
        if(evt.target == buttons[3]){
            console.log(bestOf);
            console.log(store[rand]);
            evt.target.disabled = true;  
        }else{
            console.log(bestOf);
            console.log(store[rand]);
            evt.target.disabled = true;
        }
    }
    if( bestOf % 2 == 1 && bestOf <= (Number(theLimitOutside)*2)-1 ){
        if( buttons[3].innerText == buttons[4].innerText ){
            messag.innerText = "draw";

            bestOf -= 2;
        }else{
            if(resultsCompare[buttons[3].innerText+buttons[4].innerText] == "player1"){
                player1Show.innerText ="Player 1 : "+ (Number(player1Show.innerText[Number(player1Show.innerText.length-1)])+1);
                messag.innerText = "Player 1 Won in this match";
            }else{
                player2Show.innerText ="Player 2 : "+ (Number(player2Show.innerText[Number(player2Show.innerText.length-1)])+1);
                messag.innerText = "Player 2 Won in this match";
            }
        }
        buttons[3].disabled = false;
        buttons[4].disabled = false;
    }
    if(bestOf == (Number(theLimitOutside)*2)-1 || ((Number(player1Show.innerText[Number(player1Show.innerText.length-1)])) >= Math.ceil(theLimitOutside/2)) || ((Number(player2Show.innerText[Number(player2Show.innerText.length-1)])) >= Math.ceil(theLimitOutside/2))){
        document.querySelector(".btn5").classList.toggle("visible");
        let lastWinnerDisplayer = document.createElement("button");
        let viewButton = document.createElement("button");
        let playAgain = document.createElement("button");
        lastWinnerDisplayer.classList.add("troopButton");
        viewButton.classList.add("troopButton");
        viewButton.style.fontSize = "2rem";
        viewButton.innerText = "View"
        viewButton.style.width = "70vmin";
        playAgain.classList.add("troopButton");
        playAgain.style.fontSize = "2rem";
        playAgain.style.marginTop = "0px";
        playAgain.innerText = "Play Again";
        playAgain.style.width = "80vmin";
        lastWinnerDisplayer.style.width = "70vmin";
        lastWinnerDisplayer.style.height = "70vmin";
        buttons[3].disabled = true;
        buttons[4].disabled = true;
        if(player1Show.innerText[Number(player1Show.innerText.length-1)] > player2Show.innerText[Number(player2Show.innerText.length-1)])
        {
            lastWinnerDisplayer.innerText = "Player1 Won";
            console.log("player1 Won");
        }else{
            lastWinnerDisplayer.innerText = "Player2 Won";
            console.log("Player2 Won");
        }
        document.querySelector("h1").after(lastWinnerDisplayer);
        lastWinnerDisplayer.after(viewButton);
        lastWinnerDisplayer.after(playAgain);
        playAgain.addEventListener("click",resetAnna);
        viewButton.addEventListener("click",()=>{
            document.querySelector("h2").classList.toggle("visible");
            document.querySelector("container").classList.toggle("visible");
        });
        buttons[3].disabled = true;
        buttons[4].disabled = true;
    }
    bestOf ++;
}


buttons[3].addEventListener("click", innerPrint);
buttons[4].addEventListener("click", innerPrint);