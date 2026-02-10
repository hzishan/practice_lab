# Web Crawler

基於 Python 的爬蟲練習，涵蓋從基礎的 **靜態 HTML 解析** 到複雜的 **動態網頁模擬操作**。

---

## 🚀 核心功能與腳本說明

本專案針對不同頁面結構採用了對應的抓取策略：

### 1. 靜態常見問題抓取 (`FQA_crawler.py`)
- **技術棧：** `Requests`, `BeautifulSoup4`
- **目標：** 抓取雄獅旅遊網站的 FQA（常見問題）頁面。
- **說明：** 針對結構化的靜態頁面進行解析，能快速提取問題與解答對（Q&A pairs），適合用於基礎資料蒐集或 FAQ 資料庫建立。

### 2. 動態資訊提取器 (`liontravel_relation_info.py`)
- **技術棧：** `Selenium WebDriver`
- **目標：** 獲取頁面中透過 JavaScript 非同步載入的關聯性資訊。
- **說明：** 處理動態元件加載，模擬真實用戶點擊或捲動行為，以獲取隱藏在互動標籤後的資料。

### 3. 日本旅遊方案深度爬蟲 (`japan_travel_plan.py`)
- **技術棧：** `Selenium` + 自動化流程
- **目標：** 針對「日本旅遊」分類下的所有方案進行遍歷抓取。
- **核心邏輯：**
    1. 進入日本旅遊列表頁。
    2. 自動翻頁或滾動以觸發 JavaScript 載入所有方案連結。
    3. 逐一進入各個方案詳情頁面抓取：**行程名稱、價格、出發日期、景點描述**等詳細欄位。

---

## 📖 使用指南
### 執行爬蟲

在 `lion_travel_crawler` 目錄下執行對應腳本：
```
# 執行 FQA 抓取
python FQA_crawler.py

# 執行動態關聯資訊抓取
python liontravel_relation_info.py

# 執行日本旅遊方案深度抓取
python japan_travel_plan.py
```
### 技術重點
- 等待機制： 使用 Selenium 的 WebDriverWait 與 expected_conditions 確保元素加載完成，提高爬蟲穩定性。
- 行為模擬： 加入適當的延遲 time.sleep() 模擬真人瀏覽，避免頻繁請求導致 IP 被封鎖。
- 精確定位： 結合 CSS Selector 與 XPath 處理複雜的 DOM 結構。

⚠️ 免責聲明
本專案僅供學術研究與爬蟲技術交流使用。請勿將抓取之資料用於商業用途，並請在執行前參考該網站之 robots.txt 規範。