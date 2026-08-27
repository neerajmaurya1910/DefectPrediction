import re


def analyze_java_code(code):

    issues = []

    # ==============================
    # DIVISION BY ZERO RISK
    # ==============================

    if re.search(r'/\s*[a-zA-Z_][a-zA-Z0-9_]*', code):
        issues.append({
            "type": "Potential Runtime Error",
            "message": "Possible division by zero.",
            "severity": "HIGH"
        })

    # ==============================
    # NULL CHECK
    # ==============================

    if "== null" not in code and "!= null" not in code:
        if re.search(r'\.\w+\(', code):
            issues.append({
                "type": "Null Safety",
                "message": "Object method is called without an obvious null check.",
                "severity": "MEDIUM"
            })

    # ==============================
    # SYSTEM.OUT.PRINTLN
    # ==============================

    if "System.out.println" in code:
        issues.append({
            "type": "Code Quality",
            "message": "System.out.println found. Consider using a logging framework.",
            "severity": "LOW"
        })

    # ==============================
    # EMPTY CATCH
    # ==============================

    if re.search(r'catch\s*\([^)]*\)\s*\{\s*\}', code):
        issues.append({
            "type": "Exception Handling",
            "message": "Empty catch block detected.",
            "severity": "HIGH"
        })

    # ==============================
    # TODO
    # ==============================

    if "TODO" in code:
        issues.append({
            "type": "Code Quality",
            "message": "TODO comment found.",
            "severity": "LOW"
        })

    return issues


# ==============================
# TEST
# ==============================

if __name__ == "__main__":

    code = """
    public int divide(int a, int b) {
        System.out.println("Dividing");
        return a / b;
    }
    """

    results = analyze_java_code(code)

    print("\n===== STATIC ANALYSIS =====")

    if not results:
        print("No issues found.")

    else:
        for issue in results:
            print(f"[{issue['severity']}] "
                  f"{issue['type']}: "
                  f"{issue['message']}")