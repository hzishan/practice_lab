from bs4 import BeautifulSoup
import requests, json, csv

url = "https://info.liontravel.com/category/zh-tw/support/faq?fr=cg6679C0201M04"
rsp = requests.get(url)
soup = BeautifulSoup(rsp.text, "html.parser")
# print(soup.prettify())

QAList = soup.find("script", type="application/ld+json")
data = json.loads(QAList.string)

# 提取 FAQ
faqs = []
for item in data:
    if 'mainEntity' in item:
        for q in item['mainEntity']:
            faqs.append({
                'question': q['name'],
                'answer': q['acceptedAnswer']['text']
            })

# 存成 CSV
with open('faq.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['question', 'answer'])
    writer.writeheader()
    writer.writerows(faqs)
