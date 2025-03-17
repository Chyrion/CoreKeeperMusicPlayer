# pylint: disable-all
from song import SongBpm as Song
import filereader
import time
import threading
import keyboard as kb


class SheetMusicPlayer:

    _note_lengths = {}
    _opener_brackets = "[({"
    _closer_brackets = "])}"

    def __init__(self) -> None:
        self._file_reader = filereader.CKSPFileReader()
        self._songs: list[Song] = self._file_reader.get_songs()
        self._print_instructions()

    def _print_instructions(self):
        print("=== Core Keeper Custom Song Player ===")
        if self._songs != None and len(self._songs) > 0:
            print("Select song:")
            print("0: Exit")
            for i in range(len(self._songs)):
                print(f"{i+1}: {self._songs[i].song_name}")
            while True:
                try:
                    sel_song = int(input("Selection: "))
                    if sel_song == 0:
                        print("Exiting...")
                        break
                    if sel_song not in range(len(self._songs) + 1):
                        print("Invalid selection, try again: ")
                        continue
                    self.play(self._songs[sel_song-1])
                    break
                except KeyboardInterrupt:
                    print("Keyboard interrupt caught, exiting...")
                    return
                except:
                    print("Invalid selection, try again: ")
        else:
            print("No valid songs could be found or created, exiting.")
        return

    def play(self, song: Song):
        notes = self.interpret(song)
        sel = 0
        if len(notes) > 1:
            print("Multiple texts detected!\nSelect text to play")
            print("0: Both (multithreaded)")
            for i in range(len(notes)):
                print(f'{i+1}: Text {i+1}')
            while True:
                try:
                    sel = int(input("Selection: "))
                    if sel not in range(len(notes)):
                        print("Invalid selection, try again: ")
                        continue
                    break
                except KeyboardInterrupt:
                    print("Keyboard interrupt caught, exiting...")
                    return
                except:
                    print("Invalid selection, try again: ")
        print(f"Ready to play! Starting in:")
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)
        if sel == 0:
            for n in notes:
                x = threading.Thread(target=self.play_notes, args=(n,))
                x.start()

        else:
            for note in notes[sel-1]:
                self.press_and_hold(note)
                time.sleep(0.005)

    def play_notes(self, notes: list) -> None:
        for note in notes:
            if note[0] != '-':
                self.press_and_hold(note)
            else:
                time.sleep(note[1])
            time.sleep(0.005)

    def press_and_hold(self, k: tuple[str, float]):
        kb.press(k[0])
        time.sleep(k[1])
        kb.release(k[0])

    def interpret(self, song: Song) -> list:
        self._note_lengths = self.note_length(song.bpm)
        all_keys = []
        for s in song.song_texts:
            bars = self.split_bars(s)
            keys = self.parse_notes(bars)
            keys = [item for li in keys for item in li]
            all_keys.append(keys)
        return all_keys

    def note_length(self, bpm: int):
        notes = {}
        notes[1] = round(240 / bpm, 3)
        notes[2] = round(120 / bpm, 3)
        notes[4] = round(60 / bpm, 3)
        notes[8] = round(30 / bpm, 3)
        notes[16] = round(15 / bpm, 3)
        notes[32] = round(7.5 / bpm, 3)
        notes[64] = round(3.75 / bpm, 3)
        notes[128] = round(1.875 / bpm, 3)
        return notes

    def split_bars(self, song: str) -> list[list[str]]:
        bars = song.split("|")
        sections = []
        for bar in bars:
            currbar = []
            skipto = 0
            for i in range(len(bar)):
                if i < skipto:
                    continue

                if bar[i] in self._opener_brackets:
                    closer = i+1
                    while bar[closer] not in self._closer_brackets:
                        closer += 1
                    if closer != len(bar)-1:
                        if bar[closer+1] in self._closer_brackets:
                            closer += 1
                    t = bar[i:closer+1]
                    currbar.append(t)
                    skipto = closer+1

                else:
                    currbar.append(bar[i])
            sections.append(currbar)
            # print(currbar)
        return sections

    def parse_notes(self, bars: list[list[str]]) -> list:
        keys = []
        for bar in bars:
            for brack in bar:
                keys.append(self.parse_bracket(brack))

        return keys

    def parse_bracket(self, bracket: str):
        bracket_notes = []
        length = 0.0
        if bracket[0] in self._opener_brackets:
            content = [*bracket][1:- 1]
        else:
            content = bracket
        match bracket[0]:
            case '[':
                # Currently handles . for staccato (length x 1.5)
                # and : for pause/
                content_str = ''.join(content)
                dotted_index = content_str.join(content).find('.')
                staccato_index = content_str.join(content).find(':')
                if dotted_index in [-1, 2] and staccato_index in [-1, 2]:
                    l = 4
                else:
                    l = ''.join(content[1:-1])

                if dotted_index > 0:
                    length = self._note_lengths[int(l)] * 1.5
                elif staccato_index > 0:
                    length = self._note_lengths[int(l)] * 0.5

                else:
                    l = ''.join(content[1:])
                    length = self._note_lengths[int(l)]

                bracket_notes.append((content[0], length))
                if ''.join(content).find(':') > -1:
                    bracket_notes.append(('-', length))

            case '(':
                b_count = content.count('(')
                if b_count > 0:
                    content = content[b_count:-b_count]
                    l = 8
                    for _ in range(b_count):
                        l *= 2
                    length = self._note_lengths[l]
                # if content[0] == '(':
                #     content = content[1:-1]
                #     length = self._note_lengths[16]
                else:
                    length = self._note_lengths[8]

                for c in content:
                    bracket_notes.append((c, length))

            case '{':
                keys = ""
                if content[-1] == ']':
                    content_split = bracket[1:-1].split('[')
                    length_num = content_split[1][:-1]
                    length = self._note_lengths[int(length_num)]
                    keys = '+'.join(content_split[0])

                else:
                    length = self._note_lengths[4]
                    keys = "+".join(content)
                bracket_notes.append((keys, length))

            case _:
                length = self._note_lengths[4]
                bracket_notes.append((content[0], length))

        return bracket_notes


if __name__ == "__main__":
    player = SheetMusicPlayer()
