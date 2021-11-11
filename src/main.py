import random
from typing import Set, Tuple
from word import Word
from words import Words
from app_types import WordSeq, StrSeq

class LetterBoxedSolver:
    def __init__(self, letter_groups: str) -> None:
        print(f'{LetterBoxedSolver.__name__} is ready to solve "{letter_groups}"')
        self.letters = letter_groups.replace(' ', '')
        self.words = Words(letter_groups)

    def solve(self) -> StrSeq:
        def randomly_choose_word(words: WordSeq) -> Word:
            num_words_to_choose_from = 20
            high = min(len(words), num_words_to_choose_from) - 1
            mode = -1  # todo Why doesn’t 0 work? (Yields too few 0 values)
            index = round(random.triangular(0, high, mode))
            return words[index]

        letters_needed = set(self.letters)
        selected_words = []
        first_letter = None

        while letters_needed:
            words: WordSeq = self.words.best_words_for_needed_letters(letters_needed)

            def connects_to_previous(word: Word) -> bool:
                return not first_letter or word.text[0] == first_letter

            connectable_words = list(filter(connects_to_previous, words))
            word = randomly_choose_word(connectable_words)
            selected_words.append(word.text)
            letters_needed.difference_update(word.unique_letters)
            first_letter = word.text[-1]
        return selected_words

    def solve_multiple(self, num_runs) -> StrSeq:
        random.seed(1)  # Get consistent results despite randomness

        unique_solutions: Set[Tuple[str]] = set(
            tuple(solver.solve()) for _ in range(num_runs))
        lengths_and_solutions: list[tuple[int, tuple[str]]] = [
            (len(''.join(solution)), solution)
            for solution in unique_solutions]
        lengths_and_solutions.sort()  # Fewer letters is better
        print(f'{len(lengths_and_solutions):,} unique solutions found in {num_runs:,} runs')
        solutions: StrSeq = list(map(lambda ls: ls[1], lengths_and_solutions))
        return solutions

if __name__ == '__main__':
    solver = LetterBoxedSolver('ari tkv csd uey')
    solutions = solver.solve_multiple(100)
    print('\n'.join([' ➡️ '.join(solution) for solution in solutions[:10]]))
