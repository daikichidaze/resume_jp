from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUTPUT = 'dist/職務経歴書_吉岡拓真.docx'

def set_font(run, size=10.5, bold=False):
    run.font.name = 'Aptos'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Yu Gothic')
    run.font.size = Pt(size)
    run.bold = bold

def set_cell_shading(cell, fill):
    props = cell._tc.get_or_add_tcPr()
    shade = OxmlElement('w:shd')
    shade.set(qn('w:fill'), fill)
    props.append(shade)

def keep_row_together(row):
    props = row._tr.get_or_add_trPr()
    cant_split = OxmlElement('w:cantSplit')
    props.append(cant_split)

def repeat_table_header(row):
    props = row._tr.get_or_add_trPr()
    repeat = OxmlElement('w:tblHeader')
    repeat.set(qn('w:val'), 'true')
    props.append(repeat)

def paragraph(doc, text='', style=None, before=0, after=3, bold=False):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text)
    set_font(r, 10.5, bold)
    return p

def bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(1)
    set_font(p.add_run(text))

def table(doc, headers, rows, widths):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = 'Table Grid'
    tbl.autofit = False
    header = tbl.rows[0]
    repeat_table_header(header)
    for i, value in enumerate(headers):
        cell = header.cells[i]
        cell.width = Cm(widths[i])
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_shading(cell, 'D9E2F3')
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(p.add_run(value), 9, True)
    for values in rows:
        cells = tbl.add_row().cells
        keep_row_together(tbl.rows[-1])
        for i, value in enumerate(values):
            cell = cells[i]
            cell.width = Cm(widths[i])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            set_font(p.add_run(value), 8.3)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return tbl

def project(doc, title, period, role, bullets):
    paragraph(doc, title, style='Heading 2', before=8, after=2)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run('期間・体制：')
    set_font(r, 10, True)
    set_font(p.add_run(period), 10)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run('役割：')
    set_font(r, 10, True)
    set_font(p.add_run(role), 10)
    for item in bullets:
        bullet(doc, item)

doc = Document()
sec = doc.sections[0]
sec.top_margin = Cm(1.5); sec.bottom_margin = Cm(1.5)
sec.left_margin = Cm(1.45); sec.right_margin = Cm(1.45)

styles = doc.styles
styles['Normal'].font.name = 'Aptos'
styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), 'Yu Gothic')
styles['Normal'].font.size = Pt(10.5)
for name, size in [('Title', 18), ('Heading 1', 13.5), ('Heading 2', 11.5)]:
    styles[name].font.name = 'Aptos'
    styles[name]._element.rPr.rFonts.set(qn('w:eastAsia'), 'Yu Gothic')
    styles[name].font.size = Pt(size)
    styles[name].font.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(2)
set_font(p.add_run('職務経歴書'), 18, True)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
set_font(p.add_run('吉岡 拓真'), 12, True)
paragraph(doc, 'AI/DXコンサルタント・新規事業開発\nデジタル/データを活用した事業・業務変革支援', after=4, bold=True)
p = paragraph(doc, '曖昧な事業コンセプト・業務課題を、実行可能な要件/システム/運用に落とし込む', after=6, bold=True)
p.paragraph_format.left_indent = Cm(.4)

paragraph(doc, '提供価値', style='Heading 1', before=4, after=3)
for text in [
    '経営/事業側の構想を整理する：目的、実現方法、判断軸、KPIを明確化し、合意形成できる形にする',
    '業務とシステムを接続する：業務フロー、必要データ、システム要件、運用設計に落とし込み、実行可能な計画へ変換する',
    'DX/AI導入を現実的に進める：技術ありきではなくビジネス課題を起点に、PoC、本番化、内製化/外部活用の進め方を設計する',
    'プロジェクトを推進する：関係者調整、提案、要件定義、開発チーム連携、デリバリーを担う',
    '多文化環境で橋渡しする：日本人マネージャー、現地メンバー、海外開発チームの間で認識を揃え、実行を支える']:
    bullet(doc, text)

