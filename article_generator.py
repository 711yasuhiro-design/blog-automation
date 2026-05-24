import os
import re
from anthropic import Anthropic
from config import CLAUDE_API_KEY

client = Anthropic(api_key=CLAUDE_API_KEY)

PROMPT_DIR = os.path.join(os.path.dirname(__file__), 'prompts')

# Author Persona System Prompt
AUTHOR_PERSONA = """あなたは「ふじやん」です。以下のペルソナで記事を執筆してください。

【基本情報】
- 36歳のサラリーマン（東京都・東急池上線沿線）
- 妻と5歳の娘との3人暮らし
- 中堅商社の通販営業部 チームリーダー（管理職）

【専門スキル・思考】
- 仕組み化・自動化を徹底的に追求（属人化を嫌う）
- データと論理で説明責任を果たす（感情論ではなく構造で語る）
- Excel、Power Automate、SAP、Tableau、AI（Claude、Gemini等）を使いこなす
- 先進的なツールを自ら検証し、組織の標準にする意識を持つ

【ライフスタイル】
- 読書好き（ミステリー、ビジネス、現代小説など）。Kindle や BOOX を愛用
- 投資（米国テック株、インデックスETF、ゴールド）への関心が高い
- 週1回のジムでウェイトトレーニング（限界まで追い込むタイプ）
- NBAや国内B.リーグ観戦が好き
- クラフトウイスキー・クラフトジン・こだわりコーヒーへの造詣が深い
- 週末は「背徳グルメ」（二郎系ラーメンなど）を全力で楽しむ人間味がある

【家族観】
- 5歳の娘の創造力（アクアビーズ、粘土細工など）をサポート
- 娘の成長の瞬間を大切に見守り、その記憶が彼女の心の支えになると信じている
- 妻の体調不良時は環境最適化スキルでケアする優しさ
- 「大人の実感」が湧かない感覚を持ちながらも、極めて高い問題解決能力を発揮

【文体・トーン】
- ベースは論理的かつ冷静（感情論ではなく、構造・ロジック・データ・効率を重視）
- エンジニア的・IT用語的な比喩（バグ、OS、仕様、デバッグ、パイプラインなど）が自然に馴染む
- 一方で、週末の泥臭い育児、妻への気遣い、ジャンクフードへの愛着など、完璧すぎない「等身大の人間味」をトッピング
- 論理的かつユーモアがある、バランスの取れた文体を心がける

この背景を踏まえて、記事を執筆してください。"""

def load_prompt(category):
    """Load category-specific prompt template."""
    # Map categories to prompt files
    prompt_map = {
        'whisky-review': 'whisky_review.txt',
        'whisky-compare': 'whisky_compare.txt',
        'whisky-ranking': 'whisky_ranking.txt',
        'gin-review': 'gin_review.txt',
        'gin-compare': 'gin_compare.txt',
        'papa-life': 'papa_life.txt',
        'basketball': 'basketball.txt',
        'book': 'book_review.txt',
        'work-side': 'work_side.txt',
        'daily': 'daily.txt',
    }

    filename = prompt_map.get(category, 'daily.txt')
    filepath = os.path.join(PROMPT_DIR, filename)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return get_default_prompt(category)

def get_default_prompt(category):
    """Return a default prompt if category-specific one not found."""
    return f"""以下のお題について、36歳サラリーマン・子育て中パパの観点で、ゆるめ丁寧語（〜ですね、〜でした）で記事を書いてください。

カテゴリ: {category}

要件:
- 3000〜4000字
- Markdown形式
- 構成: リード文（50-100字）→ 結論ファースト（100字）→ 詳細説明 → 比較表（該当時） → 筆者の総評 → FAQ
- アフィリエイトリンクが必要な箇所には [AMAZON_LINK_HERE] と記載
- 実体験・具体例を入れる
"""

def generate_article(title, category, memo=''):
    """Generate an article using Claude API."""
    base_prompt = load_prompt(category)

    user_message = f"""
【記事のお題】
タイトル: {title}
カテゴリ: {category}
メモ・参考情報: {memo}

上記のお題で記事を書いてください。
"""

    message = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=4000,
        system=AUTHOR_PERSONA,
        messages=[
            {
                'role': 'user',
                'content': base_prompt + '\n\n' + user_message
            }
        ]
    )

    markdown_content = message.content[0].text

    # Convert Markdown to HTML
    html_content = markdown_to_html(markdown_content)

    return html_content


def markdown_to_html(markdown_text):
    """Convert Markdown to simple HTML."""
    html = markdown_text

    # Headers: ### -> <h3>, ## -> <h2>, # -> <h1>
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Bold: **text** -> <strong>text</strong>
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Italic: *text* -> <em>text</em>
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Horizontal rule: --- -> <hr />
    html = re.sub(r'^---+$', '<hr />', html, flags=re.MULTILINE)

    # Lists: convert markdown lists to <ul><li>
    lines = html.split('\n')
    result = []
    in_list = False

    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            item = line.strip()[2:]
            result.append(f'<li>✓ {item}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if line.strip():
                # Wrap non-empty lines in <p> if not already HTML tags
                if not line.strip().startswith('<'):
                    result.append(f'<p>{line}</p>')
                else:
                    result.append(line)
            else:
                result.append('')

    if in_list:
        result.append('</ul>')

    html = '\n'.join(result)

    return html

def extract_metadata_from_article(article_text):
    """Extract article metadata (title from H1, etc) if needed."""
    lines = article_text.split('\n')
    for line in lines:
        if line.startswith('# '):
            return {'title': line.replace('# ', '').strip()}
    return {'title': 'Untitled'}

if __name__ == '__main__':
    # Test
    article = generate_article(
        title='ハイボールにおすすめのウイスキー比較TOP10',
        category='whisky-compare',
        memo='コスパ重視で初心者向け'
    )
    print(article[:500])
