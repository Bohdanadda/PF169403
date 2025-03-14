import re
from collections import Counter


class FindMostFrequentWord:
    def find_most_frequent_word(self, text):
        word = re.findall(r'\b\w+\b', text.lower())
        if not word:
            return None

        word_count = Counter(word)
        max_count = max(word_count.values())

        most_frequent_word = [word for word, count in word_count.items() if count == max_count]
        return most_frequent_word[0]
