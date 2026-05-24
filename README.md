# Blog Automation System

自動的にNotionのネタ → Claude API生成 → WordPress下書き投稿 するシステム

## セットアップ

### 1. 依存関係インストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数設定

`.env.template` をコピーして `.env` を作成し、各キーを記入:

```bash
cp .env.template .env
```

`.env` の内容:
- `CLAUDE_API_KEY`: Anthropic APIキー（sk-ant-...）
- `NOTION_API_KEY`: Notion Integration Token
- `NOTION_DATABASE_ID`: ネタDBのID
- `WORDPRESS_URL`: ブログのURL（https://fuji-tokyo.com）
- `WORDPRESS_USERNAME`: WordPress ユーザー名
- `WORDPRESS_PASSWORD`: Application Password
- `CANVA_API_KEY`: Canva API キー

### 3. ローカルテスト

```bash
# 3記事を処理（下書き作成）
python run_batch.py

# ドライランモード（動作確認のみ、実際には投稿しない）
python run_batch.py --dry-run

# 1記事だけテスト
python run_batch.py --num 1
```

## ワークフロー

### 自動実行（GitHub Actions）

毎週日曜 JST 02:00 に自動実行

**設定方法:**
1. このリポジトリをGitHubにPush
2. Settings → Secrets → New repository secret
3. 以下のSecretsを追加:
   - `CLAUDE_API_KEY`
   - `NOTION_API_KEY`
   - `NOTION_DATABASE_ID`
   - `WORDPRESS_URL`
   - `WORDPRESS_USERNAME`
   - `WORDPRESS_PASSWORD`
   - `CANVA_API_KEY`

### 手動実行（GitHub Actions）

GitHub Actions → Weekly Blog Batch Generation → Run workflow

## ファイル構成

```
blog-automation/
├── config.py                    # 環境変数読み込み
├── notion_fetcher.py            # Notionからネタ取得
├── article_generator.py         # Claude API記事生成
├── image_generator.py           # Canva画像生成（準備中）
├── wordpress_poster.py          # WordPress REST API投稿
├── run_batch.py                 # 実行スクリプト
├── prompts/                     # カテゴリ別プロンプト
│   ├── whisky_compare.txt
│   ├── whisky_review.txt
│   ├── papa_life.txt
│   ├── basketball.txt
│   ├── book_review.txt
│   ├── gin_review.txt
│   ├── work_side.txt
│   └── daily.txt
├── .github/workflows/
│   └── blog_batch.yml           # GitHub Actions定義
├── .env.template
├── requirements.txt
└── README.md
```

## 処理フロー

1. **Notionからネタ取得**
   - ステータス = "未処理" の記事ネタを3件取得
   - タイトル、カテゴリ、メモを抽出

2. **Claude APIで記事生成**
   - カテゴリに応じたプロンプトテンプレートを読み込み
   - ネタのタイトル + メモで記事を生成（3000〜4000字）

3. **WordPress下書き作成**
   - REST APIで下書き投稿を作成
   - カテゴリ自動割当

4. **Notion更新**
   - ステータスを "記事化済み" に更新

5. **ふじやん手動確認**
   - 水曜夜：WordPress管理画面で内容確認・編集
   - 必要に応じてアフィリエイトリンク挿入・画像追加
   - 公開ボタンをクリック

## トラブルシューティング

### Notion接続エラー
- APIキーと Database ID が正しいか確認
- Notionの Integration設定でデータベースへのアクセスが許可されているか確認

### WordPress投稿失敗
- Application Password が正しいか確認
- WordPress REST API が有効か確認（エックスサーバー管理画面）
- WAF設定で `/wp-json/` へのPOSTが遮断されていないか確認

### Claude API エラー
- APIキーの有効期限
- APIリクエスト上限に達していないか

## カスタマイズ

### プロンプトテンプレートの編集

`prompts/*.txt` ファイルを直接編集して、文体や構成をカスタマイズ可能

### 記事生成数の変更

自動実行: `.github/workflows/blog_batch.yml` の `run_batch.py` パラメータを変更
手動実行: `python run_batch.py --num 5` で5記事生成

### スケジュール変更

`.github/workflows/blog_batch.yml` の `cron` 設定を変更:
```yaml
- cron: '0 17 * * 0'  # 毎週日曜 JST 02:00
```

## 注意事項

- `.env` ファイルは Git にコミットしない（.gitignore に追加）
- Secrets の管理に注意（APIキーは絶対に公開リポジトリにコミットしない）
- WordPress 管理画面での最終確認は必須（自動投稿のため）
- 記事内の [AMAZON_LINK_HERE] は手動でアフィリエイトリンクに置換

## 参考

- [Anthropic Claude API](https://console.anthropic.com/)
- [Notion API Documentation](https://developers.notion.com/)
- [WordPress REST API](https://developer.wordpress.org/rest-api/)
