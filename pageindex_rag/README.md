# PageIndex 使用練習

本練習透過 **PageIndex** 將 PDF 文件轉換為結構化索引資料，並使用地端 LLM 進行文件內容搜尋與問答。

注意： LLM 節點搜尋為語意推論，可能出現誤判


##  1. 安裝 Ollama 並啟動模型

``` bash
ollama pull gpt-oss:20b
ollama run gpt-oss:20b
```

確認 API 可使用：

    http://localhost:11434


## 2. 修改  `./pageindex/utils.py`
-  使用地端模型
    ``` python
    client = openai.OpenAI(
        api_key="ollama",
        base_url="http://localhost:11434/v1"
    )
    ```
- 支援中文輸出
    ``` python
    with open(self._filepath(), "w", encoding="utf-8") as f:
        json.dump(self.log_data, f, indent=2, ensure_ascii=False)
    ```

## 3. 生成文件格式
- 將 pdf 放置 `./tests/pdf` 底下，然後執行 
`python run_pageindex.py --pdf_path <file_path> --model <model_name>`，生成的json檔會在 `./result` 底下
- 預處理: 將 tree 包成如下格式：
    ```
    [{
        'title': 'DeepSeek-R1: Incentivizing Reasoning Cap...',
        'node_id': '0000',
        'prefix_summary': '# DeepSeek-R1: Incentivizing Reasoning C...',
        'nodes': <生成json的['structure']內容>
    }]
    ```

------------------------------------------------------------------------

## 4. RAG 測試
執行 `python doc_search_sample.py` // 此為單一 Doc Search 方式 

流程說明:

    使用者問題
        ↓
    LLM 判斷相關節點
        ↓
    擷取節點摘要
        ↓
    LLM 生成答案