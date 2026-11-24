
from flask import Flask, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Space Dodger</title>

    <style>
        body {
            background: #101025;
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
        }

        h1 {
            color: #00ffcc;
            font-size: 36px;
        }

        canvas {
            background: #202040;
            border: 3px solid cyan;
        }

        button {
            padding: 12px 25px;
            background: cyan;
            border: none;
            cursor: pointer;
            font-size: 17px;
            border-radius: 8px;
        }
    </style>
</head>

<body>

<h1>🚀 SPACE DODGER</h1>

<p>Use LEFT and RIGHT arrow keys to dodge!</p>

<h2>Score: <span id="score">0</span></h2>

<canvas id="game" width="400" height="400"></canvas>

<p>
    <button onclick="startGame()">Start Game</button>
</p>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let player, obstacles, score, running;
let keys = {};

document.addEventListener("keydown", e => {
    keys[e.key] = true;
});

document.addEventListener("keyup", e => {
    keys[e.key] = false;
});

function startGame() {

    player = {
        x: 180,
        y: 340,
        size: 25
    };

    obstacles = [];
    score = 0;
    running = true;

    document.getElementById("score").textContent = score;

    draw();
}

function draw() {

    if (!running) return;

    ctx.clearRect(0, 0, 400, 400);

    // Player movement
    if (keys["ArrowLeft"]) {
        player.x -= 5;
    }

    if (keys["ArrowRight"]) {
        player.x += 5;
    }

    player.x = Math.max(0, Math.min(375, player.x));

    // Draw player
    ctx.fillStyle = "cyan";
    ctx.fillRect(player.x, player.y, 25, 25);

    // Create obstacles
    if (Math.random() < 0.025) {

        obstacles.push({
            x: Math.random() * 370,
            y: -20,
            size: 20
        });

    }

    // Move and draw obstacles
    ctx.fillStyle = "red";

    for (let i = obstacles.length - 1; i >= 0; i--) {

        let o = obstacles[i];

        o.y += 3;

        ctx.fillRect(o.x, o.y, o.size, o.size);

        // Check collision
        if (
            player.x < o.x + o.size &&
            player.x + player.size > o.x &&
            player.y < o.y + o.size &&
            player.y + player.size > o.y
        ) {

            running = false;

            ctx.fillStyle = "white";
            ctx.font = "28px Arial";
            ctx.fillText("GAME OVER!", 115, 200);

            return;
        }

        // Increase score
        if (o.y > 400) {

            obstacles.splice(i, 1);

            score++;

            document.getElementById("score").textContent = score;

        }

    }

    requestAnimationFrame(draw);

}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)


if __name__ == "__main__":
    app.run(debug=True)
