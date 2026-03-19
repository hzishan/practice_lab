import os, requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{os.environ.get('cloudflare_id')}/browser-rendering/crawl"
headers  = {"Authorization": f"Bearer {os.environ.get('cloudflare_token')} "}

res = requests.post(BASE_URL, headers=headers, json={
    "url": os.environ.get('crawler_url'),
    "limit": 100,
    "formats": ["markdown"],
    "options": {
        # "includeExternalLinks": True,
        "includeSubdomains": True,
    },
    "gotoOptions": {
      "waitUntil": "networkidle2",
      "timeout": 60000
    },
    "rejectResourceTypes": ["image", "media", "stylesheet"],
})

print(res.status_code)
print(res.json())
# 成功會看到 {'success': True, 'result': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}
# 把那個 UUID 複製起來，填到下面的 get_crawl.py