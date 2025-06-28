# streamlit_app.py
import streamlit as st
from code.mangala_engine import MangalaGame
from code.ai.kazanmaster_ai import KazanMasterAI

st.set_page_config(page_title="MANGALA AI", layout="centered")

# Session state setup
if "game" not in st.session_state:
    st.session_state.game = MangalaGame()
    st.session_state.message = "Your turn. Choose a pit to move."

game = st.session_state.game
ai = KazanMasterAI(max_depth=5)

st.title("🧠 KazanMaster: Play Mangala vs AI")

# Function to render the board
def render_board():
    board = game.board

    st.write(f"**Player 1 Kazan:** `{board[13]}`")

    # Top row (Player 1 pits 12 to 7)
    top_row = st.columns(6)
    for i, col in zip(range(12, 6, -1), top_row):
        col.markdown(f"**{i}**")
        col.button(f"{board[i]}", key=f"p1_{i}", disabled=True)

    # Bottom row (Player 0 pits 0 to 5)
    bottom_row = st.columns(6)
    for i, col in zip(range(0, 6), bottom_row):
        col.markdown(f"**{i}**")
        if game.board[i] > 0 and game.current_player == 0:
            if col.button(f"{board[i]}", key=f"p0_{i}"):
                retained = game.make_move(i)
                st.session_state.message = f"You played pit {i}."

                # Let AI play as long as it retains turn
                while not game.is_game_over() and game.current_player == 1:
                    ai_move = ai.get_best_move(game)
                    retained = game.make_move(ai_move)
                    st.session_state.message += f"\nAI played pit {ai_move}."
                    if not retained:
                        break

                st.rerun()  # <-- Refresh the app to show updated board

        else:
            col.button(f"{board[i]}", key=f"p0_{i}", disabled=True)

    st.write(f"**Player 0 Kazan:** `{board[6]}`")

# Display current board
render_board()
st.divider()
st.info(st.session_state.message)

# Check for game end
if game.is_game_over():
    game.end_game()
    p0_score = game.board[6]
    p1_score = game.board[13]
    if p0_score > p1_score:
        result = "🏆 You win!"
    elif p0_score < p1_score:
        result = "💀 AI wins!"
    else:
        result = "🤝 Draw!"
    st.success(f"Game Over!\n\n**Final Score** — You: {p0_score}, AI: {p1_score}\n\n{result}")

# Reset button
if st.button("🔄 Restart Game"):
    st.session_state.game = MangalaGame()
    st.session_state.message = "New game started!"
    st.experimental_rerun()
