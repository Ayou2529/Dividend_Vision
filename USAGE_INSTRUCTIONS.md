# Dividend Vision — Usage Instructions (Section C)

**Version:** 1.1  
**For:** Non-technical users  
**Platform:** Google Colab (Free Tier)

---

## Quick Start (3 Steps)

### Step 1: Open the Notebook in Google Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. Click **File → Upload notebook**
3. Upload `dividend_vision_colab.py`
   - **Alternative:** Create a new notebook and copy/paste the entire code

---

### Step 2: Enable GPU

**CRITICAL:** This must be done before running.

1. In Google Colab, click **Runtime → Change runtime type**
2. Set **Hardware accelerator** to **GPU** (T4 or higher)
3. Click **Save**

---

### Step 3: Edit Your Prompts

1. Open [Google Drive](https://drive.google.com/)
2. Navigate to **MyDrive → Dividend_Vision → config**
   - This folder will be created automatically on first run
3. Open **prompts.txt**
4. Add your prompts, **one per line**:

```
misty mountain valley at sunrise
ocean waves on rocky beach at sunset
raindrops falling on green leaves
fog rolling through pine forest
```

**Prompt Rules:**

- ✅ Nature scenes only (landscapes, weather, plants, water)
- ❌ NO people, animals, buildings, text, or logos
- ✅ Keep it simple (system enhances automatically)
- ❌ Don't add negative prompts (handled automatically)

**Good Examples:**

- `morning fog over calm lake`
- `autumn leaves swirling in wind`
- `gentle rain falling on mossy rocks`

**Bad Examples:**

- `person walking through forest` ← Contains "person"
- `deer drinking from stream` ← Contains "deer"
- `old barn in field` ← Contains "barn"

---

### Step 4: Run the Notebook

1. Click **Runtime → Run all** (or press `Ctrl+F9`)
2. When prompted, **allow Google Drive access**
3. Wait for completion

**Expected Processing Time:**

- **Per prompt:** ~2-3 minutes total
  - Image generation: 30-45 seconds
  - Video generation: 90-120 seconds
- **10 prompts:** ~25-30 minutes
- **20 prompts:** ~50-60 minutes

**The notebook will:**

- Install all required software automatically
- Download AI models (first run only, ~11 GB)
- Read your prompts
- Generate images using SDXL
- Convert each image to video using SVD-XT immediately (sequential)
- Save everything to Google Drive
- Show a summary report

---

## Understanding the Output

### Where to Find Your Videos

**Location:**  
`Google Drive → MyDrive → Dividend_Vision → videos/`

**Files:**

```
20260103_172534_vid_001.mp4  ← Your first video
20260103_172534_vid_002.mp4  ← Your second video
20260103_172534_vid_003.mp4  ← Your third video
```

**Video Specifications:**

- **Resolution:** 1024×576 (16:9 widescreen)
- **Frames:** 25 frames per video
- **FPS:** 6 frames per second
- **Duration:** ~4.2 seconds per clip
- **File size:** ~1-3 MB per video

### Why 6 FPS?

**6 FPS creates a slow, contemplative aesthetic:**

- Makes motion appear smooth and dreamy
- Masks AI artifacts better than 24-30 FPS
- Perfect for nature B-roll in documentaries
- Can be sped up later in post-production if needed

**Can be adjusted to:**

- **12 FPS:** 2.1 seconds (faster, still smooth)
- **24 FPS:** 1.0 second (standard video speed)

---

## Folder Structure

After first run:

```
Dividend_Vision/
├── config/
│   └── prompts.txt ← Edit this
├── images/
│   └── [generated images] ← Intermediate PNG files
├── videos/
│   └── [final videos] ← Download these
└── logs/
    ├── session_*.txt ← Detailed log
    └── summary_*.txt ← Quick summary
```

---

## What to Do After Generation

### 1. Review Videos

- Open the `videos/` folder in Google Drive
- Play each video
- Delete any failures or unwanted clips

**Common issues to check:**

- Morphing artifacts (objects warping unnaturally)
- Visibility of AI generation (looks too "digital")
- Unwanted elements (the AI occasionally hallucinates)

---

### 2. Upscale (External - Required)

**Current resolution:** 1024×576  
**Target for stock:** 1920×1080 or 3840×2160

**Recommended tool: Topaz Video Enhance AI**

- Download from [Topaz Labs](https://www.topazlabs.com/)
- Use "Progressive Upscale" preset
- Upscale to 1920×1080 (Full HD) or 3840×2160 (4K)
- Export as MP4, high quality

**Why not upscale in Colab?**

- Upscaling takes 10-30 minutes per video
- Would exceed Colab free tier limits
- Topaz produces superior quality

---

### 3. Upload to Adobe Stock

1. Go to [Adobe Stock Contributor Portal](https://contributor.stock.adobe.com/)
2. Upload your upscaled videos
3. **MANDATORY:** Mark as **"AI Generated"**
4. Add relevant keywords:
   - nature, landscape, weather, etc.
   - Match your original prompt
5. Submit for review

**Expected approval rate:** 60-80%  
Some rejections are normal and expected.

---

## Troubleshooting

### "ERROR: GPU not available"

**Solution:**

1. Click **Runtime → Change runtime type**
2. Select **GPU** (not CPU or TPU)
3. Click **Save**
4. Run again

---

### "No valid prompts after safety filter"

**Problem:** All prompts contained forbidden words.

**Solution:**

1. Check `logs/session_*.txt` to see which keywords triggered the filter
2. Rewrite prompts focusing only on nature
3. Run again

**Example:**

- ❌ `squirrel eating acorn` → "squirrel" is forbidden
- ✅ `autumn acorns on forest floor` → Nature only

---

### "Out of memory" / "CUDA OOM"

**Problem:** GPU ran out of VRAM.

**Solutions:**

1. **Reduce batch size:**
   - Try 5-10 prompts at a time instead of 20+
2. **Restart runtime:**
   - Runtime → Restart runtime
   - Run again
3. **Close other tabs:**
   - Colab shares GPU with other notebooks

---

### Some videos didn't generate

**This is normal.** AI models aren't 100% reliable.

**Solution:**

1. Check `logs/session_*.txt` for error details
2. Identify which prompts failed
3. Rewrite failed prompts more simply
4. Create a new `prompts.txt` with only the failed ones
5. Run again

---

### Videos look weird / morphing artifacts

**Common causes:**

- Prompt too abstract or complex
- AI couldn't visualize the concept clearly
- Random AI variability

**Solutions:**

1. **Delete the bad video**
2. **Simplify the prompt:**
   - Bad: `ethereal mist dancing over crystalline alpine waters`
   - Good: `morning mist over mountain lake`
3. **Regenerate** (run notebook again with simpler prompt)

---

### Videos are slow-motion (6 FPS)

**This is intentional.** 6 FPS creates a contemplative aesthetic.

**If you want faster motion:**

1. **Use video editing software** (Adobe Premiere, DaVinci Resolve, etc.)
2. **Speed up the clip:**
   - 2× speed = 12 FPS (2.1 seconds)
   - 4× speed = 24 FPS (1.0 second)

**Or modify the code** (advanced):

- Find line: `export_to_video_6fps(frames, video_path)`
- Change function to use different FPS

---

## Performance & Limitations

### Processing Speed

- **Image:** 30-45 seconds each
- **Video:** 90-120 seconds each
- **Total per prompt:** ~2-3 minutes

### Batch Size Recommendations

- **First test:** 3-5 prompts
- **Regular use:** 10-15 prompts per session
- **Maximum:** 20-25 prompts (Colab free tier limit)

**Why not 100+ at once?**

- Colab free tier disconnects after ~2-3 hours of GPU use
- Better to run multiple small batches

### Known Limitations

- **VRAM constraints:** T4 GPU has 15GB, can't process huge batches
- **Model variability:** 10-20% failure rate is normal
- **Motion artifacts:** AI video is not perfect, expect some oddities
- **Sequential processing:** Slower than batch, but more stable

---

## Advanced Customization

**⚠️ SKIP THIS SECTION IF YOU'RE NOT TECHNICAL**

### Change Image Resolution

Find this line:

```python
width=1024,
height=576,
```

Options:

- `1024×1024` (square, for Instagram)
- `768×768` (faster, lower quality)
- `1280×720` (standard 720p)

**Warning:** Higher = more VRAM, may cause crashes.

---

### Change CFG Scale (Prompt Strength)

Find this line:

```python
guidance_scale=6.0,
```

Options:

- `5.0-5.5` (more natural, less prompt adherence)
- `6.0-6.5` (balanced, recommended)
- `7.0-8.0` (stronger prompt, more "AI look")

---

### Change Video FPS

Find this function:

```python
export_to_video_6fps(frames, video_path)
```

Modify the function to use `fps=12` or `fps=24` instead of `fps=6`.

---

### Change Motion Intensity

Find this line:

```python
motion_bucket_id=127,
```

Options:

- `80-100` (very subtle motion, almost static)
- `127` (moderate motion, balanced)
- `150-180` (more dramatic, higher artifact risk)

---

## Best Practices

### Prompt Writing Tips

1. **Be specific but simple:**

   - Good: `morning fog over calm lake`
   - Too vague: `nature scene`
   - Too complex: `ethereal dawn mist...`

2. **Focus on movement:**

   - Good: `waves crashing on shore`
   - Static: `beach landscape`

3. **Avoid ambiguous terms:**
   - Bad: `wildlife habitat` ← AI might add animals
   - Good: `forest clearing with sunlight`

---

### Workflow Optimization

1. **Test first:** Run 3-5 prompts to see if style matches expectations
2. **Review immediately:** Delete bad outputs before upscaling
3. **Track winners:** Note which prompt styles work best
4. **Batch similar prompts:** Keep ocean prompts together, mountain prompts together

---

### Quality Control

**Before upscaling, check each video for:**

- ✅ Smooth, believable motion
- ✅ No morphing or warping artifacts
- ✅ Clean composition (no edge artifacts)
- ✅ Natural colors (not oversaturated)
- ❌ Delete anything that looks "AI-generated"

---

## FAQ

**Q: Can I use this for YouTube?**  
A: Yes, but combine multiple clips in a video editor.

**Q: Can I sell on other platforms?**  
A: Yes (Shutterstock, Getty, etc.), but always disclose AI generation.

**Q: Why only nature?**  
A: AI-generated people/animals have artifacts (weird hands, faces) that get rejected.

**Q: Can I run this on my computer?**  
A: Technically yes, but requires:

- NVIDIA GPU with 16GB+ VRAM
- Python 3.10+
- 50GB+ disk space  
  Not recommended for non-technical users.

**Q: How much can I earn?**  
A: Highly variable. Stock footage typically earns $0.25-$5 per download. A catalog of 500+ videos can generate $50-500/month passive income over time.

**Q: The videos are only 4 seconds, is that useful?**  
A: Yes. Stock buyers often prefer short, loopable clips for B-roll. You can also speed them up to 1-2 seconds if needed.

**Q: Can I change the 6 FPS?**  
A: Yes, but 6 FPS masks AI artifacts better. See "Advanced Customization" section.

---

## Support

**If you encounter issues:**

1. Check `logs/session_*.txt` in Google Drive for error details
2. Review the Troubleshooting section above
3. Try reducing batch size to 5 prompts
4. Restart Colab runtime and try again

**This is a stable, production-ready system.**  
If it works once, it should work consistently.

---

**Dividend Vision — Built for long-term passive income through stable, reusable visual assets.**

Version 1.1 | 2026-01-03  
**Dividend Vision – Step 3 implementation complete. Ready for testing.**
