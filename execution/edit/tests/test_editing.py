"""
Tests for the editing layer. Standard-library unittest; needs ffmpeg and numpy.

    python3 -m unittest discover -s execution/edit/tests -v

FCPXML validation runs against the Final Cut DTD when one is found ($FCPXML_DTD, or inside
the installed Final Cut Pro app). Without it those assertions are skipped **with a
message** -- the structural checks still run. Never weaken a test to make it pass.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
EDIT = HERE.parent
sys.path.insert(0, str(EDIT))

import easing  # noqa: E402
import timebase as tb  # noqa: E402
from common import next_version  # noqa: E402

HAVE_FFMPEG = shutil.which("ffmpeg") is not None
try:
    import numpy as np  # noqa: F401
    HAVE_NUMPY = True
except ImportError:
    HAVE_NUMPY = False


def run_script(name, *args):
    proc = subprocess.run([sys.executable, str(EDIT / name), *map(str, args)], capture_output=True, text=True)
    try:
        out = json.loads(proc.stdout)
    except ValueError:
        raise AssertionError(f"{name} printed non-JSON:\n{proc.stdout}\n{proc.stderr}")
    return proc.returncode, out


class TimebaseTest(unittest.TestCase):
    def test_rates(self):
        self.assertEqual(tb.parse_rate("30000/1001"), Fraction(30000, 1001))
        self.assertEqual(tb.parse_rate("29.97"), Fraction(30000, 1001))
        self.assertEqual(tb.parse_rate(25), Fraction(25))

    def test_frames_and_strings(self):
        r = "30000/1001"
        self.assertEqual(tb.seconds_to_frames(1.0, r), 30)
        self.assertEqual(tb.frames_to_fcp(1, r), "1001/30000s")
        self.assertEqual(tb.frames_to_fcp(30000, r), "1001s")
        self.assertEqual(tb.parse_fcp_time("1001/30000s"), Fraction(1001, 30000))
        self.assertEqual(tb.fcp_time(Fraction(0)), "0s")

    def test_no_drift_over_an_hour(self):
        r = "30000/1001"
        frames = tb.seconds_to_frames(3600, r)
        self.assertTrue(tb.is_frame_aligned(tb.frames_to_seconds(frames, r), r))
        self.assertAlmostEqual(float(tb.frames_to_seconds(frames, r)), 3600, delta=1 / 29.97)

    def test_timecode(self):
        self.assertEqual(tb.timecode_to_frames("01:00:00:00", "30000/1001"), (108000, False))
        f, drop = tb.timecode_to_frames("01:00:00;00", "30000/1001")
        self.assertTrue(drop)
        self.assertEqual(f, 107892)
        self.assertEqual(tb.timecode(107892, "30000/1001", drop=True), "01:00:00;00")
        self.assertEqual(tb.timecode(108000, "30000/1001"), "01:00:00:00")


class EasingTest(unittest.TestCase):
    def test_endpoints_and_monotonic(self):
        for name in ("power2.out", "power4.in", "expo.out", "power2.inOut", "sine.out", "circ.out", "none"):
            self.assertAlmostEqual(easing.ease(name, 0), 0, places=3)
            self.assertAlmostEqual(easing.ease(name, 1), 1, places=3)
            vals = [easing.ease(name, i / 50) for i in range(51)]
            self.assertTrue(all(b >= a - 1e-9 for a, b in zip(vals, vals[1:])), name)


class VersionTest(unittest.TestCase):
    def test_never_overwrites(self):
        with tempfile.TemporaryDirectory() as d:
            p1 = next_version(Path(d), "v_cuts", ".fcpxml")
            p1.write_text("x")
            p2 = next_version(Path(d), "v_cuts", ".fcpxml")
            self.assertEqual(p1.name, "v_cuts_v01.fcpxml")
            self.assertEqual(p2.name, "v_cuts_v02.fcpxml")


@unittest.skipUnless(HAVE_FFMPEG and HAVE_NUMPY, "needs ffmpeg and numpy")
class PipelineTest(unittest.TestCase):
    """Synthetic media through probe → cuts → compose → FCPXML → read back."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        code, out = run_script("make_test_media.py", "--out", cls.tmp / "media", "--seconds", 12)
        assert code == 0, out
        cls.media = out["files"]
        cls.edit = cls.tmp / "video" / "edit"
        code, out = run_script("probe_footage.py", "--out", cls.edit / "footage" / "footage.json",
                               "--role", f"camera={cls.media['camera']}", cls.media["camera"])
        assert code == 0, out
        (cls.edit / "cuts").mkdir(parents=True)
        cls.segments = [{"id": "s001", "file": "cam01", "in": 0.5, "out": 3.2, "text": "a"},
                        {"id": "s002", "file": "cam01", "in": 4.0, "out": 7.1, "text": "b"},
                        {"id": "s003", "file": "cam01", "in": 8.0, "out": 11.5, "text": "c"}]
        (cls.edit / "cuts" / "cuts.json").write_text(json.dumps({
            "segments": cls.segments,
            "markers": [{"id": "m001", "file": "cam01", "time": 5.0, "type": "take_doubt", "text": "check"}],
            "chapters": [{"file": "cam01", "time": 8.0, "title": "Part 2"}]}))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def build(self, stage="cuts"):
        tl = self.edit / f"timeline_{stage}.json"
        code, out = run_script("timeline_compose.py", "--edit-dir", self.edit, "--out", tl, "--stage", stage)
        self.assertEqual(code, 0, out)
        code, out = run_script("fcpxml_build.py", tl, "--out-dir", self.edit / "deliveries",
                               "--stem", f"t_{stage}", "--version", "1.14")
        self.assertEqual(code, 0, out)
        return out

    def test_probe_reads_timecode(self):
        fp = json.loads((self.edit / "footage" / "footage.json").read_text())
        cam = fp["files"][0]
        self.assertEqual(cam["rate"], "30000/1001")
        self.assertEqual(cam["tc_start_frames"], 108000)

    def test_cuts_delivery_is_frame_exact_and_valid(self):
        out = self.build("cuts")
        xml = Path(out["output"]).read_text()
        import xml.etree.ElementTree as ET

        root = ET.fromstring(xml.split("\n", 2)[2])
        rate = Fraction(30000, 1001)
        for clip in root.iter("asset-clip"):
            for attr in ("offset", "start", "duration"):
                if clip.get(attr):
                    t = tb.parse_fcp_time(clip.get(attr))
                    self.assertEqual((t * rate).denominator, 1, f"{attr}={clip.get(attr)} not frame-aligned")
        spine = root.find(".//spine")
        first = spine[0]
        self.assertEqual(tb.parse_fcp_time(first.get("start")), Fraction(108000 + 15) / rate)
        if out["validated"]:
            self.assertTrue(out["validated"])
        else:
            self.skipTest(f"DTD validation not run: {out.get('reason')}")

    def test_validation_works_when_the_dtd_path_has_spaces(self):
        import os

        from fcpxml_build import find_dtd, validate

        dtd = find_dtd("1.14")
        if dtd is None:
            self.skipTest("no FCPXML 1.14 DTD available (set FCPXML_DTD)")
        out = self.build("cuts")
        spaced = self.tmp / "Final Cut Pro.app" / "Contents"
        spaced.mkdir(parents=True, exist_ok=True)
        copy = spaced / "FCPXMLv1_14.dtd"
        copy.write_bytes(Path(dtd).read_bytes())
        old = os.environ.get("FCPXML_DTD")
        os.environ["FCPXML_DTD"] = str(copy)
        try:
            self.assertTrue(validate(Path(out["output"]), "1.14")["validated"])
        finally:
            if old is None:
                os.environ.pop("FCPXML_DTD", None)
            else:
                os.environ["FCPXML_DTD"] = old

    def test_round_trip_reconstructs_cuts(self):
        out = self.build("cuts")
        code, ret = run_script("fcpxml_read.py", out["output"], "--edit-dir", self.edit,
                               "--out", self.edit / "returns" / "r.json")
        self.assertEqual(code, 0, ret)
        data = json.loads((self.edit / "returns" / "r.json").read_text())
        self.assertEqual(len(data["segments"]), 3)
        for a, b in zip(data["segments"], self.segments):
            self.assertAlmostEqual(a["in"], b["in"], delta=1 / 29.97)
            self.assertAlmostEqual(a["out"], b["out"], delta=1 / 29.97)
        self.assertEqual(data["creator_markers"], [])
        self.assertEqual(data["diff"]["removed"], [])

    def test_creator_marker_and_trim_are_read(self):
        out = self.build("cuts")
        p = Path(out["output"])
        text = p.read_text()
        # the creator trims the first clip by 10 frames and adds a marker of their own
        import re

        m = re.search(r'(<asset-clip ref="r\d+" offset="0s"[^>]*duration=")([^"]+)(")', text)
        dur = tb.parse_fcp_time(m.group(2)) - Fraction(10 * 1001, 30000)
        text = text.replace(m.group(0), m.group(1) + tb.fcp_time(dur) + m.group(3), 1)
        text = text.replace("</asset-clip>", '  <marker start="7216209/2000s" duration="1001/30000s" value="tighter here"/>\n          </asset-clip>', 1)
        edited = p.with_name("edited.fcpxml")
        edited.write_text(text)
        code, ret = run_script("fcpxml_read.py", edited, "--edit-dir", self.edit, "--out", self.edit / "returns" / "e.json")
        self.assertEqual(code, 0, ret)
        self.assertEqual(len(ret["diff"]["trimmed"]), 1)
        self.assertEqual(ret["creator_markers"], 1)

    def test_camera_keyframes_stay_inside_the_frame(self):
        (self.edit / "camera").mkdir(exist_ok=True)
        (self.edit / "camera" / "plan.json").write_text(json.dumps({
            "base": {"closed_scale": 1.25, "creep": 0.05},
            "moves": [{"id": "cam01", "type": "punch", "time": 4.0},
                      {"id": "cam02", "type": "push_in", "segment": "s002"},
                      {"id": "cam03", "type": "arrive", "segment": "s003", "from": "below"}]}))
        code, out = run_script("camera_curves.py", "--edit-dir", self.edit)
        self.assertEqual(code, 0, out)
        cam = json.loads((self.edit / "camera" / "camera.json").read_text())
        firsts = [cam["keyframes"][s][0]["scale"][0] for s in ("s001", "s002", "s003")]
        self.assertLess(firsts[0], 1.01)           # first segment opens wide
        self.assertGreater(firsts[1], 1.2)         # then alternates to closed
        for seg, kfs in cam["keyframes"].items():
            for k in kfs:
                s = k["scale"][0]
                self.assertGreaterEqual(s, 1.0)
                lim_x = (s - 1) / 2 * 1920 / 1080 * 100 + 1e-6
                lim_y = (s - 1) / 2 * 100 + 1e-6
                self.assertLessEqual(abs(k["position"][0]), lim_x)
                self.assertLessEqual(abs(k["position"][1]), lim_y)
        out = self.build("final")
        self.assertEqual(out["spine_clips"], 3)

    def test_cut_edges_refine_on_audio(self):
        # camera audio is a continuous tone: edges may extend to padding but never cross words
        (self.edit / "transcript").mkdir(exist_ok=True)
        words = [{"w": f"w{i}", "start": 0.5 + i * 0.5, "end": 0.9 + i * 0.5, "p": 0.9} for i in range(20)]
        (self.edit / "transcript" / "cam01.words.json").write_text(json.dumps({"file": "cam01", "words": words}))
        (self.edit / "cuts" / "decisions.json").write_text(json.dumps({
            "segments": [{"id": "s001", "file": "cam01", "start": 1.02, "end": 2.88, "text": "w1"}], "padding": 0.1}))
        backup = (self.edit / "cuts" / "cuts.json").read_text()
        try:
            code, out = run_script("cut_edges.py", "--edit-dir", self.edit)
            self.assertEqual(code, 0, out)
            seg = json.loads((self.edit / "cuts" / "cuts.json").read_text())["segments"][0]
            self.assertGreaterEqual(seg["in"], 0.9 - 1e-6)    # never before the previous word ends
            self.assertLessEqual(seg["out"], 3.0 + 1e-6)      # never into the next word
            self.assertTrue(tb.is_frame_aligned(Fraction(str(seg["in"])), "30000/1001")
                            or abs(seg["in"] * 30000 / 1001 - round(seg["in"] * 30000 / 1001)) < 1e-3)
        finally:
            (self.edit / "cuts" / "cuts.json").write_text(backup)

    def test_sound_aligns_by_peak_and_stays_below_voice(self):
        (self.edit / "transcript").mkdir(exist_ok=True)
        words = [{"w": f"w{i}", "start": 0.5 + i * 0.5, "end": 0.9 + i * 0.5, "p": 0.9} for i in range(20)]
        (self.edit / "transcript" / "cam01.words.json").write_text(json.dumps({"file": "cam01", "words": words}))
        (self.edit / "sound").mkdir(exist_ok=True)
        (self.edit / "sound" / "plan.json").write_text(json.dumps({
            "items": [{"id": "sfx01", "time": 2.0, "file": self.media["sfx"], "layer": "main", "align": "start"},
                      {"id": "sfx02", "time": 5.0, "file": self.media["sfx"], "layer": "main", "align": "peak"}],
            "music": [{"id": "mus01", "file": self.media["music"], "start": 0.0, "end": 9.0, "duck": True}]}))
        code, out = run_script("sound_place.py", "--edit-dir", self.edit)
        self.assertEqual(code, 0, out)
        snd = json.loads((self.edit / "sound" / "sound.json").read_text())
        sfx = {i["id"]: i for i in snd["items"]}
        self.assertAlmostEqual(sfx["sfx01"]["seq_start"], 2.0, places=2)
        self.assertLessEqual(sfx["sfx02"]["seq_start"], 5.0)
        self.assertTrue(any("same file" in w for w in snd["warnings"]))
        self.assertTrue(sfx["mus01"]["volume_keyframes"])
        out = self.build("final")
        self.assertGreaterEqual(out["connected"], 3)


