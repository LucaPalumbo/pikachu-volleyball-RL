import asyncio
import websockets
import json
import numpy as np
from rl_model import RLModel

# Carica i due modelli
model_right = RLModel.load("src/AI/ppo_pikavolley_iter")
model_left = RLModel.load("src/AI/ppo_pikavolley_iter")
model_right.is_on_right = True
model_left.is_on_right = False


async def handle_client(websocket):
    print("🔌 Client connected")
    old_state = None

    try:
        async for message in websocket:
            state = json.loads(message)
            obs = np.array([
                state["player1X"],
                state["player1Y"],
                state["player1Yvelocity"],
                state["player1State"],
                state["player1DivingDirection"],
                state["player1LyingDownDurationLeft"],
                state["player2X"],
                state["player2Y"],
                state["player2Yvelocity"],
                state["player2State"],
                state["player2DivingDirection"],
                state["player2LyingDownDurationLeft"],
                state["ballX"],
                state["ballY"],
                state["ballXvelocity"],
                state["ballYvelocity"],
                float(state["isPowerHit"]),
            ])

            action_1 = np.array([1, 1, 0])  # Default action (stay)
            action_2 = np.array([1, 1, 0])  # Default action (stay)
            # Predizione dell'azione
            if state["player1IsComputer"]:
                action_1, _ = model_left.predict(obs, deterministic=False)
            if state["player2IsComputer"]:
                action_2, _ = model_right.predict(obs, deterministic=False)

            response = {
                1: {
                    "xDirection": float(action_1[0])-1,
                    "yDirection": float(action_1[1])-1,
                    "powerHit": bool(action_1[2])

                },
                2: {
                    "xDirection": float(action_2[0])-1,
                    "yDirection": float(action_2[1])-1,
                    "powerHit": bool(action_2[2])
                }
            }

            print("📤 Response sent:", response)
            await websocket.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed:
        print("❌ Connection closed")

# Start the server on ws://localhost:5000
async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 5000):
        print("🟢 WebSocket server listening on ws://localhost:5000")
        await asyncio.Future() 

if __name__ == "__main__":
    asyncio.run(main())
