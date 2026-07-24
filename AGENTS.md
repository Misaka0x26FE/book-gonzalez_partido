# AGENTS.md — gonzalez-partido 翻译项目

## 项目概览

| 项目 | 内容 |
|------|------|
| 书名 | *El Partido de la Revolución: Institución y conflicto (1928-1999)* |
| 中文书名 | 革命之党：制度与冲突（1928-1999） |
| 作者 | Miguel González Compeán, Leonardo Lomelí Vanegas (coordinadores) |
| 合作者 | Pedro Salmerón Sanginés |
| 出版社 | Fondo de Cultura Económica |
| 出版年份 | 2000 |
| 源语言 | 西班牙语 |
| 源文件 | `gonzalez-partido.pdf` (820页, 47732512 bytes) |
| 源类型 | Internet Archive 数字化 (Scribe 4.5) |
| 分析文件 | `革命之党_分析.md` |

### 三部曲定位

| 项目 | 状态 | 内容 |
|------|------|------|
| hernandez-pri | ✅ EPUB已完成 | PRI 简史（2016），入门导读 |
| krauze-mexico | ✅ EPUB已完成 | 墨西哥政治权力通史（1998），宏观背景 |
| **gonzalez-partido** | **⬜ 翻译中** | PRI 制度史（2000），最详尽的内部制度研究 |

### 当前阶段

```
book-analyze ✅ → doc-prep ✅ → translate ⬜ → doc-build ⬜ → epub-qa ⬜
```

---

## 项目结构

```
gonzalez-partido/
├── gonzalez-partido.pdf         # 源 PDF
├── 革命之党_分析.md               # book-analyze 产出
├── _原始.txt                     # pdftotext -layout 提取 (33587行)
├── _原始_clean.md                # 清洗后 (4175行, 1.83M字)
├── AGENTS.md                    # 本文件
├── split/                       # 源分片 (166片, 25行/片)
│   ├── 0001.md ~ 0166.md
├── split_translated/            # 译分片 (待翻译)
├── _reports/                    # 子代理报告 (待创建)
├── scripts/
│   ├── clean_pdf_text.py        # PDF 清洗脚本 (v2, 支持3行标题合并)
│   └── split_md.sh              # 切片脚本 (从 krauze-mexico 复制)
├── templates/
│   └── translate_chunk.md       # 西语→中文翻译模板
├── GLOSSARY.csv                 # 91条术语 (含跨书共用)
└── .progress                    # 进度追踪 (166片: pending)
```

---

## 章节-分片映射表

