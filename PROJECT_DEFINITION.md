# Dividend Vision — Project Definition

**Version:** 1.0  
**Date:** 2026-01-03  
**Status:** Foundation Phase

---

## 1. Project Philosophy

Dividend Vision operates on a simple principle: **create visual assets that generate passive income over time, like financial dividends**.

### Core Principles

**Stability Over Innovation**  
We prioritize reliable, repeatable output over experimental features. The system should work the same way today as it will in six months.

**Reusability Over Uniqueness**  
Generated videos are not art pieces. They are functional visual assets designed for broad commercial use across multiple buyer contexts.

**Production Over Perfection**  
A complete, usable 20-second nature video is more valuable than an incomplete "perfect" shot. Quality is defined by stock approval rates, not artistic merit.

**Simplicity Over Complexity**  
The entire workflow should be: edit text file → run notebook → download results. No complex configurations, no technical decisions during operation.

**Long-term Income Over Quick Sales**  
This system is designed to build a catalog of 500+ videos over time, generating consistent small revenues rather than viral hits.

---

## 2. Scope Definition

### What This System WILL Generate

**Acceptable Subjects:**

- Natural landscapes (mountains, valleys, coastlines)
- Abstract nature patterns (water ripples, cloud formations, sand textures)
- Vegetation in motion (grass swaying, leaves rustling, tree branches)
- Weather phenomena (fog rolling, rain falling, snow accumulating)
- Elemental close-ups (water droplets, ice crystals, rock surfaces)
- Seasonal transitions (autumn leaves, spring blooms)

**Acceptable Motion Types:**

- Slow, steady camera movements (gentle pan, subtle zoom)
- Natural object motion (wind effects, water flow)
- Gradual environmental changes (lighting shifts, weather progression)
- Loopable patterns (waves, particles, organic textures)

**Technical Output:**

- 512×512 or 768×768 initial resolution (will be upscaled externally via Topaz)
- 3-5 second clips (can be looped or concatenated)
- 24-30 FPS
- Documentary-neutral aesthetic (no stylization filters)

---

### What This System WILL NOT Generate

**Excluded Subjects:**

- ❌ People, faces, body parts
- ❌ Animals, wildlife, pets
- ❌ Buildings, architecture, infrastructure
- ❌ Vehicles, machinery, technology
- ❌ Branded objects, logos, identifiable products
- ❌ Text, signage, readable content
- ❌ Fantasy elements (dragons, magic, sci-fi)
- ❌ Surreal compositions (floating objects, impossible physics)
- ❌ Identifiable locations (Eiffel Tower, Grand Canyon landmarks)

**Excluded Motion Types:**

- ❌ Dramatic camera whips or crash zooms
- ❌ Exaggerated cinematic effects (lens flares, bokeh exaggeration)
- ❌ Fast action or chaotic movement
- ❌ AI-generated "morphing" or unrealistic transitions
- ❌ Time-lapse exaggeration (unless naturally believable)

**Technical Exclusions:**

- ❌ Vertical (9:16) social media formats
- ❌ 4K native generation (always upscale externally)
- ❌ Audio/music generation
- ❌ Multi-shot editing or montages

---

## 3. Pipeline Overview

### Text → Image → Video (Minimal 3-Stage Pipeline)

```
┌─────────────────────┐
│  INPUT              │
│  prompts.txt        │──► Each line = one video concept
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│  STAGE 1            │
│  Image Generation   │──► Stable Diffusion on Colab
│  (512×512)          │    (T4 GPU, ~30 sec/image)
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│  STAGE 2            │
│  Image-to-Video     │──► AnimateDiff or similar
│  (3-5 seconds)      │    (T4 GPU, ~2-3 min/video)
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│  STAGE 3            │
│  Quality Filter     │──► Auto-reject obvious failures
│  (automatic)        │    (blur, artifacts, violations)
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│  OUTPUT             │
│  Google Drive       │──► Organized by date + prompt ID
│  /results/          │    User reviews, downloads keepers
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│  EXTERNAL           │
│  Topaz Upscale      │──► User handles offline
│  (not automated)    │    1920×1080 or 4K
└─────────────────────┘
```

### Operational Flow

1. **User edits** `prompts.txt` in Google Drive (plain text, one prompt per line)
2. **User runs** Colab notebook (one-click, no configuration changes)
3. **System processes** all prompts sequentially (image → video → filter)
4. **System saves** results to Google Drive with timestamp and prompt reference
5. **User reviews** outputs in Drive, deletes failures, downloads keepers
6. **User upscales** externally using Topaz Video Enhance AI

