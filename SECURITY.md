# SECURITY.md — 探究学習ポータルのセキュリティ設計と運用

最終更新: 2026-07-12（管理認証の改修時に作成）

## 認証アーキテクチャ

```
admin.html（公開ページ）
   │  X-Admin-Pass ヘッダ（入力値）
   ▼
Cloudflare Worker (portal-proxy)
   │  env.ADMIN_PASS（シークレット）と照合 ── 一致しなければ全API 401
   │  env.GH_TOKEN でGitHub APIを代理呼び出し
   ▼
GitHub リポジトリ（コミット作成 / Actions起動）
```

- **パスワードの正本は Worker のシークレット `ADMIN_PASS` ただ一つ**。リポジトリ内のファイル（site-config.json等）には保存しない。
- admin.html のログインゲートは `GET /api/check` の 200/401 で判定する（2026-07-12改修。それ以前は公開JSONに平文の複製があった）。
- ブラウザの sessionStorage に入力パスワードを保持する（タブを閉じると消える）。共有PCでは使用後にタブを閉じること。

## 【必須】今すぐ行う運用アクション

1. **ADMIN_PASS のローテーション**: 旧パスワード `3535` は公開リポジトリのgit履歴に残っており無効化が必要。
   Cloudflareダッシュボード → Workers & Pages → portal-proxy → Settings → Variables and Secrets → `ADMIN_PASS` を推測されにくい値に変更。
2. **GH_TOKEN の最小権限化**: classic PAT（repoスコープ＝全リポジトリに書込可）を使っている場合、
   Fine-grained PAT（対象: `portal` リポジトリのみ / Contents: Read and write / Actions: Read and write）へ差し替える。
   万一Workerや端末からトークンが漏れても被害が portal リポジトリに限定される。

## 既知の論点: 朝日けんさくくんの認証情報

`index.html`（デフォルト値）と `project/site-config.json` に、契約データベースの共有ID/PWが記載され、**公開ページ上で全世界に閲覧可能**になっている。生徒への配布手段としては便利だが、次のリスクがある:

- 契約上、利用は校内者に限定されているのが通例（第三者利用は契約違反になり得る）
- 検索エンジン・アーカイブサイトに収集される

**選択肢**（要判断・現状は変更していない）:
- A. 掲載をやめ、リンクのみにして認証情報は授業・Classroom等の校内チャネルで配布（推奨）
- B. 掲載を続けるなら、提供元に公開可否を確認し、定期的にPWローテーション
- C. サイト全体に閲覧制限をかける（GitHub Pagesは非対応。Cloudflare Pages + Access等への移行が必要）

## 残リスクと将来の強化候補（優先度順）

1. **レートリミット無し**: パスワード総当たりを防ぐ仕組みがない。Cloudflare WAF のレート制限ルール（無料枠可）を
   Worker のルートに設定すると軽減できる。
2. **CORS が `*`**: 認証はヘッダのシークレットで担保されているため直ちに危険ではないが、
   `https://sakadosoutan-boop.github.io` のみに絞るとより堅い（ローカルでadmin.htmlを開く運用をやめる場合）。
3. **監査ログ無し**: 変更履歴はgitコミットで追える（コミットメッセージ「管理ページから〜」）。Workerログの保全は未設定。

## 事故時の対応

- **パスワード漏えいの疑い** → ADMIN_PASS を即変更（上記手順）。それだけで全端末のセッションが無効化される。
- **GH_TOKEN 漏えいの疑い** → GitHub → Settings → Developer settings → 該当PATを Revoke → 新規発行してWorkerのシークレットを更新。
- **不審なコミット** → `git log` で「管理ページから〜」以外の不審な変更を確認し、revert。mainのforce-push禁止設定（ブランチ保護）を推奨。