| # | 章节 | 中文标题 | 分片范围 | 片数 | 字数 |
|---|------|----------|----------|------|------|
| — | Agradecimientos | 致谢 | 0001 | 1 | 2,795 |
| — | Introducción | 引言：革命的政党及其组织 | 0001-0004 | 4 | 50,983 |
| 1 | I. La fundación (1928-1933) | 第一章：建党（1928-1933） | 0004-0015 | 11 | 179,188 |
| 2 | II. De partido de élites al partido de masas (1933-1938) | 第二章：从精英政党到群众政党（1933-1938） | 0015-0022 | 7 | 107,493 |
| 3 | III. El partido de la unidad nacional (1938-1945) | 第三章：民族团结的政党（1938-1945） | 0022-0029 | 7 | 122,264 |
| 4 | IV. El conflicto y las instituciones: La Revolución con objetivos (1946-1952) | 第四章：冲突与制度：有目标的革命（1946-1952） | 0029-0036 | 7 | 91,773 |
| 5 | V. La consolidación del sistema político mexicano: El periodo de Adolfo Ruiz Cortines | 第五章：墨西哥政治体制的巩固：阿道弗·鲁伊斯·科尔蒂内斯时期 | 0036-0044 | 8 | 107,852 |
| 6 | VI. La presidencia de Alfonso Corona del Rosal | 第六章：阿方索·科罗纳·德尔·罗萨尔的党主席任期 | 0044-0056 | 12 | 128,587 |
| 7 | VII. La presidencia de Carlos A. Madrazo | 第七章：卡洛斯·A·马德拉索的党主席任期 | 0056-0063 | 7 | 83,695 |
| 8 | VIII. El interinato de Lauro Ortega y la presidencia de Alfonso Martínez Domínguez | 第八章：劳罗·奥尔特加的过渡期与阿方索·马丁内斯·多明格斯的党主席任期 | 0063-0068 | 5 | 70,351 |
| 9 | IX. El PRI durante el gobierno de Luis Echeverría | 第九章：路易斯·埃切维里亚政府时期的革命制度党 | 0068-0078 | 10 | 110,359 |
| 10 | X. En el sexenio de la Reforma Política | 第十章：政治改革的六年任期 | 0078-0088 | 10 | 97,924 |
| 11 | XI. La nueva clase política (1982-1988) | 第十一章：新政治阶级（1982-1988） | 0088-0096 | 8 | 122,938 |
| 12 | XII. La legitimidad de la Revolución y la sociedad civil: La presidencia de Luis Donaldo Colosio | 第十二章：革命的合法性与公民社会：路易斯·多纳尔多·科洛西奥的党主席任期 | 0096-0102 | 6 | 111,906 |
| 13 | XIII. Refundación frustrada, liberalismo social y violencia política (1992-1994) | 第十三章：受挫的重建、社会自由主义与政治暴力（1992-1994） | 0102-0107 | 5 | 98,652 |
| 14 | XIV. La distancia necesaria y lo inevitable de la cercanía (1994-1999) | 第十四章：必要的距离与不可避免的接近（1994-1999） | 0107-0115 | 8 | 80,931 |
| — | Epílogo | 尾声 | 0115-0116 | 1 | 16,782 |
| — | Anexos | 附录（农民/工人/人民部门组织史） | 0116-0160 | 44 | 158,309 |
| — | Bibliografía | 参考文献 | 0160-0161 | 1 | 20,128 |
| — | Índice onomástico | 人名索引 | 0161-0166 | 6 | 66,116 |

---

## 翻译批次计划

### 主体翻译（批次 1-15，优先级高）

| 批次 | 分片范围 | 章节 | 片数 | 翻译策略 |
|------|----------|------|:----:|----------|
| 1 | 0001-0004 | 致谢 + 引言 | 4 | 正常翻译，建立西语术语基线 |
| 2 | 0004-0015 | 第一章：建党 | 11 | 正常翻译 |
| 3 | 0015-0022 | 第二章：从精英到群众 | 7 | 正常翻译 |
| 4 | 0022-0029 | 第三章：民族团结 | 7 | 正常翻译 |
| 5 | 0029-0036 | 第四章：冲突与制度 | 7 | 正常翻译 |
| 6 | 0036-0044 | 第五章：政治体制巩固 | 8 | 正常翻译 |
| 7 | 0044-0056 | 第六章：科罗纳党主席任期 | 12 | 正常翻译 |
| 8 | 0056-0063 | 第七章：马德拉索党主席任期 | 7 | 正常翻译 |
| 9 | 0063-0068 | 第八章：过渡期与多明格斯 | 5 | 正常翻译 |
| 10 | 0068-0078 | 第九章：埃切维里亚时期 | 10 | 正常翻译 |
| 11 | 0078-0088 | 第十章：改革六年任期 | 10 | 正常翻译 |
| 12 | 0088-0096 | 第十一章：新政治阶级 | 8 | 正常翻译 |
| 13 | 0096-0102 | 第十二章：合法性与社会 | 6 | 正常翻译 |
| 14 | 0102-0107 | 第十三章：受挫的重建 | 5 | 正常翻译 |
| 15 | 0107-0116 | 第十四章 + 尾声 | 9 | 正常翻译 |

### 附录处理（批次 16-17，优先级中/低）

