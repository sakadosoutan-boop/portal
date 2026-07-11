# 総合的な探究ポータルサイト

_Started 2026-06-23 03:33 UTC_

---

## User

指示:
提供するテキストデータを基に、高校生が「総合的な探究の時間」で使うための、スタイリッシュでモダンなWEBポータルサイト（シングルページアプリケーション風のデザイン）をHTML/CSS（Tailwind CSS推奨）とJavaScriptを用いたArtifactとして作成してください。

【デザイン・UI/UXの要望】
1. 全体デザイン:
   - 白や淡いグレーを基調に、アクセントカラー（例: 知的な印象のディープブルーや、探究心を刺激する鮮やかなエメラルドグリーンなど）を用いたクリーンでモダンなデザイン。
   - すべてのリンクはカード型、または洗練されたリスト形式で整理し、ホバーアニメーション（ふわっと浮き上がる、色が変わるなど）を実装してください。

2. ヒーローセクション（最上部）:
   - キャッチコピーとして「総合的な探究の時間：リサーチポータル」のようなタイトルを大きく掲げる。
   - 「最重要原則」である【Google検索の結果に安易に飛びつかない！書籍や論文などの一次情報にあたる！】という文言を、最も目立つ警告バナーやヒーローエリア内のメッセージとして、デザイン性を損なわずに強調して配置する。

3. ナビゲーションと機能:
   - ページ上部（または左側）に、各カテゴリ（総探全般、先行研究、図書、新聞、統計データ、テーマ例、デザイン）へスムーズにスクロールできるナビゲーションバー（固定 or フローティング）を設置する。
   - 「新聞記事（朝日けんさくくん）」のログイン情報（ID/PW、注意書き）は、一目でわかり、かつコピーしやすいように専用のスタイリッシュなカード（アラートボックス風）で囲む。

4. データの構造化:
   - 「統計データ」配下の「①環境問題系」「②地域系」「③文系」「④理系」は、タブ切り替え、あるいはアコーディオンUIなどを用いて、すっきりと見やすく整理する。

---
【元データ】
[総合的な探究の時間 参考・お役立ちサイト]

原則：Google検索の結果（まとめサイト・ブログ・Wikipedia）に安易に飛びつかない！書籍や論文などの一次情報にあたる！

