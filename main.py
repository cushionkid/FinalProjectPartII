import gui
from music_player import MusicPlayer

"""
Run this file to start the music player

"""
#this was all written by me

def main() -> None:
    """
    Initialize and run the music player application.
    
    Creates a MusicPlayer instance with the "Music" folder and launches the GUI.
    """
    # Initialize the music player
    player = MusicPlayer("Music")
    
    # Create and start the GUI, passing the music player to it
    app = gui.MusicPlayerGUI(player)
    app.run()

if __name__ == "__main__":
    main()