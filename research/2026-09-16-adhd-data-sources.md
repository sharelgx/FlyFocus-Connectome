# FlyFocus Connectome：ADHD 方向补充数据清单

检索日期：2026-09-16（Asia/Shanghai）

## 结论

现有三张 MaleCNS 表已经提供了神经元、递质预测和连接权重。ADHD 方向
真正缺少的是四个数据层：

1. 人类 ADHD 遗传证据；
2. 人类基因到果蝇同源基因的映射；
3. 果蝇细胞类型的基因表达；
4. 可以量化的注意、活动、睡眠和昼夜节律表型。

第一阶段建议补充 **5 个小型或中型参考文件**。暂时不需要下载约
19.5 GB 的逐突触坐标/配对表，也不需要下载单细胞原始 FASTQ。

## 第一阶段：建议补充的 5 个文件

### 1. ADHD GWAS 补充表

- 文件：`41588_2022_1285_MOESM6_ESM.xlsx`
- 大小：9,081,487 bytes（约 8.7 MiB）
- 格式：XLSX，包含 Supplementary Tables 1–20
- 官方来源：[Demontis et al., Nature Genetics 2023](https://www.nature.com/articles/s41588-022-01285-8)
- [直接下载](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41588-022-01285-8/MediaObjects/41588_2022_1285_MOESM6_ESM.xlsx)
- 用途：建立人类 ADHD 风险位点、优先候选基因和证据等级。论文报告
  27 个风险位点，并提出 76 个优先候选基因。

先用补充表，而不是一开始下载完整 GWAS summary statistics。完整统计量
适合以后做 MAGMA、遗传富集或重新计算，不是连接组初筛的必要条件。

### 2. 人类—果蝇同源基因表

- 文件：`dmel_human_orthologs_disease_fb_2026_02.tsv.gz`
- 格式：gzip 压缩 TSV
- 官方来源：[FlyBase FB2026_02 当前发布页](https://flybase.org/downloads/bulkdata)
- [直接下载](https://s3ftp.flybase.org/releases/FB2026_02/precomputed_files/orthologs/dmel_human_orthologs_disease_fb_2026_02.tsv.gz)
- 用途：把 ADHD 人类候选基因转换为果蝇 FBgn ID 和基因符号，并保留
  同源关系证据。它是整条跨物种分析链的主连接表。

### 3. 果蝇人类疾病模型表

- 文件：`human_disease_models_fb_2026_02.tsv.gz`
- 格式：gzip 压缩 TSV
- 官方来源：[FlyBase FB2026_02 当前发布页](https://flybase.org/downloads/bulkdata)
- [直接下载](https://s3ftp.flybase.org/releases/FB2026_02/precomputed_files/human_disease/human_disease_models_fb_2026_02.tsv.gz)
- 用途：判断候选基因是否已有果蝇疾病模型、等位基因、表型或文献证据，
  避免把“存在同源基因”误写成“已经验证与 ADHD 有关”。

### 4. Fly Cell Atlas 精简表达表

- 文件：`FlyCellAtlas_slimmed_gene_expression_fb_2026_02.tsv.gz`
- 格式：gzip 压缩 TSV
- 官方来源：[FlyBase 单细胞表达文件说明](https://wiki.flybase.org/wiki/FlyBase:FilesOverview)
- [直接下载](https://s3ftp.flybase.org/releases/FB2026_02/precomputed_files/genes/FlyCellAtlas_slimmed_gene_expression_fb_2026_02.tsv.gz)
- 用途：快速查看候选基因在 22 类高层级细胞中的平均表达和阳性细胞比例。
  适合先筛神经元、胶质细胞及其他组织，不适合直接定位到某个 MaleCNS
  `bodyId`。

### 5. FlyBase 详细单细胞表达表

- 文件：`scRNA-Seq_gene_expression_fb_2026_02.tsv.gz`
- 格式：gzip 压缩 TSV
- 官方来源：[FlyBase 单细胞表达文件说明](https://wiki.flybase.org/wiki/FlyBase:FilesOverview)
- [直接下载](https://s3ftp.flybase.org/releases/FB2026_02/precomputed_files/genes/scRNA-Seq_gene_expression_fb_2026_02.tsv.gz)
- 用途：提供实验、细胞簇、FBbt 细胞类型、基因、平均表达和表达细胞比例，
  用于把风险基因缩小到更具体的神经元/胶质细胞群。

FlyBase 下载站对自动化请求可能触发 AWS WAF challenge。出现 HTTP 202 时
不代表文件不存在；可从 FlyBase 当前发布页在浏览器中点击下载，或稍后用
浏览器会话获取。下载后应记录 SHA-256。

## 第二阶段：有需要再下载

### Fly Cell Atlas 神经元 H5AD

- 文件：`s_fca_biohub_neuron_10x.h5ad`
- 大小：约 3.8 GB
- [官方页面与下载入口](https://flycellatlas.org/)
- 用途：保留细胞级表达矩阵、聚类、嵌入和注释，适合自行做 Scanpy 分析。
- 判断：有价值，但第一轮候选基因筛选不需要；先用 FlyBase 汇总表。

### Fly Cell Atlas 头部 H5AD

- 文件：`s_fca_biohub_head_10x.h5ad`
- 大小：约 2.5 GB
- [官方页面与下载入口](https://flycellatlas.org/)
- 用途：检查脑内候选基因表达，覆盖神经元以外的头部细胞。
- 判断：作为神经元 H5AD 的补充，不建议两个文件同时先下。

### 成人果蝇全脑单细胞表达矩阵

- 数据集：GEO `GSE107451`
- 推荐的较小入口：57k 细胞 metadata 约 4.4 MB；对应表达矩阵约 209 MB
- [NCBI GEO 补充文件目录](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE107nnn/GSE107451/suppl/)
- 用途：独立验证成年果蝇脑细胞类型表达结果。
- 判断：当 Fly Cell Atlas 与文献结论不一致时再加入。

### PGC ADHD 完整汇总统计

- [Psychiatric Genomics Consortium ADHD 下载页](https://sites.google.com/broadinstitute.org/pgcadhd/downloads)
- 用途：自己做基因层面统计、通路富集和阈值敏感性分析。
- 判断：第一阶段只使用论文补充表；以后确实要重新计算时再下载。

## 行为层：先建立指标，不需要先下载大数据

推荐把模拟和未来湿实验统一到四类指标：

| 维度 | 可测指标 | 参考依据 |
| --- | --- | --- |
| 活动 | 昼夜运动量、夜间过度活动、速度和停顿分布 | DAT、LPHN3、NF1 果蝇研究 |
| 睡眠 | 总睡眠、睡眠潜伏期、片段数、平均 bout 长度 | DAM 红外活动监测范式 |
| 注意 | 干扰刺激下的选择、注意持续时间、反应准确率 | 果蝇视觉注意实验 |
| 昼夜节律 | 明暗周期与恒暗条件的差异 | 多巴胺和时钟回路研究 |

关键论文入口：

- [DAT、LPHN3、NF1 果蝇模型](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804182/)
- [果蝇视觉注意与多巴胺](https://pmc.ncbi.nlm.nih.gov/articles/PMC5003349/)
- [Vision in Flies: Measuring the Attention Span](https://pmc.ncbi.nlm.nih.gov/articles/PMC4744059/)
- [候选基因高通量行为筛选](https://pmc.ncbi.nlm.nih.gov/articles/PMC4934711/)
- [MEF2C、TRAPPC9 与果蝇活动/睡眠](https://pubmed.ncbi.nlm.nih.gov/32046534/)

这些实验支持研究“ADHD 相关内表型”，不能把果蝇行为直接等同于人类
ADHD，也不能用于人的诊断或治疗决策。

## 与 MaleCNS 的实际连接方式

单细胞数据不会直接提供 MaleCNS `bodyId`。第一版应采用分层、带置信度的
映射：

```text
人类 ADHD 候选基因
  -> FlyBase 同源果蝇基因（FBgn）
  -> 单细胞表达的细胞簇 / FBbt 类型
  -> MaleCNS 的 type / class / superclass / vfbId / hemibrainType / mancType
  -> 该细胞群在 connectome-weights 中的上下游回路
  -> 活动、睡眠、注意或昼夜节律假设
```

映射结果至少标记三档：

- **直接**：稳定细胞类型 ID 或权威一一对应；
- **近似**：名称、谱系和递质均一致，但没有逐神经元表达证据；
- **推测**：只有解剖区域或功能相似，不用于强结论。

## 第一批应重点检查的基因轴

不要手工把候选基因写死为最终结论；应从 GWAS 和 FlyBase 文件重新生成。
首轮可用下列已有果蝇证据作为流程阳性对照：

- `SLC6A3 / DAT` 多巴胺转运轴；
- `ADGRL3 / latrophilin`；
- `NF1`；
- `MEF2C`；
- `TRAPPC9`。

它们的作用是验证“人类证据—同源映射—表达—回路—行为指标”流水线是否
能重现已知结果，不代表这五个基因能够解释 ADHD，或优先级永远高于最新
GWAS 结果。

## 建议的项目内目录

```text
data/
├── flat-connectome/              # 已有 MaleCNS 三张表
├── human-adhd/                   # GWAS 补充表；不含个人基因数据
├── flybase/                      # 同源、疾病模型、表达汇总
└── transcriptomics/              # 第二阶段 H5AD/矩阵
metadata/
├── SHA256SUMS
└── SOURCES.md
research/
└── 2026-09-16-adhd-data-sources.md
```

所有下载仍保存在本项目目录内；大数据文件由 `.gitignore` 排除，不上传到
普通 GitHub。GitHub 只保存代码、来源清单、版本、校验值和可复现脚本。
