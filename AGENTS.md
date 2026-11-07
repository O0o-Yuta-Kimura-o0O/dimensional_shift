# 論文プロジェクトの編集方針

- 著者表記は「木村祐太・GPT-6 Astra（AI）」を維持する。
- `origin/dimensional_shift_01.txt` と `output/reference/dimensional_shift_01_original.txt` は原資料として変更しない。
- 編集対象は `output/current/dimensional_shift.typ`。PDFは `scripts/build_paper.py` から再生成する。
- 数学的内容を変更したときは、仮定・型・証明・独立変数と共有変数の扱いを確認する。
- PDFの全ページを画像で確認してから改訂を確定する。ビルド依存は `requirements-build.txt`、日本語フォントは `output/README.md` を参照する。
- 確定時は原稿の版番号と日付、`output/CHANGELOG.md` を更新し、`scripts/snapshot.py` で新しい版を保存する。既存の `output/history/<version>/` は上書きしない。
- 変更をGitに記録し、ユーザーが依頼した非公開リポジトリ `O0o-Yuta-Kimura-o0O/dimensional_shift` へ通常のpushで同期する。共有先の変更があれば先に内容を確認して取り込む。
- 認証・ネットワークなどで同期できない場合もローカル成果物と履歴を完成させ、未同期の状態を正確に報告する。
