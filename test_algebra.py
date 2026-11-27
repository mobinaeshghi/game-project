import unittest

from algebra import AlgebraicElement, Integer, Complex, Matrix, multiply


def M(s):
    return Matrix.make_matrix_from_string(s)


# ======================= بخش ۱ =======================
class TestPart1(unittest.TestCase):
    def test_abstract_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            AlgebraicElement()

    def test_inheritance(self):
        for obj in (Integer(1), Complex(1, 2), M("1 2; 3 4")):
            self.assertIsInstance(obj, AlgebraicElement)
        self.assertNotIsInstance(M("1"), (Integer, Complex))

    def test_integer_operations_return_integer(self):
        s = Integer(3) + Integer(4)
        p = Integer(3) * Integer(4)
        self.assertIsInstance(s, Integer)
        self.assertIsInstance(p, Integer)
        self.assertEqual(s.value, 7)
        self.assertEqual(p.value, 12)
        self.assertEqual((-Integer(5)).value, -5)

    def test_complex_operations(self):
        self.assertEqual(Complex(1, 2) + Complex(3, 4), Complex(4, 6))
        self.assertEqual(Complex(1, 2) * Complex(3, 4), Complex(-5, 10))
        self.assertEqual(-Complex(1, -2), Complex(-1, 2))

    def test_mixed_result_is_complex_even_if_imag_zero(self):
        r = Integer(3) + Complex(2, 0)
        self.assertIsInstance(r, Complex)
        self.assertEqual(r, Complex(5, 0))
        self.assertIsInstance(Integer(2) * Complex(0, 0), Complex)

    def test_equality_between_integer_and_complex(self):
        self.assertTrue(Integer(3) == Complex(3, 0))
        self.assertTrue(Complex(3, 0) == Integer(3))
        self.assertFalse(Integer(3) == Complex(3, 1))

    def test_from_string_valid(self):
        self.assertEqual(Integer.from_string("-12"), Integer(-12))
        self.assertEqual(Integer.from_string("+7"), Integer(7))
        self.assertEqual(Complex.from_string("5+2i"), Complex(5, 2))
        self.assertEqual(Complex.from_string("-3-4i"), Complex(-3, -4))
        self.assertEqual(Complex.from_string("0-2i"), Complex(0, -2))

    def test_from_string_invalid(self):
        with self.assertRaises(ValueError):
            Integer.from_string("abc")
        with self.assertRaises(ValueError):
            Complex.from_string("2i")
        with self.assertRaises(TypeError):
            Integer.from_string(5)

    def test_constructor_type_checks_and_bool_rejected(self):
        with self.assertRaises(TypeError):
            Integer(True)
        with self.assertRaises(TypeError):
            Integer(2.5)
        with self.assertRaises(TypeError):
            Complex(1, False)
        with self.assertRaises(TypeError):
            Complex("1", 2)

    def test_properties_are_read_only(self):
        x = Integer(1)
        with self.assertRaises(AttributeError):
            x.value = 5
        c = Complex(1, 2)
        with self.assertRaises(AttributeError):
            c.real = 5

    def test_sub_is_inherited_not_overridden(self):
        for cls in (Integer, Complex, Matrix):
            self.assertIs(cls.__sub__, AlgebraicElement.__sub__)
        self.assertEqual(Integer(8) - Integer(5), Integer(3))
        self.assertEqual(Complex(5, 5) - Integer(2), Complex(3, 5))

    def test_operands_not_modified(self):
        a, b = Integer(2), Complex(1, 1)
        _ = a + b, a * b, -a, a - b
        self.assertEqual(a, Integer(2))
        self.assertEqual(b, Complex(1, 1))


