# 上一句魔法命令在 Cell 执行时自动在本地生成该代码文件，方便 MCP Client 在本地拉起该服务
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# 创建本地 MCP Server 实例，模拟联网搜索服务
mcp = FastMCP("MockWebSearch")


# @mcp.tool() 装饰器把普通函数注册为 MCP 工具
@mcp.tool()
def web_search(query: str, max_results: int = 3) -> str:
    """模拟联网搜索，根据关键词返回搜索结果。

    Args:
        query: 搜索关键词
        max_results: 最大返回结果数量，默认为 3
    """
    mock_db = {
        "大型语言模型": [
            {
                "title": "GPT-5 发布：多模态能力再次突破",
                "snippet": "OpenAI 发布了 GPT-5，在推理和多模态理解方面取得显著进步。",
                "date": "2026-04-10",
            },
            {
                "title": "Qwen3 开源模型系列全面升级",
                "snippet": "阿里云通义千问发布 Qwen3，在数学推理、代码生成等方面全面超越前代。",
                "date": "2026-04-08",
            },
            {
                "title": "大语言模型在科学发现中的应用综述",
                "snippet": "Nature 综述总结了 LLM 在药物发现、材料科学等领域的最新应用。",
                "date": "2026-04-05",
            },
        ],
    }

    results = []
    for key, items in mock_db.items():
        if key in query or query in key:
            results.extend(items)
    if not results:

        results = [
            {
                "title": f"关于「{query}」的搜索结果",
                "snippet": f"这是关于「{query}」的模拟结果。",
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        ]

    lines = [f"搜索「{query}」共找到 {len(results[:max_results])} 条结果：\n"]
    for i, r in enumerate(results[:max_results], 1):
        lines.append(
            f"{i}. 【{r['title']}】\n   {r['snippet']}\n   日期: {r['date']}\n"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    # 以 stdio 方式启动，等待 Client 端（父进程）通过 stdin/stdout 通信
    mcp.run(transport="stdio")
