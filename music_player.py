import os
from pathlib import Path
import vlc
from typing import List, Optional





class MusicPlayer:
    
    def __init__(self, music_folder: str = "Music") -> None:
        """
        Initialize the music player with the path to the music folder.
        
        Args:
            music_folder: Path to the folder containing MP3 files (default: "Music")
        """
        self.music_folder = music_folder
        self.current_song: Optional[str] = None
        #AI was used here to set up VLC player since it was my first time and I didn't really know what I was doing
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    #I was able to map the path and set up the warning if the path doesn't exist by myself    
    def get_mp3_files(self) -> List[str]:
        """
        Get all MP3 files from the Music folder.
        
        Returns:
            List of file paths to MP3 files as strings
        """
        music_path = Path(self.music_folder)
        if not music_path.exists():
            print(f"Music folder '{self.music_folder}' not found!")
            return []

        
        mp3_files = list(music_path.glob("*.mp3"))
        return [str(file) for file in mp3_files]

    #I used AI here to help me because I was still learing how to use VLC
    def play_song(self, song_path: str) -> None:
        """
        Play a specific MP3 file.
        
        Args:
            song_path: Full path to the MP3 file to play
        """
        try:
            self.current_song = song_path
            media = self.instance.media_new(song_path)
            self.player.set_media(media)
            self.player.play()
            print(f"Now playing: {os.path.basename(song_path)}")
        except Exception as e:
            print(f"Error playing {song_path}: {e}")

    #I used AI here pretty much just to figure out the "self.player.pause()" command
    def pause(self) -> None:
        """Pause the currently playing song."""
        self.player.pause()
        print("Music paused")

    #Starting here I had learned enough that I was able to write the rest on my own with very very little to zero AI help
    def unpause(self) -> None:
        """Resume the paused song."""
        self.player.play()
        print("Music resumed")

    
    def stop(self) -> None:
        """Stop the currently playing song."""
        self.player.stop()
        self.current_song = None
        print("Music stopped")

    #except for here, I used AI and did some google searching to figure out how to get the volume to work
    def set_volume(self, volume: float) -> None:
        """
        Set the volume (0.0 to 1.0).
        
        Args:
            volume: Volume level as a float between 0.0 (mute) and 1.0 (max)
        """
        self.player.audio_set_volume(int(volume * 100))
        print(f"Volume set to {int(volume * 100)}%")

    
    def is_playing(self) -> bool:
        """
        Check if music is currently playing.
        
        Returns:
            True if music is playing, False otherwise
        """
        return self.player.is_playing()

    
    def get_length(self) -> int:
        """
        Get the length of the current song in milliseconds.
        
        Returns:
            Song length in milliseconds
        """
        return self.player.get_length()
    
    def get_time(self) -> int:
        """
        Get the current playback position in milliseconds.
        
        Returns:
            Current position in milliseconds
        """
        return self.player.get_time()
    
    def set_time(self, time_ms: float) -> None:
        """
        Set the playback position in milliseconds.
        
        Args:
            time_ms: Target position in milliseconds
        """
        self.player.set_time(int(time_ms))
    
    def has_ended(self) -> bool:
        """
        Check if the current song has ended.
        
        Returns:
            True if the song has ended, False otherwise
        """
        state = self.player.get_state()
        return state == vlc.State.Ended






