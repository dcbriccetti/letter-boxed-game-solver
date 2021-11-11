import pathlib
from typing import List, Dict
from word import Word

class Words:
    words: list[Word]

    def __init__(self, letter_groups: str) -> None:
        def find_paths(letters: str) -> Dict[str, str]:
            'Build dictionary of valid letter-to-letter transitions'

            def other_group_letters(group: str) -> str:
                return ''.join(gl for gl in grouped_letters if gl != group)

            grouped_letters: list[str] = letters.split()
            return {letter: other_group_letters(group)
                    for group in grouped_letters for letter in group}

        def word_works(word: str) -> bool:
            for i in range(len(word) - 1):
                letter = word[i]
                next_letter = word[i + 1]
                if not (ok_next_letters := paths.get(letter)):
                    return False
                if next_letter not in ok_next_letters:
                    return False
            return True

        paths: Dict[str, str] = find_paths(letter_groups)
        all_words = pathlib.Path('resources/words.txt').read_text().strip().split('\n')
        candidate_words = list(filter(word_works, all_words))
        print(f'{len(candidate_words):,} candidate words loaded from list of {len(all_words):,} words')
        self.words = list(map(Word.create, candidate_words))
        self.words.sort(key=lambda word: word.num_unique_letters, reverse=True)

    def best_words_for_needed_letters(self, needed_letters: set[str]) -> List[Word]:
        def num_needed_letters(word: Word):
            return len(word.unique_letters.intersection(needed_letters))

        num_needed_letters_and_words: list[tuple[int, Word]] = [
            (num_needed_letters(word), word) for word in self.words]
        num_needed_letters_and_words.sort(reverse=True)
        return [lw[1] for lw in num_needed_letters_and_words]
