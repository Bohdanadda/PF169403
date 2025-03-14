class StringManipulator:
    def revers_string(self, text: str) -> str:
        return text[::-1]

    def count_words(self, text: str) -> int:
        return len(text.split())

    def capitalize_words(self, text: str) -> str:
        return text.title()