# 論文プロジェクトの編集方針

- 著者表記は「木村祐太・GPT-6 Astra（AI）」を維持する。
- `origin/dimensional_shift_01.txt` と `output/reference/dimensional_shift_01_original.txt` は原資料として変更しない。
- 基準原稿は `output/current/dimensional_shift.typ`（日本語）。定義・仮定・命題・証明・例を変更した場合は `output/current/dimensional_shift_en.typ`（英語）も同時に更新する。
- 版番号・日付・著者などは `output/current/paper_config.json`、数式は `output/current/equations.json` で共有する。Typst本文では `#m("id")` / `#eq("id")` を使う。
- 日英のMarkdownは `scripts/export_markdown.py` による生成物とし、直接編集しない。`scripts/build_paper.py` はMarkdownを生成してから両PDFを組版する。
- 数学的内容を変更したときは、仮定・型・証明・独立変数と共有変数の扱いを確認する。
- 日英PDFの全ページを画像で確認し、各言語のPDFとMarkdown、および日英間の意味の一致を確認してから改訂を確定する。ビルド依存は `requirements-build.txt`、日本語フォントは `output/README.md` を参照する。
- 確定時は共通設定の版番号と日付、`output/CHANGELOG.md`、`output/discussion/version_map.json` を更新し、`scripts/snapshot.py` で新しい版を保存する。既存の `output/history/<version>/` は上書きしない。対応するGitタグも作成し、共通スタイルを含む再組版用の状態を保存する。
- 対話の逐語記録と話題要約は明確に区別する。取得できない発言・時刻・チャットIDを作らない。取得範囲、欠落、編集箇所を明示する。現在は対話全文のエクスポート・公開を実施していない。将来公開する際は内容と公開先を確定し、機密情報・他者情報を確認する。非公開リポジトリの同期を公開の許可とみなさない。
- 変更をGitに記録し、ユーザーが依頼した非公開リポジトリ `O0o-Yuta-Kimura-o0O/dimensional_shift` へ通常のpushで同期する。共有先の変更があれば先に内容を確認して取り込む。
- 認証・ネットワークなどで同期できない場合もローカル成果物と履歴を完成させ、未同期の状態を正確に報告する。
