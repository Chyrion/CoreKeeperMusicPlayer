# pylint: disable-all
import os
from song import SongBpm as Song


class CKSPFileReader:

    def __init__(self) -> None:
        self._songs = []
        self._songs_path = os.getcwd() + '\\songs\\'
        pass

    def get_songs(self) -> list[Song]:
        files = self._find_files()
        if files == None:
            return None
        raw = self._read_files(files)
        songs = self._create_songs(raw)
        return songs

    def _find_files(self):
        try:
            directory_files = os.listdir(self._songs_path)
            cksp_files = filter(lambda x: str(x)
                                .lower()
                                .rsplit('.', maxsplit=1)
                                [-1] == 'cksp', directory_files)
            return list(cksp_files)
        except:
            print("No songs folder found!")
            return None

    def _read_files(self, files: list[str]):
        raw_songs = []
        for file in files:
            with open(self._songs_path + file, 'r') as f:
                raw_content = f.readlines()
                stripped = [l.strip() for l in raw_content]
                raw_songs.append(stripped)
        return raw_songs

    def _create_songs(self, raw_songs: list[list[str]]) -> list[Song]:
        songs = []
        for raw in raw_songs:
            try:
                s = Song(raw[0], int(raw[1]))
            except ValueError as er:
                print(type(er))
                print("Failed to create song, skipping")
                continue
            texts = []
            cur_text = ""
            same_text = False
            for line in raw[2:]:
                if line == '{':
                    same_text = True
                    continue
                elif line == '}':
                    same_text = False
                    texts.append(cur_text[:-1])  # removes the last |
                    cur_text = ''
                    continue

                if same_text:
                    if line[-1] != '|':
                        line += '|'
                    line = line.lstrip('|')
                    cur_text += line
            for t in texts:
                if t != '':
                    s.add_song_text(t)
            songs.append(s)
        return songs


if __name__ == "__main__":
    fr = CKSPFileReader()
    songs = fr.get_songs()
    for s in songs:
        print(s)
        print(s.song_texts)
