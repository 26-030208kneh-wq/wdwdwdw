import streamlit as st
import random

# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="오셀로 게임",
    page_icon="⚫",
    layout="centered"
)

EMPTY = 0
BLACK = 1
WHITE = 2

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


# ==========================================
# 게임 함수
# ==========================================

def create_board():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]

    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE

    return board


def opponent(player):
    return WHITE if player == BLACK else BLACK


def inside(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def get_flips(board, row, col, player):

    if not inside(row, col):
        return []

    if board[row][col] != EMPTY:
        return []

    enemy = opponent(player)
    flips = []

    for dr, dc in DIRECTIONS:

        r = row + dr
        c = col + dc

        temp = []

        while inside(r, c) and board[r][c] == enemy:
            temp.append((r, c))

            r += dr
            c += dc

        if (
            temp
            and inside(r, c)
            and board[r][c] == player
        ):
            flips.extend(temp)

    return flips


def valid_moves(board, player):

    moves = []

    for row in range(8):
        for col in range(8):

            if get_flips(board, row, col, player):
                moves.append((row, col))

    return moves


def make_move(board, row, col, player):

    flips = get_flips(board, row, col, player)

    if not flips:
        return False

    board[row][col] = player

    for r, c in flips:
        board[r][c] = player

    return True


def count_stones(board):

    black = 0
    white = 0

    for row in board:
        black += row.count(BLACK)
        white += row.count(WHITE)

    return black, white


# ==========================================
# AI
# ==========================================

def ai_move(board):

    moves = valid_moves(board, WHITE)

    if not moves:
        return None

    candidates = []

    corners = [
        (0, 0),
        (0, 7),
        (7, 0),
        (7, 7)
    ]

    for move in moves:

        row, col = move

        flip_count = len(
            get_flips(
                board,
                row,
                col,
                WHITE
            )
        )

        score = flip_count

        # 모서리 매우 중요
        if move in corners:
            score += 1000

        # 가장자리도 약간 유리
        if row in [0, 7] or col in [0, 7]:
            score += 20

        candidates.append(
            (move, score)
        )

    best_score = max(
        score for move, score in candidates
    )

    best_moves = [
        move
        for move, score in candidates
        if score == best_score
    ]

    return random.choice(best_moves)


# ==========================================
# 게임 초기화
# ==========================================

def start_game(mode):

    st.session_state.screen = "game"
    st.session_state.mode = mode
    st.session_state.board = create_board()
    st.session_state.turn = BLACK
    st.session_state.game_over = False
    st.session_state.message = "⚫ 흑돌의 차례입니다."


def go_home():

    st.session_state.screen = "home"


# ==========================================
# 세션 초기화
# ==========================================

if "screen" not in st.session_state:
    st.session_state.screen = "home"


# ==========================================
# CSS
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7f6;
    }

    .title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: #173d2b;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #66756d;
        font-size: 18px;
        margin-bottom: 35px;
    }

    .game-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: #173d2b;
    }

    .score {
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        margin: 15px;
    }

    .board-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .othello-board {
        width: min(88vw, 600px);
        height: min(88vw, 600px);

        background-color: #168447;

        border: 8px solid #0b542d;

        border-radius: 8px;

        padding: 3px;

        display: grid;
        grid-template-columns: repeat(8, 1fr);
        grid-template-rows: repeat(8, 1fr);

        gap: 2px;

        box-shadow:
            0 8px 20px rgba(0,0,0,0.2);
    }

    .cell {
        background-color: #1c9a50;

        display: flex;
        align-items: center;
        justify-content: center;

        border: 1px solid #116f3b;
    }

    .black {
        width: 78%;
        height: 78%;

        border-radius: 50%;

        background:
            radial-gradient(
                circle at 30% 25%,
                #555,
                #111 55%,
                #000
            );

        box-shadow:
            2px 3px 5px rgba(0,0,0,0.45);
    }

    .white {
        width: 78%;
        height: 78%;

        border-radius: 50%;

        background:
            radial-gradient(
                circle at 30% 25%,
                #ffffff,
                #eeeeee 60%,
                #bbbbbb
            );

        box-shadow:
            2px 3px 5px rgba(0,0,0,0.45);
    }

    .hint {
        width: 25%;
        height: 25%;

        border-radius: 50%;

        background-color: #f7d94c;

        box-shadow:
            0 0 8px rgba(255,255,0,0.8);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 시작 화면
# ==========================================

if st.session_state.screen == "home":

    st.markdown(
        '<div class="title">⚫ 오셀로</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">돌을 놓고 상대의 돌을 뒤집어 보세요!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background:#ffffff;
            padding:35px;
            border-radius:20px;
            text-align:center;
            box-shadow:0 5px 20px rgba(0,0,0,0.08);
        ">
            <div style="font-size:80px;">
                ⚫ ⚪
            </div>

            <h2>게임을 시작하세요</h2>

            <p style="color:#777;">
                원하는 게임 방식을 선택할 수 있습니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🤖 AI와 하기",
            use_container_width=True
        ):
            start_game("ai")
            st.rerun()

    with col2:

        if st.button(
            "👥 친구와 하기",
            use_container_width=True
        ):
            start_game("friend")
            st.rerun()

    st.write("")

    st.info(
        "⚫ 흑돌이 먼저 시작합니다. "
        "노란 점이 있는 위치에 돌을 놓을 수 있습니다."
    )


# ==========================================
# 게임 화면
# ==========================================

else:

    board = st.session_state.board
    turn = st.session_state.turn
    mode = st.session_state.mode

    black, white = count_stones(board)

    st.markdown(
        '<div class="game-title">⚫ 오셀로</div>',
        unsafe_allow_html=True
    )

    # 점수
    st.markdown(
        f"""
        <div class="score">
            ⚫ {black}
            &nbsp;&nbsp;&nbsp;
            :
            &nbsp;&nbsp;&nbsp;
            {white} ⚪
        </div>
        """,
        unsafe_allow_html=True
    )

    # 게임 방식
    if mode == "ai":
        mode_text = "🤖 AI와 대결"
    else:
        mode_text = "👥 친구와 대결"

    st.caption(
        f"게임 방식: {mode_text}"
    )

    # ======================================
    # 게임 종료
    # ======================================

    if (
        len(valid_moves(board, BLACK)) == 0
        and len(valid_moves(board, WHITE)) == 0
    ):
        st.session_state.game_over = True

    # ======================================
    # 게임 종료 화면
    # ======================================

    if st.session_state.game_over:

        if black > white:
            result = "🎉 흑돌 승리!"
        elif white > black:
            result = "🎉 백돌 승리!"
        else:
            result = "🤝 무승부!"

        st.success(
            f"{result}   최종 점수: ⚫ {black} : {white} ⚪"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🔄 다시 하기",
                use_container_width=True
            ):
                start_game(mode)
                st.rerun()

        with col2:

            if st.button(
                "🏠 처음으로",
                use_container_width=True
            ):
                go_home()
                st.rerun()

    # ======================================
    # AI 차례
    # ======================================

    elif mode == "ai" and turn == WHITE:

        moves = valid_moves(board, WHITE)

        if moves:

            move = ai_move(board)

            if move:

                make_move(
                    board,
                    move[0],
                    move[1],
                    WHITE
                )

                st.session_state.turn = BLACK
                st.session_state.message = (
                    "⚫ 당신의 차례입니다."
                )

                st.rerun()

        else:

            st.session_state.turn = BLACK
            st.session_state.message = (
                "🤖 AI가 놓을 곳이 없습니다. "
                "당신의 차례입니다."
            )

            st.rerun()

    # ======================================
    # 플레이어 차례
    # ======================================

    else:

        moves = valid_moves(board, turn)

        if turn == BLACK:

            player_name = "⚫ 흑돌"

        else:

            player_name = "⚪ 백돌"

        st.info(
            f"{player_name}의 차례입니다."
        )

        # 놓을 곳이 없는 경우
        if not moves:

            st.warning(
                f"{player_name}은 놓을 수 있는 곳이 없습니다. "
                "자동으로 차례가 넘어갑니다."
            )

            st.session_state.turn = opponent(turn)

            st.rerun()

        # ==================================
        # 보드
        # ==================================

        st.markdown(
            '<div class="board-wrapper">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="othello-board">',
            unsafe_allow_html=True
        )

        for row in range(8):

            for col in range(8):

                st.markdown(
                    '<div class="cell">',
                    unsafe_allow_html=True
                )

                if board[row][col] == BLACK:

                    st.markdown(
                        '<div class="black"></div>',
                        unsafe_allow_html=True
                    )

                elif board[row][col] == WHITE:

                    st.markdown(
                        '<div class="white"></div>',
                        unsafe_allow_html=True
                    )

                elif (row, col) in moves:

                    st.markdown(
                        '<div class="hint"></div>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

        st.markdown(
            '</div></div>',
            unsafe_allow_html=True
        )

        # ==================================
        # 실제 클릭 버튼
        # ==================================

        st.markdown(
            "### 착수할 위치를 선택하세요"
        )

        for row in range(8):

            cols = st.columns(8)

            for col in range(8):

                with cols[col]:

                    if board[row][col] == BLACK:

                        label = "⚫"

                    elif board[row][col] == WHITE:

                        label = "⚪"

                    elif (row, col) in moves:

                        label = "🟡"

                    else:

                        label = " "

                    can_click = (
                        (row, col) in moves
                    )

                    if st.button(
                        label,
                        key=f"move_{row}_{col}",
                        disabled=not can_click,
                        use_container_width=True
                    ):

                        make_move(
                            board,
                            row,
                            col,
                            turn
                        )

                        st.session_state.turn = opponent(turn)

                        st.rerun()

    # ======================================
    # 하단 버튼
    # ======================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔄 게임 다시 시작",
            use_container_width=True
        ):

            start_game(mode)
            st.rerun()

    with col2:

        if st.button(
            "🏠 게임 선택으로",
            use_container_width=True
        ):

            go_home()
            st.rerun()
