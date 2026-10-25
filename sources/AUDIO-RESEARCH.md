# What level and spectrum actually suit sleep / focus

Research summary for the rain channel, with what we set and why. Numbers are quoted from the sources; our own measurements are marked **measured**.

## Loudness

| Use case | Target | Source |
|---|---|---|
| Streaming music | −14 LUFS | Insomnus loudness guide |
| Podcasts | −16 to −18 LUFS | same |
| **Sleep / ambient** | **−24 to −30 LUFS**, LRA 4–8 LU | same (sleep narration guidance; LRA range is explicit) |
| Binaural beats | −40 to −48 LUFS | same |
| White noise at the ear | **40–55 dB SPL** — "about the level of soft rain"; use the quietest setting that masks | ambientnoise.io |
| Long-exposure safety limit | 70 dB(A) | WHO, cited in the same guide |
| Bedroom background | **≤ 30 dB(A)** mean | sleep-acoustics study, PMC5187651 |

Key point: the LUFS number is not the listening level. A listener sets their own volume, so file loudness is chosen so that a *normal* playback setting lands in the 40–55 dB SPL window rather than blasting. A −14 LUFS master would sit far above it.

**Where we are (measured):** −26.4 LUFS integrated, LRA 4.1 LU, true peak −3.6 dBTP. Inside the sleep band, at the quieter end, with a loudness range at the bottom of the recommended 4–8 LU — i.e. it never swells.

If the channel ever ships a **focus** version rather than sleep, −22 LUFS is a reasonable step up; study content tolerates more level than sleep.

## Spectrum

- **Pink noise** (−3 dB/octave) has the best evidence base for sleep: in a systematic review of 34 studies, **81.9 % of pink-noise studies reported improved sleep outcomes vs 33 % for white noise** (JCSM, [link](https://link.springer.com/article/10.5664/jcsm.9860)).
- **Brown noise** (−6 dB/octave) is rated emotionally **more "sublime" and less uneasy** than white noise across two studies (n = 84 and n = 1280, Frontiers in Neuroscience 2025). It also had *minimal* effect on brainwave activity — neutral background rather than an active sedative.
- **White noise** carries the **highest unease ratings** of the three. That matches the complaint that a hissy bed "sounds like static".
- **Low frequency:** infrasound and low-frequency sound (10–60 Hz) left sleep architecture "little affected", while *audible* sound was "considerably" more disruptive (ScienceDirect). So sub-bass is harmless but pointless, and harsh mid/high content is the part that actually wakes people.
- **Transients are the enemy.** Every source on sleep audio converges on the same thing: arousals come from sudden changes, not from steady level. A thunderclap is the textbook example.

## What that means for our mix

| Property | Reference | Ours (measured) |
|---|---|---|
| Spectral slope, 50 Hz–8 kHz | pink = −9 dB/decade, brown = −18, white = 0 | **−7.4 dB/decade** |
| Energy > 6 kHz | keep low (white noise = unease) | **11.5 %** (was 22 % before the tilt) |
| Energy < 60 Hz | harmless, inaudible on most speakers | 8.2 % |
| Integrated loudness | −24 to −30 LUFS | **−26.4** |
| Loudness range | 4–8 LU | **4.1** |
| Peak | ≤ −3 dBTP | **−3.6** |

Our slope sits between white and pink, closer to pink — which is the best-supported region, and it is why the bed reads as rain rather than hiss. Pushing all the way to brown (−18) would make it a rumble that most laptops cannot reproduce at all.

## Rules derived from this

1. **No scheduled transients — unless the brief says otherwise.** Thunder is exactly the stimulus the sleep literature identifies as arousing. It is in the build because it was asked for, softened with long fades and 55 s+ spacing. Cost, measured: **LRA 13.0 LU vs the recommended 4–8**. The no-thunder variant sits near 4.
2. **Keep the slope near −7 to −9 dB/decade.** Brighter than −5 drifts toward white noise (unease, "static"); darker than −12 becomes inaudible rumble on phone speakers.
3. **Hold −26 LUFS for sleep, −22 for focus.** Never master to −14 just because streaming music does.
4. **LRA under 8 LU.** No builds, no swells, no drops.
5. **Peak ≤ −3 dBTP**, so a listener's own EQ or volume boost cannot clip it.

## Sources

- Insomnus, *Loudness Standards for Sleep Audio* — https://insomnus.app/blog/loudness-standards-sleep-audio
- Yoon & Baek, *External Auditory Stimulation as a Non-Pharmacological Sleep Aid*, Sensors 2022 — https://doi.org/10.3390/s22031264
- Systematic review, *Auditory stimulation and sleep*, JCSM — https://link.springer.com/article/10.5664/jcsm.9860
- Færøvik, Vikene & Specht, *Are brown, pink and white noise neutral control stimuli?*, Frontiers in Neuroscience 2025 — https://doi.org/10.3389/fnins.2025.1488682
- *How Loud Should White Noise Be?* — https://www.ambientnoise.io/blog/how-loud-should-white-noise-be
- Sleep acoustics / bedroom level, PMC5187651 — https://pmc.ncbi.nlm.nih.gov/articles/PMC5187651/
- *Comparative study of infrasound and low-frequency sound on sleep*, ScienceDirect — https://www.sciencedirect.com/science/article/pii/016041209090017Z
