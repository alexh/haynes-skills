---
name: lisa-documents
description: Lisa's six house styles for good-looking documents, each a finished template with its own fonts. Use whenever Lisa asks for a document, checklist, plan, report, write-up, letter, notice, invitation, save-the-date, sign, handout, newsletter, notes, minutes or anything to print or send, or names a style ("the military one", "the red report", "the stamp one", "the art gallery one", "the old internet one", "the Word one"). Presets - report, field-order, proof-sheet, gallery, web-2002, word-doc.
license: MIT for the templates and script. Fonts are SIL Open Font License 1.1, see fonts/LICENSES.txt.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/finish.py *)
---

# Lisa's documents

Six finished templates ("presets"). Each one is a complete HTML document with sample content, its own type, colors, print layout, phone layout and dark mode. To make a new document, copy the right preset, swap in Lisa's content using the preset's own pieces, and run the finishing script. Never design from scratch and never restyle a preset: its typesetting is the reason Lisa uses it.

All paths below are relative to this skill's folder (`${CLAUDE_SKILL_DIR}`): `presets/`, `fonts/`, `scripts/`.

## 1. Pick the preset

| Preset | File | Use it for | Looks like |
|---|---|---|---|
| Report | `presets/report.html` | Write-ups, recommendations, decisions, anything comparing options or costs | Letter-size report in Lisa red: Raleway headings, Lato text, typewriter-style labels |
| Field order | `presets/field-order.html` | Step-by-step plans and checklists, event setup, anything done in phases by a group | A typed military operation order: stencil title, Courier, numbered paragraphs, checkboxes |
| Proof sheet | `presets/proof-sheet.html` | One-page notices: save-the-dates, invitations, announcements, signs, cover sheets | A printer's proof on lined paper, rotated stamp, two-line title |
| Gallery | `presets/gallery.html` | Essays, reflections, letters, collections of things (photos, recipes, heirlooms, books) | Minimalist museum wall text: Bodoni title, small captions, one red dot |
| 2002 web | `presets/web-2002.html` | Family updates, newsletters, blog-style posts, fun lists of links | A personal homepage from 2002: Verdana, sidebar boxes, hit counter, 88×31 buttons |
| Word doc | `presets/word-doc.html` | Plain everyday documents: notes, minutes, handouts, simple letters | A tidy Word file: Calibri-style text, Title and Heading styles in Word's Dark Red |

If Lisa names a style, use it. Otherwise pick the best fit, make the document, and say in one line which preset you used and that she can ask for another. Don't quiz her first.

## 2. Make the document

1. **Read the whole preset file** before writing. Its sample content shows every component in use.
2. **Copy it** to a new file named for the document, for example `thanksgiving-plan.html`, in the folder where you save files for Lisa.
3. **Replace the sample content** with hers:
   - Keep `<meta name="preset" ...>`, the `<!--FONTS-->...<!--/FONTS-->` block, the entire `<style>` block and any `<script>` at the end exactly as they are.
   - Build only from the preset's own classes and elements. Delete components she doesn't need; repeat the ones she does. Don't add new CSS, fonts, colors, sizes, icons or emoji.
   - Update `<title>` to the document's name.
