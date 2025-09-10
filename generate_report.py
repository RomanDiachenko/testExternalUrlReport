import xmltodict
from pathlib import Path

# Шлях до результатів
xml_file = Path('report.xml')
report_file = Path('report/index.html')

# Читаємо XML
with open(xml_file, 'r') as f:
    data = xmltodict.parse(f.read())

tests = data['testsuite']['testcase']
if not isinstance(tests, list):
    tests = [tests]

# Створюємо HTML
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Test Report</title>
<style>
body { font-family: Arial; padding: 20px; background: #f0f0f0; }
h1 { text-align: center; }
table { width: 100%; border-collapse: collapse; margin-top: 20px; }
th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
th { background: #eee; }
.success { background-color: #c8f7c5; }
.failure { background-color: #f7c5c5; }
</style>
</head>
<body>
<h1>Test Report</h1>
<table>
<tr><th>Test Name</th><th>Status</th><th>Message</th></tr>
"""

for t in tests:
    name = t['@name']
    if 'failure' in t:
        status = 'FAILURE'
        msg = t['failure']['@message']
        row_class = 'failure'
    else:
        status = 'SUCCESS'
        msg = ''
        row_class = 'success'

    html_content += f"<tr class='{row_class}'><td>{name}</td><td>{status}</td><td>{msg}</td></tr>\n"

html_content += """
</table>
</body>
</html>
"""

# Записуємо HTML
report_file.parent.mkdir(exist_ok=True)
with open(report_file, 'w') as f:
    f.write(html_content)

print(f"Report generated at {report_file}")
