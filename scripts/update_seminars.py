#!/usr/bin/env python3
"""
PDFをGemini Files API経由で解析してseminars.jsonを更新するスクリプト。
使い方: GEMINI_API_KEY=xxx python3 scripts/update_seminars.py
"""
import os
import json
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SEMINARS_DIR = Path("project/seminars")
SEMINARS_JSON = SEMINARS_DIR / "seminars.json"
CACHE_FILE = Path("scripts/.seminars_cache.json")
BASE_URL = "https://generativelanguage.googleapis.com"

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
  "applyUrl": "申込URL（記載があれば。なければnull）",
  "accent": "チラシのメインカラー（CSSカラーコード #RRGGBB形式。不明ならnull）"
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


def api_request(method: str, path: str, body=None, headers=None) -> dict:
    url = f"{BASE_URL}{path}?key={GEMINI_API_KEY}"
    data = json.dumps(body).encode() if body else None
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        raise RuntimeError(f"HTTP {e.code}: {err[:300]}")


def upload_pdf(pdf_path: Path) -> str | None:
    """PDFをGemini Files APIにアップロードしてfileUriを返す。"""
    pdf_bytes = pdf_path.read_bytes()
    size = len(pdf_bytes)

    # Step1: アップロードセッション開始
    url = f"{BASE_URL}/upload/v1beta/files?key={GEMINI_API_KEY}"
    meta = json.dumps({"file": {"display_name": pdf_path.name}}).encode()
    req = urllib.request.Request(
        url, data=meta,
        headers={
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(size),
            "X-Goog-Upload-Header-Content-Type": "application/pdf",
            "Content-Type": "application/json",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            upload_url = resp.headers.get("X-Goog-Upload-URL")
    except urllib.error.HTTPError as e:
        print(f"  upload start failed {e.code}: {e.read().decode()[:200]}")
        return None

    if not upload_url:
        print("  no upload URL returned")
        return None

    # Step2: ファイル本体を送信
    req2 = urllib.request.Request(
        upload_url, data=pdf_bytes,
        headers={
            "Content-Length": str(size),
            "X-Goog-Upload-Offset": "0",
            "X-Goog-Upload-Command": "upload, finalize",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req2, timeout=120) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  upload finalize failed {e.code}: {e.read().decode()[:200]}")
        return None

    uri = result.get("file", {}).get("uri")
    return uri


def delete_file(file_uri: str):
    """アップロードしたファイルをGeminiから削除する。"""
    name = file_uri.split("/files/")[-1]
    try:
        url = f"{BASE_URL}/v1beta/files/{name}?key={GEMINI_API_KEY}"
        req = urllib.request.Request(url, method="DELETE")
        urllib.request.urlopen(req, timeout=15)
    except Exception:
        pass


def call_gemini(file_uri: str) -> dict | None:
    payload = {
        "contents": [{
            "parts": [
                {"text": EXTRACT_PROMPT},
                {"file_data": {"mime_type": "application/pdf", "file_uri": file_uri}}
            ]
        }],
        "generationConfig": {"temperature": 0.1}
    }
    url = f"{BASE_URL}/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  Gemini generate error {e.code}: {e.read().decode()[:200]}")
        return None

    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
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
            data = json.loads(SEMINARS_JSON.read_text())
            return data if isinstance(data, list) else []
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
    changed = False

    for pdf_path in pdfs:
        rel_path = f"seminars/{pdf_path.name}"
        h = pdf_hash(pdf_path)

        existing = next((s for s in seminars if s.get("pdf") == rel_path), None)
        already_processed = (
            existing and
            existing.get("title") and
            "自動取得中" not in existing.get("title", "") and
            cache.get(pdf_path.name) == h
        )
        if already_processed:
            print(f"skip  {pdf_path.name} (unchanged)")
            continue

        print(f"upload {pdf_path.name} ({pdf_path.stat().st_size // 1024}KB) ...", end=" ", flush=True)
        file_uri = upload_pdf(pdf_path)
        if not file_uri:
            print("upload FAILED")
            continue
        print(f"ok → extract ...", end=" ", flush=True)

        data = call_gemini(file_uri)
        delete_file(file_uri)

        if data is None:
            print("extract FAILED")
            continue

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
        time.sleep(2)

    if changed:
        save_seminars(seminars)
        save_cache(cache)
        print(f"\nseminars.json updated ({len(seminars)} entries)")
    else:
        print("変更なし（全PDF処理済みまたはAPIエラー）")


if __name__ == "__main__":
    main()
