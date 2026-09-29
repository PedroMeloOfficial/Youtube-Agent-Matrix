# Recording Script — ⟨WORKING TITLE⟩

> Fill in OUTPUT LANGUAGE. Section headings may be translated.
>
> **The deliverable is `script-recording.docx`, not this file.** You write this Markdown, run
> `execution/build_reader_doc.py` on it, and the Markdown is deleted. The creator only ever opens
> the Word document, where every convention below has become real formatting.
>
> **This is the creator-facing view of an approved script, in screenplay format.** Every spoken
> line is copied verbatim from the approved variant in `script-{a|b|c}-*.md`, which stays the
> source of truth. Never write a line here that does not exist there. If a line needs to change,
> change it in the source variant first, then regenerate.
>
> **The one job of the document:** the creator props the phone up, sees who is speaking and what
> just cut to what, and reads. Nothing on the page may compete with the words they have to say.

## How the converter reads this file

These are not style preferences — they are what the renderer keys on.

| You write | The creator sees |
|---|---|
| `# Title` | Document title |
| `## Scene heading` | Section heading — this is the scene/cut marker (see below) |
| `### SPEAKER NAME` | A speaker cue — bold, distinct from body text, sitting right above their line |
| `> stage direction` | Small, grey, italic, indented — visually impossible to mistake for a line to say |
| plain paragraph | Reading-size body text: **this is what they say out loud** |
| `- item` | A real bullet |
| `\| a \| b \|` | A real table |
| `**word**` | Real bold |

Everything the creator must *say* is a plain paragraph under a speaker cue. Everything they must
*do* is a `>` line. Everything about what the camera cuts to is in the scene heading. Get any of
the three confused and the creator will read a camera direction aloud, or lose track of what just
changed on screen.

## Content rules

- **Every scene heading names the cut.** Format: `## Scene <N> — cut from "<what was on screen
  last>" to "<what's on screen now>" — around <N> min`. The very first scene has no "cut from" —
  it opens the video. Take the "from" and "to" from the stage direction and `[B-ROLL:]` cues of
  the two beats on either side of the cut; never invent a visual the technical script didn't cue.
- **A speaker cue opens every scene**, in full capitals, using the name from
  `workspace/channel-profile.md`'s Identity table ("Host name — how they're credited"). If that
  field is `⟨TBD⟩`, ask the creator once for the name to use and say you're carrying it forward —
  do not guess or leave a placeholder in the delivered document.
- **A new speaker cue only when the speaker actually changes** — a solo host reading straight
  through does not need a fresh cue at every paragraph, only at the top of each scene, or when a
  second voice enters (a quoted clip, a guest, a co-host).
- **No production jargon.** "Punch in", "interrupt", "B-roll", "pattern break", "cold open" are
  agent vocabulary. Write what the creator actually does inside a `>` line: "cut in closer", "cut
  away to the gameplay here", "this is the opening line".
- **No timestamps down to the second.** A rough minute marker in the scene heading is enough.
  Precise timing stays in the technical script.
- **One table only** — the shot list at the end.
- **Stage direction opens every scene**, before the speaker cue. The one thing allowed *between*
  spoken paragraphs is a single short `>` emphasis cue, and only where the technical script marked
  that line `[EMPHASIS]`.
- Drop everything that is reasoning rather than performance: beat claims, evidence traces,
  transition labels, interrupt counts, word counts, the self-check. All of it stays one file away
  in the technical variant.

---

# ⟨WORKING TITLE⟩

Approximately ⟨N⟩ minutes · From ⟨script-a-narrative.md / script-b-… / script-c-…⟩ · Speaker:
⟨name from the channel profile⟩

## Scene 1 — opens on ⟨what's on screen at the very start⟩ — around 0 min

> ⟨How the creator is framed, what is on screen, what the energy is. Example: "Straight to camera,
> close framing, nothing behind you. Say this before anything else — no greeting."⟩

### ⟨SPEAKER NAME⟩

⟨THE FIRST SPOKEN LINE, WORD FOR WORD⟩

⟨The rest of the opening, as spoken paragraphs.⟩

## Scene 2 — cut from "⟨scene 1's visual⟩" to "⟨what's on screen now⟩" — around ⟨N⟩ min

> ⟨Stage direction: framing, what is on screen, whether to cut away, what the tone shift is. Two
> sentences maximum. Name the footage in normal words; the sourcing detail goes in the shot list.⟩

### ⟨SPEAKER NAME⟩ *(only if the speaker changed from the previous scene — omit otherwise)*

⟨The spoken text, as paragraphs. Verbatim from the approved variant.⟩

> ⟨Only where the source marked `[EMPHASIS]`: "slow down here" / "this is the line to land".⟩

⟨More spoken text.⟩

*(Repeat that scene block for each cut in the video — one scene per beat of the technical
script.)*

## Scene ⟨final⟩ — cut from "⟨previous scene's visual⟩" to the closing frame — around ⟨N⟩ min

> ⟨Stage direction.⟩

### ⟨SPEAKER NAME⟩ *(only if it changed)*

⟨The closing spoken text.⟩

⟨The single ask, exactly as it will be said.⟩

## What to film or find

| Where it goes | What to show | Where it comes from | Have it? |
|---|---|---|---|
| ⟨scene name⟩ | ⟨what the viewer sees, in normal words⟩ | ⟨own footage / screen recording / stock / archive⟩ | ⟨yes / no — and what to use instead⟩ |

Anything marked "no" needs a substitute before recording day, or that part gets rewritten.

## Before you record

- ⟨Anything the technical script flagged `⚠️ verify`, restated in one plain sentence so the creator
  does not state it as fact on camera. Omit the whole section if there is nothing.⟩

---

## Self-check — run before converting, then delete this section

- [ ] Every spoken line is verbatim from the approved variant — no rewriting, no smoothing
- [ ] Every scene heading names what it cuts from and to, taken from real stage direction /
      `[B-ROLL:]` cues — nothing invented
- [ ] A speaker cue (`### NAME`, capitals) opens every scene, using the name from the channel
      profile — never a placeholder left in the delivered document
- [ ] A new speaker cue appears only where the speaker actually changes
- [ ] Every line to be **said** is a plain paragraph; every line to be **done** is a `>` line
- [ ] No production jargon — a person who has never read the technical script understands it all
- [ ] Stage direction opens every scene; between spoken paragraphs there is at most one `>` cue
- [ ] Rough minute markers only
- [ ] The shot list is the only table
- [ ] Written in OUTPUT LANGUAGE
- [ ] The header names which variant this came from