| 批次 | 分片范围 | 章节 | 片数 | 翻译策略 |
|------|----------|------|:----:|----------|
| 16 | 0116-~0135 | 附录叙事+委员会名单 | ~20 | 文本部分正常翻译；委员会名单：译机构/职衔，姓名保留原文 |
| 17 | ~0135-0166 | 附录表格 + 参考文献 + 人名索引 | ~32 | 表格 OCR 乱码严重的仅译可识别列标题；参考文献保留原文；人名索引完全保留 |

### 收尾（翻译完成后）

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | `python3 scripts/unify_terms.py --csv GLOSSARY.csv --dir split_translated/` | 全局术语统一 |
| 2 | `bash ../krauze-mexico/scripts/qc_check.sh split_translated/` | 质量检查 |
| 3 | `bash ../krauze-mexico/scripts/merge_md.sh "革命之党" "Miguel González Compeán / Leonardo Lomelí Vanegas" "译者名" "Fondo de Cultura Económica" "2000"` | 合并分片 |
| 4 | 用 doc-build skill 生成 EPUB | 最终输出 |

---

## 翻译规则

### 格式规则
- 保留所有 markdown 格式：**加粗**、*斜体*、图片、链接、列表、表格、引用块
- 空行保留：段落、标题、引用块、列表等块级元素之间至少一个空行
- 引号：`"..."` → `「...」`，嵌套用 `「...『...』...」`
- 书名号：`« »` → `《 》`
- 脚注：`[^n]` 保留编号不翻译，`[^n]: 内容` 仅翻译内容部分

### 术语规则
- 优先使用 GLOSSARY.csv 的标准译法
- 政党组织缩写（PNR/PRM/PRI/CTM/CNC/CNOP）：保留原文缩写，首次出现加括号中文全称
  - 例：PNR（Partido Nacional Revolucionario，国民革命党）
- 人物名：首次出现时音译 + 括号保留原文，之后用中文译名
- 新术语出现时：写入 GLOSSARY.csv

### 引用块规则（遵循 markdown-spec）
- 诗歌/延伸性文学引用 → 保留 `*...*` 包裹（build 阶段统一转 `>`）
- 章节按语、他人言论、文献原文引用、注释段落 → 翻译时即用 `>` 前缀

### 附录特殊规则
- **委员会名单（0130-0150 区）**：
  - `Presidente:` → `主席：`
  - `Secretario General:` → `秘书长：`
  - `Secretario de Acción Agraria:` → `农业事务部长：`
  - 人名保持原文（例：Gral. Plutarco Elías Calles）
- **选举统计表（0150 以后）**：仅翻译可识别的列标题，数字/数据保持原样
- **参考文献**：作者名/书名/出版信息全部保留原文
- **人名索引**：完全保留原文，仅翻译 `ÍNDICE ONOMÁSTICO` 标题为 `## 人名索引`

### 输出格式
- 只输出译文，不要任何解释、摘要或术语说明
- 子代理（如使用）返回译文和提示给主代理，主代理审核后写入 `split_translated/`

---

## 关键脚本

```bash
# 清洗
python3 scripts/clean_pdf_text.py

# 切片
bash scripts/split_md.sh _原始_clean.md 25 split/

# 术语统一
python3 scripts/unify_terms.py --csv GLOSSARY.csv --dir split_translated/

# 质量检查
bash ../krauze-mexico/scripts/qc_check.sh split_translated/

# 合并
bash ../krauze-mexico/scripts/merge_md.sh "革命之党" "作者" "译者" "出版社" "2000"

# 进度查看
echo "已完成: $(grep -c ':done$' .progress) / 总分片: $(wc -l < .progress)"
echo "待译: $(grep -c ':pending$' .progress)"
ls split_translated/*.md | wc -l
```

---

## 已知问题与注意事项

### 清洗阶段已知问题
1. **第8章 Roman numeral 异常**：PDF 原文写的是 `VII. EL INTERINATO DE LAURO ORTEGA`（而非 `VIII.`），已在 TITLE_MAP 中添加别名
2. **OCR 残留**：
   - `BS` 作为页码残留（已用 `\bBS\b` 正则清除）
   - `delos` → `de los`, `delas` → `de las` 等西语OCR粘连（已修复）
