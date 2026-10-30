# Microscopy Image Segmentation

A simple Python application built with [Streamlit](https://streamlit.io/) for threshold-based segmentation of microscopy images.

## Features

- Upload PNG, JPG/JPEG, TIFF, and BMP images.
- Convert RGB images to grayscale for analysis.
- Segment bright or dark objects.
- Use automatic Otsu thresholding or choose a manual threshold.
- Remove small connected components and optionally fill small holes.
- View the original image, binary mask, and colored overlay.
- Estimate connected-component count and foreground area in pixels.
- Download the binary mask and overlay as PNG files.

> **Important:** This is a basic classical image-processing application. Thresholding is not a universal cell-segmentation method. Results depend on image contrast, illumination, staining, and object overlap. Always visually inspect the output before using it for research or reporting.

## Quick start (Windows, macOS, or Linux)

### 1. Install Python

Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/). On Windows, select the option to add Python to PATH during installation.

Check the installation:

```bash
python --version
```

Some systems use `python3` instead of `python`.

### 2. Download the project

Either download this repository as a ZIP from GitHub and extract it, or clone it:

```bash
git clone https://github.com/YOUR-USERNAME/microscopy-segmentation.git
cd microscopy-segmentation
```

Replace `YOUR-USERNAME` with your GitHub username.

### 3. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Start the application

```bash
streamlit run app.py
```

The terminal will show a local address, usually:

`http://localhost:8501`

Open that address in your browser. Keep the terminal open while using the app. Stop the app with `Ctrl+C`.

## How to use

1. Open the app in your browser.
2. Upload a microscopy image.
3. In the sidebar, select whether the objects are brighter or darker than the background.
4. Choose **Otsu (automatic)** for an automatically calculated threshold, or **Manual** to adjust the threshold yourself.
5. Adjust the minimum object size to remove small noise particles.
6. Optionally fill small holes and display object boundaries.
7. Inspect the original image, binary mask, overlay, and basic measurements.
8. Download the mask or overlay.

### Interpreting the output

- **Binary mask:** white (255) is foreground; black (0) is background.
- **Overlay:** green indicates segmented pixels; red indicates detected component boundaries when enabled.
- **Objects detected:** number of connected foreground components. Touching cells may be counted as one.
- **Area:** reported in pixels and percentage of image area. Physical units require image calibration.


```
## Troubleshooting

- **`streamlit` is not recognized:** activate your virtual environment and run `python -m pip install -r requirements.txt`; then start with `python -m streamlit run app.py`.
- **ModuleNotFoundError:** confirm the virtual environment is active and reinstall requirements.
- **Port 8501 is busy:** run `streamlit run app.py --server.port 8502` and open `http://localhost:8502`.
- **TIFF upload fails:** some multi-page or unusual TIFF formats may not be supported by the image reader. Export the desired page as a standard TIFF or PNG and try again.
- **Poor segmentation:** try the opposite object polarity, adjust the manual threshold, or improve image illumination/contrast before segmentation.

## Project structure

```text
microscopy-segmentation/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── examples/
│   └── README.md
└── outputs/
    └── README.md
```
