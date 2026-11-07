#!/usr/bin/env python3
"""Export only retrieved user and visible assistant messages, with disclosed edits.

The input must be a read_thread result already reduced to its visible messages.
No local session logs, tool outputs, or inferred dialogue are used.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/O0o-Yuta-Kimura-o0O/dimensional_shift"
STEM = "transcript-2026-11-07"
CUTOFF = "01a1b448-3a4b-7ec1-b878-c8c035d517bc"
THREAD = "01a1b3dc-94e8-7f92-b068-2d95bf588f7c"
PROJECT = str(ROOT)
HOME = str(Path.home())
TURN_VERSIONS = {
    "01a1b3dc-9917-7ae3-97f7-0034397857b0": ["v0.1.0"],
    "01a1b3e7-2ba0-7e80-8780-da1964ce0e05": ["v0.1.0"],
    "01a1b3fc-4ac0-72c0-88f2-8ed78caf59a7": ["v0.1.0", "v0.2.0"],
    "01a1b40f-ec50-73b3-b388-239e44d8e590": ["v0.2.0"],
    "01a1b429-4fd2-7843-ae35-325f77d1f464": ["visualizer-v0.1.0"],
    "01a1b448-396a-7b92-8cd2-f97c262d9812": ["publication-request-2026-11-07"],
}
TURN_TITLES = {
    "01a1b3dc-9917-7ae3-97f7-0034397857b0": "原メモの整理",
    "01a1b3e7-2ba0-7e80-8780-da1964ce0e05": "初版の論文化と非公開同期",
    "01a1b3fc-4ac0-72c0-88f2-8ed78caf59a7": "座標そのものを生成する規則",
    "01a1b40f-ec50-73b3-b388-239e44d8e590": "全体集合の一般化と日英版への改訂",
    "01a1b429-4fd2-7843-ae35-325f77d1f464": "ビジュアライザーの作成",
    "01a1b448-396a-7b92-8cd2-f97c262d9812": "対話記録・リポジトリ・最新版の公開依頼",
}


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def iso(epoch):
    return datetime.fromtimestamp(epoch, timezone.utc).astimezone(ZoneInfo("Asia/Tokyo")).isoformat() if epoch is not None else None


def text_of(item):
    if item["type"] == "userMessage":
        if any(part.get("type") != "text" for part in item["content"]):
            raise ValueError("Non-text user content needs an explicit export decision")
        return "".join(part["text"] for part in item["content"])
    return item["text"]


def public_text(text, turn_id):
    """Sanitize only transport-specific references; retain mathematical prose."""
    edits = []
    value = text

    def record(kind, count, description):
        if count:
            edits.append({"kind": kind, "count": count, "description": description})

    value, count = re.subn(
        r"visualize\{[^\n]*\}",
        "[編集者注：会話内の対話型表示は収録対象外。埋め込みHTML・操作状態はこの記録に含めていません。]",
        value,
    )
    record("omit_inline_visualization_reference", count,
           "表示専用の参照を編集者注に置換。参照先HTML・操作状態・画像は取得入力に含まれない。")

    paper_version = "v0.1.0" if turn_id == "01a1b3e7-2ba0-7e80-8780-da1964ce0e05" else "v0.2.0"
    citation_pattern = r':codex-file-citation\{path="' + re.escape(PROJECT) + r'/output/current/(dimensional_shift(?:_en)?\.pdf)" purpose="output"\}'

    def citation(match):
        language = "英語" if "_en" in match.group(1) else "日本語"
        return f"[PDF（{language}・{paper_version}）](../history/{paper_version}/{match.group(1)})"

    value, count = re.subn(citation_pattern, citation, value)
    record("convert_pdf_reference_to_archived_link", count,
           f"アプリ専用PDF参照を、その発言が報告した{paper_version}保存版への相対Markdownリンクに置換。")

    # Markdown links become paths relative to output/discussion/. Link labels stay unchanged.
    link_pattern = r"\]\(" + re.escape(PROJECT) + r"(/[^)\n]*)?\)"

    def local_link(match):
        suffix = (match.group(1) or "").lstrip("/")
        if suffix.startswith("output/current/") and suffix.endswith((".md", ".pdf", ".typ")):
            suffix = suffix.replace("output/current/", f"output/history/{paper_version}/", 1)
        return "](../../" + suffix + ")"

    value, count = re.subn(link_pattern, local_link, value)
    record("convert_project_link", count,
           "ローカル絶対リンクをリポジトリ内の相対リンクに置換。論文成果物は発言当時の保存版を参照。")
    count = value.count(PROJECT + "/")
    value = value.replace(PROJECT + "/", "")
    record("redact_project_prefix", count, "添付ファイル参照等のローカル絶対パスをリポジトリ相対パスに置換。")
    count = value.count(HOME)
    value = value.replace(HOME, "<LOCAL_HOME>")
    record("redact_local_home", count, "残存するローカルホームパスを<LOCAL_HOME>に置換。")
    if "/Users/" in value or "visualize" in value or ":codex-file-citation{" in value:
        raise ValueError("Unprocessed local or native reference")
    return value, edits


def build(data, published=False, published_at=None):
    if data["thread"]["id"] != THREAD:
        raise ValueError("Unexpected source thread")
    if data["page"].get("hasMore") or data["page"].get("nextCursor"):
        raise ValueError("Retrieve earlier pages before claiming the available range")
    turns = sorted(data["turns"], key=lambda turn: turn["startedAt"])
    exported, reached = [], False
    excluded_after_cutoff = 0
    for turn in turns:
        if turn["id"] not in TURN_VERSIONS:
            raise ValueError("Unknown turn: review its version mapping before export")
        messages = []
        for item in turn["items"]:
            is_visible = item["type"] == "userMessage" or (item["type"] == "agentMessage" and item.get("phase") in ("commentary", "final_answer"))
            if not is_visible:
                raise ValueError("Input contains non-visible records; refuse to export")
            if reached:
                excluded_after_cutoff += 1
                continue
            original = text_of(item)
            text, edits = public_text(original, turn["id"])
            ordinal = 1 + sum(len(t["messages"]) for t in exported) + len(messages)
            messages.append({
                "ordinal": ordinal,
                "anchor": f"message-{ordinal:03d}",
                "source_message_id": item["id"],
                "role": "user" if item["type"] == "userMessage" else "assistant",
                "phase": None if item["type"] == "userMessage" else item["phase"],
                "message_timestamp": None,
                "source_text_sha256": digest(original),
                "exported_text_sha256": digest(text),
                "edits": edits,
                "text": text,
            })
            if item["id"] == CUTOFF:
                reached = True
        if messages:
            exported.append({
                "ordinal": len(exported) + 1,
                "source_turn_id": turn["id"],
                "editorial_title": TURN_TITLES[turn["id"]],
                "related_versions": TURN_VERSIONS[turn["id"]],
                "source_status_at_retrieval": turn["status"],
                "turn_started_at_epoch_seconds": turn["startedAt"],
                "turn_completed_at_epoch_seconds": turn["completedAt"],
                "turn_started_at_jst": iso(turn["startedAt"]),
                "turn_completed_at_jst": iso(turn["completedAt"]),
                "messages": messages,
            })
    if not reached:
        raise ValueError("The requested cutoff user message is missing")
    messages = [message for turn in exported for message in turn["messages"]]
    if len(messages) != 28 or sum(m["role"] == "user" for m in messages) != 6:
        raise ValueError("Unexpected message count; inspect before exporting")
    return {
        "schema_version": 1,
        "title": "対話記録：0除算による次元移動を整理",
        "authors": ["木村祐太", "GPT-6 Astra（AI）"],
        "generated_at": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds"),
        "publication": {
            "status": "published" if published else "pending_publication",
            "public": published,
            "published_at": published_at,
            "url": REPO + f"/blob/main/output/discussion/{STEM}.md" if published else None,
            "intended_url": REPO + f"/blob/main/output/discussion/{STEM}.md",
        },
        "current_publication_policy": {
            "source": "公開作業中のユーザーの追加指定。今回の逐語記録の収録終点より後のため、本文に発言として追加していない。",
            "policy": "閲覧ページは最新版だけを配信する。GitHubの過去ソース・コミット・タグは公開してよい。旧版のローカル保存も維持する。",
            "is_editorial_metadata": True,
        },
        "source": {
            "tool": "mcp__codex_app__read_thread",
            "thread_id": data["thread"]["id"],
            "thread_title": data["thread"]["title"],
            "host_id": "local",
            "retrieval_options": {"turnLimit": 10, "includeOutputs": False, "maxOutputCharsPerItem": 20000},
            "source_page_has_more": False,
            "source_page_next_cursor": None,
            "input_is_visible_message_projection": True,
            "ordering": "Turn order changed from newest-first API page to chronological; within-turn message order preserved.",
        },
        "scope": {
            "description": "取得可能な範囲に含まれるユーザー発言とアシスタントの表示発言の編集付き逐語記録。アプリ全履歴やツール実行記録ではない。",
            "first_message_id": messages[0]["source_message_id"],
            "last_message_id": CUTOFF,
            "completed_turns": 5,
            "unfinished_turn_user_messages": 1,
            "message_count": len(messages),
            "user_message_count": 6,
            "assistant_message_count": 22,
            "assistant_commentary_count": 17,
            "assistant_final_answer_count": 5,
            "excluded_visible_messages_after_cutoff_in_input": excluded_after_cutoff,
            "excluded_categories": ["system/developer instructions", "internal reasoning", "tool calls and outputs", "sub-agent activity", "ambient UI and environment context", "embedded interactive HTML and state"],
            "limitations": [
                "各発言の個別時刻は取得されていない。記載時刻はAPIのターン開始・終了時刻である。",
                "APIが返した取得可能範囲について追加ページなしと確認した。アプリ内部の完全なイベント履歴や取得不能な内容を含むと保証しない。",
                "末尾は公開を依頼したユーザー発言。公開作業中のアシスタント発言および後続の完了報告は含めない。",
                "文章・数式の当時の主張は校正せず保持した。正誤や当時の完了報告は、この記録だけで再保証されるものではない。",
                "取得された初回userMessageには添付ファイルの参照見出しが含まれる。添付本文そのものは収録していない。",
            ],
        },
        "editorial_policy": {
            "wording": "記載した編集を除き、取得した発言の文言・数式・改行を保持する。見出し・版対応・時刻表示は編集者が付したメタデータ。",
            "edits": "各発言のeditsに変換種別・件数・理由を記載する。元のローカル絶対パスは編集一覧にも転載しない。",
            "hashes": "source_text_sha256は取得した発言文字列のUTF-8 SHA-256、exported_text_sha256は公開用編集後の同値。元データはローカル保存で公開しない。",
        },
        "turns": exported,
    }


def markdown(record):
    lines = ["# 対話記録：0除算による次元移動を整理", "", "著者表記：木村祐太・GPT-6 Astra（AI）", "",
             "このファイルは、取得できたユーザー発言とアシスタントの表示発言を収録した、編集箇所を明示する逐語記録です。話題要約や、アプリ内部の全履歴ではありません。", "",
             "初回の原メモ整理から、2026年11月7日の公開依頼までの6ターン・28発言（ユーザー6、アシスタント22）を収録しています。最後のターンはユーザー発言だけで区切っています。", "",
             "取得元：Codex `read_thread`。チャット名「" + record["source"]["thread_title"] + "」、チャットID `" + THREAD + "`。取得結果では追加の過去ページはありませんでした。", "",
             "本文の見出し、版との対応、時刻表示、編集一覧は編集者による付加情報です。時刻は**ターンの開始・終了時刻**であり、個々の発言時刻ではありません。", "",
             "ローカルの絶対パスは相対参照へ、PDFのアプリ専用参照は当時の保存版へのリンクへ置き換えました。会話内の対話型表示は収録していません。GitHubの過去版へのリンクは原文のまま保持しています。文章・数式の主張は校正せず、当時の内容を保持しています。", "",
             "[構造化JSONと発言別の編集一覧](" + STEM + ".json) ／ [論文・ビジュアライザーの版との対応](version_map.json)", "",
             "公開状態：" + ("公開済み。" if record["publication"]["public"] else "公開準備済み。リポジトリの公開確認後に状態を更新します。"), "",
             "現在の公開方針（収録終点後の追加指定を反映した編集者注）：閲覧ページは最新版のみとし、GitHubの過去ソース・コミット・タグは公開を許容します。旧版のローカル保存も維持します。この追加指定は今回の逐語本文には挿入していません。", "",
             "## 取得範囲と省略", ""]
    for limitation in record["scope"]["limitations"]:
        lines.extend(["- " + limitation])
    lines.extend(["- システム／開発者指示、内部推論、ツール呼び出しと出力、サブエージェントの活動、環境・画面コンテキストは対象外です。", "",
                  "## 版との対応", "", "| 収録ターン | 対応 |", "|---|---|"])
    for turn in record["turns"]:
        lines.append(f"| {turn['ordinal']}. {turn['editorial_title']} | {', '.join(turn['related_versions'])} |")
    for turn in record["turns"]:
        lines.extend(["", f"## ターン{turn['ordinal']}：{turn['editorial_title']}", "",
                      f"取得元ターンID：`{turn['source_turn_id']}`。対応：{', '.join(turn['related_versions'])}。", "",
                      "ターン開始：" + turn["turn_started_at_jst"] + "。終了：" + (turn["turn_completed_at_jst"] or "取得時点で未完了") + "。", ""])
        for message in turn["messages"]:
            label = "木村祐太（ユーザー）" if message["role"] == "user" else "GPT-6 Astra（AI）・" + ("進捗発言" if message["phase"] == "commentary" else "回答")
            lines.extend([f'<a id="{message["anchor"]}"></a>', "", f"### 発言{message['ordinal']:03d}：{label}", "",
                          "取得元発言ID：`" + message["source_message_id"] + "`。", ""])
            if message["edits"]:
                description = "／".join(f"{e['description']}（{e['count']}件）" for e in message["edits"])
                lines.extend(["> 編集注：" + description, ""])
            lines.append(message["text"])
    return "\n".join(lines).rstrip() + "\n"


def version_map(record):
    entries = [
        ("v0.1.0", "paper", [1, 2], ["0除算を乗算方程式の解集合として定義", "直積による次元上昇と条件による制限", "元の引数の復元を要求しない整理", "論文化と非公開リポジトリでの履歴管理"]),
        ("v0.2.0", "paper", [3, 4], ["独立座標を必要な都度生成する規則", "値の候補集合Uを明示した集合値の商", "有限離散格子と座標数・連続的次元の区別", "日英のPDFとMarkdownの対応"]),
        ("visualizer-v0.1.0", "source_history", [5], ["Lを適用する対話型表示", "実数と格子の切り替え", "高次元の投影と描画標本数"]),
        ("publication-request-2026-11-07", "publication_request", [6], ["対話記録とGitHubリポジトリの公開依頼", "ビジュアライザーの最新版だけを公開し旧版をローカル保存する方針"]),
    ]
    versions = []
    for version, kind, ordinals, topics in entries:
        turns = [t for t in record["turns"] if t["ordinal"] in ordinals]
        versions.append({
            "version": version, "kind": kind,
            "tag": version if kind in ("paper", "source_history") else None,
            "topics_are_editorial_summary": True,
            "topics": topics,
            "source_turn_ids": [t["source_turn_id"] for t in turns],
            "transcript_message_ordinals": [m["ordinal"] for t in turns for m in t["messages"]],
            "status": "published_available_range" if record["publication"]["public"] else "exported_pending_publication",
            "transcript": STEM + ".md",
            "structured_transcript": STEM + ".json",
            "public": record["publication"]["public"],
            "transcript_url": record["publication"]["url"],
            **({"artifact_public": record["publication"]["public"], "artifact_policy": "GitHubの過去ソース・コミット・タグは公開してよい。閲覧ページは最新版のみ配信し、旧版のローカル保存も維持する。"} if kind == "source_history" else {}),
        })
    return {
        "schema_version": 2,
        "description": "版・話題要約・取得元発言を対応づける編集用索引。要約は逐語記録ではない。",
        "source_thread_id": THREAD,
        "current_publication_policy": record["current_publication_policy"],
        "versions": versions,
        "cross_version_notes": [{"source_turn_id": "01a1b3fc-4ac0-72c0-88f2-8ed78caf59a7", "description": "v0.1.0への問いを受け、v0.2.0の独立座標生成を前面に出す方針につながった移行期の対話。"}],
    }


def readme(record):
    state = "公開済み" if record["publication"]["public"] else "公開準備済み（公開確認待ち）"
    return f"""# 対話記録と論文版の対応

