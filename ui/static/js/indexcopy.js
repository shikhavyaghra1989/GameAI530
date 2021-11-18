const statusDisplay = document.querySelector('.game--status');

let gameActive = true;
let noOfPlayers = document.querySelector("input[name='noOfPlayers']:checked").value
let players = ["player1", "player2", "player3", "player4"]
let currentPlayer = players[0];
let gameState = ["", "", "", "", "", "", "", "", ""];

const winningMessage = () => `Player ${currentPlayer} has won!`;
const drawMessage = () => `Game ended in a draw!`;
const currentPlayerTurn = () => `It's ${currentPlayer}'s turn`;

statusDisplay.innerHTML = currentPlayerTurn();

const winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

function handleCellPlayed(clickedCell, clickedCellIndex) {
    gameState[clickedCellIndex] = currentPlayer;
    clickedCell.innerHTML = currentPlayer;
}

function handlePlayerChange() {
    if(currentPlayer == "player4") {
        currentPlayer = players[0];
    } else if(currentPlayer == "player3")  {
        currentPlayer = players[3];
    } else if(currentPlayer == "player2")  {
        currentPlayer = players[2];
    } else {
        currentPlayer = players[1];
    }
    statusDisplay.innerHTML = currentPlayerTurn();
}

function handleResultValidation() {
    handlePlayerChange();
}

function handleCellClick(clickedCellEvent) {
    const clickedCell = clickedCellEvent.target;
    const clickedCellIndex = parseInt(clickedCell.getAttribute('data-cell-index'));

    if (gameState[clickedCellIndex] !== "" || !gameActive) {
        return;
    }

    handleCellPlayed(clickedCell, clickedCellIndex);
    handleResultValidation();
}

function handleRestartGame() {
    gameActive = true;
    currentPlayer = "X";
    gameState = ["", "", "", "", "", "", "", "", ""];
    statusDisplay.innerHTML = currentPlayerTurn();
    document.querySelectorAll('.cell').forEach(cell => cell.innerHTML = "");
}

function showPlayerThree() {
     var selected = document.querySelector("input[name='noOfPlayers']:checked").value;
     if(selected == "3") {
        document.querySelector('#playerDetails3').style.display = 'block';
        document.querySelector('#scorePlayer3').style.display = 'block';
        document.querySelector('#playerDetails4').style.display = 'none';
        document.querySelector('#scorePlayer4').style.display = 'none';
     }

     if(selected == "4") {
        document.querySelector('#playerDetails3').style.display = 'block';
        document.querySelector('#scorePlayer3').style.display = 'block';
        document.querySelector('#playerDetails4').style.display = 'block';
        document.querySelector('#scorePlayer4').style.display = 'block';
     }

     if(selected == "2") {
        document.querySelector('#playerDetails3').style.display = 'none';
        document.querySelector('#scorePlayer3').style.display = 'none';
        document.querySelector('#playerDetails4').style.display = 'none';
        document.querySelector('#scorePlayer4').style.display = 'none';
     }


}

document.querySelectorAll('.cell').forEach(cell => cell.addEventListener('click', handleCellClick));
document.querySelector('.game--restart').addEventListener('click', handleRestartGame);
document.querySelectorAll("input[name='noOfPlayers']").forEach(rad => rad.addEventListener('change', showPlayerThree));

