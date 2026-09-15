import streamlit as st
import random

BOARD_SIZE = 8

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

EMPTY = 0
BLACK = 1
WHITE = 2


def create_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE

    return board


def opponent(player):
    return WHITE if player == BLACK else BLACK


def is_inside(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def get_flips(board, row, col, player):
    if not is_inside(row, col) or board[row][col] != EMPTY:
        return []

    other = opponent(player)
    flips = []

    for dr, dc in DIRECTIONS:
        r = row + dr
        c = col + dc
        direction_flips = []

        while is_inside(r, c) and board[r][c] == other:
            direction_flips.append((r, c))
            r += dr
            c += dc

        if (
            direction_flips
            and is_inside(r, c)
            and board[r][c] == player
        ):
            flips.extend(direction_flips)

    return flips


def get_valid_moves(board, player):
    moves = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
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
    black = sum(row.count(BLACK) for row in board)
    white = sum(row.count(WHITE) for row in board)

    return black, white


def game_over(board):
    return (
        not get_valid_moves(board, BLACK)
        and not get_valid_moves(board, WHITE)
    )


def computer_move(board):
    moves = get_valid_moves(board, WHITE)

    if not moves:
        return None

    # 기본 AI:
    # 뒤집을 수 있는 돌이 많은 수를 우선 선택
    candidates = []

    for row, col in moves:
        flips = len(get_flips(board, row, col, WHITE))

        # 모서리는 매우 유리하므로 높은 점수 부여
        corner_bonus = 0

        if (row, col) in [
            (0, 0),
            (0, 7),
            (7, 0),
            (7, 7)
        ]:
            corner_bonus = 100

        score = flips + corner_bonus
        candidates.append(((row, col), score))

    best_score = max(score for _, score in candidates)

    best_moves = [
        move for move, score in candidates
        if score == best_score
    ]

    return random.choice(best_moves)


def reset_game():
    st.session_state.board = create_board()
    st.session_state.current_player = BLACK
    st.session_state.game_finished = False
    st.session_state.message = "당신의 차례입니다."


def board_to_html(board, valid_moves):
    html = """
    <style>
        .board {
            width: min(90vw, 640px);
            margin: auto;
            background: #145a32;
            border: 5px solid #0b3d24;
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 2px;
            padding: 2px;
        }

        .cell {
            aspect-ratio: 1 / 1;
            background: #1e8449;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .stone {
            width: 72%;
            height: 72%;
            border-radius: 50%;
        }

        .black {
            background: radial-gradient(circle at 30% 30%, #555, #000);
            box-shadow: 2px 3px 5px rgba(0,0,0,0.5);
        }

        .white {
            background: radial-gradient(circle at 30% 30%, #fff, #bbb);
            box-shadow: 2px 3px 5px rgba(0,0,0,0.5);
        }

        .hint {
            width: 25%;
            height: 25%;
            border-radius: 50%;
            background: #f4d03f;
            opacity: 0.9;
        }
    </style>

    <div class="board">
    """

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            html += '<div class="cell">'

            if board[row][col] == BLACK:
                html += '<div class="stone black"></div>'

            elif board[row][col] == WHITE:
                html += '<div class="stone white"></div>'

            elif (row, col) in valid_moves:
                html += '<div class="hint"></div>'

            html += "</div>"

    html += "</div>"

    return html


# -----------------------------
# Streamlit 설정
# -----------------------------

st.set_page_config(
    page_title="오셀로 게임",
    page_icon="⚫",
    layout="centered"
)

st.title("⚫ 오셀로 게임")
st.caption("사람(흑) vs 컴퓨터(백)")

# 세션 초기화
if "board" not in st.session_state:
    reset_game()


# -----------------------------
# 사이드바
# -----------------------------

with st.sidebar:
    st.header("게임 정보")

    black, white = count_stones(st.session_state.board)

    st.metric("⚫ 흑돌", black)
    st.metric("⚪ 백돌", white)

    st.divider()

    if st.button("🔄 새 게임", use_container_width=True):
        reset_game()
        st.rerun()

    st.divider()

    st.write("### 게임 방법")
    st.write(
        """
        1. 흑돌이 먼저 시작합니다.
        2. 노란 점이 표시된 곳에 돌을 놓을 수 있습니다.
        3. 상대 돌을 자신의 돌 사이에 끼우면 뒤집을 수 있습니다.
        4. 더 이상 놓을 곳이 없으면 상대방 차례로 넘어갑니다.
        5. 게임 종료 후 돌이 많은 사람이 승리합니다.
        """
    )


# -----------------------------
# 게임 상태
# -----------------------------

board = st.session_state.board
current_player = st.session_state.current_player

valid_moves = get_valid_moves(board, current_player)


# -----------------------------
# 컴퓨터 차례
# -----------------------------

if (
    current_player == WHITE
    and not st.session_state.game_finished
):
    if valid_moves:
        move = computer_move(board)

        if move:
            make_move(
                board,
                move[0],
                move[1],
                WHITE
            )

        st.session_state.current_player = BLACK
        st.session_state.message = "당신의 차례입니다."

        st.rerun()

    else:
        st.session_state.current_player = BLACK
        st.session_state.message = "컴퓨터는 놓을 곳이 없습니다. 당신의 차례입니다."
        st.rerun()


# -----------------------------
# 패스 처리
# -----------------------------

if not valid_moves and not st.session_state.game_finished:

    other_moves = get_valid_moves(
        board,
        opponent(current_player)
    )

    if other_moves:
        if current_player == BLACK:
            st.session_state.current_player = WHITE
            st.session_state.message = "놓을 곳이 없습니다. 컴퓨터의 차례입니다."
        else:
            st.session_state.current_player = BLACK
            st.session_state.message = "컴퓨터가 놓을 곳이 없습니다. 당신의 차례입니다."

        st.rerun()


# -----------------------------
# 게임 종료
# -----------------------------

if game_over(board):
    st.session_state.game_finished = True

    black, white = count_stones(board)

    if black > white:
        st.session_state.message = "🎉 당신의 승리입니다!"
    elif white > black:
        st.session_state.message = "🤖 컴퓨터의 승리입니다!"
    else:
        st.session_state.message = "🤝 무승부입니다!"


# -----------------------------
# 상태 표시
# -----------------------------

black, white = count_stones(board)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("⚫ 당신", black)

with col2:
    st.metric("현재", "당신" if current_player == BLACK else "컴퓨터")

with col3:
    st.metric("⚪ 컴퓨터", white)


st.info(st.session_state.message)


# -----------------------------
# 보드 표시
# -----------------------------

if not st.session_state.game_finished:
    valid_moves = get_valid_moves(
        board,
        st.session_state.current_player
    )
else:
    valid_moves = []

st.markdown(
    board_to_html(board, valid_moves),
    unsafe_allow_html=True
)


# -----------------------------
# 플레이어 입력
# -----------------------------

if (
    current_player == BLACK
    and not st.session_state.game_finished
):

    st.write("### 놓을 위치를 선택하세요")

    for row in range(BOARD_SIZE):
        cols = st.columns(8)

        for col in range(BOARD_SIZE):
            with cols[col]:

                cell = board[row][col]

                if cell == BLACK:
                    label = "⚫"

                elif cell == WHITE:
                    label = "⚪"

                elif (row, col) in valid_moves:
                    label = "🟡"

                else:
                    label = "·"

                disabled = (row, col) not in valid_moves

                if st.button(
                    label,
                    key=f"cell_{row}_{col}",
                    disabled=disabled,
                    use_container_width=True
                ):
                    make_move(
                        board,
                        row,
                        col,
                        BLACK
                    )

                    st.session_state.current_player = WHITE
                    st.session_state.message = "컴퓨터가 생각 중입니다..."

                    st.rerun()


# -----------------------------
# 종료 메시지
# -----------------------------

if st.session_state.game_finished:
    st.success(st.session_state.message)

    if black > white:
        st.balloons()
