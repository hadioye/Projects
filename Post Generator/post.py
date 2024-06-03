from PIL import Image, ImageDraw, ImageFont

# Control variables
profile_name = "Haroon Ismail"
show_swipe_right = False
top_margin = 100  # Set the top margin value

# Function to create a slide with title and content
def create_slide(title, content, output_path):
    width, height = 800, 800  # Image size
    background_color = "black"
    
    # Create the base image
    base = Image.new('RGB', (width, height), background_color)
    
    # Create a drawing context
    draw = ImageDraw.Draw(base)
    
    # Load the font
    font_path = "arial.ttf"  # Replace with your font path
    title_font_size = 36
    content_font_size = 24
    title_font = ImageFont.truetype(font_path, title_font_size)
    content_font = ImageFont.truetype(font_path, content_font_size)
    
    # Load the profile picture (pfp)
    pfp_path = "PFP/pfp_0.jpeg"  # Replace with the path to your profile picture
    pfp_size = 80
    pfp_margin = 20
    
    pfp = Image.open(pfp_path).resize((pfp_size, pfp_size)).convert("RGBA")
    
    # Create a circular mask for the profile picture
    mask = Image.new("L", (pfp_size, pfp_size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([(0, 0), (pfp_size, pfp_size)], fill=255)
    pfp = Image.composite(pfp, Image.new("RGB", (pfp_size, pfp_size), "black"), mask)
    
    # Paste the profile picture onto the base image
    base.paste(pfp, (pfp_margin, pfp_margin + top_margin))  # Add top margin
    
    # Add profile name
    profile_name_x = pfp_margin + pfp_size + 10
    profile_name_y = pfp_margin + (pfp_size - title_font_size) // 2 + top_margin  # Add top margin
    draw.text((profile_name_x, profile_name_y), profile_name, fill="white", font=title_font)
    
    # Add title
    title_x = 50
    title_y = pfp_margin + pfp_size + 50 + top_margin  # Add top margin
    draw.text((title_x, title_y), title, fill="white", font=title_font)
    
    # Add content
    content_x = 50
    content_y = title_y + title_font_size + 20  # Add spacing after the title
    max_width = width - 100  # Maximum width for wrapping text
    line_height = 35  # Line height for paragraphs
    
    paragraphs = split_into_paragraphs(content)
    for paragraph in paragraphs:
        lines = wrap_text(paragraph, content_font, max_width)
        for line in lines:
            draw.text((content_x, content_y), line, fill="white", font=content_font)
            content_y += line_height
        content_y += line_height  # Add extra space between paragraphs

    # Add a call to action
    if show_swipe_right:
        call_to_action_text = "Swipe right"  # Text for the call to action
        call_to_action_font_size = 30
        call_to_action_font = ImageFont.truetype("arial.ttf", call_to_action_font_size)
        call_to_action_width, call_to_action_height = draw.textbbox((0, 0), call_to_action_text, font=call_to_action_font)[2:4]

        # Load the arrow image
        arrow_image_path = "Cliparts/arrow.png"
        arrow_image = Image.open(arrow_image_path).convert('RGBA')
        arrow_size = (100, 30)  # Adjust the size of the arrow image as needed
        arrow_image = arrow_image.resize(arrow_size)

        # Position the call to action text and arrow
        call_to_action_position = ((width - call_to_action_width - arrow_size[0] - 5) - 100, height - call_to_action_height - 20)  # Adjust position as needed

        draw_text_with_outline(draw, call_to_action_text, call_to_action_position, call_to_action_font, fill="white", outline_fill="black", outline_width=2)

        # Paste the arrow image next to the call to action text
        arrow_position = (call_to_action_position[0] + call_to_action_width + 5, call_to_action_position[1] + (call_to_action_height - arrow_size[1]) // 2)
        base.paste(arrow_image, arrow_position, arrow_image)

    # Save the image
    base.save(output_path)
    print(f"Slide saved to {output_path}")

# Function to split content into paragraphs after every two sentences
def split_into_paragraphs(content):
    sentences = content.split('. ')
    paragraphs = []
    paragraph = ""
    for i, sentence in enumerate(sentences):
        if i % 2 == 0 and i != 0:
            paragraphs.append(paragraph.strip())
            paragraph = sentence.strip() + ". "
        else:
            paragraph += sentence.strip() + ". "
    if paragraph:
        paragraphs.append(paragraph.strip())
    return paragraphs

# Function to wrap text based on maximum width
def wrap_text(text, font, max_width):
    lines = []
    words = text.split(" ")
    while words:
        line = ""
        while words and font.getlength(line + words[0] + " ") <= max_width:
            line += words.pop(0) + " "
        lines.append(line.strip())
    return lines

# Function to draw text with an outline
def draw_text_with_outline(draw, text, position, font, fill, outline_fill, outline_width):
    x, y = position
    draw.text((x-outline_width, y-outline_width), text, font=font, fill=outline_fill)
    draw.text((x+outline_width, y-outline_width), text, font=font, fill=outline_fill)
    draw.text((x-outline_width, y+outline_width), text, font=font, fill=outline_fill)
    draw.text((x+outline_width, y+outline_width), text, font=font, fill=outline_fill)
    draw.text(position, text, font=font, fill=fill)

def read_script(file_path):
    with open(file_path, 'r') as file:
        script_data = file.read().strip().split('\n')

    slides = []
    current_slide = {}
    
    for line in script_data:
        if line.startswith("Title:"):
            current_slide['title'] = line.replace("Title: ", "").strip()
        elif line.startswith("Slide:"):
            if current_slide:  # If there is an existing slide, add it to slides
                slides.append(current_slide)
            current_slide = {'title': line.replace("Slide: ", "").strip()}
        elif line.startswith("Content:"):
            current_slide['content'] = line.replace("Content: ", "").strip()
    
    if current_slide:  # Add the last slide if present
        slides.append(current_slide)
    
    return slides


# Read the script
slides = read_script("post.txt")

# Generate and save slides
for idx, slide in enumerate(slides):
    output_path = f"Output/slide_{idx + 1}.png"
    create_slide(slide['title'], slide['content'], output_path)