---

## 4. Google Drive Folder Structure

```
/DividendVision/
│
├── 📁 inputs/
│   └── prompts.txt ──────────────► User edits this file
│
├── 📁 outputs/
│   ├── 📁 2026-01-03_batch_001/
│   │   ├── raw_videos/ ──────────► Unfiltered video outputs
│   │   ├── approved/ ────────────► Auto-approved by quality filter
│   │   ├── flagged/ ─────────────► Questionable outputs for review
│   │   └── batch_log.txt ────────► Generation metadata
│   │
│   └── 📁 2026-01-05_batch_002/
│       └── [same structure]
│
├── 📁 archive/
│   └── [old batches moved here after processing]
│
├── 📁 ready_for_upscale/
│   └── [user manually moves keepers here]
│
└── 📄 config.txt ────────────────► System settings (rarely changed)
```

### File Usage

**prompts.txt format:**

```
misty mountain valley at dawn, soft golden light filtering through fog
gentle ocean waves on rocky shore, overcast sky
autumn forest floor covered in fallen leaves, slight breeze
```

**config.txt format:**

```
resolution=512
fps=24
video_length=4
quality_threshold=0.7
```

---

## 5. Stock Approval Visual Constraints

To maximize Adobe Stock acceptance rates, all outputs must adhere to:

### Composition Rules

- **No centered subjects** — use rule of thirds or natural asymmetry
- **Clean edges** — no partial objects cut off awkwardly at frame borders
- **Consistent lighting** — avoid sudden exposure changes mid-clip
- **Natural color grading** — no oversaturated or artificial-looking tones

### Technical Requirements

- **100% AI-disclosed** — all uploads will be marked as AI-generated
- **No copyright elements** — zero recognizable IP, brands, or locations
- **No identifiable content** — nothing that could require a model/property release
- **Smooth motion** — no jitter, warping, or morphing artifacts
- **Sharp focus** — primary subject must be clear (slight natural blur OK)

### Common Rejection Triggers (TO AVOID)

- ❌ Visible AI morphing or "melting" effects
- ❌ Unnatural physics (water flowing upward, impossible structures)
- ❌ Blurry or low-quality outputs
- ❌ Frame-edge artifacts (black bars, warped corners)
- ❌ Inconsistent style mid-clip (lighting/color shifts)
- ❌ Text or text-like patterns the AI might hallucinate

---

## 6. Quality Definition for This Project

Quality is **NOT** about:

- Artistic beauty or emotional impact
- Cinematic drama or viral appeal
- Technical perfection or 4K sharpness

Quality **IS** defined by:

### 1. Stock Approval Rate

**Target:** 70%+ of generated videos pass Adobe Stock review  
**Measurement:** Track rejections and categorize reasons

### 2. Believability

**Test:** "Could this have been filmed with a real camera?"  
**Standard:** Footage should feel neutral and documentary-like, not obviously AI-generated

### 3. Reusability

**Test:** "Can this be used in 5+ different buyer contexts?"  
**Standard:** Generic enough for travel blogs, corporate backgrounds, meditation apps, etc.

### 4. Stability

**Test:** "Does the same prompt produce usable results 8/10 times?"  
**Standard:** Consistent output quality without frequent catastrophic failures

### 5. Efficiency

**Test:** "Can the user generate 20 videos in one Colab session?"  
**Standard:** Batch processing without manual intervention or troubleshooting

---

## Quality Tiers (Internal Classification)

**Tier 1 — Approved** (70% target)  
Meets all stock constraints, immediately uploadable

**Tier 2 — Usable with Edits** (20% acceptable)  
Minor issues fixable in post (trim edges, color correction)

**Tier 3 — Failed** (10% expected)  
Obvious artifacts, unusable, delete immediately

---

## Success Metrics (90-Day Checkpoint)

- [ ] 200+ videos generated
- [ ] 140+ videos approved by Adobe Stock (70% rate)
- [ ] System runs without code modifications for 30+ days
- [ ] User operates system without technical assistance
- [ ] First passive income received ($1+ earned)

---

## Next Steps

This document defines **WHAT** the system will do.  
The next phase will define **HOW** to implement it.

**Step 1 completed. Ready to proceed to pipeline implementation.**
