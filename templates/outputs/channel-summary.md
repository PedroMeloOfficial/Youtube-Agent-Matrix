# Channel Summary — ⟨CHANNEL NAME⟩

> Fill in OUTPUT LANGUAGE. Section headings may be translated.
>
> **The deliverable is `workspace/channel-summary.docx`, not this file.** You write this Markdown,
> run `execution/build_reader_doc.py` on it, and the Markdown is deleted. The creator only ever
> opens the Word document, where the conventions below have become real formatting they can
> highlight and annotate.
>
> **This is the creator-facing view of `channel-profile.md`.** Everything here restates a decision
> already recorded in the full profile, which stays the source of truth and the file every agent
> reads. Never decide anything here. If something needs to change, change `channel-profile.md`
> first, then regenerate.
>
> **The test it has to pass:** the creator reads it in two minutes and can say out loud what their
> channel is, who it is for, and what they are and are not allowed to make.

## How the converter reads this file

| You write | The creator sees |
|---|---|
| `## Section` | Section heading |
| plain paragraph | Reading-size body text |
| `- item` | A real bullet |
| `**word**` | Real bold |
| `\| a \| b \|` | A real table |

## Content rules

- **Plain prose in short paragraphs.** Where the full profile has a nine-column table, this has
  three sentences.
- **One table only**, for the pillars, where a list genuinely reads worse.
- **No jargon from the system.** "Archetype", "size tier", "traffic surface", "job", "unfair
  advantage" are internal vocabulary. Say the thing itself.
- **One page.** Under 500 words, and shorter is better. Anything that does not change a decision
  the creator makes gets cut — it is still in the full profile.
- **Nothing marked `⟨TBD⟩` appears here at all.** An empty field is noise to a reader; leave it out
  silently and let the full profile carry the gap.

---

# ⟨CHANNEL NAME⟩

⟨One sentence: what this channel is. Derived from the positioning sentence, but written the way the
creator would say it to a friend, not in the required "I do X for Y because Z" shape.⟩

## Who it is for

⟨Two or three sentences. Who watches, what they already watch, what they are hoping to feel or be
able to do. From §4 of the full profile.⟩

⟨One sentence on what makes them leave — the most useful line in the document, and the one most
worth keeping blunt.⟩

## What makes it different

⟨Two or three sentences on the advantage, written concretely. Not "authentic perspective" but the
actual thing: the access, the experience, the equipment, the language, the years spent on
something. From §3 of the full profile.⟩

## What you make

| The pillar | What counts | What does not | How much of the output |
|---|---|---|---|
| ⟨name⟩ | ⟨one short phrase⟩ | ⟨one short phrase⟩ | ⟨%⟩ |

⟨One sentence tying it together — what the mix is meant to achieve.⟩

## How it sounds

⟨Two or three sentences describing the voice as a person would recognise it. Then the recurring
things: the phrases, the structures, the rituals.⟩

⟨One short paragraph on what this channel never does. This is the half creators forget, so it gets
its own paragraph rather than a column in a table.⟩

## The rhythm

⟨One or two sentences: how often long-form, how often Shorts, how long videos run, and what the real
production limit is — the hours available, not an aspiration.⟩

## What is in the way

⟨Two or three sentences on the constraints that actually bind: time, equipment, rights, dates
unavailable. Written as facts, not complaints.⟩

## What is next

⟨The live queue, as a short list of working titles and roughly when. Omit the section entirely if
the queue is empty.⟩

---

⟨One closing line pointing at the full profile by name, for when the creator wants the reasoning
and the research behind any of this.⟩

---

## Self-check — run before converting, then delete this section

- [ ] Every statement traces to a decision already in `channel-profile.md` — nothing new
- [ ] No internal vocabulary — a reader who has never seen this system understands every word
- [ ] Under 500 words
- [ ] Only one table, for the pillars
- [ ] Nothing marked `⟨TBD⟩` appears
- [ ] The "what it never does" paragraph is present and specific
- [ ] Written in OUTPUT LANGUAGE