### ■ 総探全般
- [「総合的な学習（探究）の時間」応援団のページ](https://www.mext.go.jp/a_menu/shotou/sougou/syokatsu.htm)（文部科学省）：膨大な資料があるため検索ワードの活用を推奨
- [総合的な探究の時間 | NHK高校講座](https://www.nhk.or.jp/kokokoza/tanq/)
- [探究学習「情報の収集／整理・分析」に使えるリンク集【無料】 - Far East Tokyo](https://www.blog.studyvalley.jp/2021/08/26/link/)

### ■ 先行研究（論文検索サイト）
- [CiNii Research](https://cir.nii.ac.jp/)
- [J-STAGE トップ](https://www.jstage.jst.go.jp/browse/-char/ja/)
- [Google Scholar](https://scholar.google.co.jp/schhp?hl=ja)：多言語対応。海外の論文検索に。
- [国立国会図書館サーチ（NDLサーチ）](https://ndlopac.ndl.go.jp/)：全国の図書館や研究機関の資料を統合検索可能。
- [リサーチ・ナビ | 国立国会図書館](https://rnavi.ndl.go.jp/rnavi/)：調べ方案内の紹介。ウェブサイトへのリンク集も便利。
- [国立国会図書館デジタルコレクション](http://dl.ndl.go.jp/)：電子書籍・雑誌を検索・閲覧可能。

### ■ 図書
- [カーリル](https://calil.jp/)：全国の図書館からリアルタイムの貸出状況を簡単に検索可能。
- [Webcat Plus](http://webcatplus.nii.ac.jp/)：日本で出版された本の検索や、連想検索が可能。
- [想・IMAGINE](http://imagine.bookmap.info/index.jsp)：単語や文章から各データベースを連想検索。
- [日本の古本屋](https://www.kosho.or.jp/)：古本・古書の検索・通販サイト。

### ■ 新聞記事
★ [朝日けんさくくん](https://kensaku.asahi.com/)
【注意】同時ログイン100件まで。使用後は必ずログアウトしてください。
ID: dks669ken 
パスワード: k85g24ys6w

### ■ 統計データ
- [e-Stat 政府統計の総合窓口](https://www.e-stat.go.jp/)
- [RESAS 地域経済分析システム](https://resas.go.jp/#/13/13101)

#### ① 環境問題系
- [SDGs17の目標別動画クリップ | NHK for School](https://www.nhk.or.jp/school/17goals/)
- [SDGsを学べる教材 | JICA](https://www.jica.go.jp/cooperation/learn/material/sdgs.html)
- [NHK地域づくりアーカイブス](https://www.nhk.or.jp/chiiki/)：SDGs関連もあり

#### ② 地域系
- [NHK地域づくりアーカイブス](https://www.nhk.or.jp/chiiki/)

#### ③ 文系
- [NHKラーニング](https://www.nhk.or.jp/learning/)
- [現代日本語書き言葉均衡コーパス（BCCWJ）](https://clrd.ninjal.ac.jp/bccwj/)：少納言（登録不要）、中納言（登録必要）から日本語の使われ方を検索可能。
- [国際日本文化研究センター | 怪異・妖怪伝承データベース](https://www.nichibun.ac.jp/YoukaiDB/)
- [雑誌『国語学』全文データベース](https://bibdb.ninjal.ac.jp/SJL/)：国語学系の論文検索DB
- [e-Gov](https://www.e-gov.go.jp/)：政府文章や国際機関での言葉の定義を確認可能。

#### ④ 理系
- [理科自由研究データベース](http://sec-db.cf.ocha.ac.jp/)
- [日本学生科学賞](https://event.yomiuri.co.jp/jssa/)
- [JSEC（高校生・高専生科学技術チャレンジ）](https://manabu.asahi.com/jsec/)

### ■ テーマ例（高校生）
- [みんなの探究ライブラリ](https://www.benesse.co.jp/tankyu/event/library/index.html)
- [高等部1年生 発表テーマ一覧](https://www.junten.ed.jp/contents/wp-content/uploads/2022/03/b700dbb307a29fd6e8106d7ced03493d.pdf)

### ■ デザイン作成
- [伝わるデザイン](https://student.tsutawarudesign.com/)

## Assistant

_[tool: list_files]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: list_files]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: list_files]_

_[tool: view_image]_

_[tool: image_metadata]_

I have the full Gakko design system in context — a clean, friendly school system built on a sprout-green/leaf palette with the Futaba mascot. Your brief is detailed and complete, so just a few focused choices before I build:

_[tool: questions_v2]_

## User

Questions answered:
- mascot: ナビやフッターにさりげなく添える
- accent: リーフグリーン基調（デザインシステムに忠実・推奨）
- stats_ui: 両方試してほしい
- tone: その中間
- extras: サイト内検索／絞り込み（カテゴリで絞る）, リンクをお気に入り保存（ローカル保存）, ID/PWのワンクリックコピー, ダークモード切り替え

## Assistant

_[tool: update_todos]_

_[tool: list_files]_

_[tool: copy_files]_

Design context is fully loaded. Building the portal as a single interactive Design Component — leaf-green system, subtle mascot in nav/footer, live search + category filter, localStorage favorites, one-click copy for the login, dark mode, and the stats section in *both* tab and accordion views (toggleable).

_[tool: update_todos]_

## Assistant

_[tool: dc_write]_

_[tool: show_html]_

_[tool: show_html]_

_[tool: sleep]_

_[tool: save_screenshot]_

_[tool: save_screenshot]_

_[tool: show_html]_

_[tool: get_webview_logs]_

Clean load. Let me capture it.

_[tool: save_screenshot]_

_[tool: sleep]_

_[tool: save_screenshot]_

Preview capture isn't cooperating on my side; the load is clean. Let me hand off to verification.

_[tool: update_todos]_

_[tool: ready_for_verification]_

完成しました。Gakko デザインシステム（リーフグリーン基調・双葉マスコット）で、探究学習ポータルを単一のシングルページとして構築しました。

- **ヒーロー＋最重要原則バナー** — 「一次情報にあたる」を高コントラストのカードで強調
- **固定ナビ** — 検索（即時絞り込み）、カテゴリチップ、★お気に入り、ダークモード切替
- **カード型リンク** — ふわっと浮き上がるホバー、★でローカル保存（お気に入りだけ表示も可）
- **朝日けんさくくん** — ID/PW をワンクリックコピー＋ログアウト注意書きをアラートカードで
- **統計データ** — タブ表示／アコーディオン表示をトグルで切替（両方搭載）

リンクはダミーを足さず、提供データのみで構成しています。バックグラウンドで表示確認が走っています。次のステップ候補：セクション見出しのアイコン追加、スマホ幅での詰めの調整など、ご希望あれば対応します。

## User

Found issues — fixing…

## Assistant

_[tool: dc_html_str_replace]_

Fixed — the root now uses `background-color` so the dark-mode token change applies.

_[tool: ready_for_verification]_

ダークモードの背景が切り替わらない不具合を修正しました（ルート要素を `background-color` に変更）。これでライト／ダーク両方が正しくフェード切替されます。

## User

パスワードが変わっていました。34a82vbsmyが正しいパスワードです。# 各サイトのロゴや色分けなどできればお願い。# ほかに使えそうなサイトがあれば順次足していって。

