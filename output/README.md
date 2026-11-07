# 論文の出力と履歴

著者：木村祐太・GPT-6 Astra（AI）

## フォルダの役割

| パス | 内容 | 更新方法 |
|---|---|---|
| `current/dimensional_shift.typ` | 最新の編集用原稿 | 改稿時に編集 |
| `current/dimensional_shift.pdf` | 最新の組版PDF | 原稿から再生成 |
| `history/<version>/` | 確定版の原稿・PDF・メタデータ | 新しい版を追加。既存版は上書きしない |
| `reference/dimensional_shift_01_original.txt` | 受領した原メモの保存用コピー | 変更しない |
| `reference/editorial_decisions.md` | 原メモからの整理方針 | 方針変更時に記録 |
| `CHANGELOG.md` | 各版の変更理由と内容 | 版を確定するたびに追記 |

## 改稿の手順

組版には Python 3.9以上、`requirements-build.txt` に記したTypstライブラリ、日本語フォントを使います。macOSでは「ヒラギノ明朝 ProN」「Hiragino Sans」、その他の環境では「Noto Serif CJK JP」「Noto Sans CJK JP」を用意してください。

```bash
python3 -m pip install -r requirements-build.txt
python3 scripts/build_paper.py --preview-dir tmp/pdfs/review
```

`--preview-dir` を指定すると、PDFと同じ原稿から全ページの確認用PNGを生成します。中間画像はGit管理の対象外です。

以下のコマンドはリポジトリのルートで実行します。

1. `current/dimensional_shift.typ` を編集し、原稿内の版番号・日付も更新します。
2. `python3 scripts/build_paper.py` でPDFを再生成します。組版に必要な環境は同スクリプトの案内に従います。
3. PDFの全ページを確認し、数式・日本語・改ページ・参考文献を検査します。
4. `output/CHANGELOG.md` に変更内容と理由を記録します。
5. 新しい版番号を使い、確定版を保存します。

   ```bash
   python3 scripts/snapshot.py --version v0.1.1 --summary '変更内容を簡潔に記述'
   ```

6. 差分を確認し、対象ファイルを明示してGitに記録します。

   ```bash
   git diff --check
   git status --short
   git add output/current output/history/v0.1.1 output/CHANGELOG.md
   git commit -m 'Revise paper to v0.1.1'
   git push origin main
   ```

原稿以外も変更した場合は、そのファイルも確認したうえで追加します。共有先に新しいコミットがある場合は、内容を取り込んでからpushします。過去の履歴を上書きするforce pushは通常の運用に含みません。

## 版番号と検証情報

初版は `v0.1.0`（2026-11-07）です。文章や誤記の修正では末尾の番号、定義・主張・構成の変更では必要に応じて中位の番号を進めます。版番号は原稿・変更履歴・保存先でそろえます。

`scripts/snapshot.py` は、原稿とPDFの存在、PDFのヘッダー、原メモと保存用コピーの一致を確認します。`metadata.json` は版番号、JSTの保存時刻、変更概要、著者、各ファイルのSHA-256とバイト数、原メモのSHA-256を含みます。PDFの数学的な正しさや組版品質は、このスクリプトでは判定しません。

保存処理は一時ディレクトリでコピーとメタデータを完成させてから、版ディレクトリへ移します。既存の版番号を指定すると失敗します。修正が必要な場合は新しい版を作成してください。
