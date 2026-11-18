# RAE-Datasets

用于共享 10 组研究数据，共 **33,495 个文件，54,282,093,354 字节（约 50.55 GiB）**。

## 下载数据

完整数据以分卷 TAR 文件存放在 [Datasets 2026-11-18 Release](https://github.com/simple291/RAE-Datasets/releases/tag/datasets-2026-11-18)。首次上传完成并通过校验后，该 Release 会公开显示。

每个数据集单独打包，每个分卷不超过 1 GiB。分卷保留原始文件内容、中文名称、目录结构和空目录；LF 下已有的 ZIP 原始包也完整包含。

> GitHub 的 **Code → Download ZIP** 只下载本仓库中的说明和工具，不包含 Release 中的数据文件。

| 原始目录 | 文件数 | 大小 (GiB) | 下载文件前缀 |
|---|---:|---:|---|
| CO3D | 2,465 | 0.549 | CO3D |
| LF | 19,896 | 43.870 | LF |
| HDR-NeRF | 177 | 0.060 | HDR-NeRF |
| LERF | 1,256 | 0.279 | LERF |
| NERFBK | 587 | 0.315 | NERFBK |
| ObjectGS | 7,390 | 3.290 | ObjectGS |
| Real_hollow_search_20261027 | 971 | 1.698 | Real_hollow_search_20261027 |
| TRADE | 751 | 0.432 | TRADE |
| 百岁山 | 1 | 0.019 | baisuishan |
| 蜂蜜 | 1 | 0.042 | fengmi |

## 校验和还原

Release 中的 `packages.json` 列出全部分卷、字节数和 SHA-256。每组数据还提供 `.files.json` 原始文件校验清单，以及 `.package.json` 包元数据。

请下载同一数据集的所有 `.tar.partNNN` 分卷，按编号顺序连接为一个 TAR 文件，再解包。不要把单个分卷当成独立压缩包。自动下载、校验和解包工具将在首次上传时一起提供。
