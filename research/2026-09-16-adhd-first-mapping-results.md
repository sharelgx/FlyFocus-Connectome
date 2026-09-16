# ADHD 方向第一版映射结果

生成日期：2026-09-16

## 已完成的数据链

```text
Demontis 2023 ADHD 基因证据
  -> FlyBase FB2026_02 人类—果蝇同源关系
  -> Fly Cell Atlas 高层细胞表达
  -> FlyBase 成年神经系统单细胞簇表达

MaleCNS 神经递质预测
  -> 多巴胺证据分层
  -> MaleCNS bodyId、细胞类型与解剖注释
```

这两条链目前并行保存。单细胞簇不能被伪装成某个 MaleCNS `bodyId` 的
逐神经元基因表达测量。

## 结果规模

| 项目 | 数量 |
| --- | ---: |
| Supplementary Table 7 credible-set mapped genes | 76 |
| Supplementary Table 13 MAGMA genes | 45 |
| 文献阳性对照 | 5 |
| 去重后人类候选/对照基因 | 107 |
| 有 FlyBase 果蝇同源关系的人类基因 | 74 |
| 暂无 FlyBase 同源匹配的人类基因 | 33 |
| 全部同源关系行 | 177 |
| 不同果蝇基因 | 149 |
| 最高 DIOPT 优先行 | 79（74个人类基因；部分并列） |
| 详细单细胞源表扫描行数 | 29,015,086 |
| 保留的成年神经系统表达行 | 153,959 |

## 阳性对照是否正确落地

| 人类基因 | FlyBase最高DIOPT果蝇基因 | DIOPT |
| --- | --- | ---: |
| `SLC6A3` | `DAT` (`FBgn0034136`) | 12 |
| `ADGRL3` | `Cirl` (`FBgn0033313`) | 10 |
| `NF1` | `Nf1` (`FBgn0015269`) | 14 |
| `MEF2C` | `Mef2` (`FBgn0011656`) | 11 |
| `TRAPPC9` | `brun` (`FBgn0261787`) | 13 |

这一步重现了预期的跨物种阳性对照，因此基因符号和同源连接方向通过了
首轮合理性检查。它不是这些基因与 ADHD 因果关系的独立验证。

## MaleCNS 多巴胺靶神经元

从1,835,518条神经递质记录中得到4,461个不同 `bodyId`：

| 证据层级 | 神经元数 |
| --- | ---: |
| `consensus_dopamine` | 396 |
| `celltype_prediction_only` | 4,062 |
| `individual_prediction_only` | 3 |

4,461个 `bodyId` 均成功连接到 MaleCNS annotation 表；4,457个具有命名
`type`。建议第一轮回路实验先使用396个 consensus 神经元，另外4,065个仅
作为扩展敏感性分析，不把预测值混同为人工确认标签。

## Consensus多巴胺神经元的一跳连接

已流式扫描完整的151,856,684条连接权重，没有把全表一次性展开到内存：

| 项目 | 数量 |
| --- | ---: |
| consensus多巴胺源神经元 | 396 |
| 找到的直接连接边 | 508,063 |
| 不同下游 `bodyId` | 295,138 |
| 总突触权重 | 861,305 |
| 能连接到annotation表的下游神经元 | 40,479 |

未注释碎片承接了32.20%的权重，因此全图统计必须保留“未注释”类别，不能
只看有名称的神经元。另一方面，权重最高的5,000个下游目标中有4,997个能
连接到命名类型或上级分类，足以建立首批可解释子网络。

最强的已命名靶点集中在蘑菇体相关回路：`KCg-m`约占11.85%，随后包括
多类Kenyon细胞、`APL`、`MBON03/05/06/09/11`和`DPM`。排名前两位的单个
下游神经元均为`APL`。这是结构连接富集结果，不等同于ADHD机制或功能因果
证据；后续必须加入随机重连和去除多巴胺节点的对照。

## 生成文件

- `outputs/adhd-human-candidate-genes.csv`：人类候选基因与证据来源。
- `outputs/adhd-human-fly-orthologs.csv`：全部FlyBase同源关系，保留DIOPT分数。
- `outputs/adhd-priority-fly-genes.csv`：每个人类基因的最高DIOPT优先映射。
- `outputs/adhd-flycellatlas-expression-summary.csv`：六类神经相关细胞表达摘要。
- `outputs/adhd-adult-nervous-scrna-expression.csv`：成年神经系统详细表达长表。
- `outputs/malecns-dopamine-target-neurons.csv`：直接连接MaleCNS `bodyId`的多巴胺靶表。
- `outputs/malecns-consensus-dopamine-downstream-top5000.csv`：最强一跳下游神经元。
- `outputs/malecns-consensus-dopamine-downstream-groups.csv`：按命名类型汇总的一跳权重。
- `outputs/adhd-mapping-summary.json`、`outputs/malecns-dopamine-target-summary.json`：机器可读统计。

46 MB的详细表达长表以及所有原始数据保存在项目硬盘目录，但由 `.gitignore`
排除。GitHub保存生成脚本、来源、校验值、小型结果表和本报告。

## 当前边界和下一步

当前可以研究“ADHD遗传候选轴是否集中表达于某类果蝇神经细胞”以及
“MaleCNS多巴胺神经元连接到哪些下游回路”。目前不能声称某个风险基因在
某个具体 `bodyId` 中表达。

下一步应以已经提取的一跳网络为起点，生成：

1. 蘑菇体、中央复合体、视觉和昼夜节律相关回路的覆盖；
2. 原图、随机重连图和去除多巴胺节点三种对照；
3. 可用于活动、睡眠和视觉注意模拟的首批子网络；
4. 对未注释下游碎片做纳入/排除敏感性分析。
