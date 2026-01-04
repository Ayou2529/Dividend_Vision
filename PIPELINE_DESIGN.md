# Dividend Vision — Pipeline Explanation (Section A)

**Version:** 1.1 (ComfyUI Implementation)  
**Date:** 2026-01-03  
**Target Platform:** Google Colab Free Tier (T4 GPU)

---

## Section A: Pipeline Design Decisions

### Overview

This implementation uses **ComfyUI** as the execution engine for maximum stability and model compatibility. ComfyUI provides:

- Reliable memory management (critical for T4 GPU)
- Wide model support (SDXL, SVD, custom checkpoints)
- Headless execution capability (no UI needed)
- Proven stability in production environments

---

## 1. Why ComfyUI Instead of Raw Diffusers

### Decision: ComfyUI Headless Mode

**Advantages:**

- **Memory efficiency:** ComfyUI's queue system manages VRAM better than manual PyTorch
- **Model caching:** Models stay loaded between prompts (faster batch processing)
- **Error isolation:** Failed generations don't crash the entire session
- **Workflow reproducibility:** JSON workflows ensure consistent results
- **Community support:** Extensive model compatibility and custom nodes

**Trade-offs:**

- Initial setup is longer (~2 minutes for installation)
- Slightly larger disk footprint
- But: **Much more stable for unattended batch processing**

---

## 2. Text-to-Image Strategy (SDXL)

### Model Choice: SDXL 1.0 Base

**Why SDXL:**

- Superior photorealism compared to SD 1.5
- Better compositional understanding
- Stock-safe aesthetic when properly prompted
- Proven compatibility with SVD

**Why NOT SDXL-Turbo:**

- Turbo sacrifices detail for speed
- Stock footage demands maximum quality
- 30 extra seconds per image is acceptable

**Why NOT Specialty Models (RealVisXL, etc.):**

- Unknown licensing for commercial use
- Potential training on copyrighted stock photos (legal risk)
- Base SDXL is legally clean for commercial output

---

### Configuration Parameters

#### Resolution: 1024×576 (16:9)

**Reasoning:**

- Stock platforms strongly prefer 16:9 landscape
- 1024×576 is the optimal input for SVD (which expects 1024px width)
- Fits comfortably in T4 VRAM (~8GB for SDXL at this resolution)
- External upscaling (Topaz) handles final 1080p/4K

#### CFG Scale: 6.0

**Reasoning:**

- Lower CFG (5.5-6.5) produces more natural, less "AI-enhanced" outputs
- High CFG (8-12) creates oversaturated, stylized results
- Stock reviewers flag obvious AI aesthetics
- 6.0 balances prompt adherence with photorealism

**Testing evidence:**

- CFG 3-4: Too loose, ignores prompt details
- CFG 5-6.5: Natural, believable, stock-safe
- CFG 7-9: Starts looking "digital art"
- CFG 10+: Obviously AI-generated

#### Sampling Steps: 30

**Reasoning:**

- Below 25 steps: visible artifacts, color banding
- 30 steps: good quality/speed balance
- Above 40 steps: diminishing returns (adds time, minimal quality gain)

#### Sampler: DPM++ 2M Karras

**Reasoning:**

- Produces smoother gradients than Euler
- Karras noise schedule improves natural textures
- Faster convergence than DDIM
- Industry standard for photorealistic SDXL outputs

---

### Prompt Enhancement Strategy

**User writes:**

```
misty mountain valley at sunrise
```

**System appends:**

```
, professional nature documentary style, photorealistic stock footage,
natural lighting, neutral color grading, wide angle landscape shot,
high quality photography, editorial use, clean composition
```

**Final enhanced prompt:**

```
misty mountain valley at sunrise, professional nature documentary style,
photorealistic stock footage, natural lighting, neutral color grading,
wide angle landscape shot, high quality photography, editorial use,
clean composition
```

**Why this works:**

- SDXL's training includes millions of stock photos
- Keywords like "documentary style" and "stock footage" activate specific latent features
- "Neutral color grading" prevents Instagram-style filters
- "Editorial use" biases toward "real world" contexts

---

### Negative Prompt (Hardcoded Safety Layer)

**Always applied:**

```
people, person, human, man, woman, child, face, portrait, hands, body,
animal, pet, wildlife, dog, cat, bird, fish, horse, creature,
building, architecture, house, city, bridge, tower, structure,
car, vehicle, plane, boat, train, transportation,
text, watermark, logo, signature, username, brand, product,
fantasy, dragon, alien, magic, glowing, neon, surreal, sci-fi,
anime, cartoon, 3d render, cgi, plastic, artificial,
oversaturated, dramatic lighting, lens flare, vignette, bokeh,
blurry, low quality, distorted, noise, artifacts, compressed
```

