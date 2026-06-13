from PIL import Image, ImageDraw, ImageFont
import base64
import io

CATEGORY_COLORS = {
    'whisky-review': '#8B4513',
    'whisky-compare': '#8B4513',
    'whisky-ranking': '#8B4513',
    'gin-review': '#4B9CD3',
    'gin-compare': '#4B9CD3',
    'papa-life': '#4CAF50',
    'basketball': '#FF6B00',
    'book': '#9C6B2E',
    'work-side': '#2196F3',
    'daily': '#757575',
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def normalize_category(category):
    """Normalize category name from Notion format to CATEGORY_COLORS key format."""
    if not category:
        return 'daily'
    # Convert to lowercase and replace spaces with hyphens
    normalized = category.lower().replace(' ', '-').replace('_', '-')
    # Check if exact match exists
    if normalized in CATEGORY_COLORS:
        return normalized
    # Check if it's a partial match (e.g., 'whisky' matches 'whisky-compare')
    for key in CATEGORY_COLORS.keys():
        if key.startswith(normalized) or normalized in key:
            return key
    # Default to daily if no match
    return 'daily'

def get_category_color(category):
    """Get category color for featured image."""
    normalized = normalize_category(category)
    return CATEGORY_COLORS.get(normalized, '#757575')

def generate_featured_image(title, category, design_template_id=None):
    """
    Generate a simple featured image using Pillow.

    Creates a 1200x630px image with category color background and title text.
    Returns a data URL (base64 encoded PNG) for use as featured image.
    """
    try:
        # Get category color
        color_hex = get_category_color(category)
        color_rgb = hex_to_rgb(color_hex)

        # Create image
        img = Image.new('RGB', (1200, 630), color=color_rgb)
        draw = ImageDraw.Draw(img)

        # Use Japanese-supporting font (macOS and Linux)
        font = None
        font_paths = [
            # macOS paths
            "/System/Library/Fonts/Hiragino Sans.ttc",
            "/Library/Fonts/Hiragino Sans.ttc",
            # Linux paths
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
            # Fallback
            "/System/Library/Fonts/Noto Sans CJK JP.otf",
            "/Library/Fonts/NotoSansCJKjp-Regular.otf",
        ]
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 48)
                break
            except:
                continue

        if not font:
            font = ImageFont.load_default()

        # Text settings
        text_color = (255, 255, 255)  # White

        # Wrap text for long titles
        words = title.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), line_text, font=font)
            line_width = bbox[2] - bbox[0]

            if line_width > 1000:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Calculate total text height
        line_height = 60
        total_height = len(lines) * line_height

        # Draw text centered
        y_start = (630 - total_height) // 2

        for idx, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (1200 - text_width) // 2
            y = y_start + idx * line_height
            draw.text((x, y), line, fill=text_color, font=font)

        # Convert to base64 data URL
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        data_url = f'data:image/png;base64,{img_base64}'

        return {
            'status': 'created',
            'design_url': data_url,
            'title': title,
            'category': category,
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'title': title,
            'category': category,
        }

if __name__ == '__main__':
    result = generate_featured_image(
        title='ハイボールにおすすめのウイスキー',
        category='whisky-compare'
    )
    print(f"Status: {result.get('status')}")
    print(f"Title: {result.get('title')}")
    print(f"Category: {result.get('category')}")
    if result.get('status') == 'created':
        print(f"Image URL: {result.get('design_url')[:50]}...")
    else:
        print(f"Error: {result.get('error')}")
