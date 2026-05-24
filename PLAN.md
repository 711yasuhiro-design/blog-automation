# ブログ自動化システム - プロジェクトプラン

## プロジェクト概要
Notion → Claude API → WordPress への記事自動化パイプライン

## 完了したタスク ✅

### 機能テスト（2026-05-23）
- [x] Notion Integration 権限設定
- [x] Claude API キー設定（新キー生成）
- [x] WordPress Application Password 再生成
- [x] モデルアップデート（claude-3-5-sonnet → claude-sonnet-4-6）
- [x] 単一記事テスト（ドライラン）
- [x] 本番テスト（WordPress に投稿）
- [x] 複数記事テスト（バッチ処理）

### デザイン・HTML フォーマット改善（2026-05-23）
- [x] Markdown → HTML 自動変換機能を実装
- [x] 記事構造の整理（見出し、段落、区切り線）
- [x] テンプレート統一（全カテゴリーで同じフォーマット）
  - [x] whisky_compare.txt
  - [x] work_side.txt
  - [x] papa_life.txt
  - [x] book_review.txt
  - [x] gin_review.txt
  - [x] basketball.txt
  - [x] daily.txt
- [x] CSS スタイル試行（装飾なしで完了）

## 現在のワークフロー

### 1. Notion 連携 ✅
- 未処理ネタを取得
- カテゴリ別に記事生成プロンプトを選択

### 2. 記事生成 ✅
- Claude API（claude-sonnet-4-6）で 3000〜4000 字の記事を自動生成
- カテゴリ別プロンプトテンプレート対応

### 3. WordPress 投稿 ✅
- REST API で下書き投稿を自動作成
- カテゴリ自動割当

### 4. 画像生成 ⏳
- **現状**: プレースホルダー（カテゴリ色）を生成
- **実装**: WordPress で手動追加
- **将来**: Canva API 統合（保留中）

### 5. Notion 更新 ✅
- ステータスを「記事化済み」に自動更新

## 未実装タスク

### GitHub Actions 設定（次フェーズ）
- [ ] リポジトリを GitHub に Push
- [ ] Repository Secrets に環境変数を登録
  - CLAUDE_API_KEY
  - NOTION_API_KEY
  - NOTION_DATABASE_ID
  - WORDPRESS_URL
  - WORDPRESS_USERNAME
  - WORDPRESS_PASSWORD
  - CANVA_API_KEY
- [ ] GitHub Actions ワークフロー有効化（毎週日曜 02:00）
- [ ] 自動実行テスト

### Canva API 統合（保留中）
- [ ] テンプレート作成
- [ ] Client ID / Secret 取得
- [ ] OAuth 認証実装
- [ ] API で画像自動生成
**現在：** アイキャッチ画像はプレースホルダー（カテゴリ色）で、WordPress で手動追加

## 手動プロセス

### 水曜夜：ブログ管理
1. WordPress 管理画面で下書きを確認
2. 内容を編集（必要に応じて）
3. アイキャッチ画像を追加
4. アフィリエイトリンクを挿入（[AMAZON_LINK_HERE] を置換）
5. 公開ボタンをクリック

## セットアップ状態

### 環境変数（.env）✅
- CLAUDE_API_KEY: 有効（新キー）
- NOTION_API_KEY: 有効
- NOTION_DATABASE_ID: 設定済み（Integration 共有確認）
- WORDPRESS_URL: https://fuji-tokyo.com
- WORDPRESS_USERNAME: 711yasuhiro
- WORDPRESS_PASSWORD: 更新済み
- CANVA_API_KEY: 設定済み（API 統合は保留）

### 依存関係
- anthropic >= 0.7.0 ✅
- requests >= 2.31.0 ✅
- python-dotenv >= 1.0.0 ✅

## ローカルテストコマンド

```bash
# ドライラン（1記事確認）
python3 run_batch.py --dry-run --num 1

# 本番実行（3記事）
python3 run_batch.py

# カスタム件数
python3 run_batch.py --num 5
```

## 注意事項

- `.env` には機密情報が含まれるため Git にコミットしない（.gitignore 確認）
- WordPress REST API は有効状態を維持
- Notion Integration は「ふじやんブログAutomation」で設定
- 月 1 回程度は手動テストを実施して動作確認

## 次回作業予定

### GitHub Actions 設定（別タイミング）
1. リポジトリ初期化
2. GitHub にプッシュ
3. Secrets 登録
4. ワークフロー有効化

---

## 次回作業ガイド（明日以降）

1. **GitHub Actions 設定** — 毎週日曜日の自動実行を実装
   - リポジトリをGitHubに推す
   - Secrets を登録
   - ワークフロー有効化

2. **テスト手順**（デザイン改善後）
   ```bash
   python3 run_batch.py --dry-run --num 1   # ドライランで確認
   python3 run_batch.py --num 1              # 本番実行（WordPress に投稿）
   ```

3. **トラブルシューティング**
   - Notion エラー: API キー、Database ID、Integration 権限を確認
   - WordPress エラー: Application Password、REST API 有効化を確認
   - Claude エラー: API キーの有効期限、クレジット残額を確認

4. **カスタマイズ可能な項目**
   - prompts/*.txt でプロンプト調整
   - article_generator.py で出力フォーマット変更
   - run_batch.py で記事数・オプション変更

---

**最終更新**: 2026-05-23 22:25
**ステータス**: デザイン改善完了 → GitHub Actions 設定待ち
**次のマイルストーン**: 毎週日曜の自動実行開始
