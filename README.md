# OpenClaw Expert Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue.svg)](https://openclaw.ai)
[![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Compatible-green.svg)](https://workbuddy.ai)

专为 AI IDE（OpenClaw / WorkBuddy / Claude Code 等）设计的专家级多代理辩论系统。

**7位专业 Agent + 智能调度系统**，帮你从多个维度深度分析复杂问题。

---

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户问题输入                          │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              Coordinator（调度员）                       │
│         分析问题 → 匹配专家 → 组织辩论                   │
└─────────────────────────────────────────────────────────┘
                           ↓
        ┌─────────┬─────────┬─────────┬─────────┐
        ↓         ↓         ↓         ↓         ↓
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │Researcher│ Thinker │ Coach   │ Decision│ Methodology
   │领域专家 │ 炼金术  │ 教练    │ 决策模拟│ 方法论
   └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
        ↓         ↓         ↓         ↓
   ┌────────┐ ┌────────┐
   │ Human3 │ │ Naval  │
   │发展评估│ │纳瓦尔策略│
   └────────┘ └────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              综合各方观点 → 输出最终答案                 │
└─────────────────────────────────────────────────────────┘
```

---

## 7位专家 Agent

| ID | 名称 | 核心能力 | 适用场景 |
|----|------|---------|---------|
| **researcher** | 深度领域专家 | 跨领域专业知识、技术/商业/研究分析 | "XX领域最新发展是什么" |
| **thinker** | 人生炼金术 | 第一性原理、本质挖掘、纵向思考 | "这个问题的本质是什么" |
| **coach** | 思维教练 | 苏格拉底式提问、思维引导、发现盲点 | "我不知道如何思考这个问题" |
| **decision** | 高维决策模拟 | C.O.R.E.框架、多角色模拟、复杂决策 | "我面临一个艰难的决策" |
| **methodology** | 方法论创造大师 | 原创框架设计、跨领域整合 | "帮我设计一套方法论" |
| **human3** | HUMAN3.0发展评估师 | 四维度评估（心智/身体/精神/事业） | "评估我的发展水平" |
| **naval** | 纳瓦尔策略 | 财富创造、判断力、长期思维 | "关于财富/人生的建议" |

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/openclaw-expert-suite.git
```

### 2. 安装专家 Agent

将 `agents/` 目录下的配置文件复制到你的 AI IDE 工作空间：

**WorkBuddy 用户：**
```bash
# Windows
copy agents\*.md %USERPROFILE%\WorkBuddy\YourProject\.codebuddy\agents\

# macOS/Linux
cp agents/*.md ~/WorkBuddy/YourProject/.codebuddy/agents/
```

**目录结构要求：**
```
YourProject/.codebuddy/agents/
├── researcher/SOUL.md    # 复制 researcher.md 内容
├── thinker/SOUL.md       # 复制 thinker.md 内容
├── coach/SOUL.md         # 复制 coach.md 内容
├── decision/SOUL.md      # 复制 decision.md 内容
├── methodology/SOUL.md   # 复制 methodology.md 内容
├── human3/SOUL.md        # 复制 human3.md 内容
└── naval/SOUL.md         # 复制 naval.md 内容
```

### 3. 安装调度系统（可选）

如果你想使用智能调度功能：

```bash
# 复制到 skills 目录
copy coordinator\SKILL.md %USERPROFILE%\WorkBuddy\YourProject\.codebuddy\skills\multi-agent-experts.md
```

---

## 使用方法

### 方式一：直接 @ 专家

在对话中直接调用某位专家：

```
@researcher 帮我分析量子计算的最新进展
@thinker 挖掘这个问题的本质
@naval 从长期策略角度怎么看
```

### 方式二：调度员自动分配

告诉 AI 成为调度员：

```
你是专家调度员，分析一下：生物主权的下一个进化是什么？
```

调度员会自动分析问题并派遣最合适的专家（或专家组合）。

### 方式三：指定专家组合

明确指定多位专家进行辩论：

```
请派遣 researcher + thinker + naval 三位专家，从不同角度分析这个问题
```

---

## 专家组合推荐

| 场景 | 推荐组合 | 输出特点 |
|------|---------|---------|
| **战略决策** | researcher + thinker + decision | 领域知识+本质挖掘+决策模拟 |
| **个人发展** | human3 + coach + naval | 评估+引导+策略 |
| **方法论创造** | methodology + thinker + researcher | 框架设计+原理+领域 |
| **深度分析** | researcher + thinker + coach | 知识+本质+提问 |
| **全视角辩论** | researcher + thinker + decision + naval | 四位专家全面覆盖 |

---

## 完整示例

查看 [examples/bio-sovereignty-debate.md](examples/bio-sovereignty-debate.md) 了解如何使用多位专家对"生物主权的下一个进化"进行深度辩论。

---

## 文件结构

```
openclaw-expert-suite/
├── README.md                    # 本文件
├── LICENSE                      # MIT 许可证
├── .gitignore                   # Git 忽略配置
├── agents/                      # 7位专家 Agent 配置
│   ├── researcher.md           # 深度领域专家
│   ├── thinker.md              # 人生炼金术
│   ├── coach.md                # 思维教练
│   ├── decision.md             # 高维决策模拟
│   ├── methodology.md          # 方法论创造大师
│   ├── human3.md               # HUMAN3.0发展评估师
│   └── naval.md                # 纳瓦尔策略
├── coordinator/                 # 调度系统
│   └── SKILL.md                # 专家辩论调度系统配置
└── examples/                    # 使用示例
    └── bio-sovereignty-debate.md  # 生物主权辩论示例
```

---

## 专家详解

### Researcher（深度领域专家）

自动识别问题所属领域，调用该领域的顶级专家知识进行分析。

**核心能力：**
- 技术领域：系统工程思维、架构设计、最佳实践
- 商业领域：战略思维、商业模式、市场分析
- 创意领域：设计思维、用户体验、创新方法
- 学术研究：科学方法论、逻辑推理、批判思维

---

### Thinker（人生炼金术）

帮你一层层挖问题，从表象→机理→原理→公理。

**核心能力：**
- 分形视角：多维度、多层次审视问题
- 纵向挖掘：持续追问"为什么"直到本质
- 第一性原理：质疑假设，回到基本真理
- 系统思维：看到整体、识别反馈回路

---

### Coach（思维教练）

通过提问让你自己想清楚，苏格拉底式方法。

**核心能力：**
- 苏格拉底式提问：引导你自己找到答案
- 多视角建模：SWOT、六顶思考帽等框架
- 角色扮演：模拟投资人、客户、技术布道者等角色
- 思维镜鉴：客观反馈，发现盲点

---

### Decision（高维决策模拟）

使用 C.O.R.E. 框架进行多角色决策模拟。

**核心能力：**
- C.O.R.E. 框架：Context / Objectives / Roles / Execution
- 多角色模拟：CEO、CTO、投资人、用户等不同视角
- 思维模型注入：SWOT、OKR、OODA 循环等
- 分阶段推演：结构化决策流程

---

### Methodology（方法论创造大师）

为你设计专属的方法论框架。

**核心能力：**
- 框架设计：将抽象概念转化为结构化工具
- 跨领域整合：创造性组合不同领域方法
- 原创框架：基于需求设计独一无二的方法论
- 简洁原则：一页纸能说清楚的方法论

---

### Human3（HUMAN3.0发展评估师）

从心智、身体、精神、事业四个维度评估你的发展水平。

**核心能力：**
- 四维度评估：心智 / 身体 / 精神 / 事业
- 四象限分析：重要性-现状矩阵
- 个性化方案：基于评估结果的发展建议
- 长期规划：近期 / 中期 / 长期发展路径

---

### Naval（纳瓦尔策略）

运用纳瓦尔·拉维坎特（Naval Ravikant）的方法论分析和解决问题。

**核心能力：**
- 财富分析：独特专长、杠杆、复利
- 决策分析：长期后果、可逆性、内心真实
- 幸福诊断：欲望、比较、当下
- 长期主义：关注长期复利，忽略短期噪音

---

## 工作原理

### 调度系统逻辑

1. **问题分析**：调度员分析用户问题的性质和维度
2. **专家匹配**：根据问题类型匹配最适合的专家
3. **并行派遣**：通过 `sessions_spawn` 同时调用多位专家
4. **结果综合**：整合各方观点，形成完整答案

### 使用限制

- 调度员不亲自执行任务，只负责派遣
- 每次 spawn 必须指定 `sessionKey`
- 专家通过独立的 session 工作，互不可见

---

## 兼容性

| 平台 | 支持状态 | 说明 |
|------|---------|------|
| WorkBuddy | ✅ 完全支持 | 原生支持 Agent 系统 |
| OpenClaw | ✅ 完全支持 | 原生支持 Agent 系统 |
| Claude Code | ⚠️ 部分支持 | 需要手动配置 |
| 其他 AI IDE | ⚠️ 待测试 | 理论上支持 Markdown 格式的系统提示词 |

---

## 贡献指南

欢迎贡献新的专家 Agent 或改进现有配置！

### 提交新专家

1. Fork 本仓库
2. 在 `agents/` 目录下创建新的专家配置文件
3. 遵循现有格式：名称、核心能力、使用场景
4. 更新 README.md 添加专家说明
5. 提交 Pull Request

### 专家设计原则

- **单一职责**：每个专家只专注一个核心领域
- **可组合性**：专家之间可以相互配合
- **实用性**：提供可执行的建议，而非空泛理论
- **独特性**：与现有专家有明显区分

---

## 许可证

[MIT License](LICENSE) - 自由使用、修改和分享

---

## 致谢

- 调度系统基于 [multi-agent-cn](https://clawhub.ai) 架构改造
- 纳瓦尔策略基于 [Naval Ravikant](https://nav.al) 的公开分享
- 感谢 OpenClaw / WorkBuddy 社区的支持

---

**Happy Debating! 🎉**

如果你在使用过程中有任何问题或建议，欢迎提交 Issue 或 Pull Request。
