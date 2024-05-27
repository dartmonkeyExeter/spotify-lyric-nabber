from lyricsgenius import Genius
import win32gui
import win32process
import psutil

genius = Genius("get your own api key nerd")

def get_spotify_window_title():
    # Find the PID of spotify.exe
    spotify_pids = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Spotify.exe':
            spotify_pids.append(proc.info['pid'])

    if not spotify_pids:
        return "Spotify process not found"

    def callback(hwnd, pid):
        if win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
            window_title = win32gui.GetWindowText(hwnd)
            window_titles.append(window_title)
    
    window_titles = []
    for pid in spotify_pids:
        win32gui.EnumWindows(callback, pid)

    return window_titles[0]

def get_lyrics(song, artist):
    lyrics = genius.search_song(song, artist).lyrics

    # logic to get rid of stuff like [Verse 1], [Chorus], etc.
    lyrics = lyrics.split("\n")
    for line in lyrics:
        try:
            if f"{song.lower()} lyrics" in line.lower():
                lyrics.remove(line)
            if "embed" in line.lower():
                lyrics.remove(line)
            if "contributors" in line.lower():
                lyrics.remove(line)    
            if line.startswith("["):
                lyrics.remove(line)
            if "You might also like" in line:
                lyrics.remove(line)
        except:
            # this just means the line is already removed
            pass
        
        # check if a line ends with ANY number, if so remove only the number
        for letter in line[::-1]:
            if letter.isdigit():
                lyrics[lyrics.index(line)] = line[:line.index(letter)]
            else:
                break
    
    lyrics = "\n".join(lyrics)
    return lyrics

def main():
    previous_title = ""
    while True:
        try:
            title = get_spotify_window_title()
            if title != previous_title:
                artist, song = title.split(" - ")
                lyrics = get_lyrics(song, artist)
                print(lyrics)
                previous_title = title
        except:
            print("Nothing currently playing...")
            pass

if __name__ == "__main__":
    main()
