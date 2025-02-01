
var tictactoe = function(moves) {
    const acceptState = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]
    const store = new Map();
    moves.forEach((ele,index) =>{
        if(index % 2 == 0)
            store[(ele[0]*3)+ele[1]] = "X";
        else
            store[(ele[0]*3)+ele[1]] = "O";
    });
    for(ele of acceptState){
        if(store[ele[0]] != undefined && store[ele[1]] != undefined && store[ele[2]] != undefined){
            if(store[ele[0]] == store[ele[1]] && store[ele[1]] == store[ele[2]]){
                if(store[ele[0]] == "X"){
                    return "A";
                }else{
                    return "B";
                }
            }
        }
    };
    if(moves.length == 9){
        return "Draw";
    }else{
        return "Pending";
    }
};

console.log(tictactoe([[0,0],[2,0],[1,1],[2,1],[2,2]]));
