# DISCS Bento Template

A [Bento Slides](https://bento.page) theme for Ateneo DISCS, matching the
[DISCS Slidev theme](https://github.com/zzenonn/discs-slidev-template): blue
`#00b0f0` and white, Roboto titles, Roboto Condensed body text, Fira Code for
code, and the DISCS footer.

A Bento deck is one self-contained HTML file. It opens in any browser with no
install, and it is its own editor: press **Esc** to edit, **S** for the
speaker view, **Ctrl/⌘ S** to save the file in place.

## Use it

1. Download [`discs-template.bento.html`](discs-template.bento.html) and open
   it in a browser.
2. **Save as…** a new file, then edit the text in place. New slides can use
   the four DISCS layouts from the slide menu.

The fonts and the logo are embedded in the file, so it looks the same on any
machine.

## Layouts

| Layout  | Use it for                                                         |
| ------- | ------------------------------------------------------------------ |
| Cover   | the first slide: full-width blue title bar, subtitle, author, date, subject and course |
| Section | a divider between parts: centred blue bar                          |
| Default | every content slide: title, content, footer with page number, DISCS logo and department name |
| End     | the last slide: centred blue bar                                   |

The template file shows each layout, plus a code slide and a table slide.

## Text sizes

Sizes are for the 1280×720 slide. They are sized to be read from the back of a
classroom; keep to them so decks match.

- Slide titles: 50px (cover 60, section 58, end 64)
- Subtitles: 34–38px
- Body text and bullets: 32–36px, line height 1.4
- Tables: 28–30px (theme default 28)
- Code: 20–28px, 24 by default; size the panel with `code_h()` so every line fits
- Captions and labels: 22–28px
- Footer: 12–16px (unchanged)

`tools/discs.py` uses these as its defaults. Run `tools/check.py` after any change:
it fails a slide if text does not fit its box or a code block is clipped.

## Build decks from code

`tools/discs.py` has the theme, fonts and layouts as Python helpers. A deck is
a Python script that lists slides; `write()` puts them into the Bento shell.

```bash
python3 tools/build_template.py discs-template.bento.html
```

`tools/check.py` opens a deck in a headless browser (Python
[Playwright](https://playwright.dev/python/)), runs Bento's own validator,
checks that the embedded fonts loaded, and saves a screenshot of every slide:

```bash
pip install playwright && playwright install chromium
python3 tools/check.py discs-template.bento.html shots/
```

## Agent skill

`skills/bento-slides/SKILL.md` is the Bento Slides agent skill: the document
format, layout rules and checks an AI agent follows when it writes a Bento
deck. Copy it into your agent's skills folder to use it.

## What is in here

| Path                       | What it is                                         |
| -------------------------- | -------------------------------------------------- |
| `discs-template.bento.html` | the template deck                                  |
| `tools/discs.py`           | theme, fonts, layouts and element helpers          |
| `tools/build_template.py`  | builds the template deck                           |
| `tools/check.py`           | headless validation and screenshots                |
| `tools/shell.bento.html`   | the empty Bento Slides shell the decks are built on |
| `fonts/`                   | Roboto, Roboto Condensed and Fira Code (SIL Open Font License 1.1) |
| `assets/discs-logo.png`    | the DISCS logo                                     |
| `skills/bento-slides/`     | the Bento Slides agent skill                       |

## Licences

- Bento Slides (the shell): MIT License, © 2026 The Bento authors. Its
  third-party notices travel inside every deck.
- Roboto, Roboto Condensed and Fira Code: SIL Open Font License 1.1; see
  `fonts/`.
