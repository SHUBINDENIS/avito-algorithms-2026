import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from runpy import run_path

tracer = run_path(str(Path(__file__).with_name("solution.py")))["tracer"]


class TracerTest(unittest.TestCase):
    def test_recursive_call_stack(self):
        @tracer
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)

        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(factorial(3), 6)
        self.assertEqual(output.getvalue().splitlines(), [
            "-> factorial(3)", "  -> factorial(2)",
            "    -> factorial(1)", "    <- factorial = 1",
            "  <- factorial = 2", "<- factorial = 6",
        ])

    def test_arguments_and_metadata(self):
        @tracer
        def greet(name, *, mark="!"):
            """Build a greeting."""
            return name + mark

        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(greet("Ann", mark="?"), "Ann?")
        self.assertEqual(greet.__name__, "greet")
        self.assertEqual(greet.__doc__, "Build a greeting.")
        self.assertIn("greet('Ann', mark='?')", output.getvalue())

    def test_exception_restores_depth(self):
        @tracer
        def fail(n):
            if n == 0:
                raise ValueError("stop")
            return fail(n - 1)

        output = io.StringIO()
        with redirect_stdout(output):
            with self.assertRaisesRegex(ValueError, "stop"):
                fail(1)
            with self.assertRaises(ValueError):
                fail(0)
        lines = output.getvalue().splitlines()
        self.assertEqual(lines[-2], "-> fail(0)")
        self.assertEqual(lines[-1], "!! fail: ValueError('stop')")

    def test_different_decorated_functions_share_stack_depth(self):
        @tracer
        def inner():
            return None

        @tracer
        def outer():
            return inner()

        output = io.StringIO()
        with redirect_stdout(output):
            self.assertIsNone(outer())
        self.assertEqual(output.getvalue().splitlines(), [
            "-> outer()", "  -> inner()", "  <- inner = None", "<- outer = None",
        ])

    def test_repeated_calls_start_at_zero_depth(self):
        @tracer
        def one():
            return 1

        output = io.StringIO()
        with redirect_stdout(output):
            one()
            one()
        self.assertEqual(output.getvalue().splitlines()[2], "-> one()")


if __name__ == "__main__":
    unittest.main()