著者表記：木村祐太・GPT-6 Astra（AI）

公開状態：**{state}**。

- [編集箇所を明示した対話記録]({STEM}.md)
- [構造化JSON・発言ID・編集一覧]({STEM}.json)
- [論文・ビジュアライザーの版との対応表](version_map.json)

## 収録した範囲

チャット「{record['source']['thread_title']}」について、Codexの `read_thread` で取得できた5つの完了ターンと、公開を依頼した次のユーザー発言までを収録しました。6ターン・28発言（ユーザー6、アシスタント22）です。アシスタントの進捗発言と最終回答は含みます。取得結果に追加の過去ページはありませんでした。

システム／開発者指示、内部推論、ツール実行記録、サブエージェント活動、環境・画面コンテキストは収録していません。アプリ内部の全イベント履歴や、取得不能な内容までを含む「全文」とは呼びません。公開作業中のアシスタント発言と、その後の完了報告は今回の区切りに含めません。

## 原文と編集の区別

記載した編集以外は、取得した発言の文言・数式・改行を保持しています。ローカル絶対パスを相対参照等へ置き換え、PDFのアプリ専用参照を当時の保存版へのリンクへ変更しました。対話型表示の参照は省略注に置き換えています。GitHubの過去版へのリンクは原文のまま保持しています。各発言の編集内容・件数をJSONとMarkdownの編集注に記録しています。

