import asyncio
import websockets
import json
from game_logic import Game

game = Game()
connected_clients = set()

async def handle_connection(websocket, path):
    print("Client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print("Message received:", message)
            data = json.loads(message)

            if data['type'] == 'initialize':
                print("Initializing game with data:", data)  # Debug log
                game.initialize_game(data['playerA'], data['playerB'])
                print("Game initialized")
                await broadcast_state()

            elif data['type'] == 'move':
                if game.turn == data['player']:
                    if game.is_valid_move(data['player'], data['character'], data['move']):
                        game.move_character(data['player'], data['character'], data['move'])
                        game.check_winner()
                        game.turn = 'B' if game.turn == 'A' else 'A'  # Switch turn
                        await broadcast_state()
                    else:
                        await websocket.send(json.dumps({"type": "invalid_move"}))

    finally:
        connected_clients.remove(websocket)
        print("Client disconnected")


async def broadcast_state():
    state = game.get_game_state()
    if game.winner:
        state['type'] = 'game_over'
        state['winner'] = game.winner
    else:
        state['type'] = 'state_update'

    print("Broadcasting state:", state)  # Debugging log
    for ws in connected_clients:
        await ws.send(json.dumps(state))

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")  # Debugging log
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
