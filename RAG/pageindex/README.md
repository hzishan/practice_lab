# PageIndex 使用練習

本練習透過 [PageIndex](https://docs.pageindex.ai/) 將 PDF 文件轉換為結構化索引資料，並使用地端 LLM 進行文件內容搜尋與問答。

why：相似度 &ne; 相關性；傳統RAG為語意相似度來衡量相關性，但在專業/長文場景，出現以下問題：
- 語意飄移：查詢語意語文本主題接近但不包含答案。
- 跨區粒度：chunking 破壞連續性，導致須結構遍歷與多部推理。
- 上下文取捨：Recall 與 Top-K 的 trade-off，可能導致取捨片段過少無法回答，或是太長而造成幻覺。

what：索引生成器；將文件生成結構化 json，不做固定力度切割，因此在上下文連貫、精確定位與跨段推理上效果更佳。

## QuickStart
### 1. 安裝 Ollama 並下載模型
確認 API `http://localhost:11434` 可使用
``` bash
ollama pull <model_name>
```

### 2. 下載 [PageIndex](https://github.com/VectifyAI/PageIndex) 並修改  `./pageindex/utils.py`

使用地端模型
``` python
client = openai.OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)
```
encoding model 修正
```
# (原) enc = tiktoken.encoding_for_model(model) 
enc = tiktoken.get_encoding("o200k_base")
```
支援中文輸出
``` python
with open(self._filepath(), "w", encoding="utf-8") as f:
    json.dump(self.log_data, f, indent=2, ensure_ascii=False)
```

### 3. 生成文件格式
將 pdf 放置 `./tests/pdf` 底下，然後執行 
`python run_pageindex.py --pdf_path <file_path> --model <model_name>`，生成的json檔會在 `./result` 底下

預處理: 將 tree 包成如下格式：
```
[{
    'title': 'DeepSeek-R1: Incentivizing Reasoning Cap...',
    'node_id': '0000',
    'prefix_summary': '# DeepSeek-R1: Incentivizing Reasoning C...',
    'nodes': <生成json的['structure']內容>
}]
```

------------------------------------------------------------------------

### 4. RAG 測試
執行 `python doc_search_sample.py` // 此為單一 [Doc Search](https://docs.pageindex.ai/tutorials/doc-search/description) 方式 

流程說明:

    使用者問題
        ↓
    LLM 判斷相關節點
        ↓
    擷取節點摘要
        ↓
    LLM 生成答案