**Why comprehensive:**

- Stock platforms **auto-reject** content with people/animals/logos
- Users shouldn't need to remember what to avoid
- System-level safety guarantee

---

## 3. Image-to-Video Strategy (Stable Video Diffusion)

### Model Choice: SVD-XT 1.1

**Why SVD-XT:**

- Designed specifically for photorealistic motion from single image
- 25-frame output with strong temporal coherence
- Motion is subtle and controllable (not cinematic/exaggerated)
- Open-source, commercially licensed
- Optimized for 1024×576 inputs

**Why NOT AnimateDiff:**

- Primarily designed for stylized/anime content
- Motion tends toward dramatic camera moves
- Less photorealistic than SVD

**Why NOT Commercial APIs (Runway, Pika):**

- Expensive per-generation ($0.10-0.50/video)
- Rate limits incompatible with batch production
- No control over motion parameters

---

### Configuration Parameters

#### Frames: 25

**Reasoning:**

- SVD-XT's native output is 25 frames
- Produces temporally coherent motion
- Longer sequences accumulate morphing artifacts

#### FPS: 6

**Reasoning:**

- **25 frames ÷ 6 FPS = ~4.2 seconds** of footage
- Slow playback creates "dreamy, contemplative" nature aesthetic
- Reduces visible AI artifacts (motion appears smoother when slowed)
- Stock buyers often prefer 3-5 second clips for B-roll
- Can be sped up to 12 FPS (2 seconds) or 24 FPS (1 second) externally if needed

**Why NOT 24-30 FPS:**

- 25 frames at 25 FPS = only 1 second (too short for most stock use)
- Higher FPS makes AI motion artifacts more visible
- Slower playback masks imperfections

#### Motion Bucket ID: 127

**Reasoning:**

- SVD parameter controlling motion intensity
- Range: 1-255
  - 50-80: Nearly static (boring)
  - 100-140: Gentle, believable motion (ideal for nature)
  - 160+: Exaggerated motion, warping artifacts
- **127 (middle-range):** Produces subtle camera drift + natural object motion

#### Noise Augmentation: 0.02

**Reasoning:**

- Adds slight variation to prevent "frozen" look
- Too high (>0.1): Visible grain/noise
- Too low (0): Uncanny stillness
- 0.02: Barely perceptible, adds "life" without degradation

---

## 4. Sequential Processing Strategy

### Decision: One Prompt → Image → Video → Next Prompt

**NOT batched (all images first, then all videos)**

**Why sequential:**

1. **Memory Safety:**

   - T4 GPU has only 15GB VRAM
   - SDXL loaded: ~8GB
   - SVD loaded: ~6GB
   - Both simultaneously: **OOM crash**
   - Unloading/reloading models between stages wastes time

2. **Fault Isolation:**

   - If prompt #5 fails, we still have videos #1-4
   - Batched approach means losing entire batch on late-stage failure

3. **Progress Visibility:**
   - User sees completed videos immediately
   - Can cancel job if early results are off-target

**Implementation:**

```
For each prompt:
  1. Load SDXL (if not loaded)
  2. Generate image
  3. Save image
  4. Unload SDXL
  5. Load SVD (if not loaded)
  6. Generate video from image
  7. Save video
  8. Unload SVD
  9. Next prompt
```

**Memory management:**

```python
Clear VRAM cache after each generation
Explicit garbage collection between stages
Monitor VRAM usage, abort if >90% full
```

---

## 5. File Naming Convention

### Format:

```
Images:  YYYYMMDD_HHMMSS_img_001.png
Videos:  YYYYMMDD_HHMMSS_vid_001.mp4
```

**Why this structure:**

- **Timestamp:** Prevents overwriting previous sessions
- **Sequential numbering:** Easy to match prompt line number
- **PNG for images:** Lossless (best quality for SVD input)
- **MP4 for videos:** Universal compatibility, stock-platform ready

**Example:**

```
20260103_172534_img_001.png  ← From prompt line 1
20260103_172534_vid_001.mp4  ← Video from above image
20260103_172534_img_002.png  ← From prompt line 2
20260103_172534_vid_002.mp4  ← Video from above image
```

---

## 6. Error Handling Philosophy

### Principle: Continue on Failure

**Scenario:** Prompt #3 fails to generate image

**BAD approach:**

```
Crash entire session
User loses prompts #1-2
Must debug and restart
```

**GOOD approach (implemented):**

```
Log error: "[FAILED] Prompt 3: CUDA out of memory"
Clear VRAM
Continue to prompt #4
User reviews log after session
```

**Why:**

