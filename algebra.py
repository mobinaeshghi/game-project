"""
algebra.py - کتابخانه محاسبات عددی و ماتریسی

ساختار وراثت:
    AlgebraicElement (کلاس انتزاعی)
        |-- Integer
        |-- Complex
        |-- Matrix
"""
from abc import ABC, abstractmethod


# ======================= کلاس انتزاعی =======================
class AlgebraicElement(ABC):
    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __neg__(self):
        pass

    def __sub__(self, other):
        # a - b  یعنی  a + (-b)  (فقط همین‌جا نوشته می‌شود)
        return self + (-other)


# ======================= Integer =======================
class Integer(AlgebraicElement):
    def __init__(self, value: int):
        # type(value) is int یعنی int واقعی؛ bool رد می‌شود
        if type(value) is not int:
            raise TypeError("value must be int")
        self.__value = value

    @property
    def value(self):
        return self.__value

    @classmethod
    def from_string(cls, text: str):
        if type(text) is not str:
            raise TypeError("text must be str")
        digits = text
        if text.startswith("+") or text.startswith("-"):
            digits = text[1:]          # علامت را کنار می‌گذاریم
        if not digits.isdigit():
            raise ValueError("invalid integer string")
        return cls(int(text))

    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.__value + other.value)
        if isinstance(other, Complex):
            return Complex(self.__value + other.real, other.imag)
        if isinstance(other, Matrix):
            return other + self        # کار را به ماتریس می‌سپاریم
        raise TypeError("bad operand for +")

    def __mul__(self, other):
        if isinstance(other, Integer):
            return Integer(self.__value * other.value)
        if isinstance(other, Complex):
            return Complex(self.__value * other.real, self.__value * other.imag)
        if isinstance(other, Matrix):
            return other * self
        raise TypeError("bad operand for *")

    def __neg__(self):
        return Integer(-self.__value)

    def __eq__(self, other):
        if isinstance(other, Integer):
            return self.__value == other.value
        if isinstance(other, Complex):
            return other.imag == 0 and other.real == self.__value
        return False

    def __repr__(self):
        return "Integer(" + str(self.__value) + ")"


# ======================= Complex =======================
class Complex(AlgebraicElement):
    def __init__(self, real: int, imag: int):
        if type(real) is not int or type(imag) is not int:
            raise TypeError("real and imag must be int")
        self.__real = real
        self.__imag = imag

    @property
    def real(self):
        return self.__real

    @property
    def imag(self):
        return self.__imag

    @classmethod
    def from_string(cls, text: str):
        if type(text) is not str:
            raise TypeError("text must be str")
        if not text.endswith("i"):
            raise ValueError("complex string must end with i")
        body = text[:-1]                       # "5+2i" -> "5+2"
        # آخرین + یا - ، شروع بخش موهومی است
        pos = max(body.rfind("+"), body.rfind("-"))
        if pos <= 0:                           # علامت نیست یا فقط علامتِ ابتدای عدد است
            raise ValueError("invalid complex string")
        real = Integer.from_string(body[:pos]).value     # "5"
        imag = Integer.from_string(body[pos:]).value     # "+2"
        return cls(real, imag)

    def __add__(self, other):
        if isinstance(other, Integer):
            return Complex(self.__real + other.value, self.__imag)
        if isinstance(other, Complex):
            return Complex(self.__real + other.real, self.__imag + other.imag)
        if isinstance(other, Matrix):
            return other + self
        raise TypeError("bad operand for +")

    def __mul__(self, other):
        if isinstance(other, Integer):
            return Complex(self.__real * other.value, self.__imag * other.value)
        if isinstance(other, Complex):
            a, b = self.__real, self.__imag
            c, d = other.real, other.imag
            return Complex(a * c - b * d, a * d + b * c)
        if isinstance(other, Matrix):
            return other * self
        raise TypeError("bad operand for *")

    def __neg__(self):
        return Complex(-self.__real, -self.__imag)

    def __eq__(self, other):
        if isinstance(other, Complex):
            return self.__real == other.real and self.__imag == other.imag
        if isinstance(other, Integer):
            return self.__imag == 0 and self.__real == other.value
        return False

    def __repr__(self):
        return "Complex(" + str(self.__real) + ", " + str(self.__imag) + ")"


