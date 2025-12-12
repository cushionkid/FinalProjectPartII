import tkinter as tk
from tkinter import ttk
import os
from typing import Any



#Jordan Williams helped me with this as well as using AI but for the most part all of this was either written by him or I

class MusicPlayerGUI:
    def __init__(self, music_player: Any) -> None:
        """
        Initialize the GUI with a music player instance.
        
        Args:
            music_player: Instance of MusicPlayer class to control playback
        """
        self.player = music_player
        self.root = tk.Tk()
        self.root.title("Music Player")
        self.root.geometry("700x700")
        
        # Set window color
        self.root.configure(bg="#D3D3D3")  # Light grey background
        
        # border (using highlightthickness)
        self.root.configure(highlightbackground="#696969", highlightthickness=8)
        
        self.songs = self.player.get_mp3_files()
        self.current_song_index = 0
        self.is_paused = False
        self.updating_progress = False
        self.user_seeking = False
        
        self.setup_ui()
        self.check_song_status()
        
    def setup_ui(self) -> None:
        """Create all GUI elements including buttons, labels, and controls."""
        # Title Label
        title_label = tk.Label(self.root, text="Music Player", font=("Arial", 20, "bold"), 
                               bg="#D3D3D3", fg="#2F4F4F")
        title_label.pack(pady=20)
        
        # Current Song Label
        self.song_label = tk.Label(self.root, text="No song playing", font=("Arial", 12),
                                   bg="#D3D3D3", fg="#2F4F4F")
        self.song_label.pack(pady=10)
        
        # Song Listbox
        listbox_frame = tk.Frame(self.root, bg="#D3D3D3")
        listbox_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.song_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        self.song_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.song_listbox.yview)
        
        # Populate listbox with songs
        for song in self.songs:
            self.song_listbox.insert(tk.END, os.path.basename(song))
        
        # Bind double-click to play song
        self.song_listbox.bind("<Double-Button-1>", self.play_selected_song)
        
        # Progress Bar Frame
        progress_frame = tk.Frame(self.root, bg="#D3D3D3")
        progress_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.time_label = tk.Label(progress_frame, text="0:00 / 0:00", font=("Arial", 9),
                                   bg="#D3D3D3", fg="#2F4F4F")
        self.time_label.pack()
        
        self.progress_bar = tk.Scale(progress_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                     showvalue=False, length=500)
        self.progress_bar.bind("<Button-1>", self.on_progress_press)
        self.progress_bar.bind("<ButtonRelease-1>", self.on_progress_release)
        self.progress_bar.pack(fill=tk.X)
        
        # Control Buttons Frame
        button_frame = tk.Frame(self.root, bg="#D3D3D3")
        button_frame.pack(pady=20)
        
        #For all the special characters such as ▶ and ⏸ I asked an AI to print them and I just copy and pasted
        
        # Previous Button
        self.previous_button = tk.Button(button_frame, text="⏮ Previous", command=self.play_previous, 
                                        width=10, font=("Arial", 10))
        self.previous_button.grid(row=0, column=0, padx=5)
        
        
        # Play Button
        self.play_button = tk.Button(button_frame, text="▶ Play", command=self.play, 
                                     width=10, font=("Arial", 10))
        self.play_button.grid(row=0, column=1, padx=5)
        
        # Pause Button
        self.pause_button = tk.Button(button_frame, text="⏸ Pause", command=self.pause, 
                                      width=10, font=("Arial", 10))
        self.pause_button.grid(row=0, column=2, padx=5)
        
        # Stop Button
        self.stop_button = tk.Button(button_frame, text="⏹ Stop", command=self.stop, 
                                     width=10, font=("Arial", 10))
        self.stop_button.grid(row=0, column=3, padx=5)
        
        # Next Button
        self.next_button = tk.Button(button_frame, text="⏭ Next", command=self.play_next, 
                                     width=10, font=("Arial", 10))
        self.next_button.grid(row=0, column=4, padx=5)
        
        # Volume Control
        volume_frame = tk.Frame(self.root, bg="#D3D3D3")
        volume_frame.pack(pady=10)
        
        tk.Label(volume_frame, text="Volume:", font=("Arial", 10),
                bg="#D3D3D3", fg="#2F4F4F").pack(side=tk.LEFT, padx=5)
        
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                      command=self.change_volume, length=200)
        self.volume_slider.set(100)
        self.volume_slider.pack(side=tk.LEFT)
        
    def play(self) -> None:
        """
        Play the currently selected song or first song.
        
        If paused, resumes playback. Otherwise starts playing the selected song.
        """
        if self.songs:
            # If paused, just unpause
            if self.is_paused:
                self.player.unpause()
                self.is_paused = False
                song_path = self.songs[self.current_song_index]
                self.song_label.config(text=f"Now playing: {os.path.basename(song_path)}")
            else:
                # Otherwise, start playing a new song
                selection = self.song_listbox.curselection()
                if selection:
                    self.current_song_index = selection[0]
                
                song_path = self.songs[self.current_song_index]
                self.player.play_song(song_path)
                self.song_label.config(text=f"Now playing: {os.path.basename(song_path)}")
    
    def play_selected_song(self, event: tk.Event) -> None:
        """Play song when double-clicked in listbox.
        
        Args:
            event: Tkinter event from double-click
        """
        self.play()
    
    def pause(self) -> None:
        """Pause the current song and update the display label."""
        self.player.pause()
        self.is_paused = True
        song_path = self.songs[self.current_song_index]
        self.song_label.config(text=f"Paused: {os.path.basename(song_path)}")
    
    def stop(self) -> None:
        """Stop the current song and reset the player state."""
        self.player.stop()
        self.is_paused = False
        self.song_label.config(text="Stopped")
    
    def change_volume(self, value: str) -> None:
        """Change the volume based on slider value.
        
        Args:
            value: Volume value from slider (0-100) as string
        """
        volume = int(value) / 100.0
        self.player.set_volume(volume)
    
    def on_progress_press(self, event: tk.Event) -> None:
        """User started dragging the progress bar.
        
        Args:
            event: Tkinter button press event
        """
        self.user_seeking = True
    
    def on_progress_release(self, event: tk.Event) -> None:
        """Seek to position when user releases the progress bar.
        
        Args:
            event: Tkinter button release event
        """
        self.user_seeking = False
        if self.player.current_song:
            value = self.progress_bar.get()
            length = self.player.get_length()
            if length > 0:
                position = (float(value) / 100.0) * length
                self.player.set_time(position)
    
    def format_time(self, ms: int) -> str:
        """Format milliseconds to MM:SS.
        
        Args:
            ms: Time in milliseconds
            
        Returns:
            Formatted time string as MM:SS
        """
        if ms < 0:
            return "0:00"
        seconds = int(ms / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def update_progress(self) -> None:
        """Update the progress bar and time label with current playback position."""
        if self.player.current_song and self.player.is_playing() and not self.is_paused and not self.user_seeking:
            current_time = self.player.get_time()
            length = self.player.get_length()
            
            if length > 0:
                progress = (current_time / length) * 100
                self.progress_bar.set(progress)
                self.time_label.config(text=f"{self.format_time(current_time)} / {self.format_time(length)}")
    
    def check_song_status(self) -> None:
        """Check if the current song has ended and play next song.
        
        Runs every 100ms to update progress and detect song end.
        """
        if self.player.current_song and self.player.has_ended():
            # Play next song
            self.play_next()
        
        # Update progress bar
        self.update_progress()
        
        # Schedule next check
        self.root.after(100, self.check_song_status)
    
    def play_next(self) -> None:
        """Play the next song in the list.
        
        Wraps around to first song if at the end of the playlist.
        """
        if self.songs:
            self.current_song_index = (self.current_song_index + 1) % len(self.songs)
            song_path = self.songs[self.current_song_index]
            self.player.play_song(song_path)
            self.is_paused = False
            self.song_label.config(text=f"Now playing: {os.path.basename(song_path)}")
            # Update listbox selection
            self.song_listbox.selection_clear(0, tk.END)
            self.song_listbox.selection_set(self.current_song_index)
            self.song_listbox.see(self.current_song_index)
    
    def play_previous(self) -> None:
        """Play the previous song in the list.
        
        Wraps around to last song if at the beginning of the playlist.
        """
        if self.songs:
            self.current_song_index = (self.current_song_index - 1) % len(self.songs)
            song_path = self.songs[self.current_song_index]
            self.player.play_song(song_path)
            self.is_paused = False
            self.song_label.config(text=f"Now playing: {os.path.basename(song_path)}")
            # Update listbox selection
            self.song_listbox.selection_clear(0, tk.END)
            self.song_listbox.selection_set(self.current_song_index)
            self.song_listbox.see(self.current_song_index)
    
    def run(self) -> None:
        """Start the GUI main loop and display the window."""
        self.root.mainloop()








