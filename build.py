"""Genera index.html (página completa para GitHub Pages) a partir de src/app.html."""
src = open("src/app.html", encoding="utf-8").read()
head, body = src.split("<!--/head-->")
page = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
<style>:root{{color-scheme:light}} body{{margin:0}} [hidden]{{display:none!important}}</style>
</head>
<body>
{body}
</body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(page)
print("index.html generado", len(page), "bytes")
