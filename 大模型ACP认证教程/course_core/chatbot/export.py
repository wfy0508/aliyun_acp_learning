"""对话历史导出模块。

此模块不依赖 llama_index，可独立导入和测试。
"""

import json
from datetime import datetime, timezone

# 模块级变量：保存本次运行的对话历史
_history: list[dict] = []


def export_history(chat_history: list[dict], output_path: str) -> str:
    """将对话历史导出为 JSON 文件，导出前验证格式。

    参数
      chat_history(list): 对话记录列表，每条包含 timestamp, user_query, bot_response, sources
      output_path(str): 输出 JSON 文件路径
    返回
      str: 输出文件路径
    """
    _validate_history(chat_history)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)
    return output_path


def _validate_history(chat_history: list[dict]) -> None:
    """验证 chat_history 格式是否符合预期。

    每条记录必须包含：timestamp, user_query, bot_response, sources 四个字段，
    且 sources 必须是 list 类型。
    """
    required_fields = {"timestamp", "user_query", "bot_response", "sources"}
    for i, record in enumerate(chat_history):
        if not isinstance(record, dict):
            raise ValueError(f"记录 {i} 类型错误，期望 dict，实际为 {type(record).__name__}")
        missing = required_fields - set(record.keys())
        if missing:
            raise ValueError(f"记录 {i} 缺少必需字段: {missing}")
        if not isinstance(record["sources"], list):
            raise ValueError(f"记录 {i} 的 sources 字段应为 list，实际为 {type(record['sources']).__name__}")


def _append_to_history(question: str, response) -> dict:
    """内部函数：从 LlamaIndex response 对象构建单条记录并追加到历史。

    参数
      question(str): 用户问题
      response: LlamaIndex QueryEngine.query() 返回的 response 对象
    返回
      dict: 本次对话记录
    """
    source_nodes = getattr(response, "source_nodes", None) or []
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_query": question,
        "bot_response": response.response_txt if hasattr(response, "response_txt") else "",
        "sources": [node.get_content() for node in source_nodes],
    }
    _history.append(record)
    return record
