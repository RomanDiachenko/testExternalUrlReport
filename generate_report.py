import xml.etree.ElementTree as ET
from pathlib import Path

def generate_html(results):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Service Healthcheck Report</title>
<style>
body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 40px; }
h1 { text-align: center; margin-bottom: 30px; }
table { width: 80%; margin: 0 auto; border-collapse: collapse; background: #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
th { background: #f3f3f3; }
.status { font-weight: bold; padding: 6px 12px; border-radius: 6px; color: white; text-align: center; }
.up { background: #28a745; }      /* зелений */
.down { background: #dc3545; }    /* червоний */
.warn { background: #ffc107; color: black; } /* жовтий */
</style>
</head>
<body>
<h1>Service Healthcheck Report</h1>
<table>
<tr><th>Your Services</th><th>Status</th></tr>
"""
    for test_name, status, message in results:
        if status == "passed":
            status_label = '<span class="status up">UP</span>'
        elif status == "failed":
            status_label = '<span class="status down">DOWN</span>'
        else:
            status_label = '<span class="status warn">WARN</span>'

        html += f"<tr><td>{test_name}</td><td>{status_label}</td></tr>\n"

    html += "</table></body></html>"
    return html

def parse_junit_report(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    results = []

    # pytest -> testsuite/testsuites
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")

    for suite in suites:
        for case in suite.findall("testcase"):
            name = case.get("name")
            failure = case.find("failure")
            error = case.find("error")

            if failure is not None or error is not None:
                results.append((name, "failed", "Test failed"))
            else:
                results.append((name, "passed", "All checks passed"))

    return results

if __name__ == "__main__":
    xml_path = Path("report.xml")
    if not xml_path.exists():
        raise FileNotFoundError("❌ report.xml not found. Run pytest with --junitxml=report.xml")

    results = parse_junit_report(xml_path)
    html = generate_html(results)

    Path("report").mkdir(exist_ok=True)
    with open("report/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ HTML report generated at report/index.html")