3. **选举统计表 OCR 乱码**：~0150-0160 区的多列表格 pdftotext 无法正确处理，数据不可读，翻译时跳过

### 翻译注意事项
1. **第九章标题 OCR**：章节首页标题写为 `EL PRIDURANTE EL GOBIERNO`，实为 `EL PRI DURANTE EL GOBIERNO`
2. **West African 编码问题**：部分字符在 pdftotext 输出中出现 Mojibake，已由清洗脚本处理
3. **附录乱码**：0150-0159 区间存在大量不可读的 OCR 乱码，翻译时仅保留结构

### 恢复翻译时的检查项
```bash
# 1. 检查 .progress 确认进度
cat .progress | grep -c ':done'     # 已完成片数
cat .progress | grep -c ':pending'  # 待译片数
cat .progress | tail -10            # 最近状态

# 2. 检查译文目录
ls split_translated/*.md | wc -l   # 确认与 .progress 一致

# 3. 从第一个 pending 片继续
# 示例：从批次 N 开始
# milestone: batch-N-start
```

---

## 翻译 Prompt 模板

以下为标准提示词，翻译每批时使用：

```
你是西班牙语→中文翻译专家，专精学术文献翻译。

## 翻译要求
1. 保留所有 markdown 格式（**加粗**、*斜体*、图片、链接、列表、表格）
2. 术语优先使用以下标准译法：
   {GLOSSARY.csv 内容}
3. 引用块：诗歌/文学引用保留 *...*，他人言论/文献引用使用 >
4. 外文保留：西班牙语之外的片段（英语、法语等）保持原文
5. 脚注：[^n] 保留编号，仅翻译内容
6. 书名号 «» → 《》，引号 "" → 「」
7. 只输出译文，不要任何解释

## 待翻译内容
{分片内容}
```

每批翻译 5-10 片，主代理并行读取源分片、翻译后写入 `split_translated/`、更新 `.progress`。

---

## Todo 清单

### 翻译前准备
- [ ] 创建 `_reports/` 目录
- [ ] 确认 `split_translated/` 目录存在
- [ ] 确认 `.progress` 全部为 pending

### 主体翻译（批次 1-15）
- [ ] **批次 1**: 0001-0004 致谢 + 引言 (4片)
- [ ] **批次 2**: 0004-0015 第一章 (11片)
- [ ] **批次 3**: 0015-0022 第二章 (7片)
- [ ] **批次 4**: 0022-0029 第三章 (7片)
- [ ] **批次 5**: 0029-0036 第四章 (7片)
- [ ] **批次 6**: 0036-0044 第五章 (8片)
- [ ] **批次 7**: 0044-0056 第六章 (12片)
- [ ] **批次 8**: 0056-0063 第七章 (7片)
- [ ] **批次 9**: 0063-0068 第八章 (5片)
- [ ] **批次 10**: 0068-0078 第九章 (10片)
- [ ] **批次 11**: 0078-0088 第十章 (10片)
- [ ] **批次 12**: 0088-0096 第十一章 (8片)
- [ ] **批次 13**: 0096-0102 第十二章 (6片)
- [ ] **批次 14**: 0102-0107 第十三章 (5片)
- [ ] **批次 15**: 0107-0116 第十四章 + 尾声 (9片)

### 附录处理（批次 16-17）
- [ ] **批次 16**: 0116-~0135 附录叙事 + 委员会名单 (~20片)
- [ ] **批次 17**: ~0135-0166 附录表格 + 参考文献 + 人名索引 (~32片)

### 翻译后收尾
- [ ] 合并新术语到 GLOSSARY.csv（从翻译过程中收集）
- [ ] 运行 `unify_terms.py` 全局术语统一
- [ ] 运行 `qc_check.sh` + `translate-qa` 质量审查
- [ ] 运行 `merge_md.sh` 合并分片
- [ ] 用 doc-build skill 生成 EPUB
- [ ] 更新 `革命之党_分析.md` 定稿声明
