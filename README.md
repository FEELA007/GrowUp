<div align="center">

# GrowUp

**AI Image Enhancement & Restoration**

A desktop image enhancement application built with Python, PySide6, PyTorch, OpenCV and Real-ESRGAN.

</div>

---

## Features

<div align="center">

| Feature | Description |
|---|---|
| **AI Upscaling** | 2× and 4× image upscaling |
| **Denoise** | Reduce image noise |
| **Sharpen** | Improve image details |
| **Deblur** | Enhance blurry images |
| **Before / After** | Interactive comparison slider |
| **Drag & Drop** | Drop images directly into GrowUp |
| **Save** | Export enhanced images |
| **Themes** | System, Light and Dark modes |
| **Settings** | Configure application preferences |

</div>

---

## Tech Stack

<div align="center">

**Python** • **PySide6** • **PyTorch** • **OpenCV** • **Pillow** • **Real-ESRGAN** • **BasicSR**

</div>

---

## Project Structure

```text
GrowUp/
├── app.py
│
├── ui/
│   ├── main_window.py
│   ├── title_bar.py
│   ├── enhance_page.py
│   ├── settings_page.py
│   ├── comparison_view.py
│   └── drop_frame.py
│
├── processing/
│   ├── image_processing.py
│   └── upscaler.py
│
├── models/
└── assets/
```text


tAI Model

GrowUp currently uses Real-ESRGAN for AI-powered image upscaling.

The application uses GPU acceleration through PyTorch + CUDA when available.

Run
python app.py
<div align="center">
GrowUp

Enhance. Restore. Grow.

Currently under active development.

</div> ```
