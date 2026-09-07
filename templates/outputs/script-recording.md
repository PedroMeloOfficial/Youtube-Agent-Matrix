# Recording Script — ⟨WORKING TITLE⟩

> Fill in OUTPUT LANGUAGE. Section headings may be translated.
>
> **The deliverable is `script-recording.docx`, not this file.** You write this Markdown, run
> `execution/build_reader_doc.py` on it, and the Markdown is deleted. The creator only ever opens
> the Word document, where every convention below has become real formatting.
>
> **This is the creator-facing view of an approved script.** Every spoken line is copied verbatim
> from the approved variant in `script-{a|b|c}-*.md`, which stays the source of truth. Never write
> a line here that does not exist there. If a line needs to change, change it in the source
> variant first, then regenerate.
>
> **The one job of the document:** the creator props the phone up and reads. Nothing on the page
> may compete with the words they have to say.

## How the converter reads this file

These are not style preferences — they are what the renderer keys on.

| You write | The creator sees |
|---|---|
| `# Title` | Document title |
| `## Block name` | Section heading |
| `> stage direction` | Small, grey, italic, indented — visually impossible to mistake for a line to say |
| plain paragraph | Reading-size body text: **this is what they say out loud** |
| `- item` | A real bullet |
| `\| a \| b \|` | A real table |
| `**word**` | Real bold |

Everything the creator must *say* is a plain paragraph. Everything they must *do* is a `>` line.
That single distinction is what makes the document readable with a camera running — get it wrong
and they will read a camera direction aloud.

## Content rules

- **No production jargon.** "Punch in", "interrupt", "B-roll", "pattern break", "cold open" are
  agent vocabulary. Write what the creator actually does: "cut in closer", "cut away to the
  gameplay here", "this is the opening line".
- **No timestamps down to the second.** A rough minute marker in the block heading is enough.
  Precise timing stays in the technical script.
- **One table only** — the shot list at the end.
- **Stage direction opens every block**, before any spoken text. The one thing allowed *between*
  spoken paragraphs is a single short `>` emphasis cue, and only where the technical script marked
  that line `[EMPHASIS]`.
- **Block names describe the content**, the way the creator thinks about it — "Where everyone gets
  it wrong", not "Beat 3" or "The turn".
- Drop everything that is reasoning rather than performance: beat claims, evidence traces,
  transition labels, interrupt counts, word counts, the self-check. All of it stays one file away
  in the technical variant.

---

# ⟨WORKING TITLE⟩

Approximately ⟨N⟩ minutes · From ⟨script-a-narrative.md / script-b-… / script-c-…⟩

## Opening — around 0 min

> ⟨How the creator is framed, what is on screen, what the energy is. Example: "Straight to camera,
> close framing, nothing behind you. Say this before anything else — no greeting."⟩

⟨THE FIRST SPOKEN LINE, WORD FOR WORD⟩

⟨The rest of the opening, as spoken paragraphs.⟩

## ⟨BLOCK NAME IN PLAIN WORDS⟩ — around ⟨N⟩ min

> ⟨Stage direction: framing, what is on screen, whether to cut away, what the tone shift is. Two
> sentences maximum. Name the footage in normal words; the sourcing detail goes in the shot list.⟩

⟨The spoken text, as paragraphs. Verbatim from the approved variant.⟩

> ⟨Only where the source marked `[EMPHASIS]`: "slow down here" / "this is the line to land".⟩

⟨More spoken text.⟩

*(Repeat that block for each part of the video.)*

## Closing — around ⟨N⟩ min

> ⟨Stage direction.⟩

⟨The closing spoken text.⟩

⟨The single ask, exactly as it will be said.⟩

## What to film or find

| Where it goes | What to show | Where it comes from | Have it? |
|---|---|---|---|
| ⟨block name⟩ | ⟨what the viewer sees, in normal words⟩ | ⟨own footage / screen recording / stock / archive⟩ | ⟨yes / no — and what to use instead⟩ |

Anything marked "no" needs a substitute before recording day, or that part gets rewritten.

## Before you record

- ⟨Anything the technical script flagged `⚠️ verify`, restated in one plain sentence so the creator
  does not state it as fact on camera. Omit the whole section if there is nothing.⟩

---

## Self-check — run before converting, then delete this section

- [ ] Every spoken line is verbatim from the approved variant — no rewriting, no smoothing
- [ ] Every line to be **said** is a plain paragraph; every line to be **done** is a `>` line
- [ ] No production jargon — a person who has never read the technical script understands it all
- [ ] Stage direction opens every block; between spoken paragraphs there is at most one `>` cue
- [ ] Block names describe content, not structure
- [ ] Rough minute markers only
- [ ] The shot list is the only table
- [ ] Written in OUTPUT LANGUAGE
- [ ] The header names which variant this came from
