import pathlib
from queue import SimpleQueue
from typing import List, NamedTuple


class Prefix(NamedTuple):
    text: str
    start_with: List[str]
    is_word: bool

class LetterBoxedSolver:
    def __init__(self, letters: str) -> None:
        self.groups = letters.split()
        self.letters = [letter for letter in letters if letter != ' ']
        self.frontier = SimpleQueue()
        self.words = self.load_dictionary_words()
        self.letters_used = set()
        self.selected_words = []

    def load_dictionary_words(self) -> List[str]:
        words = [word for word in pathlib.Path('resources/words.txt').read_text().split('\n') if
                 not word.startswith('#') and all([letter in self.letters for letter in word])]
        print(f'{len(words)} candidate words loaded from dictionary')
        return words

    def possible_next_letters(self, letter: str) -> str:
        'Given a letter, return a string containing all letters in the three groups not containing the letter'
        return ''.join((group for group in self.groups if letter not in group))

    def longest_word(self, starting_letter: str):
        self.frontier.put(Prefix(starting_letter, [], False))
        longest_word = ''

        while not self.frontier.empty():
            word: Prefix = self.frontier.get()
            print(f'Frontier -> {word}')
            for letter in self.possible_next_letters(word.text[-1]):
                prefix = word.text + letter
                if matches := [w for w in self.words if w.startswith(prefix)]:
                    new_word = Prefix(prefix, matches, prefix in matches)
                    self.frontier.put(new_word)
                    print(f'Frontier <- {new_word}, fr={self.frontier.qsize()}')
                    if new_word.is_word and len(new_word.text) > len(longest_word) and new_word.text[0] != new_word.text[-1]:
                        longest_word = new_word.text
        self.letters_used.update(longest_word)
        self.selected_words.append(longest_word)
        return longest_word

    def solve(self, starting_letter: str) -> List[str]:
        word = starting_letter
        num_words = 0
        while num_words < 30 and not self.all_letters_are_used():
            num_words += 1
            next_word_first_letter = word[-1]
            word = self.longest_word(next_word_first_letter)
            print('\n' + ' -> '.join(self.selected_words))
            print('Letters used: ' + self.all_letters_used())
        return self.selected_words

    def all_letters_used(self) -> str:
        list_of_letters = list(self.letters_used)
        list_of_letters.sort()
        return ''.join(list_of_letters)

    def all_letters_are_used(self) -> bool:
        return len(self.letters_used) == len(self.letters)

if __name__ == '__main__':
    solver = LetterBoxedSolver('ryl pqf aeo bui')
    solver.solve('q')
