import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Jump Hero", layout="centered")

st.title("🏃 Jump Hero")

st.markdown("Press **Spacebar** to jump. Avoid obstacles. Game gets faster as you score more!")

# Initialize leaderboard in session
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# Input for player name
player_name = st.text_input("Enter your name to play:", max_chars=12)

if player_name:
    st.success(f"Welcome, {player_name}! Press space to start jumping!")
    
    components.html(f"""
    <html>
    <head>
    <style>
    canvas {{ background: #e6f2ff; display: block; margin: auto; border: 2px solid black; }}
    </style>
    </head>
    <body>
    <canvas id="gameCanvas" width="600" height="200"></canvas>
    <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let player = {{ x: 50, y: 150, width: 30, height: 30, dy: 0, jumping: false }};
    let gravity = 1.5;
    let speed = 5;
    let score = 0;
    let level = 1;

    let obstacle = {{ x: 600, y: 150, width: 30, height: 30, dx: -speed }};
    let gameOver = false;

    document.addEventListener("keydown", function(e) {{
      if (e.code === "Space" && !player.jumping) {{
        player.dy = -20;
        player.jumping = true;
      }}
    }});

    function loop() {{
      if (gameOver) return;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Player physics
      player.y += player.dy;
      player.dy += gravity;
      if (player.y >= 150) {{
        player.y = 150;
        player.dy = 0;
        player.jumping = false;
      }}

      // Draw player
      ctx.fillStyle = "#4CAF50";
      ctx.fillRect(player.x, player.y, player.width, player.height);

      // Draw obstacle
      ctx.fillStyle = "crimson";
      ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
      obstacle.x += obstacle.dx;

      if (obstacle.x < -obstacle.width) {{
        score++;
        level = Math.floor(score / 5) + 1;
        speed += 0.5;
        obstacle.x = 600 + Math.random() * 200;
        obstacle.width = 30 - Math.min(score, 15); // smaller obstacles = tougher
      }}

      // Collision check
      if (
        player.x < obstacle.x + obstacle.width &&
        player.x + player.width > obstacle.x &&
        player.y < obstacle.y + obstacle.height &&
        player.y + player.height > obstacle.y
      ) {{
        gameOver = true;
        ctx.fillStyle = "black";
        ctx.font = "24px Arial";
        ctx.fillText("Game Over!", 230, 90);
        ctx.fillText("Score: " + score, 250, 120);
        window.parent.postMessage(score, "*");  // Send score to Streamlit
        return;
      }}

      // UI
      ctx.fillStyle = "black";
      ctx.font = "16px Arial";
      ctx.fillText("Score: " + score, 10, 20);
      ctx.fillText("Level: " + level, 520, 20);

      requestAnimationFrame(loop);
    }}

    loop();
    </script>
    </body>
    </html>
    """, height=240)

    # JavaScript sends score to Streamlit
    score_holder = st.empty()

    components.html("""
    <script>
    window.addEventListener("message", (event) => {
      const score = event.data;
      const streamlitDoc = window.parent.document;
      const inputEl = streamlitDoc.querySelector('input[data-testid="stTextInput"]');
      if (inputEl) {{
        inputEl.value = score;
        inputEl.dispatchEvent(new Event("input", {{ bubbles: true }}));
      }}
    });
    </script>
    """, height=0)

    score_input = st.text_input("Hidden Score Receiver", key="score_receiver")

    # Update leaderboard
    if score_input.isnumeric():
        score_val = int(score_input)
        st.session_state.leaderboard.append((player_name, score_val))
        st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x[1], reverse=True)[:5]
        st.experimental_rerun()

# Show leaderboard
st.markdown("---")
st.subheader("🏆 Leaderboard (Top 5)")
if st.session_state.leaderboard:
    for i, (name, scr) in enumerate(st.session_state.leaderboard, start=1):
        st.markdown(f"**{i}. {name}** – {scr} points")
else:
    st.write("No scores yet. Be the first to play!")
