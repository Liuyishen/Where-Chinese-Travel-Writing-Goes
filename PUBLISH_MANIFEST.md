# GitHub 发布清单

## 现在可以上传

| 路径 | 用途 |
|---|---|
| `README.md` | 研究问题、范围、数据边界与复现入口 |
| `docs/methodology.md` | 三层模型、记录单位、地点与版权规则 |
| `docs/data_dictionary.md` | 公共元数据字段与受控词表 |
| `data/public/README.md` | 公共数据发布边界 |
| `data/public/fields.csv` | 可发布 CSV 的字段定义 |
| `scripts/build_public_metadata.py` | 从私有工作簿生成元数据公开版 |
| `scripts/validate_public_release.py` | 提交前检查公开目录中的敏感内容 |
| `scripts/build_rq1_public_release.py` | 从私有 RQ1 工作簿生成可公开的聚合结果 |
| `docs/rq1_place_visibility.md` | RQ1 的当前证据、分母与解释边界 |
| `docs/rq1_findings_20261024.md` | RQ1 冻结档案的地点可见性结论、分母与审计边界 |
| `docs/rq1_author_concentration_20261025.md` | RQ1 作者集中度检验、图表与解释边界 |
| `docs/rq2_mobility_narration_20261025.md` | RQ2 已签署移动与叙事顺序基线、图表与解释边界 |
| `scripts/build_q2_mobility_baseline_release_20261025.py` | 从私有签署工作簿生成 Q2 聚合基线与图表 |
| `docs/rq2_theme_narration_20261025.md` | RQ2 已签署主题、地点状态与叙事功能结论、图表与解释边界 |
| `scripts/build_q2_theme_narration_release_20261025.py` | 从私有关系签署与主题签署工作簿生成 Q2 聚合结果 |
| `docs/rq3_expansion_concentration_20261026.md` | RQ3 已签署国家覆盖与集中度结论、图表与解释边界 |
| `scripts/build_rq3_expansion_concentration_release_20261026.py` | 从私有关系签署与国家/地区处理签署工作簿生成 Q3 聚合结果 |
| `scripts/build_rq3_carrier_profile_release_20261026.py` | 从私有关系签署与载体签署工作簿生成 Q3 严格载体子集聚合结果 |
| `.gitignore` | 排除私有数据、工作簿、缓存和密钥 |
| `LICENSE-CODE` | 代码 MIT 许可 |
| `LICENSE-DATA.md` | 数据与来源的使用边界 |
| `CITATION.cff` | 引用信息 |

## 生成后可以上传，但须人工复核

| 路径 | 前提 |
|---|---|
| `data/public/corpus_metadata_public.csv` | 不含正文、摘要、页图或登录信息；逐批确认来源条款后提交 |
| `outputs/public/coverage_by_country_or_region.csv` | 仅发布聚合统计，确认不含未核 C 类线索 |
| `outputs/public/coverage_by_china_region.csv` | 同上 |
| `data/public/rq1_fulltext_by_decade.csv` | 仅发布全文层按年代的聚合计数，不含原文或证据定位 |
| `data/public/rq1_repeated_places.csv` | 仅发布跨文本地点的实体级计数，不含逐篇关系 |
| `data/public/rq1_bibliographic_signals_by_decade.csv` | 独立发布书目地点信号层的聚合计数，不与全文层合并 |
| `data/public/rq1_candidate_map_points.csv` | 仅发布项目负责人已确认的点状坐标，不替代线面实体 |
| `data/public/rq1_bibliographic_atomic_components.csv` | 发布规则原子化汇总，不将组件误作规范地名或旅行足迹 |
| `data/public/rq1_author_concentration_sensitivity.csv` | 仅发布作者集中度与敏感性聚合指标，不含篇目或正文 |
| `data/public/rq1_leave_one_author_out.csv` | 仅发布逐作者的聚合敏感性结果，不含篇目或正文 |
| `data/public/rq1_author_concentration_summary.json` | 仅发布作者集中度的机器可读汇总 |
| `docs/figures/q1_*_20261025.svg` | RQ1 可复核图表，不含文本、书名或来源链接 |
| `data/public/rq2_mobility_baseline_metrics.csv` | 仅发布签署关系的移动方式与地点状态聚合，不含篇目或正文 |
| `data/public/rq2_mobility_by_era.csv` | 仅发布档案内年代分层聚合，不作总体趋势推断 |
| `data/public/rq2_narrative_sequence_coverage.csv` | 仅发布路线顺序字段覆盖与相邻叙事转换总数，不发布路线或文本级序列 |
| `data/public/rq2_mobility_summary.json` | 仅发布 Q2 机器可读汇总与解释边界 |
| `data/public/rq2_theme_narration_summary.csv` | 仅发布主题、叙事功能与关系支持的聚合计数，不含篇目或正文 |
| `data/public/rq2_theme_by_era.csv` | 仅发布档案内主题分层计数，不作总体趋势推断 |
| `data/public/rq2_theme_mobility_matrix.csv` | 仅发布主题—移动方式关系支持；多主题文本会重复计入对应主题 |
| `data/public/rq2_theme_place_state_matrix.csv` | 仅发布主题—地点状态关系支持；不发布关系级地点数据 |
| `data/public/rq2_theme_narration_summary.json` | 仅发布 Q2 主题/叙事机器可读汇总与解释边界 |
| `data/public/rq3_country_coverage_by_era.csv` | 仅发布已签署国家单元的年代覆盖与多国敏感性计数 |
| `data/public/rq3_country_concentration_by_era.csv` | 仅发布严格国家关系层的集中度聚合指标 |
| `data/public/rq3_country_concentration_sensitivity.csv` | 仅发布全部保留与 visited-only 的集中度敏感性结果 |
| `data/public/rq3_country_summary.json` | 仅发布 Q3 国家口径、总量与解释边界 |
| `docs/figures/rq3_*_20261026.svg` | RQ3 可复核图表，不含文本、书名或来源链接 |
| `data/public/rq3_carrier_coverage_by_era.csv` | 仅发布确认原载类别覆盖和缺口计数，不含篇目或来源链接 |
| `data/public/rq3_carrier_distribution_by_era.csv` | 仅发布严格确认载体子集的类别聚合，不作市场份额推断 |
| `data/public/rq3_carrier_relation_support_by_era.csv` | 仅发布载体子集关联的关系支持聚合，不发布关系级证据 |
| `data/public/rq3_carrier_summary.json` | 仅发布载体子集总量与解释边界 |
| `docs/figures/q2_*_20261025.svg` | RQ2 可复核图表，不含文本、书名或来源链接 |

## 不要上传

| 类型 | 当前示例 |
|---|---|
| 工作母池与原始 Excel | `data/candidate-pool/working/`、下载目录中的 `.xlsx` |
| 全文、扫描件、长摘录 | PDF、图片、复制的正文、馆藏导出 |
| 访问凭据 | Cookie、密码、学校数据库账户、浏览器会话 |
| 未核验来源级线索 | C 类 `source_level_lead` 及其未经拆篇记录 |
| 本地辅助文件 | `.inspect.ndjson`、预览图、缓存、临时地理编码响应 |

## 发布前最后检查

1. 在仓库根目录运行 `python3 scripts/validate_public_release.py`。
2. 人工打开公共 CSV，确认没有全文、个人信息或校内访问地址。
3. 对每个聚合输出确认只使用 A/B 或明确标注为候选的数据。
4. 在 GitHub 网页的文件变更预览中再检查一次，然后才点击 Commit。
