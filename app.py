import streamlit as st
import random

# ==========================================
# 기본 설정
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
# 보드 생성
# ==========================================

def create_board():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]

    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE

    return board


# ==========================================
# 상대방
# ==========================================

def opponent(player):
    return WHITE if player == BLACK else BLACK


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
# 가능한 착수 위치
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
# 점수
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

    moves = valid_moves(board, WHITE)

    if not moves:
        return None

    corners = [
        (0, 0),
        (0, 7),
        (7, 0),
        (7, 7)
    ]

    best_score = -9999
    best_moves = []

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

        # 모서리 우선
        if move in corners:
            score += 1000

        # 가장자리 보너스
        if row == 0 or row == 7:
            score += 20

        if col == 0 or col == 7:
            score += 20

        if score > best_score:
            best_score = score
            best_moves = [move]

        elif score == best_score:
            best_moves.append(move)

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
# 처음 화면
# ==========================================

def go_home():
    st.session_state.screen = "home"


# ==========================================
# 세션 초기화
# ==========================================

if "screen" not in st.session_state:
    st.session_state.screen = "home"


# ==========================================
# 화면 디자인
# ==========================================

st.markdown(
    """
<style>
div.stButton > button {
    border-radius: 10px;
    font-weight: bold;
}

div.stButton > button[kind="primary"] {
    background-color: #167a3f;
}
</style>
""",
    unsafe_allow_html=True
)


# ==========================================
# 시작 화면
# ==========================================

if st.session_state.screen == "home":

    st.title("⚫ 오셀로 ⚪")

    st.write(
        "상대방의 돌을 사이에 끼워 뒤집는 게임입니다."
    )

    st.divider()

    st.subheader("🎮 게임을 시작하세요")

    st.write(
        "원하는 게임 방식을 선택해주세요."
    )

    st.write("")

    # AI 게임
    if st.button(
        "🤖 AI와 하기",
        type="primary",
        use_container_width=True
    ):
        start_game("ai")
        st.rerun()

    st.write("")

    # 친구 게임
    if st.button(
        "👥 친구와 하기",
        type="primary",
        use_container_width=True
    ):
        start_game("friend")
        st.rerun()

    st.write("")
    st.info(
        "⚫ 흑돌이 먼저 시작합니다."
    )


# ==========================================
# 게임 화면
# ==========================================

else:

    board = st.session_state.board
    turn = st.session_state.turn
    mode = st.session_state.mode

    black, white = count_stones(board)

    st.title("⚫ 오셀로 ⚪")

    # 점수
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("⚫ 흑돌", black)

    with col2:
        if turn == BLACK:
            st.metric("차례", "⚫ 흑")
        else:
            st.metric("차례", "⚪ 백")

    with col3:
        st.metric("⚪ 백돌", white)

    if mode == "ai":
        st.caption("🤖 AI와 하기")
    else:
        st.caption("👥 친구와 하기")

    st.divider()

    # ======================================
    # 게임 종료 확인
    # ======================================

    black_moves = valid_moves(board, BLACK)
    white_moves = valid_moves(board, WHITE)

    if not black_moves and not white_moves:
        st.session_state.game_over = True

    # ======================================
    # 게임 종료
    # ======================================

    if st.session_state.game_over:

        if black > white:
            st.success("🎉 흑돌 승리!")
        elif white > black:
            st.success("🎉 백돌 승리!")
        else:
            st.success("🤝 무승부!")

        st.write(
            f"최종 점수  ⚫ {black} : {white} ⚪"
        )

        if st.button(
            "🔄 다시 하기",
            use_container_width=True
        ):
            start_game(mode)
            st.rerun()

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
            st.rerun()

        else:

            st.session_state.turn = BLACK
            st.rerun()

    # ======================================
    # 사람 차례
    # ======================================

    else:

        moves = valid_moves(board, turn)

        if not moves:

            if turn == BLACK:
                st.warning(
                    "⚫ 흑돌은 놓을 곳이 없습니다."
                )
            else:
                st.warning(
                    "⚪ 백돌은 놓을 곳이 없습니다."
                )

            st.session_state.turn = opponent(turn)
            st.rerun()

        if turn == BLACK:
            st.info("⚫ 흑돌의 차례입니다.")
        else:
            st.info("⚪ 백돌의 차례입니다.")

        st.subheader("🟢 오셀로 판")

        # ==================================
        # 8 x 8 초록색 판
        # ==================================

        for row in range(8):

            cols = st.columns(8)

            for col in range(8):

                with cols[col]:

                    value = board[row][col]

                    if value == BLACK:
                        text = "⚫"

                    elif value == WHITE:
                        text = "⚪"

                    elif (row, col) in moves:
                        text = "🟡"

                    else:
                        text = "🟩"

                    if st.button(
                        text,
                        key=f"cell_{row}_{col}",
                        use_container_width=True,
                        disabled=(row, col) not in moves
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
            "🔄 다시 시작",
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
