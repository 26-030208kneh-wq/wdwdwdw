import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="오셀로 게임",
    page_icon="⚫",
    layout="centered"
)

components.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    background: #f4f6f5;
    font-family: Arial, sans-serif;
}

#app {
    width: 100%;
    max-width: 650px;
    margin: auto;
    text-align: center;
}

/* 제목 */

.title {
    font-size: 42px;
    font-weight: bold;
    color: #173d2b;
    margin-top: 15px;
    margin-bottom: 5px;
}

.subtitle {
    color: #68756e;
    font-size: 17px;
    margin-bottom: 25px;
}


/* 시작 화면 */

.start-box {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.start-stones {
    font-size: 65px;
    margin-bottom: 10px;
}

.start-title {
    font-size: 27px;
    font-weight: bold;
    color: #173d2b;
    margin-bottom: 10px;
}

.start-text {
    color: #777;
    margin-bottom: 25px;
}

.start-button {
    width: 100%;
    border: none;
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
    font-size: 18px;
    font-weight: bold;
    color: white;
    cursor: pointer;
    transition: 0.2s;
}

.start-button:hover {
    transform: scale(1.02);
}

.ai-button {
    background: #1976d2;
}

.friend-button {
    background: #168447;
}


/* 게임 */

#game {
    display: none;
}