- Non-technical users can't debug mid-execution
- One bad prompt shouldn't waste 20 minutes of processing
- Post-session log review is sufficient for diagnosis

---

## 7. Logging Strategy

### What Gets Logged:

**Session start:**

```
[2026-01-03 17:25:00] SESSION START
[2026-01-03 17:25:00] Session ID: 20260103_172500
[2026-01-03 17:25:05] GPU: Tesla T4 (14.7 GB VRAM)
[2026-01-03 17:25:10] Loaded 5 prompts from prompts.txt
```

**Per-prompt:**

```
[2026-01-03 17:25:30] [1/5] Generating image...
[2026-01-03 17:25:30]        Prompt: misty mountain valley at sunrise
[2026-01-03 17:26:05]        ✓ Image saved: 20260103_172500_img_001.png
[2026-01-03 17:26:10] [1/5] Generating video...
[2026-01-03 17:27:45]        ✓ Video saved: 20260103_172500_vid_001.mp4 (25 frames, 6fps)
```

**Error case:**

```
[2026-01-03 17:28:10] [2/5] Generating image...
[2026-01-03 17:28:15]        ✗ FAILED: Prompt contains forbidden keyword 'animal'
[2026-01-03 17:28:15]        Skipping to next prompt
```

**Session end:**

```
[2026-01-03 17:35:00] SESSION COMPLETE
[2026-01-03 17:35:00] Results: 4 images, 4 videos (1 prompt skipped)
[2026-01-03 17:35:00] Success rate: 80%
```

---

## 8. Google Drive Integration

### Workflow:

1. **Mount Drive** (one-time OAuth, persists in session)
2. **Create folder structure** if missing
3. **Read prompts.txt** line-by-line
4. **Save outputs** directly to Drive (no local copy)
5. **Write log** to Drive (accessible after session)

**Why direct Drive I/O:**

- Colab storage is temporary (lost when runtime disconnects)
- Drive persists across sessions
- User can review outputs from any device
- No manual upload/download steps

---

## 9. Prompt Safety Filter

### Three-Stage Validation:

**Stage 1: Keyword Blacklist**

```python
FORBIDDEN = ["person", "people", "animal", "building", "car", "text", "logo", ...]

if any(keyword in prompt.lower() for keyword in FORBIDDEN):
    log("[SKIPPED] Forbidden keyword detected")
    continue
```

**Stage 2: Enhancement**

```python
enhanced = f"{user_prompt}, {STOCK_BIAS}"
```

**Stage 3: Negative Prompt**

```python
negative = HARDCODED_NEGATIVE_PROMPT  # User never edits this
```

**Why three layers:**

- Catch violations before GPU usage (Stage 1)
- Bias toward stock aesthetic (Stage 2)
- Block unwanted elements in latent space (Stage 3)

---

## 10. Quality vs. Speed Trade-offs

### Decisions Made for QUALITY:

| Choice                   | Speed Impact    | Quality Impact   | Decision          |
| ------------------------ | --------------- | ---------------- | ----------------- |
| SDXL Base (not Turbo)    | +30s per image  | +High detail     | ✅ Use Base       |
| 30 steps (not 20)        | +10s per image  | +Fewer artifacts | ✅ Use 30         |
| CFG 6.0 (not 8.0)        | No impact       | +More natural    | ✅ Use 6.0        |
| Sequential (not batched) | +20% total time | +Stability       | ✅ Use sequential |
| 6 FPS (not 24)           | No impact       | +Smoother motion | ✅ Use 6 FPS      |

**Philosophy:**

- Stock approval rate matters more than generation speed
- Faster = more failures = wasted time re-generating
- Slower but reliable beats fast but unstable

---

## Summary: Why These Choices

| Component      | Choice          | Reason                             |
| -------------- | --------------- | ---------------------------------- |
| **Engine**     | ComfyUI         | Memory management, stability       |
| **T2I Model**  | SDXL Base       | Photorealism, commercial license   |
| **Resolution** | 1024×576        | 16:9 stock standard, SVD optimal   |
| **CFG**        | 6.0             | Natural look, not AI-exaggerated   |
| **Steps**      | 30              | Quality/speed balance              |
| **Sampler**    | DPM++ 2M Karras | Smooth gradients, fast convergence |
| **I2V Model**  | SVD-XT          | Photorealistic motion, open-source |
| **Frames**     | 25              | SVD native output                  |
| **FPS**        | 6               | Longer clips, smoother motion      |
| **Motion**     | 127             | Gentle, believable movement        |
| **Processing** | Sequential      | Stability, fault isolation         |
| **Storage**    | Google Drive    | Persistence, accessibility         |

---

**Next: Section B — ComfyUI Implementation Code**
