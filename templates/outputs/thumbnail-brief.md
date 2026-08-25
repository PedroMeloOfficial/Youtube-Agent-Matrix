# Thumbnail Brief — `{WORKING_TITLE}`

> **Always written in English**, whatever the creator's OUTPUT LANGUAGE — image-generation
> models perform materially worse in other languages. **Two exceptions:** `overlay_text` and
> `paired_title` stay in the creator's language, because viewers read them.

**Archetype:** `{PRIMARY}` · **Target CTR:** `{X}%` (`benchmarks.md` §1, archetype template §5)
**Traffic source:** `{SEARCH / SUGGESTED / BROWSE}` · **Face available:** `{YES/NO}`

---

## Concept `{N}` — `{SAFE / CURIOSITY / WILDCARD}` — "`{CONCEPT_NAME}`"

*(repeat this whole block for each of the three concepts)*

**Rationale:** `{WHY_THIS_CONCEPT_EARNS_A_CLICK_FOR_THIS_VIDEO}`

**Image-generation prompt:**

```
{FULL_PROMPT — subject, expression, composition, camera angle, lighting, background,
color palette, style, aspect ratio 16:9, resolution 1280x720 minimum, negative
constraints: no text, no watermark, no logo}
```

| Field | Value |
|---|---|
| `overlay_text` *(creator's language)* | `{TEXT}` — `{N}` words (≤5 words, 3 ideal — `benchmarks.md` §7) |
| Text placement | `{LEFT / RIGHT / TOP-LEFT / BOTTOM}` third, `{N}`% of frame height |
| Font weight / treatment | `{TREATMENT}` |
| `paired_title` *(creator's language)* | `{TITLE}` |
| Title–thumbnail relationship | `{COMPLEMENT / CONTRAST / COMPLETION}` — never repeat each other |
| Palette | `{COLOR_1}` `{COLOR_2}` `{COLOR_3}` — contrast ratio `{X}:1` |
| Focal point | `{SUBJECT}` occupying `{N}`% of frame |
| Silhouette test at 168×94 px | `{PASS/FAIL}` — `{WHAT_IS_STILL_READABLE}` |
| Mobile-feed test (thumb-sized, low light) | `{PASS/FAIL}` |

**Fallback prompt adjustment** — if the generator fails on the main prompt:

```
{SIMPLIFIED_PROMPT — the same idea with fewer elements, describing what to change and why}
```

**Fails if:** `{THE_CONDITION_THAT_MAKES_THIS_CONCEPT_NOT_WORK}`

---

## Face and reference images

| Item | Value |
|---|---|
| Face used | `{YES / NO / PARTIAL}` |
| Expression | `{EXPRESSION}` — never generic shock unless the archetype calls for it |
| Reference image needed | `{YES/NO}` — `{WHICH_SHOT}` |
| Reference image path / instruction | `{PATH_OR_HOW_TO_CAPTURE}` |
| Consistency with channel's existing thumbnails | `{HOW}` |
| Do not generate | `{PROHIBITED_ELEMENTS: real logos, real people's likeness, misleading imagery}` |

---

## Comparison

| Concept | Type | Click driver | CTR ceiling | Risk | Production cost |
|---|---|---|---|---|---|
| 1 | Safe | `{DRIVER}` | `{EST}` | `{RISK}` | `{L/M/H}` |
| 2 | Curiosity | | | | |
| 3 | Wildcard | | | | |

---

## ▶ Recommendation

> **Use concept `{N}` — `{CONCEPT_NAME}`.**
>
> **Why:** `{ONE_LINE_REASON}`
> **A/B pair:** test `{N}` against `{N}` if Test & Compare is available (`benchmarks.md` §7)
> **Switch to concept `{N}` if:** `{CONDITION}`

---

## Delivery notes

- Export at `{RESOLUTION}`, under the file-size limit in `benchmarks.md` §7
- Check overlay text is readable with the duration badge overlapping the bottom-right corner
- Verify no policy risk: no misleading claim, no prohibited imagery (`benchmarks.md` §7 Policy strikes)

---

## Self-check

- [ ] Entire document is in English, except `overlay_text` and `paired_title`
- [ ] Three genuinely different concepts — Safe, Curiosity, Wildcard, not three edits of one idea
- [ ] Every prompt is a complete, copy-pasteable block with negative constraints
- [ ] Overlay text is ≤5 words, 3 ideal (`benchmarks.md` §7); tighter if the archetype template §5 states a preference
- [ ] Title and thumbnail complement rather than repeat each other
- [ ] Resolution and file-size specs meet `benchmarks.md` §7
- [ ] Contrast and silhouette tests recorded for every concept — no blank verdicts
- [ ] Target CTR cited from `benchmarks.md` §1, matched to this archetype and traffic source
- [ ] Each concept has a working fallback prompt
- [ ] No misleading imagery; no real logo or likeness requested
- [ ] One recommendation, with a reason and an A/B pairing where testing is available
