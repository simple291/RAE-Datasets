# RAE-Datasets

用于共享 10 组研究数据，共 **33,495 个文件，54,282,093,354 字节（约 50.55 GiB）**。

## 下载数据

完整数据以分卷 TAR 文件存放在 [Datasets 2026-11-18 Release](https://github.com/simple291/RAE-Datasets/releases/tag/datasets-2026-11-18)。全部数据分卷已上传，并通过 SHA-256 校验。

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

请下载同一数据集的所有 `.tar.partNNN` 分卷，按编号顺序连接为一个 TAR 文件，再解包。不要把单个分卷当成独立压缩包。也可以使用下面的自动下载、校验和解包工具。

## 自动下载与解包

使用 Python 3.9 或以上版本。先获取说明和下载脚本，再运行下载：

```bash
git clone https://github.com/simple291/RAE-Datasets.git
cd RAE-Datasets
pip install requests
python download_datasets.py --output Datasets
```

只下载指定目录，例如：

```bash
python download_datasets.py --output Datasets --dataset CO3D --dataset 蜂蜜
```

查看目录列表：

```bash
python download_datasets.py --list
```

脚本支持断点下载，自动检查分卷 SHA-256，解包后再次核对原始文件 SHA-256。下载缓存默认保留在 `.rae-datasets-cache`，可通过 `--cache` 指定位置；`--download-only` 只下载，不解包。

下载全部数据并解包需要同时容纳分卷缓存和还原后的文件，请预留约 110 GiB 空间。