JSONには実際に取得したチャットID・ターンID・発言IDを保存しています。時刻はAPIが返したターン開始・終了時刻です。個々の発言時刻は取得されていないため、推測せず `null` としています。原文と編集後の発言のUTF-8 SHA-256も記録しています。元の取得データはローカルに残し、公開しません。

本文中の当時の「非公開」「公開していない」等は歴史的な発言として保持します。現在の公開状態はこのREADMEとJSONの `publication` を参照してください。記録に含まれる数学的主張や完了報告は、その時点の発言であり、公開に際して内容を校正したものではありません。

## 今後の更新

新しい取得範囲は別の日付・版で保存し、既存の論文保存版 `output/history/` は書き換えません。取得元、収録の終点、欠落、編集箇所、版との対応をその都度記録します。逐語記録と話題要約は区別します。

再生成は `scripts/export_discussion.py` で行います。入力はユーザー発言と表示されたアシスタント発言だけに絞った取得結果です。スクリプトはそれ以外の種類を検出すると停止します。リポジトリの公開を実際に確認した後でのみ `--published` を指定し、確認時刻を `--published-at` で渡します。

公開先：[{REPO}]({REPO})。

## 現在のビジュアライザー公開方針

公開作業中の追加指定により、閲覧ページは最新版だけを配信し、GitHubの過去ソース・コミット・タグは公開を許容する方針です。旧版のローカル保存も維持します。この追加指定は今回の収録終点より後のため、過去の発言を変更したり逐語本文に新しい発言を作ったりせず、現在の編集方針として別に記載しています。
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--published", action="store_true")
    parser.add_argument("--published-at", help="Actual verification timestamp, ISO 8601")
    args = parser.parse_args()
    if args.published != bool(args.published_at):
        parser.error("--published and --published-at must be supplied together")
    if args.published_at:
        stamp = datetime.fromisoformat(args.published_at)
        if stamp.tzinfo is None:
            parser.error("--published-at must include a timezone")
    record = build(json.loads(args.input.read_text(encoding="utf-8")), args.published, args.published_at)
    output = ROOT / "output/discussion"
    output.mkdir(parents=True, exist_ok=True)
    (output / (STEM + ".json")).write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / (STEM + ".md")).write_text(markdown(record), encoding="utf-8")
    (output / "version_map.json").write_text(json.dumps(version_map(record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "README.md").write_text(readme(record), encoding="utf-8")
    edits = sum(len(m["edits"]) for t in record["turns"] for m in t["messages"])
    print(f"Exported {record['scope']['message_count']} visible messages in {len(record['turns'])} turns; {edits} edit entries; {record['publication']['status']}")


if __name__ == "__main__":
    main()
