# pylint: disable-all

class Song:

    song_text = ""
    normal_length = 0.25
    short_length = 0.1
    long_length = 1.0
    space_length = 0.05
    pause_length = 0.25
    long_pause_length = 1.0
    bpm = 0

    def __init__(self, song_text,
                 normal_length: float = 0.25,
                 short_length: float = 0.1,
                 long_length: float = 1.0,
                 space_length: float = 0.05,
                 pause_length: float = 0.25,
                 long_pause_length: float = 1.0) -> None:
        self.song_text = song_text
        self.normal_length = normal_length
        self.short_length = short_length
        self.long_length = long_length
        self.space_length = space_length
        self.pause_length = pause_length
        self.long_pause_length = long_pause_length


class SongBpm:
    """
    Song class with a BPM property
    """

    def __init__(self, name: str, bpm: int) -> None:
        self.song_name = name
        self.bpm = bpm
        self.song_texts = []

    def add_song_text(self, song_text: str) -> None:
        self.song_texts.append(song_text)

    def __str__(self) -> str:
        return f'{self.song_name}\nBPM: {self.bpm}\nTexts: {len(self.song_texts)}'
