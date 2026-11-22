# RAE-Datasets · 论文测试批次

本仓库发布用于 RAE-Fable 与 ObjectGS 对比的 **21 个固定场景**。共 2,341 个训练视角、205 个验证视角、286 个测试视角。每个场景可以单独下载。后续模型微调沿用本版本的测试相机、图像尺寸和视角 ID，便于逐视角比较。[下载论文数据集](https://github.com/simple291/RAE-Datasets/releases/tag/paper-test21-v1) · [固定测试视角](test_views.json) · [数据来源与许可](SOURCES.md)

## 场景

点击名称下载对应场景的 ZIP。完整下载量约 2.66 GiB。

| 数据集 | 场景 ID | 训练 | 验证 | 测试 |
|---|---|---:|---:|---:|
| [百岁山](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/baisuishan.zip) | `baisuishan` | 81 | 9 | 6 |
| [NERFBK 杯子](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/nerfbk-cup.zip) | `nerfbk-cup` | 233 | 26 | 28 |
| [CO3D 水瓶 38_1742_5308](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/co3d-38-1742-5308.zip) | `co3d-38-1742-5308` | 177 | 0 | 25 |
| [蜂蜜 honey_video](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/honey.zip) | `honey` | 50 | 0 | 6 |
| [H03 金属鸟笼 23-19819-29334](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/uco3d-h03-birdcage.zip) | `uco3d-h03-birdcage` | 158 | 21 | 21 |
| [粉色白边镂空篮 9-9955-3006](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/uco3d-pink-basket.zip) | `uco3d-pink-basket` | 152 | 19 | 20 |
| [黄色长槽沥水篮 116-50670-77607](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/uco3d-yellow-basket.zip) | `uco3d-yellow-basket` | 144 | 18 | 19 |
| [H01 白色购物篮 12-10308-28681](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/uco3d-h01-shopping-basket.zip) | `uco3d-h01-shopping-basket` | 158 | 21 | 21 |
| [葡萄果篮 Basket](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/lf-basket.zip) | `lf-basket` | 120 | 15 | 15 |
| [Africa](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/lf-africa.zip) | `lf-africa` | 120 | 15 | 15 |
| [Ship](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/lf-ship.zip) | `lf-ship` | 124 | 16 | 16 |
| [Plant](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/lf-plant.zip) | `lf-plant` | 120 | 15 | 15 |
| [Thinplant](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/lf-thinplant.zip) | `lf-thinplant` | 114 | 14 | 15 |
| [Torch](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/lf-torch.zip) | `lf-torch` | 106 | 13 | 14 |
| [figurines 红色玩具椅](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/objectgs-figurines-chair.zip) | `objectgs-figurines-chair` | 123 | 0 | 4 |
| [耳机 Headphones](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/objectgs-headphones.zip) | `objectgs-headphones` | 31 | 0 | 5 |
| [teatime 茶杯与咖啡杯](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/objectgs-teatime.zip) | `objectgs-teatime` | 59 | 0 | 3 |
| [bouquet 花束](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/lerf-bouquet.zip) | `lerf-bouquet` | 102 | 0 | 15 |
| [v_004 三瓶](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/trade-v004.zip) | `trade-v004` | 56 | 0 | 8 |
| [flower 曝光组 2](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/hdrnerf-flower.zip) | `hdrnerf-flower` | 29 | 3 | 3 |
| [合成玻璃杯](https://github.com/simple291/RAE-Datasets/releases/download/paper-test21-v1/synthetic-glass.zip) | `synthetic-glass` | 84 | 0 | 12 |
| **合计** | **21 个场景** | **2341** | **205** | **286** |

## 下载与校验

使用 Python 3.9 或以上版本。场景和文件大小可离线查询。

```shell
git clone https://github.com/simple291/RAE-Datasets.git
cd RAE-Datasets
python -m pip install requests
python download_datasets.py --list
python download_datasets.py --dataset synthetic-glass --dataset nerfbk-cup --output Datasets
```

省略 `--dataset` 会下载全部 21 个场景。`--download-only` 仅缓存 ZIP，`--cache` 可指定缓存目录。下载脚本支持断点续传，对照固定清单校验每包的字节数和 SHA-256，再还原到 `Datasets/<场景 ID>/`。也可以从上表直接下载 ZIP，用仓库根目录的校验表手动核对。[包清单](datasets.json) · [SHA-256](SHA256SUMS)

## 文件与评测

每个场景包含原尺寸 RGB、逐帧相机内外参、可用掩码，以及训练时的前景与背景初始点云。`adaptation_manifest.json` 中的相对路径定位各类输入，`split.json` 记录固定划分。数据包还包含逐文件 SHA-256。合成玻璃杯的折射材质、背景与换背景真值单列在 `evaluation_only/`，仅用于评估。

微调实验使用训练视角更新参数，验证视角用于选择配置。报告结果时按 `test_views.json` 使用相同的相机和原图尺寸，先在场景内对逐视角指标等权平均，再对 21 个场景等权汇总。实际调整应记录模型版本、配置及所用验证视角。验证集为 0 的场景可从训练集另留验证帧，并记录帧 ID。

LF Ship 的 156 张轮廓中，9 张来自历史掩码，147 张通过原始网格提示与 SAM2 补齐，细索边缘可能有误分。teatime 以玻璃茶杯和咖啡杯的并集作为前景，3 个测试视角都有 RGB，完整并集参考掩码仅 `test_0` 有效。各来源的署名、引用、适配和使用条件见[来源说明](SOURCES.md)。
