# Third-Party Notices

## fluxo-de-edicao — Lucas Leite (MIT)

The editing layer (`skills/editor/`, `agents/footage-agent.md`, `cut-agent.md`, `edit-style-agent.md`,
`motion-plan-agent.md`, `asset-agent.md`, `motion-render-agent.md`, `camera-agent.md`, `sound-agent.md`,
`references/editing/` and `templates/outputs/edit/`) is adapted from **fluxo-de-edicao**
(https://github.com/LeiteZ/fluxo-de-edicao): its eight-stage workflow, its editing principles, and its
craft guides for cuts, motion, HyperFrames, assets, camera and sound effects. The material was translated
from Portuguese and adapted to this plugin's architecture; it is not a verbatim copy. Each adapted file
names its source file at the top. The Final Cut Pro delivery and the scripts in `execution/edit/` are this
project's own.

```
MIT License

Copyright (c) 2026 Lucas Leite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Tools used at runtime (not distributed with this plugin)

| Tool | Licence | Used for |
|---|---|---|
| HyperFrames (HeyGen) | Apache-2.0 | rendering animations, run through `npx` at a pinned version |
| mlx-whisper / Whisper models (OpenAI) | MIT | transcription |
| faster-whisper, Silero VAD | MIT | speech detection, CPU transcription |
| OpenCV, YuNet face model | Apache-2.0 | face tracking |
| FFmpeg | LGPL/GPL (as installed) | media decoding and measurement |

The Final Cut Pro FCPXML DTD is Apple's; it is read from the installed application and never copied
into this repository.
