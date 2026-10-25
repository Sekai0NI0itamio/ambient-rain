# Audio candidates

Every file here is a **192 kbps HQ preview** pulled from Freesound, not the original
WAV/FLAC. That is deliberate: these are the exact files that were auditioned, so
using them guarantees the approved sound. Swap in lossless originals only if you
re-audition.

All are **CC0** (public domain), filtered on licence in the Freesound search.

## Chosen

| Role | File | Source |
|---|---|---|
| Rain bed | `rain_194209_klangfabrik.mp3` | klangfabrik — *rainstorm* — freesound.org/people/klangfabrik/sounds/194209 |
| Thunder | `thunder_572444_TRP.mp3` | TRP — *Thunder, rolling med distant constant, light rain* — freesound.org/people/TRP/sounds/572444 |

## Kept for future use

| File | Source | Duration | Drops/min | Continuity | Slope | Note |
|---|---|---|---|---|---|---|
| `rain_845501_TSP-Talk.mp3` | TSP-Talk — *Continuous Light Rain on Open Window* | 16:41 | **94.7** | 3.5 dB | −18.9 | Too many discrete drops — dripping tap |
| `rain_846307_TSP-Talk.mp3` | TSP-Talk — *Indoor Roomtone, Light–Medium Rain* | 22:47 | 7.9 | 3.1 dB | −15.1 | 39.6 % below 200 Hz — disappears on laptop speakers |
| `thunder_616987_TRP.mp3` | TRP — *Thunder, various rolling cracking distant* | 7:11 | — | — | −25.8 | 8 swells, 48.7 s apart |

## Not downloaded yet

Pull with `curl` against the HQ preview, or download the original in the browser.

| ID | Source | Duration | Description |
|---|---|---|---|
| 717890 | TRP | 4:07 | Dry distant rolling |
| 717845 | TRP | 2:57 | Dry rolling distant low rumbles — highest rated (37) |
| 572443 | TRP | 1:10 | Distant rolling boomy, rain drops |
| 438740 | craigsmith | 7:23 | Long Thunder Storm — continuous low rolling, some big cracks |

URLs: `freesound.org/people/<source>/sounds/<id>/`

## How to audition a candidate

```bash
python3 - <<'EOF'
import subprocess, numpy as np
SR=16000
def stats(f):
    x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),
        "-f","s16le","-"],capture_output=True).stdout,dtype=np.int16).astype(np.float32)/32768
    dur=len(x)/SR; w=int(2*SR)
    v=np.array([20*np.log10(np.sqrt(np.mean(x[i:i+w]**2))+1e-12) for i in range(0,len(x)-w,w)])
    hop=int(0.01*SR); win=int(0.02*SR); n=(len(x)-win)//hop
    fr=np.lib.stride_tricks.sliding_window_view(x,win)[::hop][:n]
    spec=np.abs(np.fft.rfft(fr*np.hanning(win),axis=1)); ff=np.fft.rfftfreq(win,1/SR)
    db=20*np.log10(spec[:,ff>2000].sum(axis=1)+1e-12); med=np.median(db)
    pk=[i for i in range(1,len(db)-1) if db[i]>med+8 and db[i]>=db[i-1] and db[i]>=db[i+1]]
    mg=[]
    for i in pk:
        if mg and i-mg[-1]<30:
            if db[i]>db[mg[-1]]: mg[-1]=i
        else: mg.append(i)
    M=spec.mean(axis=0); sel=(ff>=50)&(ff<=8000)
    print(f"{f}: {dur:.0f}s  continuity std={v.std():.1f}dB  drops/min={len(mg)/dur*60:.1f}  "
          f"slope={np.polyfit(np.log10(ff[sel]),20*np.log10(M[sel]),1)[0]:.1f}")
stats("sources/candidates/rain_194209_klangfabrik.mp3")
EOF
```

**Reading the numbers:** `drops/min` is the dripping-tap test (lower = cleaner rain).
`continuity std` is level variance over 2 s windows (lower = steadier, less "wave").
`slope` is dB per decade — pink noise is −9, brown −18, white 0. Rain sits naturally
between −6 and −10.
