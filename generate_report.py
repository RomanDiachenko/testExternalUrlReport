from junitparser import JUnitXml
from pathlib import Path

xml_file = Path("report.xml")
html_file = Path("report/index.html")

# читаємо pytest результат
xml = JUnitXml.fromfile(xml_file)

# генеруємо HTML
html_file.parent.mkdir(exist_ok=True)
with open(html_file, "w") as f:
    f.write("<html><head><title>Healthcheck Report</title>")
    f.write("<style>body{font-family:sans-serif;} .ok{color:green;} .fail{color:red;}</style>")
    f.write("</head><body>")
    f.write("<h1>Healthcheck Results</h1><ul>")

    for suite in xml:
        for case in suite:
            if case.result:
                status = '<span class="fail">FAILED</span>'
            else:
                status = '<span class="ok">ALIVE</span>'
            f.write(f"<li>{case.name} → {status}</li>")

    f.write("</ul></body></html>")
