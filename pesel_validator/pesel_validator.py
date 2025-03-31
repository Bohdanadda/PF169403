import re
import datetime

class PeselValidator:
    @staticmethod
    def validate_format(pesel: str) -> bool:
        return bool(re.fullmatch(r"\d{11}", pesel))

    def __init__(self, pesel: str):
        self.pesel = pesel

    @staticmethod
    def validate_check_digit(pesel: str) -> bool:
        if not PeselValidator.validate_format(pesel):
            return False

        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        sum_check = sum(int(pesel[i]) * weights[i] for i in range(10))
        control_digit = (10 - (sum_check % 10)) % 10
        return control_digit == int(pesel[10])

    @staticmethod
    def validate_birth_date(pesel: str) -> bool:
        if not PeselValidator.validate_format(pesel):
            return False
        year = int(pesel[:2])
        month = int(pesel[2:4])
        day = int(pesel[4:6])

        if month > 80:
            year += 1800
            month -= 80
        elif month > 60:
            year += 2200
            month -= 60
        elif month > 40:
            year += 2100
            month -= 40
        elif month > 20:
            year += 2000
            month -= 20
        else:
            year += 1900

        try:
            datetime.date(year, month, day)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_gender(pesel: str) -> str:
        if not PeselValidator.validate_format(pesel):
            raise ValueError("Niepoprawny Pesel")
        return "Kobieta" if int(pesel[-2]) % 2 == 0 else "Mężczyzna"

    @staticmethod
    def is_valid(pesel: str) -> bool:
        return (
            PeselValidator.validate_format(pesel) and
            PeselValidator.validate_birth_date(pesel) and
            PeselValidator.validate_check_digit(pesel)
        )