# ======================= بخش ۲ =======================
class TestPart2(unittest.TestCase):
    def test_constructor_valid_and_row_major(self):
        m = Matrix(2, 3, [Integer(i) for i in range(1, 7)])
        self.assertEqual((m.rows, m.cols), (2, 3))
        self.assertEqual(Matrix.get_ith_row(m, 1),
                         [Integer(4), Integer(5), Integer(6)])

    def test_constructor_invalid(self):
        with self.assertRaises(ValueError):
            Matrix(2, 2, [Integer(1)])
        with self.assertRaises(ValueError):
            Matrix(0, 2, [])
        with self.assertRaises(TypeError):
            Matrix(1, 1, [3])
        with self.assertRaises(TypeError):
            Matrix(1.0, 1, [Integer(1)])

    def test_elements_is_tuple_and_safe(self):
        lst = [Integer(1), Integer(2)]
        m = Matrix(1, 2, lst)
        lst.append(Integer(99))
        self.assertIsInstance(m.elements, tuple)
        self.assertEqual(len(m.elements), 2)
        with self.assertRaises(AttributeError):
            m.elements = ()

    def test_make_unit_matrix(self):
        u = Matrix.make_unit_matrix(3)
        self.assertTrue(Matrix.is_unit_matrix(u))
        self.assertTrue(all(isinstance(e, Integer) for e in u.elements))
        with self.assertRaises(ValueError):
            Matrix.make_unit_matrix(0)

    def test_get_row_col_and_index_errors(self):
        m = M("1 2 3; 4 5 6")
        self.assertEqual(Matrix.get_ith_row(m, 0),
                         [Integer(1), Integer(2), Integer(3)])
        self.assertEqual(Matrix.get_ith_col(m, 2), [Integer(3), Integer(6)])
        with self.assertRaises(IndexError):
            Matrix.get_ith_row(m, 2)
        with self.assertRaises(IndexError):
            Matrix.get_ith_col(m, -1)
        with self.assertRaises(TypeError):
            Matrix.get_ith_row("not matrix", 0)

    def test_is_zero_matrix(self):
        z = Matrix(2, 2, [Complex(0, 0), Integer(0), Integer(0), Complex(0, 0)])
        self.assertTrue(Matrix.is_zero_matrix(z))
        self.assertFalse(Matrix.is_zero_matrix(M("0 0; 0 1")))
        with self.assertRaises(TypeError):
            Matrix.is_zero_matrix(5)

    def test_is_unit_matrix(self):
        self.assertTrue(Matrix.is_unit_matrix(M("1 0; 0 1")))
        self.assertFalse(Matrix.is_unit_matrix(M("1 0; 1 1")))
        self.assertFalse(Matrix.is_unit_matrix(M("1 0 0; 0 1 0")))  # نامربعی

    def test_triangular(self):
        upper = M("1 2 3; 0 4 5; 0 0 6")
        lower = M("1 0 0; 2 3 0; 4 5 6")
        self.assertTrue(Matrix.is_top_triangular_matrix(upper))
        self.assertFalse(Matrix.is_bottom_triangular_matrix(upper))
        self.assertTrue(Matrix.is_bottom_triangular_matrix(lower))
        self.assertFalse(Matrix.is_top_triangular_matrix(lower))
        zero = M("0 0; 0 0")
        self.assertTrue(Matrix.is_top_triangular_matrix(zero))
        self.assertTrue(Matrix.is_bottom_triangular_matrix(zero))
        self.assertFalse(Matrix.is_top_triangular_matrix(M("1 2 3; 4 5 6")))

    def test_make_matrix_from_string(self):
        m = M("1 2 3; 4 5+2i 6")
        self.assertEqual((m.rows, m.cols), (2, 3))
        self.assertEqual(m.elements[4], Complex(5, 2))
        self.assertIsInstance(m.elements[0], Integer)

    def test_make_matrix_from_string_errors(self):
        for bad in ("", "   ", "1 2; 3", "1 2;; 3 4", "1 x; 3 4"):
            with self.assertRaises(ValueError, msg=repr(bad)):
                M(bad)
        with self.assertRaises(TypeError):
            M(123)

    def test_matrix_equality(self):
        self.assertEqual(M("1 2; 3 4"), M("1 2; 3 4"))
        self.assertNotEqual(M("1 2; 3 4"), M("1 2; 3 5"))
        self.assertNotEqual(M("1 2"), M("1; 2"))


