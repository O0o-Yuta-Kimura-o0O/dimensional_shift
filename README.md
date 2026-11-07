# Dimensional Shift

0除算を集合値の商として扱い、解集合の次元変化を記述する日本語論文の原稿・PDF・改稿履歴を管理するプロジェクトです。

著者：**木村祐太・GPT-6 Astra（AI）**

- [最新の論文PDF](output/current/dimensional_shift.pdf)
- [編集用Typst原稿](output/current/dimensional_shift.typ)
- [変更履歴](output/CHANGELOG.md)
- [出力フォルダと改稿手順](output/README.md)
- [原メモからの整理方針](output/reference/editorial_decisions.md)

GitHub同期先：[O0o-Yuta-Kimura-o0O/dimensional_shift](https://github.com/O0o-Yuta-Kimura-o0O/dimensional_shift)（非公開）。

## 管理する内容

```text
origin/                         受領した原メモ（変更せず保存）
output/
  current/                      最新の編集用原稿とPDF
  history/<version>/            確定版の原稿・PDF・metadata.json
  reference/                    原メモの保存用コピーと編集方針
  CHANGELOG.md                  版ごとの変更内容
scripts/                        組版と版保存の補助スクリプト
```

`output/current/` は改稿の作業対象です。確定した版は `output/history/` に保存し、過去の版を上書きしません。Gitのコミット履歴に加えて、各保存版の `metadata.json` にファイルのSHA-256・バイト数・作成時刻・版番号を記録します。

GitHubへの同期は、確認済みの変更をコミットしてpushする運用です。ファイルの変更を監視して常時自動同期する設定は含みません。
