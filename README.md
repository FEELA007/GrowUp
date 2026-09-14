# GrowUp

GrowUp is a desktop AI image enhancement and restoration application built with Python and PySide6. It provides 2× / 4× AI image upscaling, denoise, sharpen, deblur, Before / After comparison, drag & drop image support, image preview, enhanced image saving, and a settings interface with theme and processing options. It uses PyTorch, OpenCV, Pillow, Real-ESRGAN, and BasicSR for image processing and AI enhancement.

## Features

- 2× / 4× AI Upscaling
- Denoise
- Sharpen
- Deblur
- Before / After Comparison Slider
- Drag & Drop
- Image Preview
- Save Enhanced Images
- Dark / Light / System Themes
- Settings Page

## Tech Stack

- Python
- PySide6
- PyTorch
- OpenCV
- Pillow
- Real-ESRGAN
- BasicSR

## Project Structure

GrowUp/
├── app.py
├── ui/
│   ├── main_window.py
│   ├── title_bar.py
│   ├── enhance_page.py
│   ├── settings_page.py
│   ├── comparison_view.py
│   └── drop_frame.py
├── processing/
│   ├── image_processing.py
│   └── upscaler.py
├── models/
└── assets/

## Run

python app.py

## Status

GrowUp is currently under active development.

More restoration tools, batch processing, processing controls, and UI improvements are planned.

## License

This project is currently for development and educational purposes.
