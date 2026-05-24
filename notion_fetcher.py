import requests
from config import NOTION_API_KEY, NOTION_DATABASE_ID

NOTION_HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json',
}

def fetch_unprocessed_ideas(limit=3):
    """Fetch unprocessed (未処理) ideas from Notion database."""
    url = f'https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query'

    payload = {
        'filter': {
            'property': 'ステータス',
            'select': {
                'equals': '未処理'
            }
        },
        'sorts': [
            {
                'property': '追加日時',
                'direction': 'ascending'
            }
        ],
        'page_size': limit
    }

    response = requests.post(url, json=payload, headers=NOTION_HEADERS)
    response.raise_for_status()
    data = response.json()

    ideas = []
    for result in data.get('results', []):
        idea = {
            'id': result['id'],
            'title': extract_title(result),
            'category': extract_category(result),
            'memo': extract_memo(result),
        }
        ideas.append(idea)

    return ideas

def extract_title(page):
    """Extract title from Notion page (ネタタイトル property)."""
    try:
        title_prop = page['properties']['ネタタイトル']['title']
        return title_prop[0]['text']['content'] if title_prop else 'Untitled'
    except (KeyError, IndexError):
        return 'Untitled'

def extract_category(page):
    """Extract category from Notion page (カテゴリ property)."""
    try:
        category_prop = page['properties']['カテゴリ']['select']
        return category_prop['name'] if category_prop else 'daily'
    except (KeyError, TypeError):
        return 'daily'

def extract_memo(page):
    """Extract memo from Notion page (メモ property)."""
    try:
        memo_prop = page['properties']['メモ']['rich_text']
        return memo_prop[0]['text']['content'] if memo_prop else ''
    except (KeyError, IndexError):
        return ''

def update_status_to_processed(page_id):
    """Update Notion page status to 記事化済み."""
    url = f'https://api.notion.com/v1/pages/{page_id}'

    payload = {
        'properties': {
            'ステータス': {
                'select': {
                    'name': '記事化済み'
                }
            }
        }
    }

    response = requests.patch(url, json=payload, headers=NOTION_HEADERS)
    response.raise_for_status()

if __name__ == '__main__':
    ideas = fetch_unprocessed_ideas(limit=1)
    for idea in ideas:
        print(f"ID: {idea['id']}")
        print(f"Title: {idea['title']}")
        print(f"Category: {idea['category']}")
        print(f"Memo: {idea['memo']}")
        print()
