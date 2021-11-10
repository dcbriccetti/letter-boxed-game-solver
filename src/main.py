from random import choice, seed
from typing import List
from words import Words

class LetterBoxedSolver:
    def __init__(self, letter_groups: str) -> None:
        self.letters = letter_groups.replace(' ', '')
        self.words = Words(letter_groups)

    def solve(self) -> List[str]:
        letters_needed = set(self.letters)
        selected_words = []
        first_letter = None

        while letters_needed:
            best_words = [word for word in self.words.best_words_for_needed_letters(letters_needed)
                    if not first_letter or word.text[0] == first_letter]
            word = choice(best_words[:20])
            selected_words.append(word.text)
            letters_needed.difference_update(set(word.text))
            first_letter = word.text[-1]
        return selected_words

    def solve_multiple(self) -> None:
        seed(1)  # Get consistent results despite randomness
        runs = 100

        solutions: list[list[str]] = []
        for n in range(runs):
            if (solution := solver.solve()) not in solutions:
                solutions.append(solution)

        solutions.sort(key=lambda solution: len(''.join(solution)))  # Fewest letters is best

        print(f'{len(solutions):,} unique solutions found in {runs:,} runs')
        for solution in solutions[:10]:
            print(' ➡️ '.join(solution))

if __name__ == '__main__':
    solver = LetterBoxedSolver('ryl pqf aeo bui')
    solver.solve_multiple()
