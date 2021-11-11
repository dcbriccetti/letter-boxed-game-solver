from random import choice, seed
from typing import List, Set, Tuple
from words import Words


class LetterBoxedSolver:
    WordSeq = List[str]

    def __init__(self, letter_groups: str) -> None:
        print(f'{LetterBoxedSolver.__name__} is ready to solve "{letter_groups}"')
        self.letters = letter_groups.replace(' ', '')
        self.words = Words(letter_groups)

    def solve(self) -> WordSeq:
        letters_needed = set(self.letters)
        selected_words = []
        first_letter = None

        while letters_needed:
            best_words = [word for word in self.words.best_words_for_needed_letters(letters_needed)
                          if not first_letter or word.text[0] == first_letter]
            word = choice(best_words[:20])
            selected_words.append(word.text)
            letters_needed.difference_update(word.unique_letters)
            first_letter = word.text[-1]
        return selected_words

    def solve_multiple(self) -> None:
        seed(1)  # Get consistent results despite randomness
        runs = 1000

        unique_solutions: Set[Tuple[str]] = set(tuple(solver.solve()) for _ in range(runs))
        lengths_and_solutions: list[tuple[int, tuple[str]]] = [
            (len(''.join(solution)), solution)
            for solution in unique_solutions]
        lengths_and_solutions.sort()  # Fewer letters is better

        print(f'{len(lengths_and_solutions):,} unique solutions found in {runs:,} runs')
        for _, solution in lengths_and_solutions[:10]:
            print(' ➡️ '.join(solution))

if __name__ == '__main__':
    solver = LetterBoxedSolver('upo xts eil ncy')
    solver.solve_multiple()
