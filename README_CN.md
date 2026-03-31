# ICP 查询工具 (ICP_FLASK)

[中文](README_CN.md) | [English](README.md)

基于 Flask 和 YOLOv11 OCR/验证码识别的高性能中文 ICP 备案查询工具。支持手动 API 访问以及 AI Agent (OpenClaw / Claude) 的 **Skills** 接入。

## ✨ 特性

- **🚀 高性能**：使用 YOLOv11 和 Siamese 网络进行快速、准确的验证码识别。
- **🛠️ 多接口支持**：
  - **REST API**：标准的 Flask API，方便集成到现有系统。
  - **AI Agent Skill (CLI)**：专用的 [icp.py](icp.py) 入口，方便 OpenClaw 或 Claude 等 AI Agent 直接通过技能调用。
- **📦 清洁结构**：优化的目录布局，便于生产环境部署和开源。

## 📁 项目结构

```text
ICP_FLASK/
├── icp.py               # AI Agent 技能 (CLI) 入口
├── main.py              # Flask REST API 入口
├── src/
│   ├── api.py           # Flask 业务逻辑
│   ├── icp_query.py     # 核心 ICP 查询逻辑
│   └── captcha.py       # YOLOv11/Siamese 验证码求解器
├── models/              # YOLOv11 & Siamese 模型文件
├── assets/              # 运行日志和静态资源
├── OPENCLAW_CONFIG.md   # OpenClaw 详细配置说明
├── SKILL.md             # AI Agent 技能定义文件 (OpenClaw 标准)
├── USERS.md             # 用户接入指南
├── requirements.txt     # Python 依赖
└── LICENSE              # MIT 开源协议
```

## 🧩 AI Agent / Skills 接入

本项目支持作为 **Skill** 被 AI Agent（如 **OpenClaw** 或 **Claude**）直接调用。

1. **安装依赖**：`pip install -r requirements.txt`
2. **技能加载**：将本项目目录链接到 OpenClaw 的 `skills` 目录，OpenClaw 将通过 [SKILL.md](SKILL.md) 自动发现。
3. **集成指南**：查看 [USERS.md](USERS.md) 和 [OPENCLAW_CONFIG.md](OPENCLAW_CONFIG.md) 了解如何集成。

### 快速开始

```bash
# 1. 克隆并安装
git clone https://github.com/your-username/ICP_FLASK.git
cd ICP_FLASK
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. 测试 CLI
python3 icp.py baidu.com

# 3. 获取绝对路径
pwd

# 4. 添加到 OpenClaw 配置（见 USERS.md）
```

### 📚 文档

- **[SKILL.md](SKILL.md)** - Skill 规范 (OpenClaw 标准)
- **[USERS.md](USERS.md)** - 集成指南
- **[OPENCLAW_CONFIG.md](OPENCLAW_CONFIG.md)** - 专用 Agent 配置说明

## 🚀 运行 Flask API

```bash
python3 main.py
```

API 将在 `http://localhost:8011/geticp?domain=baidu.com` 可用。

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
