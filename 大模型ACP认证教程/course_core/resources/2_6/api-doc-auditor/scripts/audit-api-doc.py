#!/usr/bin/env python3
# API 文档审核脚本
# 用于检查 REST API 文档的三个核心质量维度

import sys
import json
import re
from typing import Dict, List, Optional


def audit_api_documentation(doc_content: str, doc_format: str = "markdown") -> Dict:
    """
    审核 API 文档质量
    
    检查维度：
    1. 端点示例完整性
    2. 错误码说明
    3. 参数类型标注
    """
    
    result = {
        "summary": {
            "total_endpoints": 0,
            "endpoints_with_examples": 0,
            "endpoints_with_error_codes": 0,
            "endpoints_with_parameter_types": 0,
            "compliance_rate": 0.0
        },
        "issues": {
            "endpoint_examples": [],
            "error_codes": [],
            "parameter_types": []
        },
        "recommendations": []
    }
    
    # 识别端点（简化版，实际应用中需要更复杂的解析）
    endpoints = extract_endpoints(doc_content, doc_format)
    result["summary"]["total_endpoints"] = len(endpoints)
    
    for endpoint in endpoints:
        # 检查端点示例
        if not has_examples(endpoint):
            result["issues"]["endpoint_examples"].append(
                f"{endpoint['method']} {endpoint['path']}: 缺少请求或响应示例"
            )
        else:
            result["summary"]["endpoints_with_examples"] += 1
        
        # 检查错误码说明
        if not has_error_code_explanations(endpoint):
            result["issues"]["error_codes"].append(
                f"{endpoint['method']} {endpoint['path']}: 缺少错误码说明"
            )
        else:
            result["summary"]["endpoints_with_error_codes"] += 1
        
        # 检查参数类型标注
        if not has_parameter_type_annotations(endpoint):
            result["issues"]["parameter_types"].append(
                f"{endpoint['method']} {endpoint['path']}: 缺少参数类型标注"
            )
        else:
            result["summary"]["endpoints_with_parameter_types"] += 1
    
    # 计算合规率
    if endpoints:
        total_checks = len(endpoints) * 3
        passed_checks = (
            result["summary"]["endpoints_with_examples"] +
            result["summary"]["endpoints_with_error_codes"] +
            result["summary"]["endpoints_with_parameter_types"]
        )
        result["summary"]["compliance_rate"] = round((passed_checks / total_checks) * 100, 1)
    
    # 生成建议
    result["recommendations"] = generate_recommendations(result)
    
    return result


def extract_endpoints(content: str, format_type: str) -> List[Dict]:
    """提取 API 端点信息"""
    endpoints = []
    
    if format_type == "markdown":
        # 简单的 Markdown 端点匹配（实际应用中需要更复杂的解析）
        # 匹配如 "### GET /api/users" 或 "## POST /api/posts"
        pattern = r'(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(/[^\s]+)'
        matches = re.finditer(pattern, content, re.IGNORECASE)
        
        for match in matches:
            method = match.group(1).upper()
            path = match.group(2)
            endpoints.append({
                "method": method,
                "path": path,
                "content": content[match.start():match.end() + 500]  # 简化处理
            })
    
    return endpoints


def has_examples(endpoint: Dict) -> bool:
    """检查端点是否有示例"""
    content = endpoint["content"].lower()
    
    # 检查是否有请求示例
    has_request_example = (
        "curl" in content or 
        "request" in content or 
        "example" in content and ("request" in content or "req" in content)
    )
    
    # 检查是否有响应示例
    has_response_example = (
        "response" in content or 
        "json" in content or 
        "example" in content and ("response" in content or "resp" in content)
    )
    
    return has_request_example and has_response_example


def has_error_code_explanations(endpoint: Dict) -> bool:
    """检查端点是否有错误码说明"""
    content = endpoint["content"].lower()
    
    # 检查是否包含常见错误码
    error_codes = ["400", "401", "403", "404", "500"]
    has_error_codes = any(code in content for code in error_codes)
    
    # 检查是否有错误说明关键词
    error_keywords = ["error", "invalid", "unauthorized", "forbidden", "not found", "server error"]
    has_error_explanations = any(keyword in content for keyword in error_keywords)
    
    return has_error_codes and has_error_explanations


def has_parameter_type_annotations(endpoint: Dict) -> bool:
    """检查端点是否有参数类型标注"""
    content = endpoint["content"].lower()
    
    # 检查类型标注关键词
    type_keywords = [
        "type:", "data type", "string", "integer", "boolean", 
        "array", "object", "number", "enum", "required", "optional"
    ]
    
    # 检查参数相关关键词
    param_keywords = [
        "parameter", "param", "query", "path", "body", "request body",
        "request parameters", "query parameters", "path parameters"
    ]
    
    has_types = any(keyword in content for keyword in type_keywords)
    has_params = any(keyword in content for keyword in param_keywords)
    
    return has_types and has_params


def generate_recommendations(audit_result: Dict) -> List[str]:
    """生成改进建议"""
    recommendations = []
    
    if audit_result["summary"]["compliance_rate"] < 70:
        recommendations.append("文档整体质量较低，建议优先完善端点示例和错误码说明")
    
    if audit_result["issues"]["endpoint_examples"]:
        recommendations.append("为所有端点添加标准化的 cURL 请求示例和 JSON 响应示例")
    
    if audit_result["issues"]["error_codes"]:
        recommendations.append("创建全局错误码参考表，为每个常见 HTTP 状态码提供详细说明")
    
    if audit_result["issues"]["parameter_types"]:
        recommendations.append("使用 OpenAPI 3.0 标准格式化参数定义，明确标注类型、是否必需和示例值")
    
    if not recommendations:
        recommendations.append("文档质量良好，符合专业 API 文档标准")
    
    return recommendations


if __name__ == "__main__":
    # 使用示例
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = audit_api_documentation(content)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Usage: python audit-api-doc.py <api_documentation_file>")
