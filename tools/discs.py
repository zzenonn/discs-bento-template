"""DISCS Bento helpers: theme, fonts, layouts and element builders."""
import base64, json, math, os, re

W, H = 1280, 720
BLUE = "#00b0f0"
INK = "#404040"
GREY = "#666666"
PANEL = "#f5f5f5"
HEAD = "'Roboto', 'Helvetica Neue', Arial, sans-serif"
BODY = "'Roboto Condensed', 'Arial Narrow', Arial, sans-serif"
MONO = "'Fira Code', 'DejaVu Sans Mono', Menlo, Consolas, monospace"
MX = 64            # side margin (template: 3rem of a 980px slide, scaled to 1280)
CW = W - 2 * MX    # content width
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOGO = os.path.join(ROOT, "assets", "discs-logo.png")

FONT_FILES = [  # family, weight, file
    ("Roboto", "500", "roboto-latin-500-normal.woff2"),
    ("Roboto", "700", "roboto-latin-700-normal.woff2"),
    ("Roboto Condensed", "400", "roboto-condensed-latin-400-normal.woff2"),
    ("Roboto Condensed", "700", "roboto-condensed-latin-700-normal.woff2"),
    ("Fira Code", "400", "fira-code-latin-400-normal.woff2"),
]


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def fonts_and_assets():
    fonts, assets = [], {}
    for fam, wt, fn in FONT_FILES:
        key = "font-" + fam.lower().replace(" ", "-") + "-" + wt
        assets[key] = b64(os.path.join(ROOT, "fonts", fn), "font/woff2")
        fonts.append({"family": fam, "asset": key, "weight": wt})
    assets["discs-logo"] = b64(LOGO, "image/png")
    return fonts, assets


THEME = {
    "background": "#FFFFFF", "color": INK, "accent": BLUE,
    "fontFamily": BODY, "headingFamily": HEAD,
    "chartPalette": [BLUE, "#404040", "#7fd6f7", "#9e9e9e", "#0077a3", "#c8c8c8"],
    # github-light, as in the Slidev template's shiki setup
    "codePalette": {"c": "#6a737d", "s": "#032f62", "n": "#005cc5", "k": "#d73a49",
                    "f": "#6f42c1", "p": "#24292e", "a": "#22863a", "d": "#b31d28"},
    "table": {"headerBg": BLUE, "headerColor": "#FFFFFF", "zebra": "rgba(0,176,240,0.06)",
              "borderColor": "rgba(64,64,64,0.18)", "borderWidth": 1, "cellPadX": 14,
              "cellPadY": 10, "fontSize": 28, "color": INK, "radius": 0},
}


def base(eid, typ, x, y, w, h, **kw):
    e = {"id": eid, "type": typ, "x": x, "y": y, "w": w, "h": h, "rotation": 0, "opacity": 1}
    e.update(kw)
    return e


def text(eid, html, x, y, w, h, size=32, family=BODY, weight=400, color=INK,
         align="left", valign="top", lh=1.35, role=None, **kw):
    e = base(eid, "text", x, y, w, h, html=html, fontSize=size, fontFamily=family,
             fontWeight=weight, color=color, align=align, valign=valign, lineHeight=lh, **kw)
    if role:
        e["role"] = role
    return e


def rect(eid, x, y, w, h, fill=BLUE, stroke="none", sw=0, radius=0, **kw):
    return base(eid, "shape", x, y, w, h, shape="rect", fill=fill, stroke=stroke,
                strokeWidth=sw, radius=radius, **kw)


def ellipse(eid, x, y, w, h, fill="#FFFFFF", stroke=BLUE, sw=3, **kw):
    return base(eid, "shape", x, y, w, h, shape="ellipse", fill=fill, stroke=stroke,
                strokeWidth=sw, radius=0, **kw)


def line(eid, p1, p2, color=INK, sw=3, style="solid", **kw):
    """Straight line from point p1 to point p2 (x, y in slide pixels).

    Bento draws a line across the middle of its box, so the box is centred on the
    midpoint, as long as the segment, and rotated to its angle. (Connectors bound
    with from/to are not routed in the presenter, so geometry is set directly.)
    """
    (x1, y1), (x2, y2) = p1, p2
    L = math.hypot(x2 - x1, y2 - y1); h = max(10, sw * 3)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return base(eid, "shape", round(mx - L / 2), round(my - h / 2), round(L), h,
                shape="line", fill=color, stroke="none", strokeWidth=sw, radius=0,
                strokeStyle=style, **kw) | {"rotation": round(math.degrees(math.atan2(y2 - y1, x2 - x1)), 2)}


def code_h(content, size=24, lh=1.5):
    """Panel height that fits every line of content at this size."""
    return int((content.count("\n") + 1) * size * lh) + 28 + 8


def code(eid, content, x, y, w, h, grammar="sh", size=24, lh=1.5, panel=True):
    els = []
    if panel:
        els.append(rect(eid + "-panel", x, y, w, h, fill=PANEL, radius=8))
    els.append(base(eid, "code", x + 20, y + 14, w - 40, h - 28, content=content,
                    grammarName=grammar, fontSize=size, fontFamily=MONO, color="#24292e",
                    align="left", valign="top", lineHeight=lh))
    return els


