# Dividend Vision — Project Files

This directory contains the complete Dividend Vision system for generating stock-safe AI videos on Google Colab.

## Files Overview

### Documentation

- **`PROJECT_DEFINITION.md`** — Project philosophy, scope, and quality standards
- **`PIPELINE_DESIGN.md`** — Technical explanation of SDXL + SVD-XT pipeline architecture
- **`USAGE_INSTRUCTIONS.md`** — Non-technical user guide (start here)
- **`README.md`** — This file

### Code

- **`dividend_vision_colab.py`** — Main production notebook (upload to Google Colab)

### Samples

- **`sample_prompts.txt`** — Example prompts to get started

---

## Quick Start

### For Non-Technical Users:

1. **Read this first:** [`USAGE_INSTRUCTIONS.md`](./USAGE_INSTRUCTIONS.md)
2. **Upload to Colab:** `dividend_vision_colab.py`
3. **Edit prompts:** Use `sample_prompts.txt` as a template
4. **Run the notebook** and wait for videos to generate
5. **Download from Google Drive:** Check `MyDrive/Dividend_Vision/videos/`

### For Technical Users:

1. **Understand the design:** Read [`PIPELINE_DESIGN.md`](./PIPELINE_DESIGN.md)
2. **Review the code:** See `dividend_vision_colab.py`
3. **Customize as needed** (CFG scale, resolution, motion settings)
4. **Run and iterate**

---

## What This System Does

- **Input:** Simple text prompts (e.g., "misty mountain valley")
- **Output:** 4-second stock-safe nature videos (MP4, 6 FPS)
- **Platform:** Google Colab Free Tier (T4 GPU)
- **Processing:** Sequential (one complete video at a time)
- **Duration:** ~2-3 minutes per prompt
- **Quality:** Designed to pass Adobe Stock review

---

## What This System Does NOT Do

- ❌ Upscaling (use Topaz Video Enhance AI externally)
- ❌ Audio generation
- ❌ Multi-shot editing
- ❌ People/animals/buildings (stock-unsafe)
- ❌ Cinematic effects (keeping it documentary-neutral)

---

## Technical Stack

- **Text-to-Image:** Stable Diffusion XL (SDXL)
- **Image-to-Video:** Stable Video Diffusion XT (SVD-XT)
- **Framework:** Hugging Face Diffusers
- **Processing:** Sequential (image→video per prompt)
- **Storage:** Google Drive
- **Compute:** Google Colab (T4 GPU, ~15GB VRAM)

---

## Project Philosophy

This is **NOT** an AI art project.  
This is a **visual asset factory** optimized for:

1. **Stock platform approval** (Adobe Stock, Shutterstock, etc.)
2. **Long-term passive income** (build a catalog of 500+ reusable clips)
3. **Operational simplicity** (non-developers can run it)
4. **Stability over innovation** (predictable, repeatable results)

---

## Expected Results

### Quality Metrics

- **Stock approval rate:** 60-80% (some rejections are normal)
- **Believability:** "Could this have been filmed with a real camera?"
- **Reusability:** Usable across corporate, editorial, and educational contexts

### Output Specifications

- **Resolution:** 1024×576 (16:9, suitable for upscaling)
- **Frames:** 25 frames per video
- **FPS:** 6 frames per second
- **Duration:** ~4.2 seconds per clip
- **Format:** MP4 (H.264 codec)
- **Style:** Documentary-neutral, photorealistic

---

## Folder Structure (Google Drive)

After first run, your Google Drive will have:

```
MyDrive/
└── Dividend_Vision/
    ├── config/
    │   └── prompts.txt ← Edit this
    ├── images/
    │   └── [intermediate images]
    ├── videos/
    │   └── [final videos] ← Download these
    └── logs/
        └── session_*.txt ← Check if errors occur
```

---

## Workflow Summary

```
1. User edits prompts.txt in Google Drive
         ↓
2. User runs Colab notebook (Runtime → Run All)
         ↓
3. System generates images (SDXL, ~30s each)
         ↓
4. System generates videos (SVD-XT, ~90s each)
         ↓
5. Outputs saved to Google Drive automatically
         ↓
6. User reviews videos, deletes failures
         ↓
7. User upscales keepers (Topaz, external)
         ↓
8. User uploads to Adobe Stock
```

---

## Success Criteria (90-Day Checkpoint)

- [ ] 200+ videos generated
- [ ] 140+ videos approved by stock platforms (70% rate)
- [ ] System runs without modification for 30+ days
- [ ] User operates independently (no technical support needed)
- [ ] First passive income received ($1+)

---

## Limitations & Known Issues

### By Design:

- **No upscaling** — handled externally for quality/time reasons
- **Short clips only** — 1 second base (prevents morphing artifacts)
- **Nature only** — people/animals too risky for stock approval
- **Sequential processing** — slower but more stable than batch

### Technical:

- **Colab free tier limits** — max 2 hours continuous GPU use
- **T4 VRAM constraints** — can't process 50+ prompts in one session
- **AI model variability** — 10-20% failure rate expected

---

## Version History

**v1.0** (2026-01-03)

- Initial production release
- SDXL + SVD-XT pipeline
- Automatic safety filters
- Google Drive integration
- Stock-safe prompt enhancement
- Error handling and logging

---

## License & Usage Rights

### Code License:

- This pipeline code is provided as-is for your use
- Modify, distribute, or use commercially as needed

### Generated Content:

- You own all outputs generated by this system
- SDXL and SVD models are licensed for commercial use
- Always disclose "AI-generated" when uploading to stock platforms
- Follow each platform's specific AI content policies

### Model Credits:

- SDXL: Stability AI ([License](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0))
- SVD-XT: Stability AI ([License](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt))

---

## Support

This is a **stable, production-ready system** designed to run autonomously.

**If something fails:**

1. Check `logs/session_*.txt` in Google Drive for error details
2. Review [`USAGE_INSTRUCTIONS.md`](./USAGE_INSTRUCTIONS.md) troubleshooting section
3. Reduce batch size (try 5 prompts instead of 20)
4. Restart Colab runtime and try again

**Common issues are addressed in the usage guide.**

---

## Future Roadmap (Not Implemented)

Potential enhancements for future versions:

- Quality scoring automation (auto-delete obvious failures)
- Prompt templates library
- Multi-resolution output options
- Batch upscaling integration
- Stock platform API integration for auto-upload

**Current version prioritizes stability over features.**

---

**Dividend Vision — Built for long-term passive income through stable, reusable visual assets.**

Version 1.0 | 2026-01-03
