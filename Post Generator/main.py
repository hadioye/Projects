import os
import random
import uuid
from PIL import Image
from title import create_title_image

def get_random_image(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.jpeg')]
    if not files:
        raise ValueError(f"No images found in the {folder} folder.")
    file_path = os.path.join(folder, random.choice(files))
    return Image.open(file_path).convert('RGBA')

def generate_output_id():
    return str(uuid.uuid4())

def main():
    background_folder = "Background"
    pfp_folder = "PFP"
    title_text = "How to Start an Online AI Agency in 2024 Everything you need to know!"
    mystery_text = "@Hammad"
    output_folder = "Output"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the background and mystery images
    background = get_random_image(background_folder)
    mystery_image = get_random_image(pfp_folder)

    # Generate unique output ID
    output_id = generate_output_id()
    output_path = os.path.join(output_folder, f"output_{output_id}.png")

    # Create the title image
    create_title_image(background, mystery_image, title_text, mystery_text, output_path)

if __name__ == "__main__":
    main()
