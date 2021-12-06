const statusDisplay = document.querySelector('.game--status');
const is_completed = 0;

function handleCellClick(clickedCellEvent) {
    const clickedCell = clickedCellEvent.target;
    const clickedCellIndex = clickedCell.getAttribute('data-cell-index');

    if (clickedCell.innerHTML !== "" || is_completed)  {
        return;
    }

    $.ajax({
        type: "POST",
        url: "http://localhost:5001/next_state?move="+clickedCellIndex,
        contentType: "application/json",
        dataType: "json",
        success: function(response){
           populateCellWithValue(response)
        },
        error: function(response) {
           alert(JSON.stringify(response.responseText));
        }
    });

}

function handleRestartGame() {
    handleStartGame()
}

function handleCellPlayed(clickedCell, clickedCellIndex, color) {
    clickedCell.innerHTML = "<span class='dot' style='background-color: "+color+"; box-shadow:0 0 10px 1px #900;'></span>";
}

function populateCellWithValue(response){
    var splitedArray = response.board_state.split(")(")
    var first = splitedArray[0].replace('[(', '')
    splitedArray[0] = first
    var last = splitedArray[(splitedArray.length - 1)].replace(')]', ' ')
    splitedArray[(splitedArray.length - 1)] = last

    var newSplittedArray = splitedArray.map(item => {
        return item.split(',')
    })

    document.querySelectorAll('.cell').forEach((cell,index) => {
        if(newSplittedArray[index][2] == 'black'){
            cell.innerHTML = ""
        } else {
            var span  =  "<span class='dot' style='background-color: "+newSplittedArray[index][2]+"; box-shadow:0 0 10px 1px #900;'></span>"
            var size = newSplittedArray[index][3]
            for (let i = 0; i < size - 1; i++) {
                span += span
            }
            cell.innerHTML = span
        }
    } )
    statusDisplay.innerHTML = response.next_player?"It's " + response.next_player + "'s turn": ""
    if(response.is_completed == 1){
        is_completed = 1
        statusDisplay.innerHTML = "Game ended and the winner are " + response.winners
    }
}

function handleStartGame(){
    var player1 = document.querySelector('#player1').value
    var player2 = document.querySelector('#player2').value
    var player3 = document.querySelector('#player3').value
    var player4 = document.querySelector('#player4').value

    $.ajax({
        type: "POST",
        url: "http://localhost:5001/play?w=5&h=5&players="+player1+","+player2+","+player3+","+player4,
        contentType: "application/json",
        dataType: "json",
        success: function(response){
           populateCellWithValue(response)
        },
        error: function(response) {
           alert(JSON.stringify(response.responseText));
        }
    });
}


function showPlayerThree() {
     var selected = document.querySelector("input[name='noOfPlayers']:checked").value;
     if(selected == "3") {
        document.querySelector('#playerDetails3').style.display = 'block';
        document.querySelector('#playerDetails4').style.display = 'none';
     }

     if(selected == "4") {
        document.querySelector('#playerDetails3').style.display = 'block';
        document.querySelector('#playerDetails4').style.display = 'block';
     }

     if(selected == "2") {
        document.querySelector('#playerDetails3').style.display = 'none';
        document.querySelector('#playerDetails4').style.display = 'none';
     }
}

document.querySelectorAll('.cell').forEach(cell => cell.addEventListener('click', handleCellClick));
document.querySelector('.game--restart').addEventListener('click', handleRestartGame);
document.querySelectorAll("input[name='noOfPlayers']").forEach(rad => rad.addEventListener('change', showPlayerThree));
document.querySelector('.game--start').addEventListener('click', handleStartGame);

