from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 輸出 txt 檔名
output_file = "liontravel_relation_info.txt"

def get_link():
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.nvb_info_floor2.noHeading'))
    )
    links = container.find_elements(By.TAG_NAME, 'a')
    urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]
    return urls

def extract_page(url):
    driver.get(url)
    
    try:
        # 等待主內容區塊
        main_block = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.col_conl.col_conl_col_24.col_conl_col_sm_24.col_conl_col_md_4_5th.col_conl_col_lg_4_5th')
            )
        )
        # 取得文字
        main_text = main_block.get_attribute("innerText").strip()
        if main_text:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"# {main_text}\n\n")
    except:
        print(f"⚠ 無法抓取主內容：{url}")

    # 抓 ntb_conl_box 的 tab（若存在）
    try:
        tab_box = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ntb_conl_box'))
        )
        tab_items = tab_box.find_elements(By.CSS_SELECTOR, 'ul li a')
    except:
        tab_items = []

    if tab_items:
        for tab in tab_items:
            tab_name = tab.text.strip()
            # 點擊切換 tab
            driver.execute_script("arguments[0].click();", tab)
            try:
                tab_content = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ntb_conl_content'))
                )
                tab_text = tab_content.get_attribute("innerText").strip()
                if tab_text:
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write(f"## {tab_name}\n{tab_text}\n\n")
            except:
                print(f"⚠ 無法抓取 tab：{tab_name}")

# Selenium 設定
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# 開啟主頁
driver.get("https://info.liontravel.com/category/zh-tw/aboutlion/index?fr=cg41752C0301C0301M01")
main_urls = get_link()
for url in main_urls:
    extract_page(url)

driver.quit()
print(f"✅ 完成，已輸出至 {output_file}")
