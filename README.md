
# Shades

Universal skin shade transformation generator using Gemini API.

## Features
- Batch generate multiple skin tones from one input image
- Supports hands, face, neck, jewelry, and mixed poses
- Preserves jewelry, anatomy, lighting, and composition
- Uses HEX-based skin shade transformation
- Universal prompt for real-world image variation
- Organized hand-wise output folders

---

## Requirements
- Python 3.10+
- Gemini API Key

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/shades.git
cd shades
````

### 2. Create Virtual Environment

```bash
python -m venv env
```

### 3. Activate Virtual Environment

#### Windows

```bash
env\Scripts\activate
```

#### Mac/Linux

```bash
source env/bin/activate
```

### 4. Install Dependencies

```bash
pip install google-genai pillow python-dotenv
```

---

## API Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Folder Structure

```bash
shades/
│
├── hands/          # Input images
├── outputs/        # Generated outputs
├── env/            # Virtual environment
├── .env            # Gemini API key
├── .gitignore
├── README.md
└── test.py
```

---

## Add Input Images

Place all source images inside:

```bash
hands/
```

### Supported Formats:

* `.png`
* `.jpg`
* `.jpeg`

---

## Run Project

```bash
python test.py
```

---

## Workflow

1. Script scans all images inside `hands/`
2. Select target image from menu
3. Gemini generates all predefined skin shade outputs
4. Outputs are saved in:

```bash
outputs/<selected_image_name>/
```

---

## Example Output

```bash
outputs/hand1/
├── hand1_very_fair.png
├── hand1_fair.png
├── hand1_light.png
├── hand1_medium.png
├── hand1_olive_tan.png
├── hand1_brown.png
└── hand1_dark.png
```

---

## Git Ignore

The following are excluded from GitHub:

* `outputs/`
* `env/`
* `.env`
* `shades/`

---

## Notes

* Original image structure is preserved
* Only visible skin tone is transformed
* Jewelry/accessories remain unchanged
* Supports real-world pose variations automatically

---

## License

Personal/project use.

```
```
