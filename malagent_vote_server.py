from flask import Flask, request
from flask_socketio import SocketIO
import random
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

start_time = None
responses = {}

player_names = [
    "Falcon","Tiger","Lion","Eagle","Shark","Panther",
    "Wolf","Cobra","Dragon","Leopard","Hawk","Viper"
]


@app.route("/")
def home():

    name = random.choice(player_names) + "-" + str(random.randint(10,99))

    buttons = ""

    for i in range(20):
        buttons += f"""
        <button class="node" id="b{i}" onclick="toggle({i})">{i}</button>
        """

    return f"""
<html>

<head>

<script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>

<style>

.grid {{
display:grid;
grid-template-columns: repeat(5,80px);
gap:15px;
justify-content:center;
margin-top:40px;
}}

.node {{
font-size:20px;
width:70px;
height:70px;
border-radius:50%;
border:none;
background:#4da6ff;
color:white;
cursor:pointer;
}}

.selected {{
background:#2ecc71;
}}

</style>

</head>

<body style="font-family:Arial;text-align:center;margin-top:40px">

<h2>Identify the Malicious Agents</h2>

<h3>{name}</h3>

<h3 id="status">Waiting for simulation to start...</h3>

<div class="grid">
{buttons}
</div>

<br>

<button onclick="submit_vote()" style="font-size:20px;padding:10px 20px">
Submit Answer
</button>

<h3 id="answer"></h3>

<script>

const socket = io()

let selected = []
let locked = false
let player = "{name}"

socket.on("start_signal", function(){{

alert("Simulation Started!")

document.getElementById("status").innerText =
"Select up to 4 malicious nodes"

}})

function toggle(i){{

if(locked) return

let idx = selected.indexOf(i)

if(idx >= 0){{
selected.splice(idx,1)
document.getElementById("b"+i).classList.remove("selected")
return
}}

if(selected.length >= 4){{
alert("Maximum 4 selections allowed")
return
}}

selected.push(i)
document.getElementById("b"+i).classList.add("selected")

}}

function submit_vote(){{

if(locked) return

fetch("/vote",{{
method:"POST",
headers:{{"Content-Type":"application/json"}},
body:JSON.stringify({{
player:player,
answer:selected
}})
}})

locked = true

document.getElementById("answer").innerText =
"You selected: " + selected.join(", ")

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

    data = request.json
    player = data["player"]
    answer = data["answer"]

    if player in responses:
        return {"status":"locked"}

    elapsed = time.time() - start_time

    responses[player] = {
        "answer": answer,
        "time": elapsed
    }

    print(player, "->", answer, "time:", round(elapsed,2), "seconds")

    return {"status":"recorded"}


@app.route("/results")
def results():
    return responses


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)