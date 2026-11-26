# mom-skills

Skills for Claude that Alex made for Lisa. It's a Claude plugin marketplace, so once it's installed, every update pushed here reaches her automatically.

## lisa-documents

Six house styles for documents. Ask Claude for a checklist, a report, a notice or some notes, and it builds one from the right template, with the fonts built in, ready to print or send as a PDF.

| | |
|---|---|
| **Report**: write-ups, decisions, costs<br>![Report](previews/report.jpg) | **Field order**: step-by-step plans and checklists<br>![Field order](previews/field-order.jpg) |
| **Proof sheet**: notices, invitations, save-the-dates<br>![Proof sheet](previews/proof-sheet.jpg) | **Gallery**: essays, letters, collections<br>![Gallery](previews/gallery.jpg) |
| **2002 web**: family updates, newsletters<br>![2002 web](previews/web-2002.jpg) | **Word doc**: plain notes, minutes, handouts<br>![Word doc](previews/word-doc.jpg) |

Try asking:

- "Make a field order for Christmas Eve dinner."
- "Write up the roof estimates as a report."
- "A save-the-date for the reunion, the stamp one."
- "Put my garden notes in the gallery style."

## Install

### Claude app (claude.ai or desktop)

1. Open **Customize → Plugins → Add → Add marketplace**.
2. Enter `alexh/mom-skills`.
3. Install **lisa-documents**, and turn on automatic sync for the marketplace so updates arrive by themselves.

### Claude Code

```bash
claude plugin marketplace add alexh/mom-skills
claude plugin install lisa-documents@mom-skills
```

Then run `/plugin`, open **Marketplaces**, select **mom-skills** and turn on auto-update.

## Updating

Push to `main`. The plugin has no `version` field on purpose: each commit counts as a new version, so installed copies update on their next sync.

## Layout

```
.claude-plugin/marketplace.json
plugins/lisa-documents/
  .claude-plugin/plugin.json
  skills/lisa-documents/
    SKILL.md          instructions Claude follows
    presets/          the six templates, with sample content
    fonts/            bundled fonts (SIL Open Font License)
    scripts/finish.py builds the fonts into a finished file, plus an optional PDF
previews/             screenshots for this page
```

To try a preset locally:

```bash
python3 plugins/lisa-documents/skills/lisa-documents/scripts/finish.py plugins/lisa-documents/skills/lisa-documents/presets/report.html -o /tmp/report.html --pdf
```

## License

MIT for the templates and the script. The fonts are under the SIL Open Font License 1.1; see [fonts/LICENSES.txt](plugins/lisa-documents/skills/lisa-documents/fonts/LICENSES.txt).
