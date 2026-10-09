# User Management API

## GET /api/users

获取用户列表

### Parameters
- `page`: integer (optional) - 页码
- `limit`: integer (optional) - 每页数量
- `sort`: string (optional) - 排序字段

### Response
Status: 200 OK

```json
{
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 10
  }
}
```

## POST /api/users

创建新用户

### Request Body
- `name`: string (required)
- `email`: string (required)
- `age`: integer (optional)

### Response
Status: 201 Created

```json
{
  "id": 123,
  "name": "Jane Smith",
  "email": "jane@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## GET /api/users/{id}

获取单个用户

### Path Parameters
- `id`: integer (required)

### Response
Status: 200 OK

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

## Error Codes
- 400 Bad Request: 请求参数无效
- 401 Unauthorized: 认证失败
- 403 Forbidden: 权限不足
- 404 Not Found: 资源不存在
- 500 Internal Server Error: 服务器内部错误