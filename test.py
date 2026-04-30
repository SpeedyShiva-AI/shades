import os
import time
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)


MODEL_NAME = "models/gemini-3.1-flash-image-preview"


HANDS_FOLDER = "hands"
OUTPUT_FOLDER = "outputs"


# HEX SHADE DEFINITIONS

SHADE_HEX = {
    "very_fair": "#F6E5D3",
    "fair": "#F1D2B6",
    "light": "#E8C4A2",
    "light_medium": "#D9A07B",
    "medium": "#C68642",
    "olive_tan": "#B47C4D",
    "caramel": "#A86E3A",
    "brown": "#8D5524",
    "deep_brown": "#6F4B2A",
    "dark": "#4A2C1D"
}


# UNIVERSAL PROMPT TEMPLATE

PROMPT_TEMPLATE = """
UNIVERSAL SKIN SHADE TRANSFORMATION TASK:

Transform ONLY visible natural human skin tone in the ORIGINAL uploaded image to EXACTLY match this HEX skin shade:
TARGET HEX SHADE: {target_hex}

STRICT UNIVERSAL RULES:
- ONLY modify visible human skin
- Preserve ALL jewelry exactly unchanged
- Preserve rings, necklaces, bracelets, gemstones, metals, reflections, and accessories perfectly
- Preserve nails exactly
- Preserve facial features exactly
- Preserve anatomy, pose, framing, hand shape, neck shape, and body proportions exactly
- Preserve background exactly
- Preserve clothing exactly
- Preserve hair exactly
- Preserve lighting, shadows, and realism exactly
- Preserve skin texture, pores, gradients, and depth naturally
- DO NOT generate a new image composition
- DO NOT replace subject
- DO NOT hallucinate alternate poses
- DO NOT alter camera angle
- DO NOT output a reference image
- DO NOT oversoften or oversaturate skin
- Maintain photorealistic luxury commercial quality
- Skin tone transformation must be clearly visible
- Match HEX shade accurately while preserving realism

ANTI-HALLUCINATION PRIORITY:
The uploaded original image is the ONLY structural source.
Only skin color should change.
Everything else must remain identical.

FINAL GOAL:
Return the SAME original image with ONLY skin tone adjusted to target HEX shade.
"""

# HELPERS
def ensure_output_folder():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)


def list_hand_images():
    supported_ext = [".png", ".jpg", ".jpeg"]
    files = [
        f for f in os.listdir(HANDS_FOLDER)
        if os.path.splitext(f)[1].lower() in supported_ext
    ]
    return sorted(files)


def choose_hand():
    hands = list_hand_images()

    if not hands:
        raise FileNotFoundError("No images found in hands folder.")

    print("\nAvailable Input Images:")
    for idx, hand in enumerate(hands, start=1):
        print(f"{idx}. {hand}")

    while True:
        try:
            choice = int(input("\nSelect image number: "))
            if 1 <= choice <= len(hands):
                return hands[choice - 1]
            else:
                print("Invalid selection.")
        except ValueError:
            print("Enter a valid number.")


def load_image(path):
    return Image.open(path)


def save_generated_image(response, output_path):
    """
    Extract Gemini image bytes and save output.
    """
    try:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image_bytes = part.inline_data.data
                with open(output_path, "wb") as f:
                    f.write(image_bytes)
                return True
    except Exception:
        return False

    return False


# MAIN GENERATION FUNCTION
def generate_all_shades(selected_hand):
    hand_path = os.path.join(HANDS_FOLDER, selected_hand)

    if not os.path.exists(hand_path):
        raise FileNotFoundError(f"Input image not found: {hand_path}")

    original_image = load_image(hand_path)
    base_name = os.path.splitext(selected_hand)[0]

    # Hand-specific output folder
    hand_output_folder = os.path.join(OUTPUT_FOLDER, base_name)

    if not os.path.exists(hand_output_folder):
        os.makedirs(hand_output_folder)

    for shade_name, hex_code in SHADE_HEX.items():

        print(f"\nGenerating shade: {shade_name}")
        print(f"Target HEX: {hex_code}")

        final_prompt = PROMPT_TEMPLATE.format(target_hex=hex_code)

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    final_prompt,
                    original_image
                ]
            )

            output_filename = f"{base_name}_{shade_name}.png"
            output_path = os.path.join(hand_output_folder, output_filename)

            success = save_generated_image(response, output_path)

            if success:
                print(f"Saved: {output_path}")
            else:
                print(f"Failed output for shade: {shade_name}")
                print("Stopping batch process.")
                break

            # Delay to reduce API stress
            time.sleep(2)

        except Exception as e:
            print(f"Error generating {shade_name}: {str(e)}")
            print("Stopping batch due to API/resource issue.")
            break



# MAIN PROGRAM
def main():
    print("===========================================")
    print(" Universal Skin Shade Batch Generator ")
    print("===========================================")

    ensure_output_folder()

    selected_hand = choose_hand()

    print(f"\nSelected image: {selected_hand}")
    print("Generating all skin shades...\n")

    generate_all_shades(selected_hand)

    print("\nBatch generation complete.")


# ENTRY

if __name__ == "__main__":
    main()