import pathlib
from typing import List, Dict
from word import Word

class Words:
    words: list[Word]

    def __init__(self, letter_groups: str) -> None:
        def find_paths(letters: str) -> Dict[str, str]:
            'Build dictionary of valid letter-to-letter transitions'
            groups: list[str] = letters.split()
            group_dictionaries: list[dict] = [{letter: ''.join(g for g in groups if g is not group) for letter in group}
                                              for group in groups]
            single_dictionary = {k: v for gd in group_dictionaries for k, v in gd.items()}
            return single_dictionary

        def word_works(word: str, paths: Dict[str, str]) -> bool:
            for i in range(len(word) - 1):
                letter = word[i]
                next_letter = word[i + 1]
                if not (ok_next_letters := paths.get(letter)) or next_letter not in ok_next_letters:
                    return False
            return True

        paths: Dict[str, str] = find_paths(letter_groups)
        all_words = pathlib.Path('resources/words.txt').read_text().strip().split('\n')
        words = [word for word in all_words if word_works(word, paths)]
        print(f'{len(words):,} candidate words loaded from list of {len(all_words):,} words')
        self.words = [Word.create(word) for word in words]
        self.words.sort(key=lambda word: len(word.unique_letters), reverse=True)

    def best_words_for_needed_letters(self, needed_letters: set[str]) -> List[Word]:
        num_needed_letters_and_words: list[tuple[int, Word]] = [
            (len(word.unique_letters.intersection(needed_letters)), word)
            for word in self.words]
        num_needed_letters_and_words.sort(reverse=True)
        return [lw[1] for lw in num_needed_letters_and_words]
