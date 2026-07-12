# CLAUDE.md

## プロジェクト概要
「探究学習ポータル」の正本（本番）リポジトリ。高校生の「総合的な探究の時間」を支援する静的サイト＋管理画面。GitHub: sakadosoutan-boop/portal。

## アーキテクチャ（本番系）
- `index.html` … 公開ページ（本番・正本）。`project/` 配下の各JSONを実行時に fetch して描画。
- `admin.html` … 管理画面。Cloudflare Worker 経由で GitHub にコミットしてコンテンツを更新。
- `cloudflare-worker.js` … 管理→GitHub中継プロキシ。`X-Admin-Pass` 認証でファイルGET/PUT・Actions dispatch を中継（別途Cloudflareへデプロイ）。
- `scripts/update_seminars.py` … `project/seminars/` のチラシ（PDF/画像）を Gemini API で解析し `seminars.json` を自動生成。
- `.github/workflows/update-seminars.yml` … 上記スクリプトを push / 手動起動で実行し、bot が main へ自動コミット。
- `project/site-config.json` / `deadlines.json` / `forms-config.json` … 公開ページが fetch する稼働データ。
- `project/seminars/` … セミナーのチラシ原本と `seminars.json`（稼働データ）。
- `project/support.js` … 公開ページが読み込む共有スクリプト（本番依存）。
- `docs/design-handoff/` … claude.ai/design 設計ハンドオフのアーカイブ（本番と無関係）。
- `SECURITY.md` … 認証設計と運用手順（パスワード変更・トークン最小権限・事故対応）。**管理パスワードはWorkerシークレットが唯一の正本。リポジトリ内ファイルに書かない。**

## 絶対ルール
- `project/seminars/seminars.json` と `scripts/.seminars_cache.json` は自動生成物。手編集禁止。
- セミナー追加は、チラシ（PDF/画像）を `project/seminars/` に push するか、管理ページから行う。
- 「管理ページからセミナーを更新」等のコミットは bot 運用による正常な挙動。

## 公開URL
`https://sakadosoutan-boop.github.io/portal/`（クラシックGitHub Pages。main への push ごとに「pages build and deployment」が自動実行される。2026-07-12 に Actions 実行履歴で確認済み）。admin.html の `WORKER_URL=https://portal-proxy.sakadosoutan.workers.dev` は管理用プロキシで公開URLではない。

## モデル/トークン運用（標準指示）
- オーケストレーター本体のトークン消費を抑えるため、次を標準とする:
  - 大規模なコード探索・調査 → Sonnet のサブエージェントに委譲
  - 大きめの実装・リファクタ → Opus のサブエージェントに委譲
  - 本体（上位モデル）は方針決定・レビュー・統合のみを担う
- 手順の詳細は .claude/skills/delegate/ を参照。

## コミット規約
`feat:` / `fix:` / `docs:` / `chore:` ＋日本語要約。
