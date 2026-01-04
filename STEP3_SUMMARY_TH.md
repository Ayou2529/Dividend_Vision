# Dividend Vision — สรุปรายละเอียด Step 3

**เวอร์ชัน:** 1.1  
**วันที่:** 3 มกราคม 2026  
**ภาษา:** ไทย

---

## 📋 สารบัญ

1. [ภาพรวม Step 3](#ภาพรวม-step-3)
2. [ไฟล์ที่สร้างขึ้น](#ไฟล์ที่สร้างขึ้น)
3. [สถาปัตยกรรมระบบ](#สถาปัตยกรรมระบบ)
4. [การทำงานของโค้ด](#การทำงานของโค้ด)
5. [การตัดสินใจทางเทคนิค](#การตัดสินใจทางเทคนิค)
6. [ข้อกำหนดเฉพาะที่สำคัญ](#ข้อกำหนดเฉพาะที่สำคัญ)
7. [วิธีการใช้งาน](#วิธีการใช้งาน)
8. [ตัวอย่างผลลัพธ์](#ตัวอย่างผลลัพธ์)

---

## ภาพรวม Step 3

### วัตถุประสงค์

สร้างระบบ AI ที่สมบูรณ์สำหรับการสร้างวิดีโอธรรมชาติ (Nature Videos) เพื่อขายบนแพลตฟอร์ม Stock (เช่น Adobe Stock) โดยใช้ Google Colab ฟรี

### สิ่งที่ Step 3 ส่งมอบ

1. **Pipeline Explanation** — อธิบายการออกแบบระบบอย่างละเอียด
2. **Production Code** — โค้ดที่พร้อมใช้งานจริง
3. **Usage Guide** — คู่มือการใช้งานสำหรับผู้ที่ไม่ใช่โปรแกรมเมอร์

### ขอบเขตงาน (Scope)

- ✅ สร้างระบบ Text → Image → Video ที่ทำงานอัตโนมัติ
- ✅ ใช้ Google Colab (GPU ฟรี T4) และ Google Drive
- ✅ มีระบบกรองความปลอดภัย (ป้องกันสร้างคน/สัตว์/อาคาร)
- ✅ ประมวลผลแบบต่อเนื่อง (ทำทีละ prompt)
- ✅ รองรับการทำงานโดยไม่ต้องแก้โค้ด
- ❌ ไม่รวม upscaling (ทำภายนอกด้วย Topaz)
- ❌ ไม่รวมการสร้างเสียง
- ❌ ไม่สร้างคน/สัตว์/อาคาร

---

## ไฟล์ที่สร้างขึ้น

### 1. `PIPELINE_DESIGN.md` (Section A)

**ขนาด:** ~13 KB  
**ภาษา:** อังกฤษ  
**จุดประสงค์:** อธิบายการตัดสินใจทางเทคนิคทั้งหมด

**เนื้อหาหลัก:**

- **ทำไมเลือก SDXL** สำหรับสร้างภาพ
  - ความสมจริงสูงกว่า SD 1.5
  - เหมาะกับ stock photography style
  - รองรับ T4 GPU ได้
- **ทำไมเลือก SVD-XT** สำหรับสร้างวิดีโอ
  - ออกแบบมาเพื่อความสมจริง
  - Motion เบาบาง ไม่เกินจริง
  - รองรับการใช้งานเชิงพาณิชย์
- **การตั้งค่าต่างๆ:**
  - ความละเอียด: 1024×576 (16:9)
  - CFG Scale: 6.0 (ดูธรรมชาติ ไม่เกิน)
  - Steps: 30 (สมดุลระหว่างคุณภาพและความเร็ว)
  - FPS: 6 (ทำให้ดู slow-motion สวยงาม)
- **Sequential Processing Strategy:**
  - ทำไมต้องทำทีละ prompt (ไม่ batch)
  - การจัดการ VRAM
  - การแยก error ไม่ให้กระทบทั้งระบบ

**ตัวอย่างเนื้อหาสำคัญ:**

```
ทำไม 6 FPS:
- 25 frames ÷ 6 FPS = 4.2 วินาที
- สร้าง aesthetic แบบ contemplative/dreamy
- ซ่อน AI artifacts ได้ดีกว่า 24-30 FPS
- เหมาะกับ nature B-roll
- สามารถเร่งความเร็วในโปรแกรมตัดต่อได้ภายหลัง
```

---

### 2. `dividend_vision_colab.py` (Section B)

**ขนาด:** ~22 KB  
**ภาษา:** Python (คำอธิบายเป็นอังกฤษ)  
**จุดประสงค์:** โค้ดหลักสำหรับรันใน Google Colab

**โครงสร้างโค้ด (8 Sections):**

#### **Section 1: Environment Setup**

```python
# ติดตั้ง dependencies
# Mount Google Drive
# สร้างโฟลเดอร์ทั้งหมด
# เริ่ม logging system
# ตรวจสอบ GPU
```

**สิ่งที่ทำ:**

- ติดตั้ง PyTorch, Diffusers, OpenCV, Pillow
- เชื่อมต่อ Google Drive (ครั้งเดียว ต้อง authorize)
- สร้างโฟลเดอร์:
  - `/config/` — เก็บ prompts.txt
  - `/images/` — เก็บภาพที่สร้าง
  - `/videos/` — เก็บวิดีโอที่สร้าง
  - `/logs/` — เก็บ log ไฟล์
- ตรวจสอบว่ามี GPU (T4) หรือไม่

---

#### **Section 2: Configuration & Safety Filters**

```python
STOCK_BIAS = """professional nature documentary style..."""
NEGATIVE_PROMPT = """people, person, animal, building..."""
FORBIDDEN_KEYWORDS = ["person", "animal", "building", ...]
```

**สิ่งที่ทำ:**

- **STOCK_BIAS:** คำที่จะต่อท้าย prompt อัตโนมัติ
  - เพิ่มคำว่า "documentary style", "stock footage", "natural lighting"
  - ทำให้ AI สร้างในสไตล์ที่เหมาะกับ stock
- **NEGATIVE_PROMPT:** คำที่ห้ามปรากฏในภาพ
  - บล็อก: คน, สัตว์, อาคาร, ยานพาหนะ, ข้อความ, โลโก้
  - บล็อก: สไตล์ fantasy, cartoon, anime
  - บล็อก: คุณภาพต่ำ, artifacts, distortion
- **FORBIDDEN_KEYWORDS:** คำที่ห้ามใน prompt
  - ถ้า prompt มีคำเหล่านี้ → ข้าม ไม่สร้าง
  - ประหยัด GPU time

---

#### **Section 3: Load Prompts**

```python
# อ่านไฟล์ prompts.txt
# สร้างไฟล์ตัวอย่างถ้ายังไม่มี
# กรอง prompts ที่มีคำต้องห้าม
# เตรียม queue สำหรับสร้าง
```

**สิ่งที่ทำ:**

1. อ่าน `/config/prompts.txt` (หนึ่งบรรทัด = หนึ่ง video)
2. ถ้าไฟล์ไม่มี → สร้างไฟล์ตัวอย่าง 5 prompts
3. ตรวจสอบแต่ละ prompt:
   - มีคำต้องห้ามไหม (เช่น "animal", "person")
   - ถ้ามี → log "[SKIPPED]" และข้าม
   - ถ้าไม่มี → log "[QUEUED]" และเพิ่มใน queue
4. ถ้าไม่มี prompt ที่ใช้ได้ → หยุดทำงาน แจ้ง error

**ตัวอย่าง Log:**

```
[QUEUED]  Prompt 1: misty mountain valley at sunrise...
[SKIPPED] Prompt 2: Contains forbidden keyword 'deer'
[QUEUED]  Prompt 3: ocean waves washing over smooth rocks...
```

---

#### **Section 4: Generation Loop (Sequential)**

```python
for each prompt:
    # STAGE 1: สร้างภาพด้วย SDXL
    load SDXL (ครั้งแรกเท่านั้น)
    enhanced_prompt = user_prompt + STOCK_BIAS
    image = sdxl_pipe(enhanced_prompt, negative_prompt, ...)
    save image to /images/

    # STAGE 2: สร้างวิดีโอด้วย SVD-XT
    unload SDXL (เคลียร์ VRAM)
    load SVD-XT
    video = svd_pipe(image, 25 frames, 6 fps, ...)
    save video to /videos/
    unload SVD-XT (เคลียร์ VRAM)

    # วนไป prompt ถัดไป
```

**การทำงานแบบ Sequential (ทีละ prompt):**

**Prompt 1:**

```
1. Load SDXL → Generate Image 1 → Save → Unload SDXL
2. Load SVD → Generate Video 1 from Image 1 → Save → Unload SVD
3. ✓ Video 1 เสร็จสมบูรณ์
```

**Prompt 2:**

```
1. Load SDXL → Generate Image 2 → Save → Unload SDXL
2. Load SVD → Generate Video 2 from Image 2 → Save → Unload SVD
3. ✓ Video 2 เสร็จสมบูรณ์
```

**ทำไมไม่ทำแบบ Batch (ภาพทั้งหมดก่อน แล้วค่อยทำวิดีโอ):**

- ❌ ต้อง load ทั้ง SDXL และ SVD พร้อมกัน → VRAM ไม่พอ (OOM crash)
- ❌ ถ้า error ตอนทำวิดีโอ → เสียภาพทั้งหมด
- ✅ Sequential = ช้ากว่าแต่ปลอดภัย 100%

---

#### **Section 5: Helper Function (6 FPS Export)**

```python
def export_to_video_6fps(frames, output_path):
    # สร้าง VideoWriter ที่ 6 FPS
    # เขียน frames ทีละ frame
    # บันทึกเป็น MP4
```

**สิ่งที่ทำ:**

- รับ 25 frames จาก SVD
- สร้างไฟล์ MP4 ด้วย OpenCV
- ตั้ง FPS = 6 (ไม่ใช่ 25 หรือ 30)
- ใช้ codec H.264 (มาตรฐาน stock platforms)
- ผลลัพธ์: วิดีโอ 4.2 วินาที (25÷6=4.166...)

---

#### **Section 6: Error Handling**

```python
try:
    # สร้างภาพ
    # สร้างวิดีโอ
except Exception as e:
    log(f"[FAILED] Prompt {i}: {str(e)}")
    # เคลียร์ VRAM
    # ไปต่อที่ prompt ถัดไป (ไม่หยุด)
```

**สิ่งที่ทำ:**

- ถ้า prompt ใดทำงานไม่สำเร็จ
  - บันทึก error ใน log ไฟล์
  - เคลียร์ VRAM emergency
  - **ไม่หยุดทำงาน** → ไปต่อที่ prompt ถัดไป
- ทำให้ระบบ robust → 1 prompt พัง ไม่กระทบอีก 19 prompts

---

#### **Section 7-8: Summary & Cleanup**

```python
# คำนวณ success rate
# สร้างรายงานสรุป
# บันทึกรายงานเป็นไฟล์
# แสดงผลบน console
```

**ตัวอย่างรายงาน:**

```
╔═══════════════════════════════════════════════════╗
║      DIVIDEND VISION — SESSION REPORT              ║
╚═══════════════════════════════════════════════════╝

Session ID: 20260103_173412
Date: 2026-01-03 17:34:12

RESULTS:
├─ Prompts loaded:      10
├─ Prompts filtered:    2 (forbidden keywords)
├─ Videos generated:    7/8
└─ Failed:              1

SUCCESS RATE: 87.5%

OUTPUT LOCATIONS:
├─ Videos: /MyDrive/Dividend_Vision/videos/
└─ Log:    /MyDrive/Dividend_Vision/logs/session_....txt
```

---

### 3. `USAGE_INSTRUCTIONS.md` (Section C)

**ขนาด:** ~9 KB  
**ภาษา:** อังกฤษ  
**จุดประสงค์:** คู่มือสำหรับผู้ใช้ที่ไม่ใช่โปรแกรมเมอร์

**เนื้อหาหลัก:**

#### **Quick Start (3 Steps)**

1. อัปโหลด notebook ไป Google Colab
2. เปิด GPU (Runtime → Change runtime type → GPU)
3. Run All → รอผลลัพธ์

#### **วิธีเขียน Prompts**

- ✅ ธรรมชาติเท่านั้น: "misty mountain", "ocean waves"
- ❌ ห้ามคน/สัตว์/อาคาร: "person walking", "deer in forest"
- ✅ เรียบง่าย: "morning fog over lake"
- ❌ ซับซ้อนเกินไป: "ethereal mist dancing over crystalline..."

#### **Troubleshooting**

- "GPU not available" → เปิด GPU ใน settings
- "Out of memory" → ลด prompts เหลือ 5-10 อัน
- "No valid prompts" → ตรวจสอบว่าไม่มีคำต้องห้าม

#### **What to Do After**

1. Review videos
2. Delete failures
3. Upscale with Topaz (external)
4. Upload to Adobe Stock

---

### 4. ไฟล์เสริมอื่นๆ

#### **`sample_prompts.txt`**

ตัวอย่าง prompts พร้อมใช้งาน (20+ prompts)

```
misty mountain valley at sunrise, golden hour lighting
gentle ocean waves washing over smooth rocks on beach
autumn forest floor covered in orange and yellow fallen leaves
...
```

#### **`README.md`**

ภาพรวมโปรเจกต์ ไฟล์ทั้งหมด วิธีเริ่มต้น

---

## สถาปัตยกรรมระบบ

### Data Flow (การไหลของข้อมูล)

```
👤 USER
  │
  └─► แก้ไข prompts.txt ใน Google Drive
         │
         ▼
    ┌─────────────────────────────────┐
    │  Google Colab Notebook          │
    │  (dividend_vision_colab.py)     │
    └─────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────┐
    │  SECTION 3: Load Prompts        │
    │  - อ่านไฟล์                      │
    │  - กรองคำต้องห้าม                │
    │  - สร้าง queue                   │
    └─────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────┐
    │  LOOP: For each prompt          │
    └─────────────────────────────────┘
         │
         ├───► STAGE 1: Text → Image
         │     ┌──────────────────────┐
         │     │ Load SDXL Pipeline   │
         │     │ Enhanced Prompt =    │
         │     │   user_prompt +      │
         │     │   STOCK_BIAS         │
         │     │ Generate Image       │
         │     │ Save to /images/     │
         │     │ Unload SDXL          │
         │     └──────────────────────┘
         │
         └───► STAGE 2: Image → Video
               ┌──────────────────────┐
               │ Load SVD-XT Pipeline │
               │ Input: Image (1024×576) │
               │ Generate 25 frames   │
               │ Export as MP4 (6 FPS)│
               │ Save to /videos/     │
               │ Unload SVD           │
               └──────────────────────┘
         │
         ▼
    ┌─────────────────────────────────┐
    │  OUTPUT: Summary Report         │
    │  - Success rate                 │
    │  - Output locations            │
    │  - Error details (if any)      │
    └─────────────────────────────────┘
         │
         ▼
    📁 Google Drive
       /videos/
         ├─ 20260103_173412_vid_001.mp4
         ├─ 20260103_173412_vid_002.mp4
         └─ 20260103_173412_vid_003.mp4
```

---

## การทำงานของโค้ด

### ขั้นตอนละเอียด (Step-by-Step Execution)

#### **เมื่อกด Run All:**

**[1/8] Installing dependencies**

```bash
pip install diffusers transformers torch opencv-python ...
```

- ติดตั้ง library ทั้งหมด (ใช้เวลา ~2-3 นาที)
- ดาวน์โหลด PyTorch with CUDA support

**[2/8] Mounting Google Drive**

```python
from google.colab import drive
drive.mount('/content/drive')
```

- ขอสิทธิ์เข้าถึง Google Drive
- ผู้ใช้ต้องกด "Allow" (ครั้งแรกเท่านั้น)

**[3/8] Setting up folder structure**

```python
FOLDERS = {
    "config": /MyDrive/Dividend_Vision/config/,
    "images": /MyDrive/Dividend_Vision/images/,
    "videos": /MyDrive/Dividend_Vision/videos/,
    "logs": /MyDrive/Dividend_Vision/logs/
}
```

- สร้างโฟลเดอร์ทั้งหมด (ถ้ายังไม่มี)

**[4/8] Loading prompts**

```python
# อ่าน prompts.txt
# ถ้าไม่มี → สร้างไฟล์ตัวอย่าง
# กรอง forbidden keywords
# แสดง [QUEUED] หรือ [SKIPPED]
```

**[5-7/8] Generation Loop**
สำหรับแต่ละ prompt:

1. **Image Generation (30-45 วินาที)**

   ```python
   # Load SDXL (ครั้งแรก ~20 วินาที)
   # Enhance prompt
   # Generate: "misty mountain valley"
   #    → "misty mountain valley, professional nature
   #        documentary style, photorealistic stock footage..."
   # Save: 20260103_173412_img_001.png
   ```

2. **Video Generation (90-120 วินาที)**

   ```python
   # Unload SDXL (เคลียร์ RAM)
   # Load SVD-XT (~15 วินาที)
   # Generate 25 frames from image
   # Export at 6 FPS → 4.2 second clip
   # Save: 20260103_173412_vid_001.mp4
   # Unload SVD
   ```

3. **Next Prompt**
   - เคลียร์ cache
   - วนกลับไปข้อ 1

**[8/8] Session Summary**

```python
# นับจำนวน success/failed
# สร้างรายงาน
# บันทึกเป็นไฟล์
```

---

### Timeline ตัวอย่าง (10 prompts)

```
00:00 - 00:03  ติดตั้ง dependencies
00:03 - 00:05  Mount Drive + Setup folders
00:05 - 00:06  Load prompts (10 อัน)
00:06 - 00:26  SDXL Load → Prompt 1 Image (20s load + 40s gen)
00:26 - 00:28  SVD Load (15s)
00:28 - 02:30  Prompt 1 Video (120s)
02:30 - 02:31  Unload SVD
02:31 - 03:11  Prompt 2 Image (SDXL still loaded, 40s gen)
03:11 - 03:13  SVD Load
03:13 - 05:15  Prompt 2 Video
...
25:00 - 27:00  Prompt 10 Video
27:00 - 27:01  Generate Summary
═══════════════════════════════════════
Total: ~27 นาที สำหรับ 10 videos
```

---

## การตัดสินใจทางเทคนิค

### 1. ทำไมใช้ Diffusers แทน ComfyUI?

**ComfyUI:**

- ✅ UI ที่สวยงาม เหมาะกับ manual workflow
- ✅ มี custom nodes มากมาย
- ❌ ต้องติดตั้ง custom nodes สำหรับ SVD (ซับซ้อน)
- ❌ Headless mode บน Colab ไม่เสถียร
- ❌ Websocket API ต้อง setup เพิ่ม

**Diffusers:**

- ✅ Library official จาก Hugging Face
- ✅ รองรับ SDXL และ SVD โดยตรง
- ✅ Code สั้น กระชับ เข้าใจง่าย
- ✅ เสถียรบน Colab
- ❌ ไม่มี UI (แต่ไม่ต้องการ UI อยู่แล้ว)

**ตัดสินใจ:** ใช้ Diffusers เพราะความเรียบง่ายและเสถียรภาพ

---

### 2. ทำไมใช้ 6 FPS?

**ปกติวิดีโอ:** 24-30 FPS  
**Dividend Vision:** 6 FPS

**เหตุผล:**

1. **25 frames ÷ 6 FPS = 4.2 วินาที**

   - คลิปยาวพอสำหรับ stock footage
   - ไม่สั้นเกินไป (1 วินาที = น้อยเกิน)

2. **ซ่อน AI artifacts ได้ดี**

   - Motion ที่ช้า → ดูนุ่มนวล
   - Artifacts ที่ FPS สูงจะเห็นชัด → FPS ต่ำทำให้ดูนุ่ม

3. **Aesthetic แบบ contemplative**

   - เหมาะกับวิดีโอธรรมชาติ (slow-paced)
   - สามารถเร่งในโปรแกรมตัดต่อได้ (2× = 12 FPS, 4× = 24 FPS)

4. **ลดขนาดไฟล์**
   - น้อยกว่า 24 FPS → ไฟล์เล็กกว่า

---

### 3. ทำไมต้อง Sequential Processing?

**Batch Processing (ไม่ใช้):**

```
1. สร้างภาพทั้งหมด (1-10) → ต้อง keep SDXL in memory
2. สร้างวิดีโอทั้งหมด (1-10) → ต้อง keep SVD in memory
```

❌ SDXL + SVD = 8GB + 6GB = 14GB → เกือบเต็ม T4 (15GB)  
❌ ถ้า error ตอน step 2 → เสียงานทั้งหมด

**Sequential Processing (ใช้):**

```
For each prompt:
  1. Load SDXL → Generate image → Unload
  2. Load SVD → Generate video → Unload
  3. Next prompt
```

✅ ใช้ VRAM แค่ ~8GB ต่อครั้ง (ปลอดภัย)  
✅ Error ใน prompt 5 → ยังได้วิดีโอ 1-4  
✅ เสถียรกว่า

**Trade-off:** ช้ากว่า ~20% เพราะต้อง load/unload บ่อย  
**Decision:** ยอมรับความช้าเพื่อความเสถียร

---

### 4. ทำไม CFG = 6.0?

**CFG Scale คืออะไร:**

- ค่าที่บอกว่า AI ต้อง "ทำตาม prompt" แค่ไหน
- **ต่ำ (3-5):** AI มีอิสระมาก → ไม่ค่อยเป๊ะตาม prompt
- **กลาง (6-7):** สมดุล → ตาม prompt แต่ยังดูธรรมชาติ
- **สูง (8-12):** ทำตามเป๊ะ → แต่ดู "AI-generated" เกินไป (oversaturated)

**Stock platforms ไม่ชอบ:**

- ภาพที่ดู "เกินจริง" (oversaturated colors)
- แสงที่ dramatic เกินไป
- สีที่ไม่เป็นธรรมชาติ

**CFG 6.0 = Sweet Spot:**

- ✅ ทำตาม prompt พอสมควร
- ✅ ดูธรรมชาติ ไม่ใช่ "AI art"
- ✅ ผ่าน stock review ได้ง่าย

---

### 5. ทำไมความละเอียด 1024×576?

**ไม่ใช่ 1920×1080 (Full HD)?**

- ❌ SDXL ทำ 1920×1080 ได้แต่ช้ามาก (~2-3 นาที/ภาพ)
- ❌ VRAM ไม่พอบน T4
- ❌ SVD รับ input ที่ดีที่สุดคือ 1024×576

**ไม่ใช่ 1024×1024 (Square)?**

- ❌ Stock platforms ต้องการ 16:9 (landscape)
- ❌ Square ไม่เหมาะกับวิดีโอธรรมชาติ

**1024×576 เพราะ:**

- ✅ 16:9 aspect ratio (มาตรฐาน stock)
- ✅ SVD ออกแบบมาสำหรับ resolution นี้
- ✅ Upscale ภายนอก (Topaz) ได้คุณภาพดี
- ✅ พอดีกับ T4 GPU (~40 วินาที/ภาพ)

---

## ข้อกำหนดเฉพาะที่สำคัญ

### Prompt Enhancement (การปรับปรุง Prompt อัตโนมัติ)

**Input จากผู้ใช้:**

```
misty mountain valley at sunrise
```

**ระบบเพิ่มคำต่อท้าย:**

```python
enhanced = user_prompt + ", " + STOCK_BIAS
```

**ผลลัพธ์ที่ส่งให้ SDXL:**

```
misty mountain valley at sunrise, professional nature documentary style,
photorealistic stock footage, natural lighting, neutral color grading,
wide angle landscape shot, high quality photography, editorial use,
clean composition
```

**ทำไมต้องทำ:**

- SDXL เทรนมาจากภาพหลายล้านภาพ รวมทั้ง stock photos
- คำว่า "documentary style", "stock footage" จะ activate latent features ที่เกี่ยวกับ stock
- ผู้ใช้ไม่ต้องเข้าใจเทคนิค → เขียนแค่ "mountain valley" ก็พอ

---

### Negative Prompt (สิ่งที่ต้องการบล็อก)

**Hardcoded (ผู้ใช้แก้ไม่ได้):**

```python
NEGATIVE_PROMPT = """
people, person, human, man, woman, child, face, hands,
animal, pet, wildlife, dog, cat, bird, fish,
building, architecture, house, city, bridge,
car, vehicle, plane, boat, train,
text, watermark, logo, signature, brand,
fantasy, dragon, magic, surreal, sci-fi, anime,
oversaturated, dramatic lighting, lens flare, bokeh,
blurry, low quality, distorted, noise, artifacts
"""
```

**ครอบคลุมทุกสิ่งที่ stock platforms จะ reject:**

1. **คน/สัตว์** → ต้องมี model release
2. **อาคาร/ยานพาหนะ** → อาจมี property release
3. **โลโก้/ข้อความ** → copyright issue
4. **Fantasy** → ไม่ใช่ nature documentary
5. **คุณภาพต่ำ** → reject ทันที

---

### Safety Keyword Filter

**ก่อนสร้าง ตรวจสอบก่อน:**

```python
for each prompt:
    if "animal" in prompt.lower():
        log("[SKIPPED] Contains forbidden keyword")
        continue
    if "building" in prompt.lower():
        log("[SKIPPED] Contains forbidden keyword")
        continue
    # ... ต่อไป
```

**ทำไมต้องกรองก่อน:**

- ประหยัด GPU time (ไม่ต้องสร้างภาพที่จะไม่ผ่านอยู่ดี)
- ให้ feedback ผู้ใช้ทันที (ไม่ต้องรอ 2 นาทีแล้วค่อยรู้ว่าผิดพลาด)
- Educate ผู้ใช้ (อ่าน log รู้เลยว่าคำไหนห้ามใช้)

---

## วิธีการใช้งาน

### สำหรับผู้ใช้ทั่วไป (ไม่ใช่โปรแกรมเมอร์)

#### ขั้นตอนที่ 1: เตรียม Prompts

1. เปิด Google Drive
2. ไปที่ `MyDrive/Dividend_Vision/config/`
3. เปิดไฟล์ `prompts.txt`
4. เขียน prompts ของคุณ (หนึ่งบรรทัด = หนึ่งวิดีโอ)

**ตัวอย่าง:**

```
morning fog over calm lake
ocean waves crashing on rocky shore
autumn leaves falling slowly from tree
raindrops on green moss covered rocks
sunset light filtering through forest canopy
```

**ข้อควรระวัง:**

- ❌ อย่าใส่: คน, สัตว์, อาคาร, ยานพาหนะ
- ❌ อย่าซับซ้อนเกินไป
- ✅ เน้นธรรมชาติล้วนๆ
- ✅ กระชับ ชัดเจน

---

#### ขั้นตอนที่ 2: Run Notebook

1. เปิด Google Colab
2. อัปโหลด `dividend_vision_colab.py`
3. เปิด GPU: **Runtime → Change runtime type → GPU**
4. กด **Runtime → Run all**
5. อนุญาตให้เข้าถึง Google Drive (ครั้งแรกเท่านั้น)
6. รอจนเสร็จ (~3 นาทีต่อ prompt)

**ขณะรอ คุณจะเห็น:**

```
[1/8] Installing dependencies...
[2/8] Mounting Google Drive...
[3/8] Setting up folder structure...
[4/8] Loading prompts...
[QUEUED] Prompt 1: morning fog over calm lake...
[QUEUED] Prompt 2: ocean waves crashing...
[5/8] STAGE 1: Generating image...
      Prompt: morning fog over calm lake
      ✓ Image saved: 20260103_img_001.png
[6/8] STAGE 2: Generating video...
      ✓ Video saved: 20260103_vid_001.mp4 (25 frames, 6 FPS, 4.2s)
...
```

---

#### ขั้นตอนที่ 3: Review & Download

1. เปิด Google Drive
2. ไปที่ `MyDrive/Dividend_Vision/videos/`
3. เล่นวิดีโอทุกอัน
4. ลบที่ไม่ชอบ/ผิดพลาด
5. ดาวน์โหลดที่ต้องการเก็บ

---

#### ขั้นตอนที่ 4: Upscale (ภายนอก)

1. เปิดโปรแกรม **Topaz Video Enhance AI**
2. นำวิดีโอที่ชอบไป upscale
3. ตั้งค่า:
   - Input: 1024×576
   - Output: 1920×1080 หรือ 3840×2160
   - Preset: Progressive Upscale
4. Export เป็น MP4

---

#### ขั้นตอนที่ 5: Upload to Stock

1. ไปที่ Adobe Stock Contributor Portal
2. อัปโหลดวิดีโอ (หลัง upscale)
3. **สำคัญ:** เลือก "AI-Generated" (บังคับ)
4. ใส่ keywords: nature, landscape, fog, mountain, etc.
5. Submit รอ review (~1-3 วัน)

**อัตราผ่าน:** 60-80% (บางอันโดน reject เป็นเรื่องปกติ)

---

## ตัวอย่างผลลัพธ์

### ตัวอย่าง Session Log

```
[2026-01-03 17:34:12] SESSION START
[2026-01-03 17:34:12] Session ID: 20260103_173412
[2026-01-03 17:34:17] GPU: Tesla T4 (14.7 GB VRAM)
[2026-01-03 17:34:20] ✓ Loaded 10 prompts
[2026-01-03 17:34:22] [QUEUED]  Prompt 1: misty mountain valley at sunrise...
[2026-01-03 17:34:22] [QUEUED]  Prompt 2: gentle ocean waves...
[2026-01-03 17:34:22] [SKIPPED] Prompt 3: Contains forbidden keyword 'deer'
[2026-01-03 17:34:22] [QUEUED]  Prompt 4: autumn forest floor...
...
[2026-01-03 17:35:00] [1/9] STAGE 1: Generating image...
[2026-01-03 17:35:00]         Prompt: misty mountain valley at sunrise
[2026-01-03 17:35:00]         Enhanced: misty mountain valley at sunrise, professional...
[2026-01-03 17:35:45]         ✓ Image saved: 20260103_173412_img_001.png
[2026-01-03 17:35:50] [1/9] STAGE 2: Generating video...
[2026-01-03 17:35:50]         Source: 20260103_173412_img_001.png
[2026-01-03 17:37:30]         ✓ Video saved: 20260103_173412_vid_001.mp4
[2026-01-03 17:37:30]           Specs: 25 frames, 6 FPS, 4.2 seconds
...
[2026-01-03 18:02:15] SESSION COMPLETE
[2026-01-03 18:02:15] Results: 8 images, 8 videos (1 prompt skipped, 1 failed)
[2026-01-03 18:02:15] Success rate: 80%
```

---

### ตัวอย่าง Output Files

**โครงสร้างโฟลเดอร์:**

```
/MyDrive/Dividend_Vision/
├── config/
│   └── prompts.txt
├── images/
│   ├── 20260103_173412_img_001.png  (1.2 MB)
│   ├── 20260103_173412_img_002.png  (1.3 MB)
│   └── 20260103_173412_img_003.png  (1.1 MB)
├── videos/
│   ├── 20260103_173412_vid_001.mp4  (2.1 MB, 4.2s)
│   ├── 20260103_173412_vid_002.mp4  (1.9 MB, 4.2s)
│   └── 20260103_173412_vid_003.mp4  (2.3 MB, 4.2s)
└── logs/
    ├── session_20260103_173412.txt  (12 KB)
    └── summary_20260103_173412.txt  (2 KB)
```

---

### Metrics ที่คาดหวัง

| Metric                  | ค่าที่คาดหวัง                  |
| ----------------------- | ------------------------------ |
| **เวลาต่อ prompt**      | 2-3 นาที                       |
| **Success rate**        | 70-90%                         |
| **Video duration**      | 4.2 วินาที (25 frames @ 6 FPS) |
| **Video file size**     | 1-3 MB                         |
| **Image file size**     | 1-2 MB                         |
| **Stock approval rate** | 60-80% (หลัง upscale)          |

---

## สรุป

### สิ่งที่ Step 3 ส่งมอบ:

✅ **ระบบแบบ End-to-End ที่พร้อมใช้งาน**

- Text → Image → Video
- ทำงานอัตโนมัติทั้งหมด
- ไม่ต้องแก้โค้ด

✅ **เอกสารครบถ้วน**

- คำอธิบายทางเทคนิค (PIPELINE_DESIGN.md)
- คู่มือการใช้งาน (USAGE_INSTRUCTIONS.md)
- โค้ดที่มี comments ละเอียด

✅ **ความปลอดภัย**

- กรอง prompts ที่อันตราย
- ป้องกัน OOM crashes
- Continue on error (ไม่หยุดงาน)

✅ **คุณภาพระดับ Stock**

- Documentary-neutral aesthetic
- 6 FPS สำหรับ smooth motion
- Auto-enhancement ทุก prompt
- ออกแบบมาเพื่อผ่าน Adobe Stock review

---

### Next Steps (หลัง Step 3):

1. **Testing** — ลองรัน 3-5 prompts ดูผลลัพธ์
2. **Iteration** — ปรับ prompts ให้ได้ผลลัพธ์ที่ต้องการ
3. **Production** — สร้างวิดีโอ 50-100 อัน
4. **Upscaling** — Topaz ยกระดับเป็น 1080p/4K
5. **Upload** — อัปโหลดไป Adobe Stock
6. **Track** — ติดตามอัตราการผ่าน แก้ปัญหา

---

**Dividend Vision — สร้างสินทรัพย์ดิจิทัลสำหรับรายได้แบบ passive income ระยะยาว**

Version 1.1 | 3 มกราคม 2026  
Status: ✅ พร้อมใช้งาน

**Dividend Vision – Step 3 implementation complete. Ready for testing.**
