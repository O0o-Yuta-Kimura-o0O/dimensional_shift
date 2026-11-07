# 論文の出力と履歴

著者：木村祐太・GPT-6 Astra（AI）

論文を読む場合は **[paper/ の閲覧入口](../paper/README.md)** から日英のPDF・Markdownへ進めます。このフォルダは原稿・生成物・確定版を管理する場所です。

## フォルダの役割

| パス | 内容 | 更新方法 |
|---|---|---|
| `current/dimensional_shift.typ` | 日本語の基準原稿 | 改稿時に編集 |
| `current/dimensional_shift_en.typ` | 対応する英語原稿 | 日本語版と同時に更新 |
| `current/dimensional_shift{,_en}.pdf` | 日英の組版PDF | 各言語の原稿から再生成 |
| `current/dimensional_shift{,_en}.md` | 日英のMarkdown | エクスポーターで生成。直接編集しない |
| `current/paper_config.json` | 共通の版番号・日付・著者など | 改訂時に更新 |
| `current/equations.json` | Typst/Markdown共通の数式辞書 | 数式の変更時に更新 |
| `history/<version>/` | 確定版の成果物・設定・メタデータ | 新しい版を追加。既存版は上書きしない |
| `discussion/` | 取得範囲を明示した対話記録と版対応表 | 対応する版や方針が変わるときに更新 |
| `reference/dimensional_shift_01_original.txt` | 受領した原メモの保存用コピー | 変更しない |
| `reference/editorial_decisions.md` | 原メモからの整理方針 | 方針変更時に記録 |
| `CHANGELOG.md` | 各版の変更理由と内容 | 版を確定するたびに追記 |

## 改稿の手順

組版には Python 3.9以上、`requirements-build.txt` に記したTypstライブラリ、日本語フォントを使います。macOSでは「ヒラギノ明朝 ProN」「Hiragino Sans」、その他の環境では「Noto Serif CJK JP」「Noto Sans CJK JP」を用意してください。

```bash
python3 -m pip install -r requirements-build.txt
python3 scripts/build_paper.py --preview-dir tmp/pdfs/review
```

ビルドは最初に `scripts/export_markdown.py` の `export_all(ROOT)` を呼び、日英のMarkdownを生成します。その後、両言語のPDFを組版します。`--preview-dir` を指定すると、同じ原稿から全ページの確認用PNGを `ja/` と `en/` のサブフォルダに生成します。中間画像はGit管理の対象外です。

以下のコマンドはリポジトリのルートで実行します。

1. 日本語Typst原稿を編集し、英語Typst原稿の定義・仮定・命題・証明・例も対応させます。数式の変更は `current/equations.json` に反映し、本文から `#m("id")`（インライン）または `#eq("id")`（独立表示）で参照します。
2. `current/paper_config.json` の版番号・日付を更新し、`python3 scripts/build_paper.py --preview-dir tmp/pdfs/review` でMarkdownとPDFを再生成します。
3. 日英PDFの全ページを確認し、数式・文字・改ページ・参考文献を検査します。両Markdownの内容、数式、見出しも確認し、各言語のPDFと意味が一致することを確かめます。日英間の意味の一致も別途確認します。
4. `output/CHANGELOG.md` に変更内容と理由を記録し、`output/discussion/version_map.json` に該当版と話題の対応を追加します。対話を未書き出しの場合は、その状態を維持して明記します。
5. 新しい版番号を使い、確定版を保存します。

   ```bash
   python3 scripts/snapshot.py --version v0.2.2 --summary '変更内容を簡潔に記述'
   ```

6. 差分を確認し、対象ファイルを明示してGitに記録します。

   ```bash
   git diff --check
   git status --short
   git add output/current output/history/v0.2.2 output/CHANGELOG.md output/discussion/version_map.json
   git commit -m 'Revise paper to v0.2.2'
   git tag -a v0.2.2 -m 'Paper v0.2.2'
   git push origin main
   git push origin v0.2.2
   ```

原稿以外も変更した場合は、そのファイルも確認したうえで追加します。共有先に新しいコミットがある場合は、内容を取り込んでからpushします。過去の履歴を上書きするforce pushは通常の運用に含みません。

## 版番号と検証情報

初版は `v0.1.0`、日英・PDF/Markdown対応版は `v0.2.0`、題名と要旨を整えた最新版は `v0.2.1`（いずれも2026-11-07）です。文章や誤記の修正では末尾の番号、定義・主張・構成の変更では必要に応じて中位の番号を進めます。版番号は共通設定・変更履歴・保存先・Gitタグでそろえます。

`scripts/snapshot.py` は日英のTypst・PDF・Markdown、共通設定、数式辞書の8ファイルを保存します。版対応表がある場合は `discussion/version_map.json` として同じ保存版にコピーします。共通設定との版番号一致、各ファイルの存在、両PDFのヘッダー、原メモと保存用コピーの一致を確認します。

`metadata.json` は版番号、JSTの保存時刻、変更概要、著者、各ファイルの言語・形式・SHA-256・バイト数、原メモのSHA-256を含みます。数学的な正しさ、日英翻訳の正確さ、PDFの組版品質は、このスクリプトでは判定しません。旧版の保存内容は、その版の時点の形式のまま維持します。

保存処理は一時ディレクトリでコピーとメタデータを完成させてから、版ディレクトリへ移します。既存の版番号を指定すると失敗します。修正が必要な場合は新しい版を作成してください。

## 保存版の再組版

保存版のPDFとMarkdownは直接閲覧できます。Typst原稿は共通のスタイルや数式処理をリポジトリ内の絶対ルートから参照するため、`history/` のコピーだけを単独で組版する運用は用意していません。対応するGitタグを別の作業ツリーなどでチェックアウトし、そのタグの `output/current/` と `scripts/` を使って再組版します。

## 対話記録の扱い

`discussion/README.md` に対話の収録範囲・編集方針・公開確認状態を記します。`transcript-2026-11-07.md` と対応するJSONが記録本文です。`version_map.json` は話題要約と版の索引であり、全文記録ではありません。ビジュアライザーの最新版へのリンクは `visualizer.md` にあります。
