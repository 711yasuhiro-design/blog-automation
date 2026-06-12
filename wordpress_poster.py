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
    Upload featured image from data URL to WordPress.

    Decodes base64 data URL, uploads to media library, and attaches to post.
    """
    try:
        import base64

        # Parse data URL: "data:image/png;base64,{base64_string}"
        if not image_url.startswith('data:image/'):
            print(f'Invalid image URL format: {image_url[:50]}...')
            return None

        # Extract base64 data
        parts = image_url.split(',', 1)
        if len(parts) != 2:
            return None

        base64_data = parts[1]
        image_bytes = base64.b64decode(base64_data)

        # Upload to WordPress media library
        media_url = f'{WORDPRESS_URL}/wp-json/wp/v2/media'
        headers = {
            'Content-Disposition': 'attachment; filename="featured-image.png"',
            'Content-Type': 'image/png',
        }

        response = requests.post(
            media_url,
            data=image_bytes,
            headers=headers,
            auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
        )
        response.raise_for_status()
        media_data = response.json()
        media_id = media_data.get('id')

        if media_id:
            # Attach to post as featured image
            post_url = f'{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}'
            update_payload = {'featured_media': media_id}
            update_response = requests.put(
                post_url,
                json=update_payload,
                auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
            )
            update_response.raise_for_status()
            return media_id

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
