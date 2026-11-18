# Assets for Animations

> Adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/etapa-assets.md`.
> Translated and adapted, not copied.

**Purpose.** Find the real files the animations need and code cannot draw. Read by `asset-agent`.
The stage skips itself when nothing is missing, and works on its own ("find the Notion logo").

## 1. Who solves what

| Needs… | Solved by |
|---|---|
| A brand or tool logo, an icon, a capture of a public web page | this stage |
| A character, shape, built scene, diagram | the render, drawing it in code |
| A logged-in screen, a personal recording, a photo of the creator | the creator — remind them |
| A stock photo or video | only from a source with a clear licence; otherwise the creator sends it |

## 2. Sources that work

- **Logos:** first the creator's local logo library (`workspace/edit-profile/logos/`), then official SVG
  sources and Iconify collections (`logos`, `devicon`).
- **Icons:** Iconify, one option from each of a few collections for variety (Lucide, Phosphor, Tabler…).
  Single-colour SVG; the render recolours.
- **Web captures:** a headless browser at the video's resolution, the page as it opens.
Check current sources and licences before writing the search script; they change.

## 3. Showing options

- **One numbered contact sheet per round** (one image, options side by side over the video's background),
  never loose files.
- Before showing, discard the obviously wrong: wrong brand (the parent company instead of the product),
  an old logo, a capture with a cookie banner or a page that did not load.
- Option 1 is the recommendation. The creator answers by number ("a1 1, a3 2, a4 I'll send it").
- Save with the option's own extension (an SVG where a PNG was expected is better) and update the plan.
- Ask which go into the fixed library (logos that will come back in other videos).

## 4. Licences

- **Logos** are trademarks: use the official mark, never redrawn or distorted, to talk about the tool. If
  the official one cannot be found it stays missing — never a look-alike.
- **Icons** from open collections (MIT, ISC, Apache, CC BY). CC BY needs credit: record it in
  `edit/motion/credits.md` for the video description.
- **Web captures:** public pages, to comment on the product. Never a logged-in screen or someone else's
  account.
- An image found on the web without a clear licence does not go in: it becomes "the creator sends it".

## 5. Files and summary

- Saved to `edit/motion/assets/<asset-id>.<ext>`; recorded in `edit/motion/assets.json` with source,
  licence, credit line and which plan items use it.
- Summary: what came in (file, source, licence), what is still missing and what **the creator** must record
  or send, with the expected file name. The render builds a visible placeholder for anything still missing.
