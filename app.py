import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Jump Game", layout="centered")

st.title("🏃 Jumping Game in Streamlit")

st.markdown("Click inside the game area and press **Spacebar** to jump over obstacles.")

# Embed the game using HTML Canvas + JS
components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  canvas { background: #d0f0f7; display: block; margin: auto; border: 2px solid black; }
</style>
</head>
<body>
<canvas id="gameCanvas" width="600" height="200"></canvas>
<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let player = { x: 50, y: 150, width: 30, height: 30, dy: 0, jumping: false };
let gravity = 1.5;
let obstacle = { x: 600, y: 150, width: 30, height: 30, dx: -5 };
let score = 0;
let gameOver = false;

document.addEventListener("keydown", function(e) {
  if (e.code === "Space" && !player.jumping) {
    player.dy = -20;
    player.jumping = true;
  }
});

function resetGame() {
  obstacle.x = 600;
  player.y = 150;
  player.dy = 0;
  player.jumping = false;
  score = 0;
  gameOver = false;
  loop();
}

function loop() {
  if (gameOver) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw player
  ctx.fillStyle = "green";
  ctx.fillRect(player.x, player.y, player.width, player.height);

  // Player physics
  player.y += player.dy;
  player.dy += gravity;
  if (player.y >= 150) {
    player.y = 150;
    player.dy = 0;
    player.jumping = false;
  }

  // Draw obstacle
  ctx.fillStyle = "red";
  ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);

  obstacle.x += obstacle.dx;
  if (obstacle.x < -30) {
    obstacle.x = 600 + Math.random() * 200;
    score++;
  }

  // Collision detection
  if (
    player.x < obstacle.x + obstacle.width &&
    player.x + player.width > obstacle.x &&
    player.y < obstacle.y + obstacle.height &&
    player.y + player.height > obstacle.y
  ) {
    gameOver = true;
    ctx.fillStyle = "black";
    ctx.font = "30px Arial";
    ctx.fillText("Game Over!", 220, 100);
    ctx.font = "20px Arial";
    ctx.fillText("Score: " + score, 260, 130);
    ctx.fillText("Refresh to Restart", 210, 160);
    return;
  }

  // Draw score
  ctx.fillStyle = "black";
  ctx.font = "16px Arial";
  ctx.fillText("Score: " + score, 10, 20);

  requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
""", height=240)
