import ast
import os
from collections import Counter


class ProjectAnalyzer:
    """Analyze Python source files without executing them."""

    def __init__(self, project_path):
        self.project_path = os.path.abspath(project_path)

    def _python_files(self):
        if not os.path.exists(self.project_path):
            raise FileNotFoundError(
                "The specified path does not exist."
            )

        if not os.path.isdir(self.project_path):
            raise NotADirectoryError(
                "The specified path is not a directory."
            )

        ignored_folders = {
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            "node_modules"
        }

        for root, folders, files in os.walk(self.project_path):
            folders[:] = [
                folder
                for folder in folders
                if folder not in ignored_folders
            ]

            for filename in files:
                if filename.endswith(".py"):
                    yield os.path.join(root, filename)

    @staticmethod
    def _analyze_file(path):
        with open(path, "r", encoding="utf-8") as file:
            source = file.read()

        lines = source.splitlines()

        non_empty_lines = [
            line for line in lines
            if line.strip()
        ]

        try:
            tree = ast.parse(source)
            syntax_error = None

        except SyntaxError as error:
            tree = None
            syntax_error = (
                f"{error.msg} (line {error.lineno})"
            )

        if tree is None:
            return {
                "lines": len(lines),
                "code_lines": len(non_empty_lines),
                "functions": 0,
                "classes": 0,
                "imports": [],
                "todos": sum(
                    "TODO" in line.upper()
                    for line in lines
                ),
                "syntax_error": syntax_error
            }

        functions = 0
        classes = 0
        imports = []

        for node in ast.walk(tree):

            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                functions += 1

            elif isinstance(node, ast.ClassDef):
                classes += 1

            elif isinstance(node, ast.Import):
                imports.extend(
                    alias.name.split(".")[0]
                    for alias in node.names
                )

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(
                        node.module.split(".")[0]
                    )

        return {
            "lines": len(lines),
            "code_lines": len(non_empty_lines),
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "todos": sum(
                "TODO" in line.upper()
                for line in lines
            ),
            "syntax_error": None
        }

    def analyze(self):
        files = []

        total_lines = 0
        total_code_lines = 0
        total_functions = 0
        total_classes = 0
        total_todos = 0

        import_counter = Counter()
        syntax_errors = []

        for path in self._python_files():

            relative_path = os.path.relpath(
                path,
                self.project_path
            )

            data = self._analyze_file(path)

            files.append({
                "file": relative_path,
                **data,
                "imports": sorted(
                    set(data["imports"])
                )
            })

            total_lines += data["lines"]
            total_code_lines += data["code_lines"]
            total_functions += data["functions"]
            total_classes += data["classes"]
            total_todos += data["todos"]

            import_counter.update(
                data["imports"]
            )

            if data["syntax_error"]:
                syntax_errors.append({
                    "file": relative_path,
                    "error": data["syntax_error"]
                })

        files.sort(
            key=lambda item: item["code_lines"],
            reverse=True
        )

        return {
            "project": os.path.basename(
                self.project_path
            ),
            "path": self.project_path,
            "python_files": len(files),
            "total_lines": total_lines,
            "code_lines": total_code_lines,
            "functions": total_functions,
            "classes": total_classes,
            "todos": total_todos,
            "top_imports": import_counter.most_common(10),
            "syntax_errors": syntax_errors,
            "files": files
        }