.game-header {
    background: white;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

.score {
    display: flex;
    justify-content: space-around;
    align-items: center;
    font-size: 22px;
    font-weight: bold;
}

.turn {
    margin-top: 10px;
    color: #555;
    font-size: 17px;
}


/* ==================================
   오셀로 판
   사진처럼 초록색 + 검은 격자
   ================================== */

.board-wrapper {
    display: flex;
    justify-content: center;
    width: 100%;
}

.board {
    width: min(92vw, 580px);
    height: min(92vw, 580px);

    background: #16b84e;

    border: 7px solid #111;

    display: grid;

    grid-template-columns: repeat(8, 1fr);
    grid-template-rows: repeat(8, 1fr);

    box-shadow:
        0 8px 20px rgba(0,0,0,0.35);

    position: relative;
}


/* 각각의 칸 */

.cell {
    position: relative;

    border-right: 2px solid #111;
    border-bottom: 2px solid #111;

    background: #18bd50;

    display: flex;
    align-items: center;
    justify-content: center;

    cursor: pointer;
}

.cell:nth-child(8n) {
    border-right: none;
}

.cell:nth-child(n+57) {
    border-bottom: none;
}

.cell:hover {
    background: #22c958;
}


/* 돌 */

.stone {
    width: 72%;
    height: 72%;

    border-radius: 50%;

    position: relative;

    z-index: 3;

    box-shadow:
        2px 4px 5px rgba(0,0,0,0.45);
}


/* 흑돌 */

.black {
    background:
        radial-gradient(
            circle at 30% 25%,
            #777 0%,
            #333 30%,
            #111 65%,
            #000 100%
        );

    border: 1px solid #111;
}


/* 백돌 */

.white {
    background:
        radial-gradient(
            circle at 30% 25%,
            #ffffff 0%,
            #eeeeee 45%,
            #cfcfcf 75%,
            #999999 100%
        );

    border: 1px solid #aaa;
}


/* 착수 가능한 위치 */

.hint {
    width: 23%;
    height: 23%;

    border-radius: 50%;

    background: #ffe600;

    box-shadow:
        0 0 8px rgba(255,255,0,0.9);

    z-index: 2;
}


/* 버튼 */

.buttons {
    margin-top: 20px;
    display: flex;
    gap: 10px;
}

.game-button {
    flex: 1;

    padding: 13px;

    border: none;
    border-radius: 10px;

    font-size: 16px;
    font-weight: bold;

    cursor: pointer;
}

.restart {
    background: #168447;
    color: white;
}

.home {
    background: #555;
    color: white;
}


/* 결과 */

.result {
    margin-top: 15px;

    background: white;

    border-radius: 15px;

    padding: 20px;

    font-size: 23px;
    font-weight: bold;
}

</style>
</head>


<body>

<div id="app">

    <!-- =========================
         시작 화면
         ========================= -->

    <div id="home">

        <div class="title">
            ⚫ 오셀로 ⚪
        </div>

        <div class="subtitle">
            상대방의 돌을 사이에 끼워 뒤집어 보세요!
        </div>

        <div class="start-box">

            <div class="start-stones">
                ⚫ ⚪
            </div>

            <div class="start-title">
                게임을 시작하세요
            </div>

            <div class="start-text">
                게임 방식을 선택해주세요.
            </div>

            <button
                class="start-button ai-button"
                onclick="startGame('ai')"
            >
                🤖 AI와 하기
            </button>

            <button
                class="start-button friend-button"
                onclick="startGame('friend')"
            >
                👥 친구와 하기
            </button>

        </div>

    </div>


    <!-- =========================
         게임 화면
         ========================= -->

    <div id="game">

        <div class="title">
            ⚫ 오셀로 ⚪
        </div>

        <div class="game-header">

            <div class="score">

                <div>
                    ⚫ <span id="blackScore">2</span>
                </div>

                <div>
                    ⚪ <span id="whiteScore">2</span>
                </div>

            </div>

            <div
                class="turn"
                id="turnText"
            >
                ⚫ 흑돌의 차례입니다.
            </div>

        </div>


        <!-- 오셀로 판 -->

        <div class="board-wrapper">

            <div
                class="board"
                id="board"
            >
            </div>

        </div>


        <!-- 결과 -->

        <div
            id="result"
            class="result"
            style="display:none;"
        >
        </div>


        <!-- 버튼 -->

        <div class="buttons">

            <button
                class="game-button restart"
                onclick="restartGame()"
            >
                🔄 다시 시작
            </button>

            <button
                class="game-button home"
                onclick="goHome()"
            >
                🏠 처음으로
            </button>

        </div>

    </div>

</div>


<script>

/* =====================================
   오셀로 게임
   ===================================== */

const EMPTY = 0;
const BLACK = 1;
const WHITE = 2;

let board = [];
let currentPlayer = BLACK;
let gameMode = "ai";
let gameOver = false;


/* 방향 */

const directions = [

    [-1, -1],
    [-1, 0],
    [-1, 1],

    [0, -1],
    [0, 1],

    [1, -1],
    [1, 0],
    [1, 1]

];


/* =====================================
   새 보드
   ===================================== */

function createBoard() {

    board = [];

    for (let r = 0; r < 8; r++) {

        board[r] = [];

        for (let c = 0; c < 8; c++) {
            board[r][c] = EMPTY;
        }

    }

    board[3][3] = WHITE;
    board[3][4] = BLACK;
    board[4][3] = BLACK;
    board[4][4] = WHITE;

}


/* =====================================
   상대방
   ===================================== */

function opponent(player) {

    if (player === BLACK) {
        return WHITE;
    }

    return BLACK;

}


/* =====================================
   보드 안인지
   ===================================== */

function inside(r, c) {

    return (
        r >= 0 &&
        r < 8 &&
        c >= 0 &&
        c < 8
    );

}


/* =====================================
   뒤집을 돌 찾기
   ===================================== */

function getFlips(r, c, player) {

    if (!inside(r, c)) {
        return [];
    }

    if (board[r][c] !== EMPTY) {
        return [];
    }

    const enemy = opponent(player);

    let flips = [];

    for (const direction of directions) {

        const dr = direction[0];
        const dc = direction[1];

        let rr = r + dr;
        let cc = c + dc;

        let temp = [];

        while (
            inside(rr, cc) &&
            board[rr][cc] === enemy
        ) {

            temp.push([rr, cc]);

            rr += dr;
            cc += dc;

        }

        if (
            temp.length > 0 &&
            inside(rr, cc) &&
            board[rr][cc] === player
        ) {

            flips = flips.concat(temp);

        }

    }

    return flips;

}


/* =====================================
   가능한 위치
   ===================================== */

function getValidMoves(player) {

    let moves = [];

    for (let r = 0; r < 8; r++) {

        for (let c = 0; c < 8; c++) {

            if (
                getFlips(r, c, player).length > 0
            ) {

                moves.push([r, c]);

            }

        }

    }

    return moves;

}


/* =====================================
   돌 놓기
   ===================================== */

function makeMove(r, c, player) {

    const flips = getFlips(
        r,
        c,
        player
    );

    if (flips.length === 0) {
        return false;
    }

    board[r][c] = player;

    for (const position of flips) {

        board[position[0]][position[1]] = player;

    }

    return true;

}


/* =====================================
   점수
   ===================================== */

function getScore() {

    let black = 0;
    let white = 0;

    for (let r = 0; r < 8; r++) {

        for (let c = 0; c < 8; c++) {

            if (board[r][c] === BLACK) {
                black++;
            }

            if (board[r][c] === WHITE) {
                white++;
            }

        }

    }

    return {
        black: black,
        white: white
    };

}


/* =====================================
   화면에 보드 그리기
   ===================================== */

function renderBoard() {

    const boardElement =
        document.getElementById("board");

    boardElement.innerHTML = "";

    const moves =
        getValidMoves(currentPlayer);

    for (let r = 0; r < 8; r++) {

        for (let c = 0; c < 8; c++) {

            const cell =
                document.createElement("div");

            cell.className = "cell";

            const value = board[r][c];

            /* 흑돌 */

            if (value === BLACK) {

                const stone =
                    document.createElement("div");

                stone.className =
                    "stone black";

                cell.appendChild(stone);

            }

            /* 백돌 */

            else if (value === WHITE) {

                const stone =
                    document.createElement("div");

                stone.className =
                    "stone white";

                cell.appendChild(stone);

            }

            /* 착수 가능 위치 */

            else {

                const canMove =
                    moves.some(
                        move =>
                            move[0] === r &&
                            move[1] === c
                    );

                if (canMove) {

                    const hint =
                        document.createElement("div");

                    hint.className = "hint";

                    cell.appendChild(hint);

                }

            }


            /* 클릭 */

            cell.onclick = function() {

                playerClick(r, c);

            };


            boardElement.appendChild(cell);

        }

    }


    updateScore();

}


/* =====================================
   점수 표시
   ===================================== */

function updateScore() {

    const score = getScore();

    document.getElementById(
        "blackScore"
    ).textContent = score.black;

    document.getElementById(
        "whiteScore"
    ).textContent = score.white;

}


/* =====================================
   차례 표시
   ===================================== */

function updateTurnText() {

    const text =
        document.getElementById("turnText");

    if (gameOver) {
        return;
    }

    if (gameMode === "ai") {

        if (currentPlayer === BLACK) {

            text.textContent =
                "⚫ 당신의 차례입니다.";

        } else {

            text.textContent =
                "🤖 AI가 생각하고 있습니다...";

        }

    } else {

        if (currentPlayer === BLACK) {

            text.textContent =
                "⚫ 흑돌의 차례입니다.";

        } else {

            text.textContent =
                "⚪ 백돌의 차례입니다.";

        }

    }

}


/* =====================================
   사람 클릭
   ===================================== */

function playerClick(r, c) {

    if (gameOver) {
        return;
    }

    /* AI 모드에서 백은 AI */

    if (
        gameMode === "ai" &&
        currentPlayer === WHITE
    ) {
        return;
    }


    const success =
        makeMove(
            r,
            c,
            currentPlayer
        );

    if (!success) {
        return;
    }


    currentPlayer =
        opponent(currentPlayer);

    renderBoard();

    checkTurn();

}


/* =====================================
   차례 확인
   ===================================== */

function checkTurn() {

    if (gameOver) {
        return;
    }

    let moves =
        getValidMoves(currentPlayer);


    /* 놓을 곳이 없는 경우 */

    if (moves.length === 0) {

        const otherMoves =
            getValidMoves(
                opponent(currentPlayer)
            );

        /* 둘 다 놓을 곳 없음 */

        if (otherMoves.length === 0) {

            finishGame();
            return;

        }

        /* 패스 */

        currentPlayer =
            opponent(currentPlayer);

        renderBoard();

    }


    updateTurnText();


    /* AI 차례 */

    if (
        gameMode === "ai" &&
        currentPlayer === WHITE
    ) {

        setTimeout(
            aiTurn,
            600
        );

    }

}


/* =====================================
   AI
   ===================================== */

function aiTurn() {

    if (gameOver) {
        return;
    }

    const moves =
        getValidMoves(WHITE);

    if (moves.length === 0) {

        currentPlayer = BLACK;

        checkTurn();

        return;
    }


    const corners = [

        [0, 0],
        [0, 7],
        [7, 0],
        [7, 7]

    ];


    let bestMove = null;
    let bestScore = -999999;


    for (const move of moves) {

        const r = move[0];
        const c = move[1];

        let score =
            getFlips(
                r,
                c,
                WHITE
            ).length;


        /* 모서리 */

        const isCorner =
            corners.some(
                corner =>
                    corner[0] === r &&
                    corner[1] === c
            );

        if (isCorner) {
            score += 1000;
        }


        /* 가장자리 */

        if (
            r === 0 ||
            r === 7 ||
            c === 0 ||
            c === 7
        ) {

            score += 30;

        }


        if (score > bestScore) {

            bestScore = score;
            bestMove = move;

        }

    }


    makeMove(
        bestMove[0],
        bestMove[1],
        WHITE
    );


    currentPlayer = BLACK;

    renderBoard();

    checkTurn();

}


/* =====================================
   게임 종료
   ===================================== */

function finishGame() {

    gameOver = true;

    const score = getScore();

    let message = "";

    if (score.black > score.white) {

        if (gameMode === "ai") {
            message = "🎉 당신의 승리!";
        } else {
            message = "🎉 흑돌 승리!";
        }

    }

    else if (score.white > score.black) {

        if (gameMode === "ai") {
            message = "🤖 AI의 승리!";
        } else {
            message = "🎉 백돌 승리!";
        }

    }

    else {

        message = "🤝 무승부!";

    }


    const result =
        document.getElementById("result");

    result.style.display = "block";

    result.innerHTML =
        message +
        "<br><br>" +
        "⚫ " +
        score.black +
        " : " +
        score.white +
        " ⚪";

}


/* =====================================
   게임 시작
   ===================================== */

function startGame(mode) {

    gameMode = mode;

    document.getElementById(
        "home"
    ).style.display = "none";

    document.getElementById(
        "game"
    ).style.display = "block";

    restartGame();

}


/* =====================================
   다시 시작
   ===================================== */

function restartGame() {

    createBoard();

    currentPlayer = BLACK;

    gameOver = false;

    document.getElementById(
        "result"
    ).style.display = "none";

    renderBoard();

    updateTurnText();

}


/* =====================================
   처음으로
   ===================================== */

function goHome() {

    document.getElementById(
        "game"
    ).style.display = "none";

    document.getElementById(
        "home"
    ).style.display = "block";

}

</script>

</body>
</html>
""",
    height=850,
    scrolling=False
)
