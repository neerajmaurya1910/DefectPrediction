
import re


def calculate_software_metrics(code):
    """
    Calculate basic source-code metrics for Java code.

    These are source-based estimates, not a full Java parser.
    """

    lines = code.splitlines()

    # Remove blank lines for the non-blank line count
    non_blank_lines = [
        line for line in lines if line.strip()
    ]

    # Count comment lines (basic Java // and /* */ handling)
    comment_lines = 0
    inside_block_comment = False

    for line in lines:
        stripped = line.strip()

        if inside_block_comment:
            comment_lines += 1
            if "*/" in stripped:
                inside_block_comment = False
            continue

        if stripped.startswith("//"):
            comment_lines += 1
        elif "/*" in stripped:
            comment_lines += 1
            if "*/" not in stripped[stripped.find("/*") + 2:]:
                inside_block_comment = True

    total_lines = len(lines)
    non_blank_count = len(non_blank_lines)
    loc = sum(
        1 for line in lines
        if line.strip() and not line.strip().startswith("//")
    )

    comment_percentage = (
        round((comment_lines / total_lines) * 100, 2)
        if total_lines else 0.0
    )

    # Estimate Java method count using method-like declarations.
    # Constructors are included; control statements are excluded.
    method_pattern = re.compile(
        r"^\s*(?:(?:public|private|protected|static|final|"
        r"synchronized|native|abstract|default)\s+)*"
        r"[\w<>\[\], ?]+\s+\w+\s*\([^;{}]*\)\s*"
        r"(?:throws\s+[\w, ]+\s*)?\{"
    )

    method_count = sum(
        1 for line in lines
        if method_pattern.search(line)
        and not re.match(
            r"^\s*(if|for|while|switch|catch|synchronized)\s*\(",
            line
        )
    )

    
    # Estimate cyclomatic complexity using decision keywords.
    # This is a lexical estimate, not control-flow graph analysis.
    # Remove comments and string literals to avoid counting keywords inside them.
    cleaned_code = re.sub(r'//.*|/\*[\s\S]*?\*/', '', code)
    cleaned_code = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '""', cleaned_code)

    decision_pattern = re.compile(
        r"\b(if|for|while|case|catch)\b|&&|\|\||\?"
    )

    complexity = 1 + len(decision_pattern.findall(cleaned_code))


    return {
        "total_lines": total_lines,
        "non_blank_lines": non_blank_count,
        "loc": loc,
        "comment_lines": comment_lines,
        "comment_percentage": comment_percentage,
        "method_count": method_count,
        "cyclomatic_complexity_estimate": complexity
    }


if __name__ == "__main__":
    sample_code = """
public class Example {
    // Check whether a number is positive
    public int checkNumber(int n) {
        if (n > 0) {
            return 1;
        } else {
            return -1;
        }
    }
}
"""

    metrics = calculate_software_metrics(sample_code)

    print("\\n===== SOFTWARE METRICS =====")
    for name, value in metrics.items():
        print(f"{name}: {value}")
