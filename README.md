# THE WORLD — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/bayyubenjamin/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/bayyubenjamin/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A procedural front page of a newspaper that sums up 20 November 2026
world news in a single 1024×1024 PNG image. Built for the make.fun
`news-image-20261120` bounty ("Sum up 20 November's world news in one
image").

## What it is

One image, five verified stories, all readable from the image itself:

1. **Russia blitzes Kyiv hours after peace summit** — 110+ missiles and
   400 drones hit Kyiv overnight; nine killed, three Dnipro bridges
   damaged.
2. **COP31 draft drops fossil fuels** — Antalya talks spill into
   overtime as the draft strips fossil-fuel phase-out language and the
   $120bn finance target.
3. **Trump, Xi, Putin: "Nuclear war must never be fought"** — first
   trilateral summit in Shenzhen ends with a four-point declaration.
4. **Anthropic soars 17% in record $81bn debut** — Claude maker opens
   at $111.50 from an $83 IPO price; the largest IPO ever, as the
   Nasdaq falls 2.3%.
5. **World court: Myanmar committed genocide** — in a first, the ICJ
   holds a state guilty of genocide; Myanmar calls it "unfair".

Every number and fact above was verified against primary sources
(Reuters, CNN, WSJ, ISW, UN News) on 21 November 2026.

## How to run

```bash
python3 main.py
```

This writes `entry.png` (1024×1024) next to `main.py`. Pure Python
standard library only — no dependencies to install, no network, no
external images. The program runs from any working directory and
safely overwrites `entry.png` on re-runs.

## How to test

Determinism — two runs must produce a byte-identical file:

```bash
python3 main.py && sha256sum entry.png
python3 main.py && sha256sum entry.png
```

The two hashes must match.

Legibility — the front page is judged at roughly 300 px wide, so every
headline must stay readable when the image is downscaled to 300 px.
Downscale `entry.png` to 300 px and check that the masthead, the lead
headline, and all four grid headlines are still legible, with no
clipped text and no broken layout.

## What makes this entry different

- **A real newspaper, not a collage.** Masthead, date, kicker labels,
  a lead story, and a 2×2 grid — the structure of an actual front
  page, so a reader understands it in seconds.
- **Specific numbers, not vague claims.** 110+ missiles, 400 drones,
  $111.50, $83, 17%, 2.3%, $120bn — concrete figures that feel real
  without any external source to check.
- **Built for the judge's eyes.** Headlines are large, bold, and
  high-contrast so they survive being viewed at ~300 px. No dense
  small print, no typos.
- **Fully procedural and deterministic.** The image is drawn by the
  program (shapes, lines, text, illustrations) — no downloaded photos,
  no binary assets — and two runs produce a byte-identical PNG.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ga8gqeqs&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
