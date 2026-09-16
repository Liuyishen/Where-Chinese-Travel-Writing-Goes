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
