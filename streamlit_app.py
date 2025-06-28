import streamlit as st
import pyttsx3
from code.mangala_engine import MangalaGame
from code.ai.kazanmaster_ai import KazanMasterAI

st.set_page_config(page_title="Rigged 1v1 Mangala", layout="centered")

# Initialize session state
if "game" not in st.session_state:
    st.session_state.game = MangalaGame()
    st.session_state.message = "Player 0's turn."
    st.session_state.current_player = 0
    st.session_state.last_moves = []

# AI helper (used secretly for one side)
ai = KazanMasterAI(max_depth=5)
engine = pyttsx3.init()

# Function to speak moves
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Game object
game = st.session_state.game

st.title("🎭 Rigged 1v1 Mode: One Side is Assisted")

# Kazans
st.markdown(f"### 🧍 Player 0 Kazan: `{game.board[6]}`")
st.markdown(f"### 🧠 Player 1 Kazan: `{game.board[13]}`")

# Player 1 row (12–7)
top = st.columns(6)
for i, col in zip(range(12, 6, -1), top):
    col.markdown(f"⬇️ **{i}**")
    col.button(f"{game.board[i]}", disabled=True, key=f"ai_{i}")

# Player 0 row (0–5)
bottom = st.columns(6)
for i, col in zip(range(0, 6), bottom):
    col.markdown(f"⬆️ **{i}**")
    if game.current_player == 0 and game.board[i] > 0:
        if col.button(f"{game.board[i]}", key=f"p0_{i}"):
            retained = game.make_move(i)
            st.session_state.last_moves.append((0, i))
            st.session_state.current_player = 0 if retained else 1
            st.rerun()
    elif game.current_player == 1 and game.board[i] > 0:
        if col.button(f"{game.board[i]}", key=f"p1_{i}"):
            retained = game.make_move(i)
            st.session_state.last_moves.append((1, i))
            st.session_state.current_player = 1 if retained else 0
            st.rerun()
    else:
        col.button(f"{game.board[i]}", disabled=True, key=f"p0_{i}_d")

# Suggest best move for P1 using AI
if game.current_player == 1:
    best_move = ai.get_best_move(game)
    st.warning(f"🤖 (Rigged Helper): Player 1 should play pit {best_move}.")
    speak(f"Player one should play pit {best_move}")

# Show last move info
if st.session_state.last_moves:
    last = st.session_state.last_moves[-1]
    st.info(f"Last move — Player {last[0]} played pit {last[1]}")

# Game Over
if game.is_game_over():
    game.end_game()
    p0_score = game.board[6]
    p1_score = game.board[13]
    result = "🏆 Player 0 wins!" if p0_score > p1_score else "🏆 Player 1 wins!" if p1_score > p0_score else "🤝 Draw!"
    st.success(f"Game Over! Final score: P0 = {p0_score}, P1 = {p1_score}\n\n{result}")

# Restart button
if st.button("🔄 Restart Game"):
    st.session_state.clear()
    st.rerun()
