import requests
from requests.auth import HTTPBasicAuth
from config import WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD

def create_draft_post(title, content, category, featured_image_url=None):
    """
    Create a draft post in WordPress via REST API.

    Args:
        title: Post title
        content: Post content (HTML or Markdown converted to HTML)
        category: Category slug (e.g., 'whisky-review')
        featured_image_url: URL of featured image (optional)

    Returns:
        dict with post_id and edit_url if successful
    """
    url = f'{WORDPRESS_URL}/wp-json/wp/v2/posts'

    payload = {
        'title': title,
        'content': content,
        'status': 'draft',
        'slug': slugify(title),
    }

    # Map category to WordPress category ID
    category_id = get_wordpress_category_id(category)
    if category_id:
        payload['categories'] = [category_id]

    auth = HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)

    try:
        response = requests.post(url, json=payload, auth=auth)
        response.raise_for_status()
        post_data = response.json()

        post_id = post_data.get('id')
        edit_url = post_data.get('link', f'{WORDPRESS_URL}/?p={post_id}')

        result = {
            'status': 'success',
            'post_id': post_id,
            'edit_url': edit_url,
            'title': title,
        }

        # If featured image URL provided, try to set it
        if featured_image_url:
            featured_image_id = upload_featured_image(featured_image_url, post_id)
            if featured_image_id:
                result['featured_image_id'] = featured_image_id

        return result

    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'error': str(e),
            'title': title,
        }

def get_wordpress_category_id(category_slug):
    """
    Get WordPress category ID from slug.

    Map categories to WordPress category IDs.
    These should be set up in WordPress admin first.
    """
    category_map = {
        'whisky-review': 1,
        'whisky-compare': 2,
        'whisky-ranking': 2,
        'gin-review': 3,
        'gin-compare': 3,
        'papa-life': 4,
        'basketball': 5,
        'book': 6,
        'work-side': 7,
        'daily': 8,
    }
    return category_map.get(category_slug)

def slugify(text):
    """Convert title to URL-friendly slug."""
    import re
    # Remove non-word characters, convert to lowercase
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def upload_featured_image(image_url, post_id):
    """
    Upload featured image from URL to WordPress.

    For now, returns image_url as fallback.
    Full implementation would download and upload to media library.
    """
    try:
        # In production: download image -> upload to /wp-json/wp/v2/media -> attach to post
        # For MVP: set featured image URL in post meta or acknowledge limitation
        return None
    except Exception as e:
        print(f'Featured image upload failed: {e}')
        return None

def get_post_preview_url(post_id):
    """Get preview URL for draft post."""
    return f'{WORDPRESS_URL}/?p={post_id}&preview=true'

if __name__ == '__main__':
    # Test (requires valid credentials)
    result = create_draft_post(
        title='テスト記事：ハイボールおすすめウイスキー',
        content='<h2>まえがき</h2><p>テスト記事です。</p>',
        category='whisky-compare'
    )
    print(result)
