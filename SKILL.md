---
name: query_icp
description: "查询任何域名的中国 ICP 备案（互联网内容提供商）信息。自动使用 YOLOv11 求解验证码。"
version: 1.0.0
metadata:
  openclaw:
    type: command
    command: "python3"
    args: ["icp.py", "{domain}"]
    parameters:
      - name: domain
        type: string
        description: "要查询的域名（例如：baidu.com）"
        required: true
    timeout: 30
    output_format: json
---

# ICP 查询 Skill

该技能允许 Agent 查询域名的 ICP 备案信息。

## 使用方法

当用户询问某个域名的备案信息时，Agent 会自动调用该技能。

### 输入示例
- `domain`: `baidu.com`

### 输出示例
返回包含公司名称、备案号、企业性质等信息的 JSON 数据。
