#!/usr/bin/env python3
"""يبني index.html المستقل: يدمج خطوط الهوية (woff2) وشعار كِفّة داخل الملف."""
import base64, pathlib, sys

HERE = pathlib.Path(__file__).parent

FACES = [
    ("Frutiger LT Arabic", 400, "frutiger-400.woff2"),
    ("Frutiger LT Arabic", 700, "frutiger-700.woff2"),
    ("Frutiger LT Arabic", 900, "frutiger-900.woff2"),
    ("Lato", 400, "lato-400.woff2"),
    ("Lato", 900, "lato-900.woff2"),
]

def font_css():
    out = []
    for family, weight, fname in FACES:
        b64 = base64.b64encode((HERE / fname).read_bytes()).decode()
        out.append(
            '@font-face{font-family:"%s";font-style:normal;font-weight:%d;font-display:swap;'
            'src:url(data:font/woff2;base64,%s) format("woff2")}' % (family, weight, b64)
        )
    return "\n".join(out)

def main():
    html = (HERE / "app.template.html").read_text(encoding="utf-8")
    html = html.replace("/*FONT_CSS*/", font_css())
    html = html.replace("<!--MARK-->", (HERE / "mark.svg").read_text(encoding="utf-8").strip())
    out = HERE / "index.html"
    out.write_text(html, encoding="utf-8")
    print("index.html →", f"{out.stat().st_size/1024:.0f} KB")

if __name__ == "__main__":
    sys.exit(main())
