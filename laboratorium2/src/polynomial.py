class Polynomial:
    def __init__(self, coefficients):
        self.coeff = list(coefficients)
        self._remove_leading_zeros()
        if not self.coeff:
            self.coeff = [0]

    def _remove_leading_zeros(self):
        while len(self.coeff) > 1 and self.coeff[0] == 0:
            self.coeff.pop(0)

    def degree(self):
        return len(self.coeff) - 1

    def evaluate(self, x):
        result = 0
        for coef in self.coeff:
            result = result * x + coef
        return result

    def __str__(self):
        terms = []
        degree = self.degree()

        for i, coef in enumerate(self.coeff):
            if coef == 0:
                continue
            power = degree - i

            if coef == 1 and power != 0:
                coef_str = ""
            elif coef == -1 and power != 0:
                coef_str = "-"
            else:
                coef_str = str(coef)

            if power == 0:
                terms.append(f"{coef}")
            elif power == 1:
                terms.append(f"{coef_str}x")
            else:
                terms.append(f"{coef_str}x^{power}")

        if not terms:
            return "0"

        result = " + ".join(terms)
        return result.replace("+ -", "- ")
    def __repr__(self):
        return f"Polynomial({self.coeff})"

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.coeff == other.coeff
        if isinstance(other, (int, float)):
            return self.degree() == 0 and self.coeff[0] == other
        return False

    def __add__(self, other):
        if isinstance(other, (int, float)):
            new_coeff = self.coeff[:]
            new_coeff[-1] += other
            return Polynomial(new_coeff)
        elif isinstance(other, Polynomial):
            max_len = max(len(self.coeff), len(other.coeff))
            coeff1 = [0] * (max_len - len(self.coeff)) + self.coeff
            coeff2 = [0] * (max_len - len(other.coeff)) + other.coeff
            return Polynomial([c1 + c2 for c1, c2 in zip(coeff1, coeff2)])
        return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            new_coeff = self.coeff[:]
            new_coeff[-1] -= other
            return Polynomial(new_coeff)
        elif isinstance(other, Polynomial):
            max_len = max(len(self.coeff), len(other.coeff))
            coeff1 = [0] * (max_len - len(self.coeff)) + self.coeff
            coeff2 = [0] * (max_len - len(other.coeff)) + other.coeff
            return Polynomial([c1 - c2 for c1, c2 in zip(coeff1, coeff2)])

    def __rsub__(self, other):
        return -(self - other)

    def __neg__(self):
        return Polynomial([-c for c in self.coeff])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Polynomial([coef * other for coef in self.coeff])
        elif isinstance(other, Polynomial):
            result_coeff = [0] * (len(self.coeff) + len(other.coeff) - 1)
            for i, c1 in enumerate(self.coeff):
                for j, c2 in enumerate(other.coeff):
                    result_coeff[i + j] += c1 * c2
            return Polynomial(result_coeff)

    def __rmul__(self, other):
        return self * other
