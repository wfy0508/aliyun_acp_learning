# API 文档审核检查清单

## 端点示例完整性检查
- [ ] 每个端点是否有请求示例（cURL 或其他格式）
- [ ] 每个端点是否有成功响应示例（JSON 格式）
- [ ] 每个端点是否有错误响应示例（4xx/5xx 状态码）
- [ ] 示例是否包含实际可运行的参数值
- [ ] 示例是否标注 HTTP 方法和状态码

## 错误码说明检查
- [ ] 是否有全局错误码参考表
- [ ] 是否列出 400 Bad Request 及其常见原因
- [ ] 是否列出 401 Unauthorized 及其认证要求
- [ ] 是否列出 403 Forbidden 及其权限要求
- [ ] 是否列出 404 Not Found 及其可能原因
- [ ] 是否列出 500 Internal Server Error 及其处理建议
- [ ] 错误响应示例是否包含 error_code、message、details 字段

## 参数类型标注检查
- [ ] 路径参数是否标注类型（如 `id: integer`, `slug: string`）
- [ ] 查询参数是否标注类型和是否必需（如 `page: integer (required)`, `sort: string (optional)`）
- [ ] 请求体参数是否标注类型、是否必需、是否有示例值
- [ ] 响应体参数是否标注类型和是否必需
- [ ] 是否使用标准数据类型（string, integer, boolean, array, object, number）
- [ ] 是否标注枚举值（如 `status: string (active, inactive, pending)`）

## 文档质量检查
- [ ] 所有端点是否有清晰的描述
- [ ] 是否有认证要求说明
- [ ] 是否有速率限制说明
- [ ] 是否有版本信息
- [ ] 是否有更新历史

## OpenAPI 3.0 合规性检查（如果适用）
- [ ] 是否符合 OpenAPI 3.0 规范
- [ ] components/schemas 是否正确定义
- [ ] parameters 是否正确引用
- [ ] responses 是否包含 content/type 和 examples
- [ ] securitySchemes 是否正确定义