# ======================= Matrix =======================
class Matrix(AlgebraicElement):
    def __init__(self, rows: int, cols: int, elements: list):
        if type(rows) is not int or type(cols) is not int:
            raise TypeError("rows and cols must be int")
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive")
        if type(elements) is not list:
            raise TypeError("elements must be a list")
        if len(elements) != rows * cols:
            raise ValueError("number of elements must be rows * cols")
        for e in elements:
            if not isinstance(e, (Integer, Complex)):
                raise TypeError("elements must be Integer or Complex")
        self.__rows = rows
        self.__cols = cols
        self.__elements = list(elements)       # کپی می‌گیریم

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    @property
    def elements(self):
        return tuple(self.__elements)          # tuple قابل‌تغییر نیست

    # ---------- متدهای ایستا ----------
    @staticmethod
    def make_unit_matrix(n):
        if type(n) is not int:
            raise TypeError("n must be int")
        if n <= 0:
            raise ValueError("n must be positive")
        elements = []
        for i in range(n):
            for j in range(n):
                if i == j:
                    elements.append(Integer(1))
                else:
                    elements.append(Integer(0))
        return Matrix(n, n, elements)

    @staticmethod
    def get_ith_row(matrix, i):
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be a Matrix")
        if i < 0 or i >= matrix.rows:
            raise IndexError("row index out of range")
        row = []
        for j in range(matrix.cols):
            row.append(matrix.elements[i * matrix.cols + j])
        return row

    @staticmethod
    def get_ith_col(matrix, j):
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be a Matrix")
        if j < 0 or j >= matrix.cols:
            raise IndexError("column index out of range")
        col = []
        for i in range(matrix.rows):
            col.append(matrix.elements[i * matrix.cols + j])
        return col

    @staticmethod
    def is_zero_matrix(matrix):
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be a Matrix")
        for e in matrix.elements:
            if e != Integer(0):
                return False
        return True

    @staticmethod
    def is_unit_matrix(matrix):
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be a Matrix")
        if matrix.rows != matrix.cols:
            return False
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                e = matrix.elements[i * matrix.cols + j]
                if i == j and e != Integer(1):
                    return False
                if i != j and e != Integer(0):
                    return False
        return True

    @staticmethod
    def is_top_triangular_matrix(matrix):
        # بالامثلثی: زیر قطر (i > j) همه صفر
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be a Matrix")
        if matrix.rows != matrix.cols:
            return False
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                if i > j and matrix.elements[i * matrix.cols + j] != Integer(0):
                    return False
        return True

    @staticmethod
    def is_bottom_triangular_matrix(matrix):
        # پایین‌مثلثی: بالای قطر (i < j) همه صفر
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be a Matrix")
        if matrix.rows != matrix.cols:
            return False
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                if i < j and matrix.elements[i * matrix.cols + j] != Integer(0):
                    return False
        return True

    # ---------- متد کلاسی ----------
    @classmethod
    def make_matrix_from_string(cls, elements: str):
        if type(elements) is not str:
            raise TypeError("elements must be str")
        if elements.strip() == "":
            raise ValueError("empty string")
        all_elements = []
        n_cols = None
        row_texts = elements.split(";")
        for row_text in row_texts:
            tokens = row_text.split()          # جدا کردن با فاصله
            if len(tokens) == 0:
                raise ValueError("empty row")
            if n_cols is None:
                n_cols = len(tokens)
            elif len(tokens) != n_cols:
                raise ValueError("rows have different lengths")
            for t in tokens:
                if t.endswith("i"):
                    all_elements.append(Complex.from_string(t))
                else:
                    all_elements.append(Integer.from_string(t))
        return cls(len(row_texts), n_cols, all_elements)

    # ---------- عملگرها ----------
    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        return (self.rows == other.rows and self.cols == other.cols
                and self.elements == other.elements)

    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("matrices must have the same shape")
            new = []
            for k in range(len(self.elements)):
                new.append(self.elements[k] + other.elements[k])
            return Matrix(self.rows, self.cols, new)
        if isinstance(other, (Integer, Complex)):
            new = []
            for e in self.elements:
                new.append(e + other)
            return Matrix(self.rows, self.cols, new)
        raise TypeError("bad operand for +")

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("inner dimensions do not match")
            new = []
            for i in range(self.rows):
                row = Matrix.get_ith_row(self, i)
                for j in range(other.cols):
                    col = Matrix.get_ith_col(other, j)
                    total = Integer(0)
                    for k in range(len(row)):
                        total = total + row[k] * col[k]
                    new.append(total)
            return Matrix(self.rows, other.cols, new)
        if isinstance(other, (Integer, Complex)):
            new = []
            for e in self.elements:
                new.append(e * other)
            return Matrix(self.rows, self.cols, new)
        raise TypeError("bad operand for *")

    def __neg__(self):
        new = []
        for e in self.elements:
            new.append(-e)
        return Matrix(self.rows, self.cols, new)

    def __repr__(self):
        return "Matrix(" + str(self.rows) + ", " + str(self.cols) + ", " + str(list(self.elements)) + ")"


# ======================= تابع مستقل =======================
def multiply(a, b):
    return a * b
