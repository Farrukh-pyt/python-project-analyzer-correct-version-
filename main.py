from analyzer import ProjectAnalyzer
from report import print_report, save_json_report


def main():
    print("=" * 60)
    print("PYTHON PROJECT ANALYZER")
    print("=" * 60)

    path = input("Enter the path to a Python project: ").strip()

    analyzer = ProjectAnalyzer(path)

    try:
        result = analyzer.analyze()
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        return

    print_report(result)

    answer = input("\nSave the report as JSON? (y/n): ").strip().lower()

    if answer == "y":
        output_file = "analysis_report.json"
        save_json_report(result, output_file)
        print(f"Report saved to: {output_file}")


if __name__ == "__main__":
    main()
