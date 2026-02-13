
import json
import asyncio
import openai

import pageindex.utils as utils
from tests.testcase_generate import testcase_generate


async def call_llm(prompt: str, model="gpt-oss:20b", temperature=0) -> str:
    """
    呼叫地端 LLM (Ollama)
    """
    client = openai.AsyncOpenAI(
        api_key="ollama",
        base_url="http://localhost:11434/v1"
    )

    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


def create_node_mapping(nodes: list) -> dict:
    """
    將樹狀節點轉換為扁平 mapping
    key: node_id
    value: node object
    """
    node_map = {}

    def traverse(node_list):
        for node in node_list:
            node_id = node.get("node_id")

            if node_id:
                node_map[node_id] = node

            children = node.get("nodes")
            if isinstance(children, list):
                traverse(children)

    traverse(nodes)
    return node_map


def build_tree_search_prompt(query: str, tree: dict) -> str:
    return f"""
        You are given a question and a tree structure of a document.

        Your task is to find all nodes that are likely to contain the answer.

        Question: {query}

        Document tree structure:
        {json.dumps(tree, indent=2)}

        Reply in JSON only:

        {{
        "thinking": "...",
        "node_list": ["node_id_1", "node_id_2"]
        }}
    """


def build_answer_prompt(query: str, context: str) -> str:
    return f"""
        Answer the question using ONLY the provided context.

        Question:
        {query}

        Context:
        {context}
    """


async def main():
    query = "Your Question"
    tree = testcase_generate() # 測試文件樹
    tree_without_summary = utils.remove_fields( # 降低模型 input token
        tree.copy(),
        fields=["summary"]
    )
    node_map = create_node_mapping(tree[0]["node"]) # 文件 node mapping

    # ===== 搜尋節點 =====
    search_prompt = build_tree_search_prompt(
        query,
        tree_without_summary
    )
    raw_result = await call_llm(search_prompt)
    # print("\nRetrieved Nodes:")
    # print(raw_result)
    node_list = json.loads(raw_result)["node_list"]


    # ===== 蒐集摘要 =====
    summaries = []
    for node_id in node_list:
        node = node_map.get(node_id)
        if node and "summary" in node:
            summaries.append(node["summary"])
    context = "\n\n".join(summaries)

    # ===== 產生答案 =====
    answer_prompt = build_answer_prompt(query, context)

    print("\nGenerated Answer:\n")
    answer = await call_llm(answer_prompt)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
