import requests
from config import CANVA_API_KEY

CANVA_HEADERS = {
    'Authorization': f'Bearer {CANVA_API_KEY}',
    'Content-Type': 'application/json',
}

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

def get_category_color(category):
    """Get category color for featured image."""
    return CATEGORY_COLORS.get(category, '#757575')

def generate_featured_image(title, category, design_template_id=None):
    """
    Generate featured image using Canva API.

    Note: Full Canva API integration requires:
    1. Canvaで事前に作成したテンプレートIDを指定
    2. APIでテンプレートのテキスト要素を置き換え
    3. 画像をエクスポート

    For now, returns metadata. Full implementation requires Canva template setup.
    """
    try:
        if not design_template_id:
            # Placeholder: return color metadata
            color = get_category_color(category)
            return {
                'status': 'placeholder',
                'color': color,
                'title': title,
                'category': category,
                'note': 'Canvaテンプレート未設定。Canva管理画面で手動作成推奨'
            }

        # If template_id is provided, call Canva API
        url = 'https://api.canva.com/rest/v1/designs'
        payload = {
            'name': title,
            'template_id': design_template_id,
        }
        response = requests.post(url, json=payload, headers=CANVA_HEADERS)
        response.raise_for_status()
        design_data = response.json()

        return {
            'status': 'created',
            'design_id': design_data.get('id'),
            'design_url': design_data.get('url'),
            'title': title,
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'title': title,
        }

def get_placeholder_image_url(category):
    """Return a placeholder image URL for the category."""
    color = get_category_color(category)
    # Using placeholder.com as fallback
    # In production, use specific Canva templates
    return f'https://via.placeholder.com/1200x630/{color.lstrip("#")}/FFFFFF?text=記事作成中'

if __name__ == '__main__':
    result = generate_featured_image(
        title='ハイボールにおすすめのウイスキー',
        category='whisky-compare'
    )
    print(result)