4. **Finish it:**
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/finish.py thanksgiving-plan.html --pdf
   ```
   Use whichever Python the computer has (`python3`, `python`, or `uv run --no-project python`); the script needs nothing beyond the standard library. This writes `thanksgiving-plan.final.html` with every font built in (it works offline, in email, and prints exactly), plus `thanksgiving-plan.final.pdf` when Chrome or Playwright is available. Hand Lisa the `.final` files.
5. **Look at the result** if you can (open the PDF or take a screenshot) and fix what you see: text running off the page, a heading stranded at the bottom of a page, a stamp sitting on top of text.

If the script can't run, the working `.html` still looks right in a browser with an internet connection, except the proof sheet and the report's labels, which fall back to a plain monospace until finished.

## 3. Write it the way Lisa would

- Plain words and short sentences. Real dates, times, places, names and amounts.
- Don't invent facts. If something essential is missing (a date, an address, a price), ask once, or write `TBD` where it goes and say so.
- She's the author: "Prepared by Lisa Haynes" unless she says otherwise.
- Dates: field order uses military style (`26 NOV 2026`, `2:30 PM`). Every other preset uses `November 26, 2026`.
- Never put passwords, account numbers or other secrets in a document.

## 4. Preset by preset

### Report
- `.banner` (optional): the one fact the reader needs first, such as a deadline or a link. `.label` on top, `.big` value, `.note` on the right.
- `header.title`: `.eyebrow` ("Who · Topic"), `h1` with the key 1 to 3 words wrapped in `<b>` (they turn red), `.byline`.
- `.lead`: one paragraph saying what this is and what's needed.
- `.summary`: exactly 2 or 4 tiles (`.k` label, `.v` value, `.s` note).
- Parts: `h2` with `<span class="n">PART 1</span>`. Number parts only when there are two or more.
- `.finding`: a severity tag `.sev.high` / `.med` / `.low` / `.good` (text such as High, Medium, Low, Fine), then `h3`, `p` and an optional `p.fix`.
- `.points`: an even number (2 to 6) of short facts, each an `h3` plus `p`. `.callout`: one line of good news.
- `.choice`: an `h3` question and two `.opt`s. Mark the recommended one `.opt.pick`. To change its badge, write `<span class="t" data-badge="Lisa recommends">`.
- `ol.steps`, and a `table` with `th.num`/`td.num` for right-aligned numbers and `tr.total` for the total row (wrap it in `.table-wrap`).
- Put `class="page-break"` on an `h2` to start it on a new printed page.

### Field order
- `.bar` top and bottom: a classification line ("UNCLASSIFIED // FAMILY USE ONLY", or for example "FOR THE COOKS ONLY").
- `.meta`: `OPORD MM-YY` and `DTG <date>` both use the day the order is written (today). The event's own date goes in the Situation and Mission. `COPY 1 OF <number of people getting it>`; if that isn't known, just `COPY 1`.
- `h1`: "Operation" plus a two-word codename. Make up a playful one if she doesn't give one.
- Always these five paragraphs, in this order:
  1. Situation: a short paragraph plus a `dl` of facts. Use `dd.on` for the one thing that must not go wrong.
  2. Mission: one bold sentence saying what, by when.
  3. Execution: as many `.phase` blocks as the job has, usually 2 to 5 (`h3` "Phase I" with `<small>` "Name · time", or just "Name" when there's no time). Each step is one action. Number steps as phase.step (1.1, 1.2, 2.1). Give each checkbox a unique id (s1, s2, ...). Put a hint in `<em>` inside `.t`.
  4. Rules of engagement: `DO NOT`, `GUARD` (and `MUST` if useful), one line each. Sensible safety rules may be suggested.
  5. Command & signal: Lisa is in charge unless she says otherwise. Only name other people for jobs she mentioned. A sensible fallback plan ("Abort") may be suggested, since it's advice rather than a fact.
- Checkboxes remember their state on the device that ticks them. On paper they print as empty boxes.

### Proof sheet
- One printed page, so keep it short.
- `.slug`: left "Notice 01" / "Invitation" / "Proof 01", right the topic.
- `.stamp`: 2 to 3 words ("Save the date", "Not public", "RSVP").
- `h1`: two short lines, the first heavy and the second light in red (`<span class="light">`). Keep each line to about 9 letters or less.
- `.for`: one or two sentences, with the key name in `<b>`.
- `dl.details`: 3 to 5 rows (When, Where, Cost, RSVP...). `.foot`: one line.

### Gallery
- Built as pairs: a `.rail` (a `<strong>` label plus a quiet note) beside its content.
- `h1`: the name, with an `<em>` subtitle. `.dates`: the dates or the occasion.
- `.text`: wall-text paragraphs. The first line of the first paragraph turns slightly bolder by itself.
- `blockquote` with `<cite>`: one short quote.
- `ol.works`: museum-style captions. Each `.work` has `.no`, `.title`, `.maker`, `.meta` (year, then material and size), and an optional `.note`.
- `<span class="dot"></span>` after a title is the gallery's red dot. Use it for favorites, keep the `.key` line explaining it, and use it sparingly.
- Put `new-page` on a `.rail` to start that pair on a fresh printed page.
- Works for anything worth showing slowly: photos, recipes, heirlooms, garden plants, a reading list.

### 2002 web
- `.masthead`: `h1` site name plus a short tagline. `.ticker`: one line of news, separated with `***`.
- Sidebar `.box`es (an `h2` title plus `.in`): Navigation links (use `#` unless there are real addresses), the Visitors counter digits, and 88×31 buttons (`.b88.red` / `.blue` / `.gray`, a short `.l` and `.r`).
- Posts: `.date`, then `article.post` with `h2`, the body (`p`, `ul`, `table`) and the `.by` line. A `.new` badge goes on the newest post only. Put an `hr` between posts.
- `.foot`: copyright years and "last updated".

### Word doc
- `.title`, `.subtitle`, body `p`, `h1`/`h2`/`h3`, `ul`/`ol`, and a `table` (first column bold, red header row) in `.table-wrap`. `.quote` is Word's Intense Quote. Page numbers appear by themselves when printed.
- If Lisa needs a real editable Word file (.docx), make one with the same styles: Calibri 11 pt, line spacing 1.15, 8 pt after paragraphs; Title 28 pt; Heading 1 16 pt, Heading 2 13 pt, Heading 3 12 pt; headings in Dark Red `C00000` (Heading 3 `800000`); table header fill `C00000` with white bold text and banded rows `FBE4E4`; Letter size with 1-inch margins.

## 5. Colors

Lisa's favorite color is red. The red presets use `#c0182f`; Word doc uses Word's own Dark Red `#c00000`. The field order is olive by default, because it's an army order. If she asks for it in red, replace these tokens in its `:root`:

```css
--accent: #8f1426; --bar: #a3162b; --alert: #c0182f;
```

Change a preset's colors only when she asks, and only through its `:root` tokens.

## 6. Printing and sharing

- The `.final.html` is one self-contained file: email it, text it, or open it in any browser.
- To print or make a PDF yourself: open it in Chrome or Safari, choose Print, Letter size. In Chrome, tick "Background graphics" if the colors are missing.
- The proof sheet prints edge to edge on one page. Everything else uses normal margins.
