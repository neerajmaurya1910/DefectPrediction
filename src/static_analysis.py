
import re


def analyze_java_code(code):
    issues = []
    lines = code.splitlines()

    # DIVISION BY ZERO RISK
    for line_number, line in enumerate(lines, start=1):
        # Ignore comments so // TODO is not treated as division
        code_part = line.split("//", 1)[0]

        if re.search(r'/\s*[a-zA-Z_][a-zA-Z0-9_]*', code_part):
            issues.append({
                "type": "Potential Runtime Error",
                "message": "Possible division by zero.",
                "severity": "HIGH",
                "line": line_number,
                "code": line.strip()
            })

    # NULL SAFETY (simple heuristic)
    has_null_check = "== null" in code or "!= null" in code

    if not has_null_check:
        for line_number, line in enumerate(lines, start=1):
            if re.search(r'\.\w+\s*\(', line):
                issues.append({
                    "type": "Null Safety",
                    "message": (
                        "Object method is called without "
                        "an obvious null check."
                    ),
                    "severity": "MEDIUM",
                    "line": line_number,
                    "code": line.strip()
                })

    # SYSTEM.OUT.PRINTLN
    for line_number, line in enumerate(lines, start=1):
        if "System.out.println" in line:
            issues.append({
                "type": "Code Quality",
                "message": (
                    "System.out.println found. Consider "
                    "using a logging framework."
                ),
                "severity": "LOW",
                "line": line_number,
                "code": line.strip()
            })

    # EMPTY CATCH BLOCK (single-line form)
    for line_number, line in enumerate(lines, start=1):
        if re.search(r'catch\s*\([^)]*\)\s*\{\s*\}', line):
            issues.append({
                "type": "Exception Handling",
                "message": "Empty catch block detected.",
                "severity": "HIGH",
                "line": line_number,
                "code": line.strip()
            })

    # TODO
    for line_number, line in enumerate(lines, start=1):
        if "TODO" in line:
            issues.append({
                "type": "Code Quality",
                "message": "TODO comment found.",
                "severity": "LOW",
                "line": line_number,
                "code": line.strip()
            })

    return issues


if __name__ == "__main__":
    code = """
public class Test {
    public int divide(int a, int b) {
        System.out.println("Dividing");
        return a / b;
    }
}
"""

    results = analyze_java_code(code)

    print("\n===== STATIC ANALYSIS =====")

    if not results:
        print("No issues found.")
    else:
        for issue in results:
            print(
                f"[{issue['severity']}] "
                f"Line {issue['line']}: "
                f"{issue['type']}: "
                f"{issue['message']}"
            )
            print(f"    Code: {issue['code']}")
