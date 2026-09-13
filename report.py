import json


def print_report(result):

    print("\n" + "=" * 60)
    print(f"Project: {result['project']}")
    print("=" * 60)

    print(f"Python files : {result['python_files']}")
    print(f"Total lines  : {result['total_lines']}")
    print(f"Code lines   : {result['code_lines']}")
    print(f"Functions    : {result['functions']}")
    print(f"Classes      : {result['classes']}")
    print(f"TODO markers : {result['todos']}")

    print("\nTop imports:")

    if result["top_imports"]:

        for name, count in result["top_imports"]:
            print(
                f"  {name:<20} {count}"
            )

    else:
        print("  No imports found.")

    print("\nFiles:")

    if result["files"]:

        for item in result["files"]:

            if item["syntax_error"]:
                status = (
                    "SYNTAX ERROR: "
                    + item["syntax_error"]
                )
            else:
                status = "OK"

            print(
                f"  {item['file']:<35} "
                f"{item['code_lines']:>5} "
                f"code lines  {status}"
            )

    else:
        print("  No Python files found.")

    print("\nSyntax errors:")

    if result["syntax_errors"]:

        for error in result["syntax_errors"]:
            print(
                f"  {error['file']}: "
                f"{error['error']}"
            )

    else:
        print("  None detected.")


def save_json_report(result, filename):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )
