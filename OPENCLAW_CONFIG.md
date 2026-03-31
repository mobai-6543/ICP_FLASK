# OpenClaw 专用代理 (Agent) 配置指南

本文档说明如何为 ICP 查询创建一个**独立、专用**的 OpenClaw Agent。

> **为什么要创建专用 Agent？**
> 默认 Agent 通常集成了大量 Skill（如文件管理、浏览器等），在处理特定任务时可能会产生干扰。创建一个专用 Agent 可以确保：
> 1. **功能纯粹**：Agent 只专注于 ICP 查询，响应更快且更准确。
> 2. **上下文清晰**：系统提示词专门为备案查询优化。
> 3. **资源隔离**：拥有独立的工作空间和配置。

## 快速开始

### 1. 安装和验证
(同前...)

---

## 方式一：YAML 配置文件 (推荐)

在 OpenClaw 配置中定义一个完全隔离的 Agent。

```yaml
# icp_agent_config.yaml

# 1. 定义工具 (Skill)
tools:
  - id: query_icp
    name: "查询 ICP 备案"
    type: "command"
    command: "python3"
    args: ["/绝对路径/到/ICP_FLASK/icp.py", "{domain}"]
    parameters:
      - name: domain
        type: string
        required: true
    timeout: 30
    output_format: "json"

# 2. 定义专用 Agent (仅绑定上述工具)
agents:
  - id: icp_expert
    name: "ICP 备案专家"
    description: "专门负责中国域名 ICP 备案信息的查询与分析"
    
    # 核心：只给它这一个技能，实现功能隔离
    skills:
      - query_icp
    
    # 专门优化的系统提示词
    system_prompt: |
      你是一个专业的 ICP 备案查询助手。
      你的唯一任务是帮助用户查询域名的备案信息。
      请始终使用 `query_icp` 工具获取数据，并以整洁的表格或列表形式展示：
      - 主体名称、备案号、单位性质、审核时间。
    
    model: "claude-3-5-sonnet" # 推荐使用高性能模型
    temperature: 0.1 # 调低随机性，确保查询稳定
```

---

## 方式二：命令行快速创建

如果您想通过命令行快速创建一个只代理 ICP 功能的助手：

### 1. 创建基础 Agent
```bash
# 创建一个名为 icp_expert 的独立代理
openclaw agents add icp_expert --model claude-3-5-sonnet --workspace /path/to/icp_workspace
```

### 2. 设置专家身份
```bash
openclaw agents set-identity \
  --agent icp_expert \
  --name "ICP 备案查询专家" \
  --emoji "�️"
```

### 3. 绑定单一 Skill (实现代理隔离)
确保您已经通过 `SKILL.md` 自动发现了 `query_icp` 技能，然后在该 Agent 的私有配置或全局配置中，确保 `icp_expert` 的 `skills` 列表**只包含** `query_icp`。

---

## 如何切换到该专用代理？

在 OpenClaw TUI 或客户端中，您可以直接指定 Agent ID 进行对话：

```bash
# 使用专用代理发送询问
openclaw agent --agent icp_expert --message "帮我查一下 baidu.com 的备案"
```

### 查看已添加的 Skills 和 Agents

```bash
# 列出所有 Skills
openclaw skills list

# 查看特定 Skill 详情
openclaw skills show query_icp

# 列出所有 Agents
openclaw agents list

# 查看特定 Agent 详情
openclaw agents show icp_query_agent
```

### 测试 Skill

```bash
# 直接测试 Skill
openclaw skills test query_icp --params domain=baidu.com

# 查看执行日志
openclaw skills test query_icp --params domain=baidu.com --verbose
```

---

## 方式三：Python API 添加

### 使用 OpenClaw Python SDK

