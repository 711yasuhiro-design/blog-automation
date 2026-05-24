# セットアップガイド：blog-automation を動かすまでの手順

## 準備物チェック

以下のAPIキー・認証情報が揃っているか確認:

- [ ] Claude API キー (sk-ant-...)
- [ ] Notion API キー
- [ ] Notion ネタ Database ID
- [ ] WordPress Application Password
- [ ] Canva API キー

**不足している場合:**
- Claude API: Anthropic console で生成
- Notion: Notion Integration を作成・Database に接続
- WordPress: エックスサーバー管理画面 → アプリケーションパスワード生成
- Canva: Canva Developers console で生成

---

## ステップ1: ローカルセットアップ

### 1.1 Python依存パッケージをインストール

```bash
cd blog-automation/
pip install -r requirements.txt
```

### 1.2 .env ファイルを作成

```bash
cp .env.template .env
```

`.env` を開いて、以下を入力:

```
CLAUDE_API_KEY=sk-ant-api03-...
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=1234567890...
WORDPRESS_URL=https://fuji-tokyo.com
WORDPRESS_USERNAME=711yasuhiro
WORDPRESS_PASSWORD=B4mP DdSU 0DtI xC90 hJHo f0S8
CANVA_API_KEY=...
```

---

## ステップ2: ローカルテスト

### 2.1 ドライランモード（実際には投稿しない）

```bash
python run_batch.py --dry-run --num 1
```

**期待される出力:**
```
[2026-05-11T...] Starting batch article generation...
Mode: DRY RUN

Step 1: Fetching unprocessed ideas from Notion...
✓ Fetched 1 ideas
  - [ネタのタイトル] (category)

Processing idea 1/1: [ネタのタイトル]
  Generating article with Claude API...
  ✓ Generated XXXX characters
  ...
```

### 2.2 エラーが出た場合

| エラー | 対策 |
|-------|------|
| `ModuleNotFoundError: anthropic` | `pip install -r requirements.txt` を再実行 |
| `ValueError: Missing required environment variables` | `.env` の値をすべて確認 |
| Notion接続エラー | APIキーとDatabase IDが正しいか確認 |
| Claude API エラー | APIキーの有効期限確認 |

### 2.3 本番モード（実際に投稿）

**⚠️ 初回は慎重に実行:**

```bash
# 1記事だけ投稿してみる
python run_batch.py --num 1
```

WordPress管理画面で下書きが作成されたか確認。

---

## ステップ3: GitHub Actions セットアップ（自動実行）

### 3.1 リポジトリを GitHub に Push

```bash
cd blog-automation/

# 初回のみ
git init
git add .
git commit -m "Initial commit: blog automation system"
git remote add origin https://github.com/YOUR_USERNAME/blog-automation.git
git branch -M main
git push -u origin main
```

### 3.2 GitHub Secrets を設定

**操作:**
1. GitHub のリポジトリページを開く
2. Settings → Secrets and variables → Actions → New repository secret
3. 以下を1つずつ追加:

| Secret名 | 値 |
|---------|-----|
| `CLAUDE_API_KEY` | sk-ant-... |
| `NOTION_API_KEY` | secret_... |
| `NOTION_DATABASE_ID` | 1234567890... |
| `WORDPRESS_URL` | https://fuji-tokyo.com |
| `WORDPRESS_USERNAME` | 711yasuhiro |
| `WORDPRESS_PASSWORD` | B4mP DdSU 0DtI xC90 hJHo f0S8 |
| `CANVA_API_KEY` | ... |

### 3.3 自動実行をテスト

**手動トリガー:**
1. GitHub → Actions タブ
2. "Weekly Blog Batch Generation" をクリック
3. "Run workflow" → Run workflow

**成功した場合:**
- Action の実行ログが表示される
- ✅ が表示される
- WordPress に下書きが 1-3 件作成される

**失敗した場合:**
- ❌ が表示される
- "Run workflow" から "Run workflow again" で再実行可能
- ログを確認して原因を特定

### 3.4 定期実行の確認

毎週日曜 JST 02:00 に自動実行されます。

**次の実行予定を確認:**
1. Actions タブ
2. "Weekly Blog Batch Generation" → cron スケジュール確認

---

## ステップ4: 週間オペレーション

### 月曜: ネタ整理（15分）
- Notionで今週のネタを確認
- 優先度を決める

### 日曜夜（自動実行）
- GitHub Actions が自動的に3記事を生成
- WordPress に下書き作成

### 水曜: 編集・公開（30分）
- WordPress 管理画面で下書きを確認
- 実体験を追記
- アフィリエイトリンク挿入 ([AMAZON_LINK_HERE] → 実リンク)
- 画像を追加（Canva手動設定か、AIイラスト）
- 「公開」ボタンをクリック

### 金曜: 数値確認（15分）
- Googleサーチコンソール
- AdSense
- もしもアフィリエイト

---

## トラブルシューティング

### GitHub Actions が動かない

**確認項目:**
1. Secrets が全て設定されているか
2. `.env.template` に全て記載があるか
3. ローカル `python run_batch.py --dry-run` は動くか

**ログ確認方法:**
1. Actions タブ → 実行ログをクリック
2. "Run batch article generation" ステップを展開
3. エラーメッセージを確認

### Notion から記事が取得できない

**確認:**
```bash
python -c "from notion_fetcher import fetch_unprocessed_ideas; print(fetch_unprocessed_ideas(limit=1))"
```

エラーが出た場合:
- Notion APIキーが正しいか
- Database ID が正しいか（24文字）
- Notion Integration がデータベースにアクセスできるか

### WordPress に投稿されない

**確認:**
```bash
python -c "from wordpress_poster import create_draft_post; print(create_draft_post('テスト', '<p>テスト</p>', 'daily'))"
```

エラーが出た場合:
- WordPress URL が正しいか（末尾のスラッシュなし）
- Application Password が正しいか
- `wp-json/` への POST がファイアウォールで遮断されていないか

**エックスサーバーWAF確認:**
1. エックスサーバー管理画面
2. セキュリティ → WAF設定
3. ブログドメイン → WAF を確認
4. 必要に応じて `wp-json` への POST を許可

---

## 次のステップ

1. ✅ ローカルテスト完了
2. ✅ GitHub Secrets 設定完了
3. ✅ GitHub Actions 動作確認完了
4. 📝 優先記事20本を Notion に登録する
5. 📝 X（Twitter）自動投稿を設定する（Uncanny Automator or Zapier）

---

## 参考リンク

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [WordPress REST API](https://developer.wordpress.org/rest-api/)
- [Notion API](https://developers.notion.com/)
- [Anthropic Claude API](https://docs.anthropic.com/)
