# Dimensional Shift

0除算を集合値の商として扱い、新しい独立座標の生成と解集合の次元変化を記述する論文の原稿・成果物・改稿履歴を管理するプロジェクトです。日本語版を基準とし、同じ定義・命題・例を英語版にも反映します。

著者：**木村祐太・GPT-6 Astra（AI）**

| 言語 | PDF | Markdown | 編集用Typst原稿 |
|---|---|---|---|
| 日本語 | [PDF](output/current/dimensional_shift.pdf) | [Markdown](output/current/dimensional_shift.md) | [Typst](output/current/dimensional_shift.typ) |
| English | [PDF](output/current/dimensional_shift_en.pdf) | [Markdown](output/current/dimensional_shift_en.md) | [Typst](output/current/dimensional_shift_en.typ) |

- [変更履歴](output/CHANGELOG.md)
- [出力フォルダと改稿手順](output/README.md)
- [原メモからの整理方針](output/reference/editorial_decisions.md)
- [対話記録と論文版の対応](output/discussion/README.md)
- [独立座標生成のビジュアライザー](output/visualizer.md)（対応論文 v0.2.0、最新版のみ配信）

GitHub公開先：[O0o-Yuta-Kimura-o0O/dimensional_shift](https://github.com/O0o-Yuta-Kimura-o0O/dimensional_shift)。公開確認の状態と対話の収録範囲は [対話記録の案内](output/discussion/README.md) に記します。

## 管理する内容

```text
origin/                         受領した原メモ（変更せず保存）
output/
  current/                      日英Typst・PDF・Markdownと共通設定・数式辞書
  history/<version>/            確定版の成果物・設定・metadata.json
  discussion/                   取得範囲・編集箇所を明示した対話記録・版対応表
  reference/                    原メモの保存用コピーと編集方針
  CHANGELOG.md                  版ごとの変更内容
scripts/                        組版と版保存の補助スクリプト
visualizer/                     Lの表示ソース・検証コード（history/ の保存版はローカルのみ）
```

`output/current/` は改稿の作業対象です。PDFとMarkdownは各言語のTypst原稿から生成し、共通の数式辞書を使います。Markdownを直接編集しません。日英間の意味の一致は原稿レビューで確認します。

確定した版は `output/history/` に保存し、過去の版を上書きしません。Gitのコミット履歴に加えて、各保存版の `metadata.json` にファイルのSHA-256・バイト数・言語・形式・作成時刻・版番号を記録します。組版を再現するときは、対応するGitタグをチェックアウトして共通スクリプトとスタイルも復元します。

GitHubへの同期は、確認済みの変更をコミットしてpushする運用です。ファイルの変更を監視して常時自動同期する設定は含みません。

対話記録は `output/discussion/transcript-2026-11-07.md`、構造化データは対応するJSONに保存しています。取得可能なユーザー・アシスタントの表示発言を収録し、ローカルパス等の編集を明示します。内部推論・ツール実行記録・システム指示は含めません。`version_map.json` の話題要約は記録本文と区別します。

ビジュアライザーは [公開サイト](https://dimensional-shift-l-visualizer.yummy-pig-6822.chatgpt.site) で最新版だけを配信します。旧版の保存用スナップショットはローカルに保持します。ユーザーの指定により、ソースのGit履歴と過去コードは公開します。論文の保存版は従来どおり公開リポジトリに残します。
