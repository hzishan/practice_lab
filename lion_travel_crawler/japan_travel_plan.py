import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

OUTPUT_FILE = "liontravel_japan_plan.txt"

# -----------------------
# Anti-bot 用的隨機等待
# -----------------------
def random_sleep(a=2, b=5):
    time.sleep(random.uniform(a, b))

# -----------------------
# 模擬滑鼠滾動（降低 bot 風險）
# -----------------------
def human_scroll(driver, scroll_times=3):
    for _ in range(scroll_times):
        driver.execute_script("window.scrollBy(0, arguments[0]);", random.randint(200, 500))
        random_sleep(0.5, 1.2)

# -----------------------
# 取得地區連結
# -----------------------
def get_region_link():
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cmg_cota_img_container'))
    )

    human_scroll(driver)

    links = container.find_elements(By.TAG_NAME, 'a')
    urls, regions = [], []
    for link in links:
        urls.append(link.get_attribute("href"))
        regions.append(link.text.replace("\n", "(")+")")

    return regions, urls

# -----------------------
# 抓單頁內容
# -----------------------
def extract_page(url, region_name=None):
    driver.get(url)
    random_sleep(3, 6)
    human_scroll(driver, scroll_times=5)

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        if region_name:
            f.write(f"# {region_name}\n\n")

        # 熱門景點
        try:
            hot_spots = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.scrollArea.stack'))
            )
            hot_text = " ".join(hot_spots.get_attribute("innerText").split('\n'))
            f.write("📄 熱門景點：\n")
            f.write(f"{hot_text}\n\n")
        except:
            f.write("⚠ 無熱門景點資料\n\n")

        # Other blocks
        try:
            other_spot_blocks = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div.sc-n8ustd-0.fhflnP.ntb_conl_wrap.new_ntb_conl')
                )
            )
        except:
            other_spot_blocks = []

        for block in other_spot_blocks:
            try:
                block_name = block.find_element(By.TAG_NAME, "h2").text.strip()
            except:
                block_name = "未知區塊"

            f.write(f"## {block_name}\n")

            # 找 ul li a
            try:
                spot_labels = block.find_elements(By.CSS_SELECTOR, "div.ntb_conl_box ul li a")
            except:
                spot_labels = []

            if not spot_labels:
                f.write("⚠ 無有效的 label\n")

            # 抓內容
            try:
                spot_content = block.find_element(
                    By.CSS_SELECTOR,
                    'div.ntb_conl_content:not([style*="display:none"])'
                )
                content_text = " ".join(spot_content.get_attribute("innerText").split('\n'))
                f.write("📘 景點內容：\n")
                f.write(f"{content_text}\n\n")
            except:
                f.write("⚠ 無法抓取區塊內容\n\n")

        f.write("\n" + "="*50 + "\n\n")

# -----------------------
# Selenium 防偵測設定
# -----------------------
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
]

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument(f"user-agent={random.choice(user_agents)}")

# 避免 Selenium 自動化標記被發現
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)

# -----------------------
# 開始爬
# -----------------------
url_list = ["https://travel.liontravel.com/category/zh-tw/japan/index?fr=cg41752mega"]
driver.get(url_list[0])
random_sleep(4, 8)
human_scroll(driver, scroll_times=4)

# region links
regions_names, region_urls = get_region_link()

# 清空舊檔案
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("# 日本\n\n")

# 抓首頁
# extract_page(url_list[0])
# random_sleep(5, 10)

# 抓每個 region
for i in range(1,len(region_urls)):
    extract_page(region_urls[i], region_name=regions_names[i])
    random_sleep(6, 12)   # 重要！避免 IP 被封

driver.quit()
