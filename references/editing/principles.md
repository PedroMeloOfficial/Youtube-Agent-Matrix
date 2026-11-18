# Editing Principles

> Adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/principios-do-fluxo.md`
> and `guias/decisoes.md`. Translated and adapted for the YouTube Agent Matrix — not copied.
> See `THIRD_PARTY_NOTICES.md`.

**Purpose.** The habits that make editing with agents work video after video, for any creator and
any channel. The editor skill and every editing agent follow them. Taste (colours, how much zoom,
how much air between sentences) is never here — it lives in the creator's edit profile.

**Contents:** 1 One stage at a time · 2 Plan whole, execute in chunks · 3 Memory in files ·
4 Claude decides, scripts calculate · 5 Save points and pending requests · 6 The learnings notebook ·
7 Craft vs taste · 8 Tendency, not rule · 9 Safety · 10 Check before trusting · 11 Spending tokens well

---

## 1. One stage at a time

- A single prompt that does everything delivers an average video. Small stages, each with one job,
  deliver far more: footage → cuts → motion plan → assets → motion render → camera → sound.
- Each stage starts from the previous one **locked** (approved). If something approved changes later
  — the cut changes after the animations were planned — the stage that depends on it says what has
  to be redone instead of carrying on with a stale plan. `edit_state.py status` computes these alerts.
- No chaining stages on its own. The creator approves one and says "yes" to the next.

## 2. Plan whole, execute in chunks

- What needs the whole picture — cuts, the motion plan — reads the whole video: story, variety,
  rhythm from start to end.
- What is heavy to execute — rendering, camera, sound — can go **by chunk**, chosen by the creator
  ("render up to 3:00", "the hook", "the rest"). An item belongs to the chunk it **starts** in.
- Each chunk reads what earlier chunks did, so the same formula is not repeated.
- Long videos (15–30 min) are the normal case, not the exception.

## 3. Memory lives in files, not in the conversation

- Every video has an `edit/` folder inside its matrix folder. Each stage owns its decision file;
  `edit-state.json` holds the status of every stage and the pending requests.
- So the chat can be cleared between stages without losing anything: the editor reads the state
  and says where the video stopped.
- State files grow large. `edit_state.py` reads and summarizes only the piece a step needs. Never
  open a whole decision file to answer "where are we".

## 4. Claude decides, scripts calculate

- Agents decide on **text**: which take, where an animation goes, which sound. They read the
  transcript **by sentence**, never word by word.
- **Scripts** do the arithmetic: word times, frames, cut edges, keyframes, audio levels and the
  Final Cut file. A script makes fewer mistakes than mental arithmetic and costs far fewer tokens.
- An agent never writes FCPXML, never computes a frame by hand, never edits a script's output file.

## 5. Save points and pending requests

- **Save point:** the stage (or chunk) is finished, requested changes are applied and the delivery
  file is built. Only then does the editor suggest clearing the chat.
- **Pending request:** anything the creator asked for and that is not applied yet is recorded
  (`edit_state.py --pending`) and shows in the status until resolved.
- Never suggest clearing the chat with a change that was neither applied nor recorded.

## 6. The learnings notebook

- During review, every correction, compliment or preference that holds **for other videos** becomes
  one line in `edit/learnings.md`: `- [ ] <stage> · <what was asked, with context> · <date>`.
- A content fix for this video only ("cut that sentence") is not a learning. In doubt, it goes in
  with "(maybe only this video)".
- Recording is not changing. Nothing changes until the creator asks (`/yt edit learnings`): the
  editor proposes where each line goes, the creator filters, then it is written and marked
  `[x] → <where it went>` or `[-]` (only that video).
- Taste goes to the edit profile (workspace). Craft — a rule true for any creator — is listed as
  *craft, for the plugin*: the installed plugin is read-only, so craft changes reach the repository
  through its maintainer, never silently at runtime.

## 7. Craft vs taste

- **Craft** (true for any video: choosing a take, a fluid animation curve, aligning a sound) lives in
  `references/editing/` and the agents.
- **Taste** (this creator's: colours, fonts, zoom, animation density, preferred sounds) lives in
  `workspace/edit-profile/`. Agents only point at it. Every craft constant in these references is a
  **craft default, overridden by the edit profile**.
- A creator with two styles (two channels, a client) has two profiles, never a copy of the workflow.

## 8. Tendency, not rule

- In creative decisions, what the references and the profile say is a starting point. Absolute
  rules make every video the same.
- Technical rules — sync, levels, frame accuracy, file format — are firm.

## 9. Safety

- **Never move, rename or delete** the creator's raw footage, sound library, music or Final Cut
  libraries. Never write inside a `.fcpbundle`. Never copy media into the workspace — store
  absolute paths and times. The only media created are the matrix's own renders.
- **Never overwrite a delivery:** `<slug>_cuts_v01`, `_v02`… then `_motion_v01`, `_final_v01`.
- Deleting, when ever needed, means moving to a holding folder for the creator to delete.
- **Install nothing without explaining it and getting a yes.** `setup_check.py` lists what is
  missing with the exact command.
- **No computer use to drive Final Cut.** Delivery is always a file the creator imports.

## 10. Check before trusting

- Every delivery format starts with a **short test project** the creator imports and checks: it
  opens, right clips, right audio, markers visible, timing right. Recorded in `edit-config.json`
  (`validated`). Only then is the format used for real (see `delivery-fcpxml.md` §9).
- When unsure how Final Cut represents something, ask the creator to build it in Final Cut and
  export it — then copy that, instead of guessing.
- After changing a script that works, compare its output on a frozen test video with the output
  before. A change nobody asked for is a bug. The test suite in `execution/edit/tests/` is never
  weakened to make something pass.

## 11. Spending tokens well

- Clear the chat between stages; long history is reprocessed on every message.
- Read summaries and slices: the transcript by sentence, the state through the script, a frame only
  when there is real doubt.
- Long renders run in the background; waiting costs nothing.
- Models: light agents (footage, assets) run on the lighter model; decisions where a mistake costs a
  whole review round (cuts, motion, camera, sound, style) run on the most capable one.
