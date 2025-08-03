from game import pikaVolley as pv


def main():
    
    # Create game instance
    game = pv.PikachuVolleyball(isPlayer1Computer=False, isPlayer2Computer=False, display=True)
    game.startOfNewGame()
    running = True
    while running:
        # Handle events and user input
        game.round()
        
    
 

if __name__ == "__main__":
    main()