# 職務経歴書（日本語）

このリポジトリは、吉岡拓真の日本語版職務経歴書を GitHub Pages で公開するためのものです。

- 公開サイト（日本語）: https://daikichidaze.github.io/resume_jp/
- 英語版: https://daikichidaze.github.io/resume/

## 構成

- `index.md`: 公開される職務経歴書本体
- `_config.yml`: GitHub Pages（Jekyll）の設定
- `advisory/index.md`: AI / DataアドバイザリーLPの下書き
- `_layouts/advisory.html`: LP専用レイアウト
- `assets/css/advisory.scss`: LP専用スタイル

## 更新方法

1. `index.md` を編集
2. 変更をコミットして push
3. GitHub Pages に反映

## ローカルで確認（任意）

### Docker Compose を使う

Docker と Compose plugin がある環境で以下を実行します。

```bash
docker compose up
```

ブラウザで `http://localhost:4000` を開いて確認できます。
LPの下書きは `http://localhost:4000/advisory/` で確認できます。
Docker Composeは `_config.local.yml` を追加して下書き表示を有効にします。
設定ファイルを変更した場合は `docker compose restart` で再起動してください。

### Ruby で直接実行する

Ruby と Bundler がある環境で以下を実行します。

```bash
bundle install
bundle exec jekyll serve
```

LPの下書きも表示する場合は、以下を使用します。

```bash
bundle exec jekyll serve --config _config.yml,_config.local.yml
```

通常のビルドでは `published: false` のLPは生成されません。
GitHub Pagesでは `_config.local.yml` を読み込まないでください。

### アドバイザリーLPの相談フォーム接続

LPの本文・図解は `advisory/index.md`、スタイルは `assets/css/advisory.scss` にあります。
相談申込みはGoogleフォームで受け付け、そのURLをLPのfront matterの `contact_url` に設定しています。
ヘッダー・ヒーロー・相談欄のボタンは、このURLを新しいタブで開きます。
フォームの内容と作成手順は `scripts/consultation-form-setup.md` を参照してください。

`contact_url` が空の間は、ボタンは相談欄へのページ内リンクになり、相談欄には受付準備中の案内を表示します。
フォームの入力・送信・完了まで確認してから `published: true` に変更してください。
通常ビルドでの表示、サイトのbaseurl、相談ボタンの遷移先を確認して公開します。
プレビュー中は `noindex, nofollow` が付与されます。

## PDF 出力

ローカルプレビューを `http://localhost:4000` で起動した状態で、以下を実行します。

```bash
node scripts/export_single_page_pdf.mjs http://localhost:4000 dist/takuma-yoshioka.pdf
```

1枚の長いPDFとして出力したい場合は `--single-page` を付けます。

```bash
node scripts/export_single_page_pdf.mjs --single-page http://localhost:4000 dist/resume-long.pdf
```

このスクリプトは Chromium で PDF を出力した後、Ghostscript (`gs`) が使える環境では `/ebook` 設定で再圧縮します。最終サイズは標準出力に表示され、`1,000,000 bytes` を超える場合は警告を出します。
