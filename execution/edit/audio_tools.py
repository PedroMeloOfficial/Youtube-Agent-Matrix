"""
Audio measurements shared by the editing scripts (library module, no CLI).

- ``envelope``: RMS energy in short windows, in dBFS -- the basis for cut edges, silence
  maps and "sound without words" detection;
- ``noise_floor`` / ``speech_threshold``: adaptive levels per file, because a quiet room
  and a noisy street need different thresholds;
- ``speech_regions``: Silero VAD (the ONNX model bundled with faster-whisper, no PyTorch)
  when available, else an energy-based fallback that says so;
- ``integrated_lufs``: EBU R128 loudness through ffmpeg's ``ebur128`` filter;
- ``cross_correlate``: offset between two recordings of the same sound (sync).

All times are seconds from the start of the file.
"""

from __future__ import annotations

import re

from common import require_module, require_tool, run

RATE = 16000
HOP = 0.01  # 10 ms analysis windows


def envelope(pcm, rate: int = RATE, hop: float = HOP):
    np = require_module("numpy")
    n = max(1, int(rate * hop))
    usable = len(pcm) - len(pcm) % n
    if usable <= 0:
        return np.array([-120.0])
    frames = pcm[:usable].reshape(-1, n)
    rms = np.sqrt(np.mean(frames.astype(np.float64) ** 2, axis=1) + 1e-12)
    return 20 * np.log10(rms + 1e-12)


def noise_floor(env) -> float:
    np = require_module("numpy")
    return float(np.percentile(env, 10))


def speech_threshold(env) -> float:
    """Halfway (in dB) between the noise floor and typical speech level, at least +10 dB."""
    np = require_module("numpy")
    floor = noise_floor(env)
    loud = float(np.percentile(env, 90))
    return max(floor + 10.0, (floor + loud) / 2.0)


def voiced_mask(env, threshold: float):
    return env > threshold


def runs(mask, hop: float = HOP, min_len: float = 0.0):
    """Contiguous True runs of a boolean mask -> [(start_s, end_s)]."""
    out, start = [], None
    for i, v in enumerate(mask):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if (i - start) * hop >= min_len:
                out.append((start * hop, i * hop))
            start = None
    if start is not None and (len(mask) - start) * hop >= min_len:
        out.append((start * hop, len(mask) * hop))
    return out


def speech_regions(pcm, rate: int = RATE):
    """[(start, end)] of speech, and which method produced them."""
    try:
        from faster_whisper.vad import VadOptions, get_speech_timestamps

        ts = get_speech_timestamps(pcm, VadOptions(min_silence_duration_ms=250, speech_pad_ms=60))
        return [(t["start"] / rate, t["end"] / rate) for t in ts], "silero-vad"
    except ImportError:
        env = envelope(pcm, rate)
        return runs(voiced_mask(env, speech_threshold(env)), min_len=0.15), "energy (install faster-whisper for Silero VAD)"


def integrated_lufs(path, start: float | None = None, duration: float | None = None) -> float | None:
    require_tool("ffmpeg")
    cmd = ["ffmpeg", "-nostdin", "-hide_banner"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", str(path)]
    if duration is not None:
        cmd += ["-t", f"{duration:.3f}"]
    cmd += ["-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"]
    import subprocess

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    text = proc.stderr
    m = re.findall(r"I:\s+(-?[\d.]+)\s+LUFS", text)
    return float(m[-1]) if m else None


def true_peak_dbfs(path) -> float | None:
    import subprocess

    require_tool("ffmpeg")
    proc = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path), "-map", "0:a:0",
                           "-af", "ebur128=peak=true", "-f", "null", "-"],
                          capture_output=True, text=True, timeout=600)
    m = re.findall(r"Peak:\s+(-?[\d.]+|-inf)\s+dBFS", proc.stderr)
    if not m or m[-1] == "-inf":
        return None
    return float(m[-1])


def cross_correlate(ref, other, rate: int = RATE, max_lag_s: float | None = None):
    """Offset of ``other`` inside ``ref``: ref(t + lag) ≈ other(t). Returns (lag_s, confidence).

    Confidence is the Pearson correlation of the two signals over their overlap at the
    best lag (0..1). Below ~0.3 the match is not trustworthy and must not be used.
    """
    np = require_module("numpy")
    a = ref.astype(np.float64)
    b = other.astype(np.float64)
    n = 1
    while n < len(a) + len(b):
        n *= 2
    corr = np.fft.irfft(np.fft.rfft(a - a.mean(), n) * np.conj(np.fft.rfft(b - b.mean(), n)), n)
    corr = np.concatenate([corr[-(len(b) - 1):], corr[:len(a)]]) if len(b) > 1 else corr[:len(a)]
    lags = np.arange(-(len(b) - 1), len(a))
    if max_lag_s is not None:
        keep = np.abs(lags) <= int(max_lag_s * rate)
        corr, lags = corr[keep], lags[keep]
    lag = int(lags[int(np.argmax(corr))])
    lo_a, hi_a = max(0, lag), min(len(a), lag + len(b))
    seg_a = a[lo_a:hi_a]
    seg_b = b[lo_a - lag:hi_a - lag]
    if len(seg_a) < rate // 2:
        return lag / rate, 0.0
    conf = float(np.corrcoef(seg_a, seg_b)[0, 1])
    return lag / rate, max(0.0, conf)


def run_ffmpeg_extract(path, out_wav, rate: int = RATE):
    require_tool("ffmpeg")
    run(["ffmpeg", "-y", "-v", "error", "-nostdin", "-i", str(path), "-map", "0:a:0",
         "-ac", "1", "-ar", str(rate), str(out_wav)], timeout=3600)
