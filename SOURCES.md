# 论文测试批次的数据来源

下表列出 21 个发布包的原始场景，以及 RAE 项目对该场景实际使用的适配。下载参数使用第一列的场景 ID。掩码描述物体在画面中的轮廓。对于透明物体，轮廓内可以透出背景。图像、掩码、相机和点云的具体文件、划分及坐标约定见各包清单。

| 场景 ID | 数据来源和对象 | 本批采用的适配 |
|---|---|---|
| `baisuishan` | 项目实拍，百岁山水瓶视频 | 按冻结的视角划分发布视频抽帧、轮廓、相机和前背景初始点。 |
| `nerfbk-cup` | 3DOM-FBK，NeRFBK 的 Cup 照片 | 基于照片重建 COLMAP 相机，配准图像与代理掩码，构造前背景初始点。 |
| `co3d-38-1742-5308` | Meta，CO3Dv2，水瓶 `38_1742_5308` | 对齐图像、官方相机和瓶身轮廓，以稀疏云生成物体初始点，另行初始化背景。 |
| `honey` | 项目实拍，`honey_video` 蜂蜜瓶 | 使用对齐的视频帧、相机和经 SAM2.1 跟踪、后处理的瓶身轮廓。 |
| `uco3d-h03-birdcage` | Meta，uCO3D，H03 金属鸟笼 `23-19819-29334` | 沿用校正后的多视角输入及 BiRefNet 代理掩码。细金属丝与间隙的标签有误差。 |
| `uco3d-pink-basket` | Meta，uCO3D，粉色白边篮 `9-9955-3006` | 保留历史输入的相机、视角划分与轮廓，按训练视角的掩码投影选择初始点。 |
| `uco3d-yellow-basket` | Meta，uCO3D，黄色长槽篮 `116-50670-77607` | 保留历史输入的相机、视角划分与轮廓，按训练视角的掩码投影选择初始点。 |
| `uco3d-h01-shopping-basket` | Meta，uCO3D，H01 白色塑料购物篮 `12-10308-28681` | 使用冻结的图像、BiRefNet M0 轮廓、稀疏点和相机。背景点按训练视角筛选。 |
| `lf-basket` | ETH 光场分割数据，Basket 葡萄果篮 | 选取 150 个已标定视角，使用项目归档的代理轮廓和固定划分。 |
| `lf-africa` | 同一光场数据，Africa | 采用归档校正的 150 张轮廓，使用多视角轨迹准备前背景初始点。 |
| `lf-ship` | 同一光场数据，Ship 帆船模型 | 156 个视角保留 9 张历史掩码，另 147 张根据历史轮廓、几何投影和 SAM2 推断。细索和背景灯具处存在局部误分。 |
| `lf-plant` | 同一光场数据，Plant | 保留标定和划分，使用归档代理轮廓与按训练视角筛选的初始点。 |
| `lf-thinplant` | 同一光场数据，Thin Plant | 保留标定和划分，使用归档代理轮廓与按训练视角筛选的初始点。 |
| `lf-torch` | 同一光场数据，Torch | 保留标定和划分，使用归档代理轮廓与按训练视角筛选的初始点。 |
| `objectgs-figurines-chair` | ObjectGS 整理的 LERF-Mask，figurines 中的红色玩具椅 | 选择椅子作为前景。训练使用跟踪轮廓，四个测试视角有手工标注。 |
| `objectgs-headphones` | 3D-OVS，lawn 场景中的耳机 | 选择耳机作为前景，保留该目标的固定训练和测试视角。 |
| `objectgs-teatime` | ObjectGS 整理的 LERF-Mask，teatime | 将茶杯 51 与咖啡杯 103 合并为前景。三个测试视角均有 RGB。只有 `test_0` 有两个杯子的完整联合参考掩码。 |
| `lerf-bouquet` | LERF，bouquet 花束 | 选取编号 1–117 的片段，使用包括花茎和花瓶的修订代理轮廓。 |
| `trade-v004` | TU Wien，TRADE 实拍序列 `v_004` | 将官方扫描模型投影到相机视角，取三只瓶子轮廓的并集。 |
| `hdrnerf-flower` | HDR-NeRF，实拍 flower 曝光组 2 | 使用冻结的单曝光场景和 BiRefNet 前景轮廓。遮挡处的花盆、枝叶边界属于代理标注。 |
| `synthetic-glass` | 项目合成玻璃杯，种子 0 | 沿用原包 96 张 RGB、整杯轮廓、相机、3,700 个物体初始点和 64,000 个背景初始点。材质分区、空背景与换背景真值作为单独的评估资源归档。 |

## 有明确数据许可的上游来源