class TranscriptLogicTest(unittest.TestCase):
    def test_gaps_and_sentences(self):
        import transcribe_footage as tf

        words = [{"w": "Olá.", "start": 0.0, "end": 0.4, "p": 0.9},
                 {"w": "tudo", "start": 2.0, "end": 2.3, "p": 0.9}, {"w": "bem?", "start": 2.3, "end": 2.6, "p": 0.9}]
        gaps = tf.regions_without_words([(0.0, 0.4), (0.8, 1.6), (2.0, 2.6)], words)
        self.assertEqual(gaps, [(0.8, 1.6)])
        lines = tf.sentences(words, "cam01")
        self.assertEqual([ln["text"] for ln in lines], ["Olá.", "tudo bem?"])
        self.assertGreater(lines[0]["pause_after"], 1.5)


class NotesTest(unittest.TestCase):
    def test_finds_notes_with_variants(self):
        import spoken_notes as sn

        def ws(text, t0=0.0):
            return [{"w": w, "start": t0 + i * 0.3, "end": t0 + i * 0.3 + 0.25} for i, w in enumerate(text.split())]
        words = ws("então a gente vai ver isso. Nota de edicão, usa o segundo take, fim da nota. e segue")
        notes = sn.find_notes(words, "nota de edição", "fim da nota", "cam01")
        self.assertEqual(len(notes), 1)
        self.assertIn("segundo take", notes[0]["text"])
        self.assertNotEqual(notes[0]["confidence"], "low")


@unittest.skipUnless(HAVE_NUMPY, "needs numpy")
class SyncTest(unittest.TestCase):
    def test_finds_offset(self):
        import numpy as np

        from audio_tools import cross_correlate

        rng = np.random.default_rng(1)
        ref = rng.standard_normal(4000 * 20).astype(np.float32)
        other = ref[4000 * 5:4000 * 12]  # starts 5 s into the camera audio
        lag, conf = cross_correlate(ref, other, 4000)
        self.assertAlmostEqual(lag, 5.0, places=3)
        self.assertGreater(conf, 0.9)


if __name__ == "__main__":
    unittest.main()
