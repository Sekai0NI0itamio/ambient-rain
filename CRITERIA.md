# Criteria: ambient rain MVP

- [x] 60s REAL-sample rain WAV renders without clipping (peak 0.89, crest 18.27 vs synth 5.15)
- [x] Real footage muxed: ambient_real.mp4 60s 1280x720 30fps (Mixkit forest rain + real rain mix)
- [ ] No audible loop click when looped (end crossfades to start, equal-power)
- [ ] Three layers present: bed wash + patter + sparse droplets with different timescales
- [ ] Weather-state intensity curve changes over minutes, seeded for reproducibility
- [ ] Video looper creates seamless xfade loop from any input mp4 + muxes generated WAV
- [x] All source assets PD / CC BY / Pexels only — no SA, no NC, no login-walled samples in repo (audit: sources/LICENSED-ASSETS.md)
- [ ] Legacy copyleft assets removed and re-rendered (`rain_garden.ogg` FAL, `rain_heavy.ogg` CC BY-SA)
- [ ] `python3 rain_sim.py --duration 30` + `python3 video_loop.py` both exit 0
