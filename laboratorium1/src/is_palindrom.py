import re

class IsPalindrom:
    def is_palindrom(self, s):
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
        return cleaned == cleaned[::-1]