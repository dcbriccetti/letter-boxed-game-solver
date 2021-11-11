from typing import NamedTuple, Set

class Word(NamedTuple):
    text: str
    unique_letters: Set[str]
    num_unique_letters: int

    @staticmethod
    def create(text: str):
        unique_letters = set(text)
        return Word(text, unique_letters, len(unique_letters))
