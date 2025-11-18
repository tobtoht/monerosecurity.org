#!/usr/bin/env python3
import os
import shutil
try:
    import yaml
except:
    print("pyyaml is not installed")
    exit(1)

with open("data.yaml") as f:
    data = yaml.safe_load(f.read())

tbody = ""

wallets = ["cli", "gui", "feather"]

for section_name in data:
    section = data[section_name]
    if len(section) < 1:
        continue

    first_row = True

    for row_name in section:
        row = section[row_name]

        section_header = ""
        if first_row:
            section_header = f'<th scope="row" rowspan="{len(section)}">{section_name}</th>'
            first_row = False

        row_header = row_name

        if "link" in row:
            row_header = f'<a href="{row['link']}">{row_header}</a>'

        row_header = f'<th>{row_header}</th>'

        if not all(x in row for x in wallets):
            print(f"Missing keys for row: {row_name}")
            continue

        rows = ""
        for wallet in wallets:
            cell = row[wallet]

            link_key = f'{wallet}.link'
            if link_key in row:
                cell = f'<a href="{row[link_key]}">{cell}</a>'

            rows += f'<td>{cell}</td>'

        tbody += f'<tr>{section_header}{row_header}{rows}</tr>'

with open("index.html") as f:
    html = f.read()

html = html.replace('{tbody}', tbody)

if not os.path.exists("out"):
    os.mkdir("out")

with open("out/index.html", "w") as f:
    f.write(html)

shutil.copy("main.css", "out")
