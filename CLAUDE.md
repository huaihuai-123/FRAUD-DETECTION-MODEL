# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

信用卡欺诈检测 ML 系统，8 阶段流水线：加载数据 → EDA → 预处理(特征工程+缩放) → SMOTE 均衡 → 训练 4 模型 → 评估排序 → SHAP 可解释性 → 生成报告。附带 Streamlit 交互式仪表盘和 Hugging Face 自然语言解释。

## 常用命令

```bash
# 激活虚拟环境
source .venv/Scripts/activate   # Windows Git Bash

# 运行完整训练流水线（需要先放置数据集）
python main.py

# 启动 Streamlit 仪表盘（需要先运行过 main.py）
streamlit run app/streamlit_app.py

# 安装依赖
pip install -r requirements.txt
```

## 架构与数据流

### 8 阶段流水线 (`main.py`)

1. `ensure_project_directories()` + `set_seed(42)` — 创建目录、固定随机种子
2. `load_data()` — 读取 `data/raw/transactions.csv`（284,807 条，0.17% 欺诈）
3. `run_eda(df)` — 生成类别平衡、金额分布、时间分布、相关性热力图 → `reports/figures/`
4. `preprocess_data(df)` — 特征工程 + train/test 分层拆分(80/20) + StandardScaler → 保存 scaler.pkl 和 feature_names.json
5. `train_models(X_train, y_train)` — SMOTE(sampling_strategy=0.2) 均衡后训练 4 个模型，各自存为 .pkl
6. `evaluate_models(models, X_test, y_test)` — 计算 ROC-AUC/PR-AUC/Precision/Recall/F1，按 ROC-AUC 降序排列，为每个模型生成混淆矩阵/ROC/PR 曲线图
7. 保存最佳模型为 `fraud_model.pkl`，生成特征重要性图和 SHAP beeswarm 图
8. 写入 `reports/report.md` 和 `reports/metrics.csv`

### 关键模块

| 模块 | 路径 | 职责 |
|------|------|------|
| 配置中心 | `src/utils/config.py` | 所有路径、超参数、常量的唯一定义点 |
| 工具函数 | `src/utils/helpers.py` | 目录创建、随机种子、JSON/文本读写 |
| 数据加载 | `src/data/load_data.py` | 读取 CSV，基础验证 |
| 特征工程 | `src/data/feature_engineering.py` | 派生 Hour/Amount_Log/Is_Night/Is_Large_Amount |
| 预处理 | `src/data/preprocess.py` | 组装特征工程+拆分+缩放，保存处理后的数据 |
| 模型训练 | `src/models/train_model.py` | SMOTE + 4 模型训练(LogisticRegression/RandomForest/XGBoost/LightGBM) |
| 模型评估 | `src/models/evaluate_model.py` | 多指标评分 + 诊断图表生成 |
| 预测 | `src/models/predict.py` | 单笔交易推理，加载模型+scaler+feature_names |
| HF 解释 | `src/models/huggingface_model.py` | 用 FLAN-T5 将预测结果转为自然语言解释 |
| SHAP | `src/explainability/shap_explainer.py` | TreeExplainer 计算 SHAP 值，生成文本摘要和 beeswarm 图 |
| EDA 可视化 | `src/visualization/eda.py` | 数据探索图表 |
| 评估可视化 | `src/visualization/plots.py` | 混淆矩阵、ROC、PR、特征重要性图 |
| Streamlit | `app/streamlit_app.py` | 交互式仪表盘：选择交易 → 运行分析 → 显示风险仪表盘+判决+AI 解释 |

### 4 个模型及关键参数

- **Logistic Regression**: `max_iter=2000`, `class_weight=balanced`
- **Random Forest**: `n_estimators=200`, `class_weight=balanced_subsample`, `n_jobs=-1`
- **XGBoost**: `n_estimators=200`, `learning_rate=0.05`, `max_depth=5`, `subsample=0.8`, `colsample_bytree=0.8`, `tree_method=hist`
- **LightGBM**: `n_estimators=200`, `learning_rate=0.05`, `n_jobs=-1`

模型选择主指标为 **ROC-AUC**（Accuracy 不适用，因为欺诈仅占 0.17%）。

## 架构设计要点

### 统一的特征工程

所有入口（`preprocess.py`、`predict.py`、`streamlit_app.py`）均调用 `create_features()` from `feature_engineering.py`，生成 4 个派生特征：`Hour`、`Amount_Log`、`Is_Night`、`Is_Large_Amount`。不存在多套特征工程分叉。

### 延迟加载模式

- `src/models/predict.py` — 模型/scaler/feature_names 首次调用时才加载，避免 import 即 I/O
- `src/models/huggingface_model.py` — FLAN-T5 pipeline 首次调用 `generate_explanation()` 时才下载（~1GB），避免 import 时阻塞

### 模型选择策略

- `main.py` 按 ROC-AUC 选最佳模型保存为 `fraud_model.pkl`
- `predict.py` 和 `streamlit_app.py` 优先加载 `fraud_model.pkl`，fallback `lightgbm_model.pkl`

### SHAP 兼容性

`shap_explainer.py` 自动处理：
- TreeExplainer 优先，非树模型 fallback KernelExplainer
- SHAP ≥ 0.42 返回 3D 数组，`_extract_fraud_shap()` 统一提取欺诈类 SHAP 值

### SMOTE 安全性

`train_model.py` 动态计算 `k_neighbors = min(5, max(1, minority_count - 1))`，少数类 < 2 时跳过 SMOTE 并警告，避免 k_neighbors 超过样本数崩溃。

## 数据集

使用 Kaggle Credit Card Fraud Detection 数据集。下载后重命名为 `transactions.csv`，放置到 `data/raw/transactions.csv`。

- 284,807 条交易，492 条欺诈 (0.17%)
- 30 个特征：Time, V1-V28 (PCA 匿名化), Amount, Class (目标)
- 下载地址：https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

## 配置要点 (`src/utils/config.py`)

所有可调参数集中于此，修改后对整个流水线生效：

- `RANDOM_STATE = 42` — 全局随机种子
- `TEST_SIZE = 0.2` — 测试集比例
- `SMOTE_RATIO = 0.2` — 欺诈类重采样目标比例（相对多数类）
- `THRESHOLD = 0.5` — 分类决策阈值
- `LARGE_AMOUNT_THRESHOLD = 200.0` — 大额交易判定线(USD)