paragraph(doc, '専門領域', style='Heading 1', before=5, after=3)
table(doc, ['領域', '支援内容'], [
    ('システム/DXコンサルティング', '業務課題の整理、改善テーマの優先順位付け、システム企画、要件定義、導入計画の策定'),
    ('AI/生成AI導入支援', '目的整理、AI活用ユースケース設計、業務プロセスへの組み込み、エージェント開発'),
    ('プロジェクトマネジメント', '提案から要件定義、開発推進、ステークホルダー調整、進捗/課題/リスク管理までの推進'),
    ('プロダクト/新規事業企画', '価値仮説、対象顧客、ユースケース、提供プロセス、KPIを整理し、サービス化まで支援'),
    ('データ活用/意思決定支援', 'データ取得設計、分析観点、可視化、ダッシュボード、機械学習、シミュレーションの設計'),
    ('数理最適化/OR', '複雑な業務・現実世界をモデル化し、施策比較や意思決定を支援'),
    ('開発・技術理解', 'Python、SQL、クラウド、No Code、AI駆動開発を理解し、事業側と開発側の橋渡しを行う')], [5.0, 13.7])

paragraph(doc, '職務経歴', style='Heading 1', before=5, after=3)
table(doc, ['期間', '会社・役割', '雇用形態・職務内容'], [
    ('2025年〜現在', '株式会社 AI Training\nAIコンサルタント、事業開発', '業務委託\nAIエージェント導入支援サービスの企画、研修設計、共同実装、導入コンサルティング'),
    ('2024年〜2026年', 'ISS Resolution Ltd.\nDigital Solutions Strategy Consultant', '契約社員（TOYOTA TSUSHO SYSTEMS向け）\nデジタルソリューション投資判断支援、新規サービス企画、提案整理、ITコンサルモデルへの転換推進'),
    ('2024年', '株式会社データラーニング\n生成AI研修の開発・コンテンツディレクター', '業務委託\n企業向けリスキリング講座のコンテンツ制作・デリバリー'),
    ('2019年〜2024年', 'TOYOTA TSUSHO SYSTEMS (THAILAND) Co., Ltd.\nHead of Digital Solutions & New Business', '正社員／Business Development Group Leader（課長級）\n新規事業企画部を立ち上げ（1→5名）。構想整理〜提案〜要件定義〜開発推進を担当'),
    ('2021年〜2023年', 'Flare (Thailand) Co., Ltd.\nAIエンジニア', '業務委託\nスマホセンサーデータによる運転挙動検出のアルゴリズム開発、越境リモート開発を推進'),
    ('2021年〜2024年', '株式会社データラーニング\nデータサイエンススクールメンター', '業務委託\n1:1での学習支援とキャリア伴走（20名強）'),
    ('2016年〜2019年', '株式会社構造計画研究所\n数理最適化エンジニア', '正社員\n数理最適化・シミュレーション・データ分析。PLとして20件規模を並行推進')], [3.0, 7.3, 8.4])

paragraph(doc, '実績ハイライト', style='Heading 1', before=5, after=3)
table(doc, ['案件', '役割', '技術/テーマ', '成果'], [
    ('デジタルソリューション戦略と新規事業立ち上げ＠タイ', '部門立ち上げリーダー\n企画・要件定義・PM・事業開発', '組織設計 / 新規事業 / Web開発 / AWS', '新規/受託10件に展開し、累計20M+ THBを創出'),
    ('豊田通商＠タイにおけるDX推進組織の立ち上げ', '立ち上げリーダー\n提案支援・企画/要件定義・業務標準化', 'DX企画 / ワークショップ設計 / 業務標準化', '4つの支援メニューを整備し、年間平均15プロジェクトを推進する体制を構築'),
    ('AIエージェント導入支援事業の推進', '事業開発リード\n構想設計・提案設計・導入コンサル', 'Claude Code / Agent Skills / 仕様駆動開発', '企業向け研修・共同実装・運用伴走の提供モデルを整備し、年間売上1000万円規模'),
    ('MaaS企画検証のためのシミュレーター開発', 'PM / データサイエンティスト / ソフトウェアエンジニア', 'Python / simpy / 組合せ最適化 / シミュレーション', '40M JPY規模で新サービス要件の事前検証基盤を構築し、意思決定精度を向上'),
    ('スマートフォンGPS/センサーデータを活用した運転挙動評価アルゴリズムの開発', 'テックリード兼PM\n技術提案・評価設計・デリバリー管理', 'Python / GPS・慣性センサー / FastAPI', 'センサーデータ活用アルゴリズムを実装し、CTO向け技術提案と越境開発運用を定着')], [4.4, 4.3, 4.5, 5.5])

paragraph(doc, '主要プロジェクト', style='Heading 1', before=5, after=2)
project(doc, '1. デジタルソリューション戦略と新規事業立ち上げ＠タイ', '2019年〜2022年、最大5名のクロスファンクショナルチーム', '部門立ち上げリーダー（価値仮説設計・サービス企画・要件定義・PM・事業開発）', [
    '対象顧客、ユースケース、提供価値、判断軸を整理し、事業として説明できる形に構造化',
    '業務フロー、必要データ、KPI、システム要件を設計し、提案から開発までの共通フォーマットを整備',
    'bubble.ioなどでプロトタイプを提示し、企画から実装まで一気通貫で推進',
    'デジタル活用テーマを新規/受託10件に展開、累計20M+ THBを創出'])
