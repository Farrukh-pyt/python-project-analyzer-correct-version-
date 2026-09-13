import os
import tempfile
import unittest

from analyzer import ProjectAnalyzer


class TestProjectAnalyzer(unittest.TestCase):

    def test_analyzes_python_file(self):

        with tempfile.TemporaryDirectory() as folder:

            path = os.path.join(
                folder,
                "example.py"
            )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "import math\n\n"
                    "class Calculator:\n"
                    "    def add(self, a, b):\n"
                    "        return a + b\n"
                )

            result = ProjectAnalyzer(folder).analyze()

            self.assertEqual(
                result["python_files"],
                1
            )

            self.assertEqual(
                result["classes"],
                1
            )

            self.assertEqual(
                result["functions"],
                1
            )

            self.assertIn(
                "math",
                [
                    name
                    for name, _ in result["top_imports"]
                ]
            )

    def test_detects_syntax_error(self):

        with tempfile.TemporaryDirectory() as folder:

            path = os.path.join(
                folder,
                "broken.py"
            )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "def broken(:\n"
                    "    pass\n"
                )

            result = ProjectAnalyzer(folder).analyze()

            self.assertEqual(
                len(result["syntax_errors"]),
                1
            )


if __name__ == "__main__":
    unittest.main()
