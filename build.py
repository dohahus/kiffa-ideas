#!/usr/bin/env python3
"""يبني index.html من app.template.html.

الوضع الافتراضي: يربط الخطوط كملفات منفصلة داخل fonts/ — أخف وأسرع،
لأن المتصفح يحمّلها بالتوازي ويخزّنها فلا تتكرر في كل زيارة.

    python3 build.py

الوضع المدمج: يدسّ الخطوط داخل الـ HTML كـ base64 فينتج ملفًا واحدًا
يعمل بلا إنترنت ولا ملفات مجاورة — للاستخدام من الجهاز مباشرة.

    python3 build.py --inline    →  kiffa-offline.html
"""
import base64, pathlib, sys

HERE = pathlib.Path(__file__).parent

FACES = [
    ("Frutiger LT Arabic", 400, "frutiger-400.woff2"),
    ("Frutiger LT Arabic", 700, "frutiger-700.woff2"),
    ("Frutiger LT Arabic", 900, "frutiger-900.woff2"),
    ("Lato",               400, "lato-400.woff2"),
    ("Lato",               900, "lato-900.woff2"),
]

# تُحمَّل مبكرًا لأنها تظهر في أول شاشة: المتن، العناوين، والأرقام الكبيرة
PRELOAD = {"frutiger-400.woff2", "frutiger-900.woff2", "lato-900.woff2"}

FACE = ('@font-face{font-family:"%s";font-style:normal;font-weight:%d;'
        'font-display:swap;src:url(%s) format("woff2")}')


def font_css(inline):
    out = []
    for family, weight, fname in FACES:
        if inline:
            b64 = base64.b64encode((HERE / "fonts" / fname).read_bytes()).decode()
            src = "data:font/woff2;base64," + b64
        else:
            src = "fonts/" + fname
        out.append(FACE % (family, weight, src))
    return "\n".join(out)


def preload_tags(inline):
    if inline:
        return ""
    return "\n".join(
        '<link rel="preload" href="fonts/%s" as="font" type="font/woff2" crossorigin>' % f
        for _, _, f in FACES if f in PRELOAD
    )


def main():
    inline = "--inline" in sys.argv
    html = (HERE / "app.template.html").read_text(encoding="utf-8")
    html = html.replace("/*FONT_CSS*/", font_css(inline))
    html = html.replace("<!--PRELOAD-->", preload_tags(inline))
    html = html.replace("<!--MARK-->", (HERE / "mark.svg").read_text(encoding="utf-8").strip())

    out = HERE / ("kiffa-offline.html" if inline else "index.html")
    out.write_text(html, encoding="utf-8")
    print("%s → %.0f KB%s" % (out.name, out.stat().st_size / 1024,
                              "" if inline else "  (+ fonts/ %.0f KB, تُخزَّن في المتصفح)"
                              % (sum((HERE / "fonts" / f).stat().st_size for _, _, f in FACES) / 1024)))


if __name__ == "__main__":
    sys.exit(main())
