from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import random
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

responses = {}
start_time = None

player_names = [
    "Falcon","Tiger","Lion","Eagle","Shark","Panther",
    "Wolf","Cobra","Dragon","Leopard","Hawk","Viper"
]


@app.route("/")
def home():

    name = random.choice(player_names) + "-" + str(random.randint(10,99))

    return f"""
<html>

<head>
<script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>
</head>

<body style="font-family:Arial;text-align:center;margin-top:50px">

<h2>Guess the Number of Clusters</h2>

<h3>{name}</h3>

<h3 id="status">Waiting for simulation to start...</h3>

<div style="margin-top:40px">

<button id="b1" onclick="vote(1)" style="font-size:30px;margin:10px">1</button>
<button id="b2" onclick="vote(2)" style="font-size:30px;margin:10px">2</button>
<button id="b3" onclick="vote(3)" style="font-size:30px;margin:10px">3</button>
<button id="b4" onclick="vote(4)" style="font-size:30px;margin:10px">4</button>

</div>

<h3 id="answer"></h3>

<script>

let locked = false
let player = "{name}"

const socket = io()

socket.on("start_signal", function(){{
    alert("Simulation Started!")
    document.getElementById("status").innerText =
        "Submit your answer now"
}})

function vote(ans){{

    if(locked) return

    fetch("/vote",{{
        method:"POST",
        headers:{{"Content-Type":"application/json"}},
        body:JSON.stringify({{
            player:player,
            answer:ans
        }})
    }})

    locked = true

    let btn = document.getElementById("b"+ans)
    btn.style.backgroundColor = "green"
    btn.style.color = "white"

    document.getElementById("answer").innerText =
        "You selected: " + ans
}}

</script>

</body>
</html>
"""


@app.route("/start", methods=["POST"])
def start():

    global responses, start_time

    responses = {}
    start_time = time.time()

    socketio.emit("start_signal")

    print("Simulation started")

    return {"status":"started"}


@app.route("/vote", methods=["POST"])
def vote():

    global start_time

    data = request.json
    player = data["player"]
    answer = data["answer"]

    if player in responses:
        return {"status":"locked"}

    response_time = time.time() - start_time

    responses[player] = {
        "answer": answer,
        "time": response_time
    }

    print(player, "->", answer, "time:", round(response_time,2), "seconds")

    return {"status":"recorded"}


@app.route("/results")
def results():
    return responses


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)