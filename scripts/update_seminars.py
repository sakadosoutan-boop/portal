#!/usr/bin/env python3
"""
PDFをGemini APIで解析してseminars.jsonを更新するスクリプト。
使い方: GEMINI_API_KEY=xxx python3 scripts/update_seminars.py
"""
import os
import json
import time
import base64
import hashlib
import urllib.request
import urllib.error
from pathlib import Path

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SEMINARS_DIR = Path("project/seminars")
SEMINARS_JSON = SEMINARS_DIR / "seminars.json"
CACHE_FILE = Path("scripts/.seminars_cache.json")

EXTRACT_PROMPT = """このPDFはセミナー・講座・ワークショップのチラシまたは要項です。
以下のJSONフォーマットで情報を抽出してください。
値が不明・記載なしの場合は null にしてください。

{
  "title": "セミナー・講座のタイトル（正式名称）",
  "date": "開催日（YYYY-MM-DD形式。複数日ある場合は最初の日）",
  "deadline": "申込締切日（YYYY-MM-DD形式。なければnull）",
  "organizer": "主催者・運営団体名",
  "target": "対象者（例: 高校生、中高生、高校1〜3年 など）",
  "format": "開催形式（online / onsite / hybrid のいずれか一つ）",
  "applyUrl": "申込URL（記載があれば）",
  "accent": "チラシのメインカラー（CSSカラーコード #RRGGBB形式。不明なら null）"
}

JSONのみ返してください。マークダウンの```は不要です。"""

ACCENT_COLORS = ["#189048", "#ee7e66", "#4fb8e8", "#f7b500", "#2e9bd6",
                 "#a855f7", "#f97316", "#06b6d4", "#84cc16", "#ec4899"]


def pdf_hash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:16]


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            pass
    return {}


def save_cache(cache: dict):
    CACHE_FILE.parent.mkdir(exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2))


def call_gemini(pdf_bytes: bytes) -> dict | None:
    pdf_b64 = base64.b64encode(pdf_bytes).decode()
    payload = {
        "contents": [{
            "parts": [
                {"text": EXTRACT_PROMPT},
                {"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}}
            ]
        }],
        "generationConfig": {"temperature": 0.1}
    }
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}")
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  Gemini API error {e.code}: {e.read().decode()}")
        return None

    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    # マークダウンのコードブロックを除去
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"  JSON parse failed:\n{text[:200]}")
        return None


def load_seminars() -> list:
    if SEMINARS_JSON.exists():
        try:
            return json.loads(SEMINARS_JSON.read_text())
        except Exception:
            pass
    return []


def save_seminars(seminars: list):
    SEMINARS_JSON.write_text(
        json.dumps(seminars, ensure_ascii=False, indent=2) + "\n"
    )


def next_id(seminars: list) -> str:
    nums = [int(s["id"][1:]) for s in seminars if s.get("id", "").startswith("s")]
    return f"s{max(nums, default=0) + 1}"


def pick_accent(seminars: list) -> str:
    used = {s.get("accent") for s in seminars}
    for c in ACCENT_COLORS:
        if c not in used:
            return c
    return ACCENT_COLORS[len(seminars) % len(ACCENT_COLORS)]


def main():
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY が設定されていません")
        raise SystemExit(1)

    pdfs = sorted(SEMINARS_DIR.glob("*.pdf"))
    if not pdfs:
        print("PDFが見つかりません:", SEMINARS_DIR)
        return

    seminars = load_seminars()
    cache = load_cache()
    existing_pdfs = {s.get("pdf", "") for s in seminars}
    changed = False

    for pdf_path in pdfs:
        rel_path = f"seminars/{pdf_path.name}"
        h = pdf_hash(pdf_path)

        # すでに処理済みかつ内容変更なし → スキップ
        if rel_path in existing_pdfs and cache.get(pdf_path.name) == h:
            print(f"skip  {pdf_path.name} (unchanged)")
            continue

        print(f"process {pdf_path.name} ...", end=" ", flush=True)
        data = call_gemini(pdf_path.read_bytes())
        if data is None:
            print("FAILED")
            continue

        # 既存エントリを更新 or 新規追加
        existing = next((s for s in seminars if s.get("pdf") == rel_path), None)
        if existing:
            existing.update({k: v for k, v in data.items() if v is not None})
            print(f"updated: {existing['title']}")
        else:
            entry = {
                "id": next_id(seminars),
                "title": data.get("title") or pdf_path.stem,
                "date": data.get("date"),
                "deadline": data.get("deadline"),
                "organizer": data.get("organizer"),
                "target": data.get("target"),
                "format": data.get("format", "onsite"),
                "applyUrl": data.get("applyUrl") or "",
                "pdf": rel_path,
                "accent": data.get("accent") or pick_accent(seminars),
            }
            seminars.append(entry)
            print(f"added: {entry['title']}")

        cache[pdf_path.name] = h
        changed = True
        time.sleep(1)  # API レート制限対策

    # 削除されたPDFをJSONからも除去
    pdf_names = {f"seminars/{p.name}" for p in pdfs}
    before = len(seminars)
    seminars = [s for s in seminars if not s.get("pdf") or s["pdf"] in pdf_names
                or not s["pdf"].startswith("seminars/")]
    if len(seminars) != before:
        print(f"removed {before - len(seminars)} deleted PDF entries")
        changed = True

    if changed:
        save_seminars(seminars)
        save_cache(cache)
        print(f"seminars.json updated ({len(seminars)} entries)")
    else:
        print("変更なし")


if __name__ == "__main__":
    main()
