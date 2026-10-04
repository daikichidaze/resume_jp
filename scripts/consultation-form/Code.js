/**
 * 30分オンライン相談の申込フォームを作成する。
 * Apps Script エディタで createConsultationForm を1回実行する。
 * 再実行しても新しいフォームは作らず、既存フォームのURLを表示する。
 */
const CONSULTATION_ACCOUNT = 'dkch.yoshioka.t@gmail.com';
const FORM_ID_KEY = 'ADVISORY_CONSULTATION_FORM_ID';

function createConsultationForm() {
  if (Session.getEffectiveUser().getEmail() !== CONSULTATION_ACCOUNT) {
    throw new Error(CONSULTATION_ACCOUNT + ' でログインして実行してください。');
  }
  const properties = PropertiesService.getScriptProperties();
  const existingId = properties.getProperty(FORM_ID_KEY);
  if (existingId) {
    return logLinks_(FormApp.openById(existingId));
  }

  const form = FormApp.create('AI・データ活用｜30分のオンライン相談', false);
  // 途中で失敗しても重複作成しないよう、先にIDを保存する。
  properties.setProperty(FORM_ID_KEY, form.getId());

  form.setDescription(
    '吉岡拓真への相談申込みです。オンラインで30分、相談料はかかりません。\n' +
    'テーマが決まっていなくても構いません。\n\n' +
    '送信後、メールで日程調整のご連絡をします。機密情報は記載しないでください。'
  );
  form.setConfirmationMessage(
    'お申込みを受け付けました。吉岡拓真より、メールで日程調整のご連絡をします。'
  );
  form.setShowLinkToRespondAgain(false);

  form.addTextItem().setTitle('お名前').setRequired(true);
  form.addTextItem().setTitle('会社名').setRequired(true);
  form.addTextItem().setTitle('メールアドレス').setRequired(true)
    .setValidation(FormApp.createTextValidation().requireTextIsEmail()
      .setHelpText('メールアドレスの形式で入力してください。').build());
  form.addCheckboxItem().setTitle('相談したいこと（複数選択可）')
    .setChoiceValues([
      'ベンダーのAI提案の確認',
      '試験導入の進め方・結果',
      '事業・業務でのAIの活かし方',
      '社内での進め方・利用ルール',
      'まだ決まっていない'
    ]);
  form.addParagraphTextItem().setTitle('現在の状況・希望日時（任意）')
    .setHelpText('箇条書きで構いません。希望日時があれば日本時間でご記入ください。');

  form.setPublished(true);
  form.setAcceptingResponses(true);
  return logLinks_(form);
}

function logLinks_(form) {
  console.log('編集URL: ' + form.getEditUrl());
  console.log('申込URL（LPのcontact_urlに設定）: ' + form.getPublishedUrl());
  return form.getPublishedUrl();
}
