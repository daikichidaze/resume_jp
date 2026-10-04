# 相談申込みフォームの作成

フォームは個人アカウント `dkch.yoshioka.t@gmail.com` 上の Apps Script から作成する。スクリプトは `scripts/consultation-form/`（`Code.js`・`appsscript.json`）。

## フォームの内容（5項目）

| 項目 | 必須 | 形式 |
| --- | --- | --- |
| お名前 | 必須 | 短文 |
| 会社名 | 必須 | 短文 |
| メールアドレス | 必須 | 短文（形式を検証） |
| 相談したいこと | 任意 | 複数選択（LPの相談テーマ4件＋「まだ決まっていない」） |
| 現在の状況・希望日時 | 任意 | 自由記述 |

説明文は「30分・無料・テーマ未定でも可・メールで日程調整・機密情報は書かない」のみ。部署・役職、希望日時の独立項目、「その他」選択肢は置かない（相談の場で聞く）。

## アカウントへ載せる（clasp）

1. 個人アカウントで https://script.google.com/home/usersettings を開き、Google Apps Script API をオンにする。
2. 個人アカウントで clasp にログインする（既定のログインは別アカウントのため、名前付きで追加する）。
   ```bash
   npx @google/clasp login --user personal
   ```
3. プロジェクトを作成して push する。
   ```bash
   cd scripts/consultation-form
   npx @google/clasp create-script --user personal --type standalone --title "Advisory consultation form"
   npx @google/clasp push --user personal --force
   ```
   作成される `.clasp.json` はコミットしない（`.gitignore` 済み）。

## 実行と接続

1. https://script.google.com/ で「Advisory consultation form」を開き、関数 `createConsultationForm` を実行して権限を許可する。
2. 実行ログの **申込URL** を `advisory/index.md` の `contact_url` に設定する。編集URLはLPに載せない。
3. フォームの「回答」で、新しい回答のメール通知を有効にする。
4. 未ログインのブラウザから申込みをテストし、LPの導線を確認してから `published` を切り替える。

再実行しても新しいフォームは作られず、既存フォームのURLが表示される。別プロジェクトに複製して実行すると別のフォームができる。自動返信・カレンダー予約は行わない。
