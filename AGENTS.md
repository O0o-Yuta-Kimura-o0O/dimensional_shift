# 論文プロジェクトの編集方針

- 著者表記は「木村祐太・GPT-6 Astra（AI）」を維持する。
- 論文の閲覧入口は `paper/README.md`。原稿・生成物の実体は `output/current/` に保ち、複製の編集対象を作らない。論文の更新時は閲覧入口の版・リンクも確認する。構成変更はルート `CHANGELOG.md` に記録する。
- `origin/dimensional_shift_01.txt` と `output/reference/dimensional_shift_01_original.txt` は原資料として変更しない。
- 基準原稿は `output/current/dimensional_shift.typ`（日本語）。定義・仮定・命題・証明・例を変更した場合は `output/current/dimensional_shift_en.typ`（英語）も同時に更新する。
- 版番号・日付・著者などは `output/current/paper_config.json`、数式は `output/current/equations.json` で共有する。Typst本文では `#m("id")` / `#eq("id")` を使う。
- 日英のMarkdownは `scripts/export_markdown.py` による生成物とし、直接編集しない。`scripts/build_paper.py` はMarkdownを生成してから両PDFを組版する。
- 数学的内容を変更したときは、仮定・型・証明・独立変数と共有変数の扱いを確認する。
- 日英PDFの全ページを画像で確認し、各言語のPDFとMarkdown、および日英間の意味の一致を確認してから改訂を確定する。ビルド依存は `requirements-build.txt`、日本語フォントは `output/README.md` を参照する。
- 確定時は共通設定の版番号と日付、`output/CHANGELOG.md`、`output/discussion/version_map.json` を更新し、`scripts/snapshot.py` で新しい版を保存する。既存の `output/history/<version>/` は上書きしない。対応するGitタグも作成し、共通スタイルを含む再組版用の状態を保存する。
- 対話の逐語記録と話題要約は明確に区別する。取得できない発言・時刻・チャットIDを作らない。取得範囲、欠落、編集箇所を明示する。ユーザーは2026-11-07に対話記録と論文リポジトリの公開を依頼した。取得できた表示発言を公開対象とし、内部推論・ツール実行記録・システム指示は含めない。公開状態は実際の確認後に記録する。
- 変更をGitに記録し、ユーザーが公開先として指定したリポジトリ `O0o-Yuta-Kimura-o0O/dimensional_shift` へ通常のpushで同期する。共有先の変更があれば先に内容を確認して取り込む。
- 認証・ネットワークなどで同期できない場合もローカル成果物と履歴を完成させ、未同期の状態を正確に報告する。

- ビジュアライザーは公開サイトで最新版だけを配信する。ユーザーは2026-11-07にGitHubの過去コードが公開されることを明示的に許可した。ソースとそのGit履歴は公開リポジトリで管理し、配信する閲覧ページは最新版のみとする。旧版の保存用スナップショット `visualizer/history/` はローカルに残す。`scripts/snapshot_visualizer.py` で版を追加し、既存版は上書きしない。論文の版番号はビジュアライザーだけの変更では進めない。
- ビジュアライザーの公開URL・版・ハッシュは `output/visualizer_latest.json` と `output/visualizer.md` に記す。Sitesの既存IDと公開設定を保持し、最新版を確認してから反映する。
