"""
Affiliate link management for blog monetization.
"""

AMAZON_STORE_ID = 'fujisanwhisky-22'

CATEGORY_AFFILIATE_CONFIG = {
    'whisky-review': {
        'affiliate_program': 'amazon',
        'keywords': ['whisky', 'whiskey', 'scotch', 'bourbon', 'japanese whisky'],
        'description': 'ウイスキー商品',
        'instructions': '記事内で紹介しているウイスキーの Amazon リンクを含めてください（2-3個）'
    },
    'whisky-compare': {
        'affiliate_program': 'amazon',
        'keywords': ['whisky', 'whiskey', 'scotch', 'bourbon', 'japanese whisky'],
        'description': 'ウイスキー商品',
        'instructions': '比較対象のウイスキーについて Amazon リンクを含めてください（3-4個）'
    },
    'whisky-ranking': {
        'affiliate_program': 'amazon',
        'keywords': ['whisky', 'whiskey', 'scotch', 'bourbon'],
        'description': 'ウイスキー商品',
        'instructions': 'ランキング内の各ウイスキーについて Amazon リンクを含めてください（4-5個）'
    },
    'work-side': {
        'affiliate_program': 'amazon',
        'keywords': ['book', 'tool', 'software', 'service', 'course'],
        'description': 'ビジネス書・ツール',
        'instructions': '仕事関連の推奨書籍やツール、サービスについて Amazon リンクを含めてください（2-3個）'
    },
}

def get_affiliate_instructions(category):
    """
    Get affiliate link instructions for a category.

    Args:
        category: Category slug (e.g., 'whisky-compare')

    Returns:
        dict with affiliate config and instructions, or None if not configured
    """
    # Normalize category (handle partial matches)
    for key, config in CATEGORY_AFFILIATE_CONFIG.items():
        if key.startswith(category.lower().replace(' ', '-')) or category.lower() in key:
            return config
    return None

def build_amazon_affiliate_url(asin):
    """
    Build Amazon affiliate URL with store ID.

    Args:
        asin: Amazon Standard Identification Number

    Returns:
        Full affiliate URL
    """
    return f'https://amazon.co.jp/dp/{asin}?tag={AMAZON_STORE_ID}'

def get_affiliate_prompt_addition(category):
    """
    Get the additional prompt text for Claude to include affiliate link placeholders.

    Args:
        category: Category slug

    Returns:
        str: Prompt addition for Claude
    """
    config = get_affiliate_instructions(category)
    if not config:
        return ''

    instructions = config.get('instructions', '')
    program = config.get('affiliate_program', '')

    if program == 'amazon':
        return f"""

## 商品リンク挿入指示
{instructions}
商品を紹介する際は、以下の形式で Amazon リンク用のプレースホルダーを入れてください：

形式: <a href="[AMAZON_LINK]">[商品名]</a>

例：<a href="[AMAZON_LINK]">山崎 18年</a>

※ [AMAZON_LINK] の部分は記事執筆者が後から実際の Amazon アフィリエイトリンクに置換します
"""

    return ''

if __name__ == '__main__':
    # Test
    categories = ['whisky-compare', 'work-side', 'daily']
    for cat in categories:
        config = get_affiliate_instructions(cat)
        print(f"{cat}: {config}")
        print()
