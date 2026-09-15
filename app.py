import streamlit as st
import random

# ==========================================
# 설정
# ==========================================

st.set_page_config(
    page_title="오셀로",
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
# 보드 만들기
# ==========================================

def create_board():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]

    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE

    return board


# ==========================================
# 상대 돌
# ==========================================

def opponent(player):
    if player == BLACK:
        return WHITE
    return BLACK


# ==========================================
# 보드 안인지 확인
# ==========================================

def inside(row, col):
    return 0 <= row < 8 and 0 <= col < 8


# ==========================================
# 뒤집을 돌 찾기
# ==========================================

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


# ==========================================
# 놓을 수 있는 위치
# ==========================================

def valid_moves(board, player):

    moves = []

    for row in range(8):
        for col in range(8):

            if get_flips(board, row, col, player):
                moves.append((row, col))

    return moves


# ==========================================
# 돌 놓기
# ==========================================

def make_move(board, row, col, player):

    flips = get_flips(
        board,
        row,
        col,
        player
    )

    if not flips:
        return False

    board[row][col] = player

    for r, c in flips:
        board[r][c] = player

    return True


# ==========================================
# 점수 계산
# ==========================================

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

    moves = valid_moves(
        board,
        WHITE
    )

    if not moves:
        return None

    corners = [
        (0, 0),
        (0, 7),
        (7, 0),
        (7, 7)
    ]

    candidates = []

    for move in moves:

        row, col = move

        score = len(
            get_flips(
                board,
                row,
                col,
                WHITE
            )
        )

        # 모서리는 매우 좋은 위치
        if move in corners:
            score += 1000

        # 가장자리 보너스
        if row == 0 or row == 7:
            score += 20

        if col == 0 or col == 7:
            score += 20

        candidates.append(
            (move, score)
        )

    best_score = max(
        score
        for move, score in candidates
    )

    best_moves = [
        move
        for move, score in candidates
        if score == best_score
    ]

    return random.choice(best_moves)


# ==========================================
# 게임 시작
# ==========================================

def start_game(mode):

    st.session_state.screen = "game"
    st.session_state.mode = mode
    st.session_state.board = create_board()
    st.session_state.turn = BLACK
    st.session_state.game_over = False


# ==========================================
# 처음 화면으로
# ==========================================

def go_home():
    st.session_state.screen = "home"


# ==========================================
# 세션 초기화
# ==========================================

if "screen" not in st.session_state:
    st.session_state.screen = "home"


