# プロジェクトの変更履歴

論文本文の改訂は [output/CHANGELOG.md](output/CHANGELOG.md)、ビジュアライザーの改訂は [visualizer/CHANGELOG.md](visualizer/CHANGELOG.md) に記録します。

## 2026-11-07 — 閲覧操作と論文の入口を整備

- ビジュアライザー v0.2.0 に、ドラッグ回転・ホイール拡大縮小・視点の初期化を追加。
- 最上位に `paper/README.md` を追加し、日英のPDF・Markdown・保存版・編集手順をまとめた。
- ルートREADMEを「論文」「ビジュアライザー」「対話記録」の入口として整理した。
- 原稿の基準位置 `output/current/` と確定版 `output/history/` は維持。論文の内容・版番号・原資料は変更していない。
- 版番号を共通設定から読み込むようビジュアライザーの書き出し処理を更新し、表示名と公開メタデータのずれを防ぐ。
