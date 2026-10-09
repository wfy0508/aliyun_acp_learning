import json
import os
import tempfile

from course_core.chatbot.export import (
    export_history,
    _validate_history,
    _append_to_history,
    _history,
)


class MockNode:
    def __init__(self, content: str):
        self._content = content

    def get_content(self):
        return self._content


class MockResponse:
    def __init__(self, text: str, sources: list[str]):
        self.response_txt = text
        self.source_nodes = [MockNode(s) for s in sources]


def setup_function():
    _history.clear()


def test_append_to_history():
    resp = MockResponse("北京是中国的首都。", ["参考资料1", "参考资料2"])
    record = _append_to_history("中国的首都是哪里？", resp)

    assert record["user_query"] == "中国的首都是哪里？"
    assert record["bot_response"] == "北京是中国的首都。"
    assert len(record["sources"]) == 2
    assert record["sources"][0] == "参考资料1"
    assert record["sources"][1] == "参考资料2"
    assert len(_history) == 1
    assert "timestamp" in record


def test_export_history():
    resp = MockResponse("答案", ["来源"])
    _append_to_history("问题", resp)

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name

    try:
        result_path = export_history(_history, path)
        assert result_path == path
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["user_query"] == "问题"
        assert data[0]["bot_response"] == "答案"
        assert data[0]["sources"] == ["来源"]
        assert "timestamp" in data[0]
    finally:
        os.unlink(path)


def test_export_history_multiple_records():
    _append_to_history("Q1", MockResponse("A1", ["S1"]))
    _append_to_history("Q2", MockResponse("A2", ["S2a", "S2b"]))

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name

    try:
        export_history(_history, path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["user_query"] == "Q1"
        assert data[0]["bot_response"] == "A1"
        assert len(data[1]["sources"]) == 2
        assert data[1]["sources"] == ["S2a", "S2b"]
    finally:
        os.unlink(path)


def test_validate_history_missing_field():
    bad_history = [{"timestamp": "t", "user_query": "q", "bot_response": "a"}]  # 缺少 sources
    try:
        _validate_history(bad_history)
        assert False, "应抛出 ValueError"
    except ValueError as e:
        assert "缺少必需字段" in str(e)


def test_validate_history_wrong_sources_type():
    bad_history = [{"timestamp": "t", "user_query": "q", "bot_response": "a", "sources": "不是list"}]
    try:
        _validate_history(bad_history)
        assert False, "应抛出 ValueError"
    except ValueError as e:
        assert "sources 字段应为 list" in str(e)


class MockResponseNoSources:
    """模拟没有 source_nodes 属性的 response 对象。"""
    def __init__(self, text: str):
        self.response_txt = text


class MockResponseEmptySources:
    """模拟 source_nodes 为空的 response 对象。"""
    def __init__(self, text: str):
        self.response_txt = text
        self.source_nodes = []


def test_append_to_history_no_source_nodes():
    """response 没有 source_nodes 属性时，sources 应为空 list。"""
    resp = MockResponseNoSources("这是一个没有来源的回答。")
    record = _append_to_history("没有来源的问题", resp)
    assert record["sources"] == []
    assert record["bot_response"] == "这是一个没有来源的回答。"
    assert len(_history) == 1


def test_append_to_history_empty_source_nodes():
    """response 的 source_nodes 为空 list 时，sources 应为空 list。"""
    resp = MockResponseEmptySources("来源为空。")
    record = _append_to_history("空来源问题", resp)
    assert record["sources"] == []
    assert record["bot_response"] == "来源为空。"


def test_validate_history_not_dict():
    bad_history = ["不是dict", {"timestamp": "t", "user_query": "q", "bot_response": "a", "sources": []}]
    try:
        _validate_history(bad_history)
        assert False, "应抛出 ValueError"
    except ValueError as e:
        assert "类型错误" in str(e)
