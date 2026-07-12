# 探究学習ポータル（portal）

高校生向け「探究学習ポータル」の本番リポジトリ（正本）。

- 公開URL: https://sakadosoutan-boop.github.io/portal/ （main への push で自動デプロイ）

## 構成

- `index.html` — 公開ページ本体
- `admin.html` — 管理ページ（Cloudflare Worker 経由で本リポジトリへコミットし、内容を更新する）
- `cloudflare-worker.js` — 管理ページ→GitHub の中継プロキシのソース
- `project/` — 稼働データと本番参照アセット（`seminars/`、`site-config.json`、`deadlines.json`、`forms-config.json`、`assets/fonts/`、`support.js`）
- `scripts/update_seminars.py` — チラシ（PDF/画像）から `seminars.json` を自動生成（GitHub Actions: `update-seminars.yml`、Gemini API 使用）
- `docs/design-handoff/` — 初期設計（claude.ai/design）ハンドオフのアーカイブ（本番では未使用）

## 運用ルール

- `project/seminars/seminars.json` と `scripts/.seminars_cache.json` は自動生成物。手編集しない。
- セミナーの追加は管理ページから行うか、チラシ画像/PDF を `project/seminars/` へ push する（Actions が自動反映）。
- 「管理ページからセミナーを更新」系のコミットは bot 運用によるもので正常。
- 編集ガイドの詳細は `CLAUDE.md` を参照。