project(doc, '2. 豊田通商＠タイにおけるDX推進組織の立ち上げ', '2022年〜2024年、IT子会社からの逆提案で立ち上げ、4人体制へ拡大', '立ち上げリーダー（提案支援・企画/要件定義・業務標準化）', [
    '各事業部の業務課題を整理し、データ/システム活用案として提案できる支援メニューを定義',
    '常設相談窓口、プロジェクト創出ワークショップ、e-learning、啓蒙イベントを企画・運営',
    '4つの標準化された支援メニューを定着させ、年間平均15プロジェクトを推進する体制を構築'])
project(doc, '3. AIエージェント導入支援事業の推進', '2024年〜現在、小規模チーム', '事業開発リード（構想設計・提案設計・プロダクト企画/開発・導入コンサル）', [
    '価値仮説を「効率化」から「スケーラビリティ拡張」へ再定義し、対象業務ごとのユースケースと導入判断軸を設計',
    '企業向け研修、Agent Skills共同実装、運用伴走を組み合わせた3フェーズの支援メニューを設計',
    'データサイエンティスト・マッチングプラットフォームで設計期間を約3か月から1か月に短縮',
    '企業向け研修・導入支援の提供基盤を整備し、年間売上1000万円規模に拡大'])
project(doc, '4. MaaS企画検証のためのシミュレーター開発', '2016年〜2019年、3〜4名チーム、総額40M JPY規模', 'PM / データサイエンティスト / ソフトウェアエンジニア（要件定義〜設計〜実装〜分析）', [
    'サービス仮説をユースケース、需要想定、評価指標に分解し、意思決定ポイントとデータ取得定義を設計',
    '組合せ最適化とシミュレーション条件を設計・実装し、代替案を比較可能な形にした',
    '40M JPY規模プロジェクトで新サービス要件の事前検証基盤を構築し、意思決定精度を向上'])
project(doc, '5. スマートフォンGPS/センサーデータを活用した運転挙動評価アルゴリズムの開発', '2021年〜2023年、日本/ベトナムの2拠点クロスボーダー体制（フルリモート・パートタイム）', 'テクニカルリード兼プロジェクトマネージャー（技術提案・評価設計・デリバリー管理）', [
    'GPS/慣性センサーデータの取得条件と評価観点を整理し、イベント検知アルゴリズムを設計・実装',
    '非同期ワークフローとコードレビュー運用を定着させ、越境開発体制を安定化',
    '運転挙動イベント検知・運転トリップ安全性評価アルゴリズムを新規リリース'])

paragraph(doc, '技術スタック', style='Heading 1', before=6, after=3)
table(doc, ['カテゴリ', '項目', '主な用途/役割'], [
    ('開発言語', 'Python / SQL / C# / Go / TypeScript', 'データ分析、自動化、バックエンド、アルゴリズム、Web開発'),
    ('データ分析・機械学習', 'pandas / Jupyter / seaborn / matplotlib / scikit-learn / Power BI', '分析、可視化、機械学習、ダッシュボード構築'),
    ('最適化・シミュレーション', 'PuLP / simpy', '組合せ最適化、イベントドリブンシミュレーション'),
    ('クラウド', 'AWS / GCP / Azure', 'データ分析基盤、PaaS活用、クラウド活用方針整理'),
    ('AI駆動開発', 'Claude Code / Codex', 'AIエージェント導入設計、開発支援、仕様駆動開発')], [4.0, 7.7, 7.0])

paragraph(doc, '資格・語学', style='Heading 1', before=5, after=3)
for value in ['AWS Certified Developer - Associate（2023）', '技術士補（経営工学）（2017）', '応用情報技術者（2016）', '日本語：ネイティブ / 英語：ビジネス']:
    bullet(doc, value)
paragraph(doc, '学歴', style='Heading 1', before=5, after=3)
for value in ['首都大学東京大学院 理工学研究科 分子物質化学専攻 修士（2016）', '首都大学東京 理学部 化学科 学士（2014）']:
    bullet(doc, value)

doc.core_properties.title = '職務経歴書 - 吉岡 拓真'
doc.core_properties.author = '吉岡 拓真'
doc.save(OUTPUT)
print(OUTPUT)