# ======================= بخش ۳ =======================
class TestPart3(unittest.TestCase):
    def test_matrix_add_matrix(self):
        self.assertEqual(M("1 2; 3 4") + M("5 6; 7 8"), M("6 8; 10 12"))

    def test_matrix_add_shape_error(self):
        with self.assertRaises(ValueError):
            M("1 2") + M("1; 2")

    def test_add_scalar_both_orders(self):
        m = M("1 2; 3 4")
        self.assertEqual(m + Integer(2), M("3 4; 5 6"))
        self.assertEqual(Integer(2) + m, m + Integer(2))
        self.assertEqual(Complex(0, 1) + m, m + Complex(0, 1))
        r = m + Complex(0, 1)
        self.assertEqual(r.elements[0], Complex(1, 1))

    def test_matrix_multiplication(self):
        self.assertEqual(M("1 2; 3 4") * M("2 0; 1 2"), M("4 4; 10 8"))
        a = M("1 2 3; 4 5 6")      # 2x3
        b = M("1; 2; 3")           # 3x1
        self.assertEqual(a * b, M("14; 32"))

    def test_multiplication_is_not_commutative(self):
        a, b = M("1 2; 3 4"), M("2 0; 1 2")
        self.assertNotEqual(a * b, b * a)

    def test_multiplication_shape_error(self):
        with self.assertRaises(ValueError):
            M("1 2 3") * M("1 2 3")

    def test_scalar_multiplication_both_orders(self):
        m = M("1 2; 3 4")
        self.assertEqual(m * Integer(2), M("2 4; 6 8"))
        self.assertEqual(Integer(2) * m, m * Integer(2))
        self.assertEqual(Complex(0, 1) * m, m * Complex(0, 1))

    def test_matrix_with_complex_multiplication(self):
        a = M("0+1i 0; 0 0+1i")
        self.assertEqual(a * a, M("-1+0i 0; 0 -1+0i") )

    def test_identity_multiplication(self):
        m = M("1 2; 3 4")
        u = Matrix.make_unit_matrix(2)
        self.assertEqual(m * u, m)
        self.assertEqual(u * m, m)

    def test_neg_and_sub(self):
        m, n = M("5 6; 7 8"), M("1 2; 3 4")
        self.assertEqual(-m, M("-5 -6; -7 -8"))
        self.assertEqual(m - n, M("4 4; 4 4"))
        self.assertEqual(m - Integer(1), M("4 5; 6 7"))
        self.assertEqual(Integer(10) - n, M("9 8; 7 6"))
        self.assertEqual(Complex(1, 1) - Integer(1), Complex(0, 1))

    def test_type_errors_for_invalid_operands(self):
        m = M("1 2; 3 4")
        for bad in ("3", 3.0, 3, None):
            for obj in (Integer(1), Complex(1, 1), m):
                with self.assertRaises(TypeError):
                    obj + bad
                with self.assertRaises(TypeError):
                    obj * bad
                with self.assertRaises(TypeError):
                    obj - bad

    def test_operators_do_not_modify_operands(self):
        a, b = M("1 2; 3 4"), M("5 6; 7 8")
        _ = a + b, a * b, -a, a - b, a + Integer(1), a * Integer(3)
        self.assertEqual(a, M("1 2; 3 4"))
        self.assertEqual(b, M("5 6; 7 8"))

    def test_results_are_library_objects_not_raw_int(self):
        r = M("1 2; 3 4") * M("1 0; 0 1")
        self.assertTrue(all(isinstance(e, (Integer, Complex)) for e in r.elements))
        self.assertIsInstance(Integer(1) + Integer(1), Integer)

    def test_multiply_duck_typing(self):
        m = M("1 2; 3 4")
        self.assertEqual(multiply(m, Integer(2)), m * Integer(2))
        self.assertEqual(multiply(Integer(2), Integer(3)), Integer(6))
        self.assertEqual(multiply(m, m), m * m)
        # با نوع‌های غیر از کتابخانه هم کار می‌کند
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply("ab", 2), "abab")
        with self.assertRaises(TypeError):
            multiply(Integer(1), "3")


if __name__ == "__main__":
    unittest.main()
