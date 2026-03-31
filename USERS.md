# USERS.md - OpenClaw 集成指南


## 安装

### 第一步：克隆并安装

```bash
git clone https://github.com/your-username/ICP_FLASK.git
cd ICP_FLASK

python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 第二步：验证安装

```bash
python3 icp.py baidu.com
```

## 集成到 OpenClaw

### 推荐方式：自动发现

OpenClaw 能够通过根目录下的 `SKILL.md` 自动加载技能。

1. 将项目软链接到 OpenClaw 的 skills 目录：
   ```bash
   ln -s /绝对路径/到/ICP_FLASK ~/.openclaw/skills/icp-query
   ```
2. 检查技能是否已加载：
   ```bash
   openclaw skills list
   ```

## 创建专用查询代理 (Agent)

如果您希望创建一个专门负责 ICP 查询的助手（而不是混在默认助手中），请执行：

1. **添加专家代理**：
   ```bash
   openclaw agents add icp_expert 
   ```
2. **设置身份信息**：
   ```bash
   openclaw agents set-identity --agent icp_expert --name "ICP 专家" --emoji "🔍"
   ```
3. **在对话中使用**：
   ```bash
   openclaw agent --agent icp_expert --message "查下 baidu.com"
   ```