# ==========================================
# 디자인
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f3f6f4;
    }

    .title {
        text-align: center;
        color: #173d2b;
        font-size: 50px;
        font-weight: 800;
        margin-top: 20px;
    }

    .subtitle {
        text-align: center;
        color: #66756d;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .game-title {
        text-align: center;
        color: #173d2b;
        font-size: 40px;
        font-weight: 800;
    }

    .board {
        width: min(92vw, 600px);
        height: min(92vw, 600px);

        margin: 20px auto;

        background-color: #168447;

        border: 8px solid #084d29;

        border-radius: 10px;

        padding: 3px;

        display: grid;

        grid-template-columns: repeat(8, 1fr);
        grid-template-rows: repeat(8, 1fr);

        gap: 2px;

        box-shadow:
            0 8px 20px rgba(0,0,0,0.25);
    }

    .cell {
        background-color: #1c9950;

        display: flex;

        align-items: center;
        justify-content: center;

        border: 1px solid #11723b;
    }

    .black-stone {
        width: 75%;
        height: 75%;

        border-radius: 50%;

        background:
            radial-gradient(
                circle at 30% 25%,
                #555,
                #222 50%,
                #000
            );

        box-shadow:
            2px 4px 6px rgba(0,0,0,0.5);
    }

    .white-stone {
        width: 75%;
        height: 75%;

        border-radius: 50%;

        background:
            radial-gradient(
                circle at 30% 25%,
                #ffffff,
                #eeeeee 55%,
                #bbbbbb
            );

        box-shadow:
            2px 4px 6px rgba(0,0,0,0.4);
    }

    .hint {
        width: 25%;
        height: 25%;

        border-radius: 50%;

        background-color: #f6d743;

        box-shadow:
            0 0 8px #fff000;
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
        """
        <div class="title">
            ⚫ 오셀로 ⚪
        </div>

        <div class="subtitle">
            돌을 놓고 상대의 돌을 뒤집어 보세요!
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background:white;
            padding:30px;
            border-radius:20px;
            text-align:center;
            box-shadow:0 5px 20px rgba(0,0,0,0.08);
        ">

            <div style="
                font-size:70px;
                margin-bottom:10px;
            ">
                ⚫ ⚪
            </div>

            <h2 style="color:#173d2b;">
                게임을 시작하세요
            </h2>

            <p style="color:#777;">
                게임 방식을 선택하세요.
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
            use_container_width=True,
            type="primary"
        ):
            start_game("ai")
            st.rerun()

    with col2:

        if st.button(
            "👥 친구와 하기",
            use_container_width=True,
            type="primary"
        ):
            start_game("friend")
            st.rerun()

    st.write("")

    st.info(
        "⚫ 흑돌이 먼저 시작합니다. "
        "노란색 점이 있는 곳에 돌을 놓을 수 있습니다."
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
        '<div class="game-title">⚫ 오셀로 ⚪</div>',
        unsafe_allow_html=True
    )

    # 점수
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("⚫ 흑", black)

    with col2:

        if turn == BLACK:
            st.metric("현재 차례", "⚫ 흑")
        else:
            st.metric("현재 차례", "⚪ 백")

    with col3:
        st.metric("⚪ 백", white)

    # 게임 방식
    if mode == "ai":
        st.caption("🤖 AI와 하기")
    else:
        st.caption("👥 친구와 하기")

    # ======================================
    # 게임 종료 확인
    # ======================================

    black_moves = valid_moves(
        board,
        BLACK
    )

    white_moves = valid_moves(
        board,
        WHITE
    )

    if not black_moves and not white_moves:
        st.session_state.game_over = True

    # ======================================
    # 게임 종료
    # ======================================

    if st.session_state.game_over:

        if black > white:
            result = "🎉 흑돌 승리!"
        elif white > black:
            result = "🎉 백돌 승리!"
        else:
            result = "🤝 무승부!"

        st.success(
            f"{result}  최종 점수: ⚫ {black} : {white} ⚪"
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

        st.info("🤖 AI가 생각하고 있습니다...")

        moves = valid_moves(
            board,
            WHITE
        )

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

            st.rerun()

        else:

            st.session_state.turn = BLACK

            st.rerun()

    # ======================================
    # 플레이어 차례
    # ======================================

    else:

        moves = valid_moves(
            board,
            turn
        )

        # 놓을 곳이 없는 경우
        if not moves:

            if turn == BLACK:
                st.warning(
                    "⚫ 흑돌은 놓을 수 있는 곳이 없습니다."
                )
            else:
                st.warning(
                    "⚪ 백돌은 놓을 수 있는 곳이 없습니다."
                )

            st.session_state.turn = opponent(turn)

            st.rerun()

        # 현재 차례
        if turn == BLACK:
            st.info("⚫ 흑돌의 차례입니다.")
        else:
            st.info("⚪ 백돌의 차례입니다.")

        # ==================================
        # 초록색 오셀로 판
        # ==================================

        st.markdown(
            '<div class="board">',
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
                        '<div class="black-stone"></div>',
                        unsafe_allow_html=True
                    )

                elif board[row][col] == WHITE:

                    st.markdown(
                        '<div class="white-stone"></div>',
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
            '</div>',
            unsafe_allow_html=True
        )

        # ==================================
        # 착수 버튼
        # ==================================

        st.markdown(
            "### 🟡 놓을 위치를 선택하세요"
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
                        label = "·"

                    if st.button(
                        label,
                        key=f"cell_{row}_{col}",
                        disabled=(row, col) not in moves,
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
            "🏠 처음으로",
            use_container_width=True
        ):
            go_home()
            st.rerun()
