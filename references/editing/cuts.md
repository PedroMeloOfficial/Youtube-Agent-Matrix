# Cuts

> Adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/etapa-cortes.md`.
> Translated and adapted, not copied.

**Purpose.** The first clean cut: choose the takes, remove mistakes, false starts, spoken notes and
pauses. No zoom, no animation, no effects. Not the final cut — the base the creator refines. Read by
`cut-agent`.

**Contents:** 1 How to decide · 2 Choosing a take · 3 Pauses and hesitations · 4 Humour and beats ·
5 Order · 6 Edges (script work) · 7 Markers · 8 Chapters · 9 State, delivery, review

---

## 1. How to decide

- **Read by sentence, decide by sentence.** `transcript.txt` is what the agent reads. The word-level
  file is opened only for one stretch, by script.
- **Identify takes:** repeated or near-identical sentences, restarts, abandoned sentences, "wait",
  "again", "let me redo that" (in the creator's language). Expect several attempts per passage.
- Choose and discard **between ideas and takes, never in the middle of a sentence.**
- The agent chooses by **text**, not by delivery (voice, expression, eye line). It cannot hear comic
  timing or see a bad face. That is why doubt becomes a marker, not a cut.
- **In doubt, do not cut — mark.**

## 2. Choosing a take

In this order:
1. A spoken note about that passage.
2. The **last complete** take (usually the most relaxed).
3. If the last one stumbles and an earlier one is clean, the earlier one.

Before discarding a sentence as incomplete, look for another take of it that the transcript swallowed
(◌ sound without words, ⚑ recovered words). With two good takes and a hard call: pick one and mark
the other with where it is.

## 3. Pauses and hesitations

- Cut the considerable pauses; how much air remains is the profile's (`cuts.air`, craft default
  ~0.25 s).
- Hesitations ("um", "uh", "like" — and the creator's own, listed in the voice profile): cut only when
  **isolated by silence on both sides and long**. A hesitation glued to speech stays: from the text it
  cannot be known whether the cut would sound wrong, and the creator judges. Mark the ones considered.
- A habit the voice profile marks as part of how they talk is not a mistake.

## 4. Humour and beats

- A pause before or after a punchline is **content**. Lines marked `[BEAT]` in the approved script,
  and pauses right after a line that reads as a joke, are kept at their full length and get a marker.
- If unsure whether a pause is a beat: keep it, mark it.

## 5. Order

The order recorded. Reordering is only **suggested** (in the summary and as a marker), and only when
strong — a punchline that would clearly work better as the hook.

## 6. Edges (script work)

The agent writes `cuts/decisions.json` with approximate start and end per segment (from the sentence
timecodes). `cut_edges.py` then:
- snaps to the word boundary, refines on the **audio energy** (Whisper's word edges are ±0.1–0.2 s off);
- pads by the profile's margin (`cuts.padding`, craft default 0.10 s) without crossing into a
  neighbouring word that was cut;
- keeps untranscribed voice glued to an edge and **marks** it (often a filler; sometimes just a
  misaligned word — never assert which);
- snaps to whole frames.
Never re-run edge refinement on segments that came back from the creator's Final Cut edit (`locked`):
it would undo their work.

## 7. Markers (in the timeline, not in the chat)

| Type | When |
|---|---|
| `take_doubt` | another good take exists — say where |
| `hesitation` | considered cutting it and did not |
| `beat` | a kept pause for humour or effect |
| `note` | a spoken note with low confidence, or not understood |
| `suggestion` | e.g. a reordering |
| `alert` | technical: doubtful sync, poor transcript in the stretch, variable frame rate |

Anchored to **source** time, so they survive new versions of the cut. Short, direct, in the creator's
language.

## 8. Chapters

Propose chapter starts at real section changes (the approved script's section headings help). They
become chapter markers in Final Cut and can become YouTube chapters. Named by content, not by
function ("Why the first plan failed", not "Part 2").

## 9. State, delivery, review

- `cuts/decisions.json` (agent) → `cuts/cuts.json` (script): each segment has an id, file, in, out (in
  the camera file's time) and the opening words. Screen recordings and external audio come from sync,
  never duplicated.
- The editor builds `<slug>_cuts_vNN` (`delivery-fcpxml.md`).
- **Summary, short:** raw duration → cut duration, markers by type, anything important, the path.
- **Review:** by chat (sequence time is converted to source time through the segment list), or by the
  return trip. The creator's adjustments win. If an adjustment contradicts something the agent
  claimed, say so.
- **Once approved, the cut locks.** If it changes after the motion plan or the camera, those stages are
  flagged stale and must be recomputed.
