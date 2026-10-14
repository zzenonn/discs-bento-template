import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from discs import *

S = [
    slide_cover("cover", "DISCS Bento Template", "A Bento Slides theme for Ateneo DISCS",
                "Your Name", "October 2026", "CSCI 60", "Data Communications and Networking",
                notes="Cover layout: blue title bar, subtitle, author and date, subject and course at the bottom. Edit the text in place."),
    slide_section("section", "Section Layout", "This is a section divider",
                  notes="Section layout: a centred blue bar. The bar morphs into the next section divider."),
    slide_default("default", "Default Layout",
                  (bullets(["Clean and minimalist design",
                            "Blue (#00b0f0) and white colour scheme",
                            "Roboto for titles, Roboto Condensed for body text",
                            "Footer: page number, DISCS logo and department name"]), 140, 300, 28),
                  notes="Default layout: title, content, footer. The footer elements keep the same ids on every slide, so they stay still while the content changes."),
    slide_default("code", "Code Example", (
        "Code uses Fira Code on a light grey panel, coloured like GitHub Light:", 130, 40, 24),
        extra=code("code-py", 'def hello_world():\n    print("Hello from DISCS!")\n    return True',
                   MX, 190, 560, 150, grammar="py", size=22)
        + code("code-js", 'const greet = () => {\n  console.log("Hello from DISCS!");\n  return true;\n};',
               MX, 370, 560, 180, grammar="js", size=22),
        notes="Code elements use the deck code palette. Put a rect panel behind each one."),
    slide_default("table", "Table Example", None, extra=[
        table("tbl", [["Layout", "Use it for"], ["Cover", "the first slide"],
                      ["Section", "a divider between parts"], ["Default", "every content slide"],
                      ["End", "the last slide"]], MX, 140, 760, 260, cols=[1, 2], size=24)],
        notes="Tables take the theme's table style: blue header, light zebra rows."),
    slide_end("end", "Thank You", "Questions?", notes="End layout: a centred blue bar."),
]
LAYOUTS = [as_layout(S[0], "discs-cover", "DISCS Cover"),
           as_layout(S[1], "discs-section", "DISCS Section"),
           as_layout(S[2], "discs-default", "DISCS Default"),
           as_layout(S[5], "discs-end", "DISCS End")]
d = doc("DISCS Bento Template", S, layouts=LAYOUTS,
        meta={"company": "Ateneo de Manila University", "subject": "DISCS"}, template=True)
write(d, sys.argv[1])
print("wrote", sys.argv[1])