def table(eid, rows, x, y, w, h, cols=None, size=28):
    st = dict(THEME["table"]); st["fontSize"] = size
    return base(eid, "table", x, y, w, h, header=True,
                columns=[{"w": c} for c in (cols or [1] * len(rows[0]))],
                rows=[{"cells": [{"html": c} for c in r]} for r in rows], style=st)


def bullets(items, sub=None):
    """items: list of str or (str, [sub items]) -> html with bullets."""
    out = []
    for it in items:
        if isinstance(it, tuple):
            out.append("•&nbsp; " + it[0])
            out += ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦&nbsp; " + s for s in it[1]]
        else:
            out.append("•&nbsp; " + it)
    return "<br>".join(out)


# ---- the four layouts of discs-slidev-template ----

def footer():
    return [
        rect("ft-rule", MX, 652, CW, 2, fill=BLUE),
        text("ft-page", "{{page}} / {{pages}}", MX, 666, 200, 30, size=16, color=GREY,
             valign="middle"),
        base("ft-logo", "image", W - MX - 236, 660, 28, 39, src="asset:discs-logo",
             fit="contain", radius=0),
        text("ft-text", "INFORMATION SYSTEMS &amp;<br>COMPUTER SCIENCE", W - MX - 200, 662, 200, 36,
             size=12, family=HEAD, weight=500, color=GREY, lh=1.3, valign="middle"),
    ]


def slide_cover(sid, title, subtitle, author="", date="", subject="DISCS",
                institution="Ateneo de Manila University", notes=""):
    els = [
        rect("cv-bar", 0, 170, W, 120, fill=BLUE),
        text("cv-title", title, MX, 170, CW, 120, size=60, family=HEAD, weight=700,
             color="#FFFFFF", align="center", valign="middle", lh=1.1, role="title"),
        text("cv-sub", subtitle, MX, 306, CW, 56, size=38, align="center", role="subtitle"),
        text("cv-author", author, MX, 378, CW, 40, size=28, align="center", role="body"),
        text("cv-date", date, MX, 420, CW, 36, size=26, color=GREY, align="center"),
        text("cv-subject", subject, MX, 540, CW, 62, size=52, family=HEAD, weight=700,
             color=BLUE, align="center", lh=1.1, role="kicker"),
        text("cv-inst", institution, MX, 604, CW, 36, size=26, align="center"),
    ]
    return {"id": sid, "background": "#FFFFFF", "transition": "fade", "unnumbered": True,
            "notes": notes, "elements": els}


def slide_section(sid, title, subtitle="", notes=""):
    els = [rect("sec-bar", 0, 290, W, 112, fill=BLUE),
           text("sec-title", title, MX, 290, CW, 112, size=58, family=HEAD, weight=700,
                color="#FFFFFF", align="center", valign="middle", lh=1.1, role="title")]
    if subtitle:
        els.append(text("sec-sub", subtitle, MX, 420, CW, 56, size=38, align="center",
                        role="subtitle"))
    return {"id": sid, "background": "#FFFFFF", "transition": "morph", "notes": notes,
            "elements": els}


def slide_default(sid, title, body=None, notes="", extra=(), transition="morph"):
    els = [text("df-title", title, MX, 40, CW, 70, size=50, family=HEAD, weight=700,
                lh=1.1, role="title")]
    if body is not None:
        html, y, h, size = body
        els.append(text("df-body", html, MX, y, CW, h, size=size, lh=1.4, role="body"))
    els += list(extra)
    els += footer()
    return {"id": sid, "background": "#FFFFFF", "transition": transition, "notes": notes,
            "elements": els}


def slide_end(sid, title="Thank You", subtitle="", notes=""):
    els = [rect("end-bar", 0, 290, W, 124, fill=BLUE),
           text("end-title", title, MX, 290, CW, 124, size=64, family=HEAD, weight=700,
                color="#FFFFFF", align="center", valign="middle", lh=1.1, role="title")]
    if subtitle:
        els.append(text("end-sub", subtitle, MX, 432, CW, 48, size=34, align="center",
                        role="subtitle"))
    return {"id": sid, "background": "#FFFFFF", "transition": "fade", "unnumbered": True,
            "notes": notes, "elements": els}


def as_layout(s, lid, name):
    """Turn a slide into an editor layout: text html -> placeholder."""
    s = json.loads(json.dumps(s))
    s["id"], s["name"] = lid, name
    for e in s["elements"]:
        if e["type"] == "text" and e.get("role"):
            e["placeholder"] = re.sub("<[^>]+>", " ", e["html"])
            e["html"] = ""
    return s


def doc(title, slides, layouts=None, meta=None, template=False):
    fonts, assets = fonts_and_assets()
    d = {"format": "bento/slides", "version": 1, "title": title,
         "size": {"width": W, "height": H}, "theme": THEME, "fonts": fonts, "assets": assets,
         "present": {"morphSeconds": 0.8, "slideNumber": False, "progress": True},
         "slides": slides}
    if layouts:
        d["layouts"] = layouts
    if meta:
        d["meta"] = meta
    if template:
        d["template"] = True
    return d


def write(d, out, shell=os.path.join(HERE, "shell.bento.html")):
    t = open(shell, encoding="utf-8").read()
    tag = '<script type="application/bento+json" id="bento-doc"></script>'
    assert t.count(tag) == 1, "shell block not found/empty"
    js = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    open(out, "w", encoding="utf-8").write(
        t.replace(tag, '<script type="application/bento+json" id="bento-doc">' + js + "</script>"))
    return out
