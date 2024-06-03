from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

# Function to create the gradient overlay
def apply_gradient(image):
    width, height = image.size
    gradient = Image.new('L', (1, height), color=0xFF)
    for y in range(height):
        gradient.putpixel((0, y), int(255 * (y / height)))  # Invert the gradient calculation
    alpha = gradient.resize(image.size)
    black_im = Image.new('RGBA', (width, height), color='black')
    black_im.putalpha(alpha)
    return Image.alpha_composite(image.convert('RGBA'), black_im)

# Function to create a circular mask
def create_circular_mask(image):
    size = image.size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    result = Image.new('RGBA', size)
    result.paste(image, (0, 0), mask)
    return result

# Function to add text with outline
def draw_text(draw, text, position, font, fill, outline_fill, outline_width):
    x, y = position
    # Draw outline
    draw.text((x-outline_width, y-outline_width), text, font=font, fill=outline_fill)
    draw.text((x+outline_width, y-outline_width), text, font=font, fill=outline_fill)
    draw.text((x-outline_width, y+outline_width), text, font=font, fill=outline_fill)
    draw.text((x+outline_width, y+outline_width), text, font=font, fill=outline_fill)
    # Draw text
    draw.text(position, text, font=font, fill=fill)

# Function to draw the title text with wrapping
def draw_wrapped_text(draw, text, position, font, fill, outline_fill, outline_width, max_width):
    # Wrap the title text into lines
    wrapped_text = textwrap.wrap(text, width=40)  # Adjust the width parameter as needed

    # Calculate total height of the wrapped text
    total_text_height = sum([draw.textbbox((0, 0), line, font=font, spacing=0, align="center")[3] - draw.textbbox((0, 0), line, font=font, spacing=0, align="center")[1] for line in wrapped_text])
    current_height = position[1] - total_text_height // 2  # Center text vertically

    # Draw each line of wrapped text
    for line in wrapped_text:
        text_width, text_height = draw.textsize(line, font=font)
        title_text_position = (position[0] - text_width // 2, current_height)
        draw_text(draw, line, title_text_position, font, fill, outline_fill, outline_width)
        current_height += draw.textbbox((0, 0), line, font=font, spacing=0, align="center")[3] - draw.textbbox((0, 0), line, font=font, spacing=0, align="center")[1]

# Main function to create the final image
def create_title_image(background_path, mystery_image_path, title_text, output_path):
    # Load the background image
    background = Image.open(background_path).convert('RGBA')
    width, height = background.size

    # Apply gradient overlay
    background = apply_gradient(background)

    # Load and process the mystery image
    mystery_image = Image.open(mystery_image_path).convert('RGBA')
    mystery_image_size = (250, 250)  # Change this size if needed
    mystery_image = mystery_image.resize(mystery_image_size)
    mystery_image = create_circular_mask(mystery_image)

    # Paste the mystery image onto the background
    mystery_image_position = ((width // 2 - mystery_image_size[0] // 2) - 150, (height // 2 - mystery_image_size[1] // 2) - 150)
    background.paste(mystery_image, mystery_image_position, mystery_image)

    # Add "@SkipRatRace" text below the mystery image
    handle_text = "@SkipRatRace"
    handle_font_size = 30
    handle_font = ImageFont.truetype("arial.ttf", handle_font_size)
    draw = ImageDraw.Draw(background)
    handle_text_width, handle_text_height = draw.textsize(handle_text, font=handle_font)
    handle_text_position = (mystery_image_position[0] + mystery_image_size[0] // 2 - handle_text_width // 2,
                            mystery_image_position[1] + mystery_image_size[1] + 10)

    draw_text(draw, handle_text, handle_text_position, handle_font, fill="white", outline_fill="black", outline_width=2)

    # Additional lines to add the blue tick image next to the text "SkipRatRace"
    blue_tick_path = "Cliparts/Bluetick.png"
    blue_tick_image = Image.open(blue_tick_path).convert('RGBA')
    blue_tick_size = (40, 40)  # Adjust the size of the blue tick image as needed
    blue_tick_image = blue_tick_image.resize(blue_tick_size)

    # Paste the blue tick image next to the text "SkipRatRace"
    blue_tick_position = (handle_text_position[0] + handle_text_width + 5, handle_text_position[1] -5)  # Adjust position as needed
    background.paste(blue_tick_image, blue_tick_position, blue_tick_image)

    # Draw the title text
    font_path = "arial.ttf"  # Change to the path of your font
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)
    max_text_width = width - 40  # Maximum text width with 20-pixel margins on each side
    title_text_position = (width // 2, height - height // 5)

    draw_wrapped_text(draw, title_text, title_text_position, font, fill="yellow", outline_fill="black", outline_width=2, max_width=max_text_width)

    # Add a call to action
    call_to_action_text = "Swipe right"  # Text for the call to action
    call_to_action_font_size = 30
    call_to_action_font = ImageFont.truetype("arial.ttf", call_to_action_font_size)
    call_to_action_width, call_to_action_height = draw.textsize(call_to_action_text, font=call_to_action_font)

    # Load the arrow image
    arrow_image_path = "Cliparts/arrow.png"
    arrow_image = Image.open(arrow_image_path).convert('RGBA')
    arrow_size = (100, 30)  # Adjust the size of the arrow image as needed
    arrow_image = arrow_image.resize(arrow_size)

    # Position the call to action text and arrow
    call_to_action_position = ((width - call_to_action_width - arrow_size[0] - 5) -100, height - call_to_action_height - 20)  # Adjust position as needed

    draw_text(draw, call_to_action_text, call_to_action_position, call_to_action_font, fill="white", outline_fill="black", outline_width=2)

    # Paste the arrow image next to the call to action text
    arrow_position = (call_to_action_position[0] + call_to_action_width + 5, call_to_action_position[1] + (call_to_action_height - arrow_size[1]) // 2)
    background.paste(arrow_image, arrow_position, arrow_image)

    # Save the final image
    output_folder = "Output"
    output_path = f"{output_folder}/{output_path}"
    background.save(output_path)
    print(f"Title image saved to {output_path}")


# Function to read title from script.txt
def read_title_from_script(script_path):
    with open(script_path, 'r') as file:
        for line in file:
            if line.startswith("Title:"):
                # Extract the title text
                title_text = line[len("Title:"):].strip()
                return title_text

# Example usage
script_path = "script.txt"
title_text = read_title_from_script(script_path)
background_path = "Background/background_1.jpeg"
mystery_image_path = "PFP/pfp_2.jpeg"
output_path = "output.png"
create_title_image(background_path, mystery_image_path, title_text, output_path)