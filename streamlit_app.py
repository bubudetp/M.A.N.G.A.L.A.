import streamlit as st
from code.mangala_engine import MangalaGame
from code.ai.kazanmaster_ai import KazanMasterAI

st.set_page_config(page_title="MANGALA AI", layout="centered")

# Session state init
if "game" not in st.session_state:
    st.session_state.game = MangalaGame()
    st.session_state.message = "Your turn. Choose a pit to move."
    st.session_state.awaiting_ai = False
    st.session_state.last_ai_move = None
    st.session_state.last_player_move = None

game = st.session_state.game
ai = KazanMasterAI(max_depth=5)

st.title("KazanMaster: Play Mangala vs AI")

# Display game rules
with st.expander("📜 How to Play Mangala"):
    st.markdown("""
- **Objective**: Collect more seeds in your Kazan (store) than your opponent.
- **Your side**: Pits `0` to `5`, your Kazan is at index `6`.
- **AI side**: Pits `7` to `12`, AI’s Kazan is at index `13`.

### 🎯 Turn Rules:
- On your turn, pick a pit from your side (0–5) with seeds.
- Seeds are distributed one by one counterclockwise.
- Skip the opponent’s Kazan during sowing.
- If the last seed lands in **your Kazan**, you get another turn.
- If the last seed lands in **your empty pit** on your side, and the opposite pit has seeds, **capture** both into your Kazan.

### 🏁 End of Game:
- The game ends when all pits on one side are empty.
- Remaining seeds go to the opponent’s Kazan.
- The player with the most seeds in their Kazan **wins**.
""")

# Render Kazan for AI
st.markdown(f"### AI Kazan (P1): `{game.board[13]}`")

# Top row (AI pits 12–7)
top_row = st.columns(6)
for i, col in zip(range(12, 6, -1), top_row):
    col.markdown(f"⬇️ **{i}**")
    col.button(f"🟪 {game.board[i]}", key=f"ai_{i}", disabled=True)

# Bottom row (Player pits 0–5)
bottom_row = st.columns(6)
for i, col in zip(range(0, 6), bottom_row):
    col.markdown(f"⬆️ **{i}**")
    if game.current_player == 0 and game.board[i] > 0:
        if col.button(f"🟩 {game.board[i]}", key=f"p0_{i}"):
            player_retains_turn = game.make_move(i)
            st.session_state.last_player_move = i
            st.session_state.last_ai_move = None
            st.session_state.awaiting_ai = not player_retains_turn  # AI plays only if player doesn't retain turn
            st.rerun()
    else:
        col.button(f"🟩 {game.board[i]}", key=f"p0_{i}", disabled=True)

# Render Kazan for player
st.markdown(f"### 🧍 Your Kazan (P0): `{game.board[6]}`")

# Perform AI move if needed
if game.current_player == 1 and st.session_state.awaiting_ai and not game.is_game_over():
    ai_move = ai.get_best_move(game)
    ai_retains_turn = game.make_move(ai_move)
    st.session_state.last_ai_move = ai_move
    st.session_state.awaiting_ai = ai_retains_turn  # AI continues only if it retains turn
    st.rerun()

# Message display
msg = ""
if st.session_state.last_player_move is not None:
    msg += f"🟩 You played pit {st.session_state.last_player_move}.  "
if st.session_state.last_ai_move is not None:
    msg += f"🟪 AI played pit {st.session_state.last_ai_move}."
st.divider()
st.info(msg or st.session_state.message)

# Game Over
if game.is_game_over():
    game.end_game()
    p0_score = game.board[6]
    p1_score = game.board[13]
    result = "🏆 You win!" if p0_score > p1_score else "💀 AI wins!" if p1_score > p0_score else "🤝 Draw!"
    st.success(f"**Game Over!** Final Score — You: `{p0_score}` | AI: `{p1_score}`\n\n{result}")

# Restart
if st.button("🔄 Restart Game"):
    st.session_state.clear()
    st.experimental_rerun()
