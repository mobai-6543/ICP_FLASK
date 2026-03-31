# ICP Query Tools (ICP_FLASK)

[中文](README_CN.md) | [English](README.md)

A high-performance Chinese ICP filing (Internet Content Provider) query tool based on Flask and YOLOv11 OCR/CAPTCHA solving. It supports manual API access and AI Agent (OpenClaw / Claude) **Skills** integration.

## ✨ Features

- **🚀 High Performance**: Built with YOLOv11 and Siamese networks for fast and accurate CAPTCHA solving.
- **🛠️ Multi-Interface**:
  - **REST API**: Standard Flask API for easy integration.
  - **AI Agent Skill (CLI)**: Dedicated [icp.py](icp.py) for direct AI Agent (OpenClaw / Claude) integration.
- **📦 Clean Structure**: Optimized directory layout for production and open-source.

## 📁 Project Structure

```text
ICP_FLASK/
├── icp.py               # AI Agent Skill (CLI) entry point
├── main.py              # Flask REST API entry point
├── src/
│   ├── api.py           # Flask API logic
│   ├── icp_query.py     # Core ICP query logic
│   └── captcha.py       # YOLOv11/Siamese solver
├── models/              # YOLOv11 & Siamese models
├── assets/              # Logs and static assets
├── OPENCLAW_CONFIG.md   # Detailed OpenClaw configuration
├── SKILL.md             # AI Agent skill definition (OpenClaw standard)
├── USERS.md             # User integration guide
├── requirements.txt     # Python dependencies
└── LICENSE              # MIT License
```

## 🧩 AI Agent / Skills Integration

This project is designed to be used as a **Skill** by AI Agents like **OpenClaw** or **Claude**.

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Skill Loading**: Link this project directory to OpenClaw's `skills` directory. OpenClaw will automatically discover it via [SKILL.md](SKILL.md).
3. **Integration Guide**: See [USERS.md](USERS.md) and [OPENCLAW_CONFIG.md](OPENCLAW_CONFIG.md) for details.

### Quick Start

```bash
# 1. Clone and install
git clone https://github.com/your-username/ICP_FLASK.git
cd ICP_FLASK
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Test CLI
python3 icp.py baidu.com

# 3. Get absolute path
pwd

# 4. Add to OpenClaw config (see USERS.md)
```

### 📚 Documentation

- **[SKILL.md](SKILL.md)** - Skill specification (OpenClaw standard)
- **[USERS.md](USERS.md)** - Integration guide
- **[OPENCLAW_CONFIG.md](OPENCLAW_CONFIG.md)** - Dedicated Agent configuration

## 🚀 Run Flask API

```bash
python3 main.py
```

The API will be available at `http://localhost:8011/geticp?domain=baidu.com`.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
