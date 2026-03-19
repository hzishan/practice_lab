import os, json, time, requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{os.environ.get('cloudflare_id')}/browser-rendering/crawl"
headers  = {"Authorization": f"Bearer {os.environ.get('cloudflare_token')}"}

JOB_ID = "<your_job_id>"  # ← 唯一需要改的地方

# ── polling ───────────────────────────────────────────────────────────────
status = ""
while status != "completed":
    time.sleep(11)

    res    = requests.get(f"{BASE_URL}/{JOB_ID}?limit=1", headers=headers)
    data   = res.json().get("result", {})
    status = data.get("status", "unknown")
    print(f"\r[進度] {status} | {data.get('finished','?')}/{data.get('total','?')} 頁", end="", flush=True)

    if status in {"errored", "cancelled_by_user", "cancelled_due_to_timeout", "cancelled_due_to_limits"}:
        print(f"\n[結束] 任務失敗，狀態：{status}")
        exit()

print()

# ── 取完整結果並存檔 ──────────────────────────────────────────────────────
res     = requests.get(f"{BASE_URL}/{JOB_ID}", headers=headers)
records = res.json().get("result", {}).get("records", [])

with open(f"result.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"[完成] 共 {len(records)} 頁，已存檔")