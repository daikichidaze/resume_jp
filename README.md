# 職務経歴書（日本語）

このリポジトリは、吉岡拓真の日本語版職務経歴書を GitHub Pages で公開するためのものです。

- 公開サイト（日本語）: https://daikichidaze.github.io/resume_jp/
- 英語版: https://daikichidaze.github.io/resume/

## 構成

- `index.md`: 公開される職務経歴書本体
- `_config.yml`: GitHub Pages（Jekyll）の設定

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

### Ruby で直接実行する

Ruby と Bundler がある環境で以下を実行します。

```bash
bundle install
bundle exec jekyll serve
```

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