```python
from openclaw import OpenClaw, Skill, Agent

# 初始化 OpenClaw
claw = OpenClaw()

# 添加 Skill
skill = Skill(
    id="query_icp",
    name="查询 ICP 备案",
    description="查询任何域名的中国 ICP 备案信息",
    type="command",
    command="python3",
    args=["/绝对路径/到/ICP_FLASK/icp.py", "{domain}"],
    parameters=[
        {
            "name": "domain",
            "type": "string",
            "description": "要查询的域名",
            "required": True
        }
    ],
    timeout=30,
    output_format="json",
    cache={"enabled": True, "ttl": 3600}
)
claw.add_skill(skill)

# 添加 Agent
agent = Agent(
    id="icp_query_agent",
    name="ICP 查询助手",
    description="帮助用户查询域名的 ICP 备案信息",
    skills=["query_icp"],
    model="claude-opus-4-6",
    system_prompt="你是一个 ICP 备案查询助手...",
    temperature=0.7,
    max_tokens=1024
)
claw.add_agent(agent)

# 测试 Agent
result = claw.run_agent(
    agent_id="icp_query_agent",
    user_input="查询 baidu.com 的 ICP 备案"
)
print(result)
```

---

## 使用示例

### 场景 1：查询单个域名

```
用户：查询 baidu.com 的 ICP 备案
Agent：我来帮你查询 baidu.com 的 ICP 备案信息...
[执行 Skill: query_icp(domain="baidu.com")]
结果：
- 公司名称：百度在线网络技术（北京）有限公司
- ICP 证号：京ICP证030173号
- 企业性质：企业
- 内容类型：网站
- 更新时间：2024-01-01 00:00:00
```

### 场景 2：对比多个域名

```
用户：对比 baidu.com 和 qq.com 的 ICP 备案
Agent：我来查询这两个域名的信息...
[执行 Skill: query_icp(domain="baidu.com")]
[执行 Skill: query_icp(domain="qq.com")]
结果对比：
| 域名 | 公司名称 | ICP 证号 |
|------|---------|---------|
| baidu.com | 百度在线网络技术（北京）有限公司 | 京ICP证030173号 |
| qq.com | 腾讯科技有限公司 | 粤B2-20090059号 |
```

### 场景 3：批量查询

```
用户：查询这些域名的 ICP 备案：baidu.com, qq.com, alibaba.com
Agent：我来批量查询这些域名...
[执行工作流: batch_icp_query]
结果：已查询 3 个域名，生成报告...
```

---

## 故障排除

### 问题 1：找不到 python3 命令

```bash
# 查找 python3 完整路径
which python3
# 或
which python

# 在配置中使用完整路径
command: "/usr/bin/python3"
```

### 问题 2：ModuleNotFoundError

```bash
# 设置 PYTHONPATH
export PYTHONPATH=/绝对路径/到/ICP_FLASK:$PYTHONPATH

# 或在配置中设置环境变量
env:
  PYTHONPATH: "/绝对路径/到/ICP_FLASK"
```

### 问题 3：模型文件找不到

```bash
# 检查模型文件
ls -la /绝对路径/到/ICP_FLASK/models/

# 应该包含：
# - yolov11.onnx
# - siamese.onnx
```

### 问题 4：超时错误

```yaml
# 增加超时时间
timeout: 60  # 从 30 秒增加到 60 秒
```

---

## 最佳实践

1. **使用绝对路径**：始终在配置中使用绝对路径，避免相对路径问题

2. **设置合理的超时**：根据网络情况调整超时时间（建议 30-60 秒）

3. **启用缓存**：对于频繁查询的域名，启用缓存可以提高性能

4. **错误处理**：配置重试机制处理临时网络问题

5. **日志记录**：启用详细日志便于调试

6. **权限管理**：确保 OpenClaw 进程有权限执行 Python 脚本

---

## 相关文档

- [SKILLS.md](SKILLS.md) - Skill 技术规范
- [USERS.md](USERS.md) - 用户集成指南
- [README.md](README.md) - 项目概述