以下条款分别适用于对应场景中的上游素材。发布包包含本项目整理的选帧、轮廓或点云时，上表同时标明改动内容。

- **CO3Dv2** 由 Meta / Facebook Research 发布。请引用 Jeremy Reizenstein、Roman Shapovalov、Philipp Henzler、Luca Sbordone、Patrick Labatut、David Novotny 的 *Common Objects in 3D*（ICCV 2021）。`co3d-38-1742-5308` 的 CO3Dv2 素材采用 **CC BY-NC 4.0**，再利用时须署名、注明改动，并限非商业使用。[官方数据条款](https://ai.meta.com/datasets/co3d-downloads/) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
- **uCO3D** 由 Meta 发布。请引用 Xingchen Liu 等人的 *UnCommon Objects in 3D*（CVPR 2025）。四个 `uco3d-*` 包的上游视频和标注采用 **CC BY 4.0**，再利用时须署名并注明改动。[官方数据仓库与引用](https://github.com/facebookresearch/uco3d#license) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **NeRFBK** 的发布方为 Fondazione Bruno Kessler 的 3D Optical Metrology 单位（3DOM-FBK）。`nerfbk-cup` 的上游数据采用 **CC BY-NC-SA 4.0**。分享 Cup 的改编数据应署名、说明改动、限非商业使用，并以相同许可分享改编数据。请按上游说明引用 Ziyang Yan、Gabriele Mazzacca、Simone Rigon、Elisa Mariarosaria Farella、Pawel Trybala、Fabio Remondino 的数据论文以及 Fabio Remondino 等人的重建评估论文。[官方数据与许可](https://github.com/3DOM-FBK/NeRFBK#license) · [数据论文](https://doi.org/10.5194/isprs-archives-XLVIII-1-W3-2023-219-2023) · [重建评估论文](https://doi.org/10.3390/rs15143585) · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- **TRADE** 的全称为 *Transparent and Deformable Objects Dataset for Shape and Pose Estimation*，数据创建者 Jean-Baptiste Weibel，发布机构 TU Wien，项目负责人 Markus Vincze。`trade-v004` 的上游数据采用 **CC BY 4.0**，分享时须署名并注明改动。[官方记录与 DOI](https://doi.org/10.48436/j72kx-6fw97) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## 其他上游数据与引用

- **六个 ETH 光场场景**出自 Kaan Yücer、Alexander Sorkine-Hornung、Oliver Wang、Olga Sorkine-Hornung 的 *Efficient 3D Object Segmentation from Densely Sampled Light Fields with Applications to 3D Reconstruction*（ACM Transactions on Graphics，2016）。项目页要求使用图像或结果时引用论文。该页未列出影像的单独许可证。[官方场景下载与论文](https://igl.ethz.ch/projects/light-field-segmentation/)
- **LERF 的 bouquet、figurines、teatime** 源于 Justin Kerr、Chung Min Kim、Ken Goldberg、Angjoo Kanazawa、Matthew Tancik 的 *LERF: Language Embedded Radiance Fields*（ICCV 2023）。figurines 与 teatime 的 LERF-Mask 标注另请引用 Mingqiao Ye 等人的 *Gaussian Grouping*。本项目使用的 ObjectGS 数据适配来源为 Ruijie Zhu 等人的 *ObjectGS*（ICCV 2025）。[LERF 数据项目](https://www.lerf.io/) · [LERF-Mask 标注说明](https://github.com/lkeab/gaussian-grouping/blob/main/docs/dataset.md#1-lerf-mask-dataset) · [ObjectGS 整理的子集](https://github.com/RuijieZhu94/ObjectGS#-dataset-preparation)
- **耳机所在的 lawn** 来自 Kunhao Liu 等人发布的 3D-OVS 数据，场景和标签归属见上游。ObjectGS 在其数据准备说明中同样列出了该来源。[3D-OVS 数据与引用](https://github.com/Kunhao-Liu/3D-OVS) · [ObjectGS 数据准备说明](https://github.com/RuijieZhu94/ObjectGS#-dataset-preparation)
- **HDR-NeRF 的 flower** 为 Xin Huang、Qi Zhang、Feng Ying、Hongdong Li、Xuan Wang、Qing Wang 在 *HDR-NeRF: High Dynamic Range Neural Radiance Fields*（CVPR 2022）中发布的实拍场景。[官方数据入口与引用](https://github.com/xhuangcv/hdr-nerf)

LERF、LERF-Mask、3D-OVS、ObjectGS 和 HDR-NeRF 的上述页面用于追溯数据和标注。模型实现、训练代码或数据加载代码的开源许可证，其适用范围按各上游声明确定。对于百岁山、蜂蜜和合成玻璃杯，来源为本项目归档，本页未为它们另行指定开放许可证。
