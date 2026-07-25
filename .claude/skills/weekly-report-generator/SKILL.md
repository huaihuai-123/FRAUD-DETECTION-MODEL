---
name: weekly-report-generator
description: >
  根据本周Git提交记录和TODO变更生成结构化周报Markdown文件。
  当用户提到"周报"、"weekly report"、"本周工作总结"、"生成报告"、
  "本周做了什么"、"weekly summary"、"工作汇报"时使用此技能。
---

# Weekly Report Generator

扫描本周一至今天的 Git 提交记录和 TODO 注释变更，生成一份结构化的周报 Markdown 文件，输出到项目根目录。

## 工作流程

### 1. 确定时间范围

计算本周一的日期：

```bash
python -c "from datetime import date, timedelta; d=date.today(); print(d - timedelta(days=d.weekday()))"
```

- **开始日期**: 本周一 YYYY-MM-DD 的 00:00:00
- **结束日期**: 明天的 YYYY-MM-DD（`git log --until` 不包含当天，需要用明天）
- 设变量 `$MONDAY` 和 `$TOMORROW` 方便后续命令复用：

```bash
MONDAY=$(python -c "from datetime import date, timedelta; d=date.today(); print((d - timedelta(days=d.weekday())).isoformat())")
TOMORROW=$(python -c "from datetime import date, timedelta; d=date.today(); print((d + timedelta(days=1)).isoformat())")
TODAY=$(python -c "from datetime import date; print(date.today().isoformat())")
```
注意：git log 的 `--since`/`--until` 在只传日期（如 `2026-06-29`）而不带时间时，跨平台行为不一致。务必使用 ISO 格式 `YYYY-MM-DD` 并追加 `T00:00:00`，确保日期边界准确：

```bash
git log --since="${MONDAY}T00:00:00" --until="${TOMORROW}T00:00:00" ...
```

### 2. 收集 Git 提交记录

依次执行以下命令，利用 `$MONDAY` 和 `$TOMORROW` 变量：

**总提交数**:
```bash
git log --since="${MONDAY}T00:00:00" --until="${TOMORROW}T00:00:00" --oneline --no-merges | wc -l
```

**每个作者的提交数**:
```bash
git shortlog --since="${MONDAY}T00:00:00" --until="${TOMORROW}T00:00:00" -sn --no-merges
```

**提交详情（按日期倒序）**:
```bash
git log --since="${MONDAY}T00:00:00" --until="${TOMORROW}T00:00:00" --format="%ad|%an|%s" --date=short --no-merges
```

**变更文件统计**:
```bash
git diff --stat $(git log --since="${MONDAY}T00:00:00" --until="${TOMORROW}T00:00:00" --format=%H --no-merges | tail -1)^..HEAD -- . 2>/dev/null | tail -1
```

如果本周没有提交，跳过提交相关章节，在报告中注明"本周无提交记录"。

### 3. 扫描 TODO 变更

**本周新增的 TODO（从 diff 中提取）**:
```bash
git log --since="${MONDAY}T00:00:00" --until="${TOMORROW}T00:00:00" -p --no-merges | grep -E "^\+\s*(TODO|FIXME|HACK|XXX):?" | sed 's/^+\s*//' | sort | uniq -c | sort -rn | head -20
```

如果没有结果，注明"本周无新增 TODO"。

**当前代码库中遗留的 TODO（用 Glob + Grep 替代裸 grep）**:
先用 Glob 找到项目中的源码文件，再用 Grep 搜索：

```bash
grep -rn "TODO\|FIXME" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx" --include="*.py" --include="*.rs" --include="*.go" --include="*.java" --include="*.vue" --include="*.html" --include="*.css" . 2>/dev/null | head -30
```

如果项目有其他主要语言，调整 `--include` 模式。

### 4. 收集分支和标签

```bash
git log --since="${MONDAY}T00:00:00" --until="${TOMORROW}T00:00:00" --oneline --decorate --no-merges | grep -oP '(tag:\s*\S+|HEAD -> \S+|\S+/\S+)' | sort -u | head -20
```

### 5. 生成周报文件

将收集到的数据填入以下模板，写入项目根目录。

**文件名**: `weekly-report-${TODAY}.md`

**模板**:

```markdown
# 周报: $MONDAY ~ $TODAY

## 概览

| 指标 | 数值 |
|------|------|
| 周期 | $MONDAY ~ $TODAY |
| 总提交数 | $TOTAL_COMMITS |
| 贡献者数 | $AUTHOR_COUNT |

## 提交记录

### 按作者统计

| 作者 | 提交数 |
|------|--------|
$AUTHOR_STATS

### 提交详情

$COMMIT_DETAILS

## TODO 变更

### 本周新增 TODO

$NEW_TODOS

### 当前未完成的 TODO（前 30 条）

$OPEN_TODOS

## 变更文件

### 统计

$FILE_CHANGE_STATS

### 高频变更文件

$TOP_FILES

---

*由 weekly-report-generator 自动生成于 $(date '+%Y-%m-%d %H:%M:%S')*
```

#### 模板填充规则

**提交详情格式化** — 按日期分组，每条提交前加类型标签：

根据提交信息推断类型：
- **feat**: 以 `feat:`、`add`、`新增`、`添加` 开头
- **fix**: 以 `fix:`、`bug`、`修复`、`hotfix`、`patch` 开头
- **refactor**: 以 `refactor:`、`重构`、`clean`、`rewrite` 开头
- **docs**: 以 `docs:`、`doc:`、`readme`、`文档` 开头
- **chore**: 以 `chore:`、`deps:`、`bump`、`update` 开头
- **test**: 以 `test:`、`spec:` 开头
- **style**: 以 `style:`、`format:` 开头
- **other**: 无法归类时使用

格式: `- **[<type>]** <commit message> — *<author>`

按日期分组：
```markdown
#### YYYY-MM-DD

- **[feat]** 添加用户登录功能 — *zhangsan*
- **[fix]** 修复密码验证bug — *zhangsan*
```

**TODO 列表格式**:
```markdown
- [ ] `<file:line>` — TODO 内容
```

遗留 TODO 超过 30 条时，只取前 30 条并在末尾加 `... 共 N 条`。

**变更文件格式** — 列出变更最多的前 10 个文件：
```markdown
| 文件 | 变更行数 |
|------|----------|
| src/foo.ts | +12 -3 |
```

### 6. 保存报告

将生成的 Markdown 内容写入项目根目录下的 `weekly-report-${TODAY}.md`。

完成后告知用户文件路径、提交总数、TODO 变化概况。

## 注意事项

- 如果本周（周一到今天）没有任何 git 提交，生成一份空报告，在概览中标注"本周无提交"，并提示用户确认时间范围是否正确。
- 如果仓库没有 git 历史（初始提交之前），直接提示"当前仓库无提交记录"并退出。
- 扫描 TODO 时只关注源码文件，跳过 `node_modules/`、`.git/`、`dist/`、`build/`、`target/` 等目录。
- 对大型仓库（提交数 > 200），提交详情只列出最近 50 条，并注明"共 N 条提交，仅显示最近 50 条"。
