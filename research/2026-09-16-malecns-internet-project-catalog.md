# MaleCNS 互联网趣味项目清单

检索日期：2026-09-16（Asia/Shanghai）

这是一份尽量全面、但不能保证穷尽整个互联网的动态清单。2026 年 9 月 MaleCNS 论文发布后，相关仓库在数日内快速增长；以 GitHub `MaleCNS` 关键词检索时约有 158 个仓库。大量条目仍是原型、README 自述或社交媒体展示，不能据此认定它们具有生物学真实性或已经成功复现。

## 证据标签

- **官方**：数据发布方或论文作者维护。
- **研究基础**：论文、成熟工具或明确的分析/仿真基础设施。
- **开源实验**：有公开代码；此清单未逐个完成本机复现。
- **新近原型**：近期出现，主要依据仓库 README/描述，需进一步审计。
- **社媒展示**：主要证据是 X、Reddit、YouTube 或新闻嵌入视频。
- **计划接入**：当前仓库尚未真正接入 MaleCNS，不应算完成项目。

## 0. 持续更新的总索引

1. [Awesome Fly](https://github.com/cobanov/awesome-fly) — 当前最清晰的人工整理清单，区分 MaleCNS、FlyWire、子回路、身体模型和科学限制。
2. [Awesome Fruit Fly](https://github.com/townie/awesome-fruit-fly) — 更宽的发现清单，收录游戏、艺术、交易、社媒项目和未验证搜索分片。
3. [GitHub: MaleCNS repositories](https://github.com/search?q=MaleCNS&type=repositories) — 实时关键词搜索，噪声较多但更新最快。
4. [MaleCNS 官方主页](https://male-cns.janelia.org/) — 官方探索、数据、neuPrint、Clio、细胞类型和雌雄差异入口。
5. [MaleCNS 官方下载页](https://male-cns.janelia.org/download/) — Feather、突触、骨架、Neo4j、图像体数据和编程接口。

## 1. 官方与论文配套项目

1. **官方** [janelia-flyem/male-cns](https://github.com/janelia-flyem/male-cns) — MaleCNS 项目网站与 Dimorphism Explorer 源码。
2. **官方** [flyconnectome/2025malecns](https://github.com/flyconnectome/2025malecns) — Berg 等论文的补充数据、眼柱映射和分析笔记本。
3. **官方/研究基础** [natverse/malecns](https://github.com/natverse/malecns) — R 语言访问 MaleCNS/neuPrint、形态与注释。
4. **研究基础** [funkelab/synister_malecns](https://github.com/funkelab/synister_malecns) — MaleCNS 神经递质预测工作。
5. **研究基础** [MaleCNS Cell Type Explorer](https://reiserlab.github.io/male-cns-cell-type-explorer/) — 细胞类型、连接、脑区和形态浏览。
6. **官方服务** [neuPrint MaleCNS](https://neuprint.janelia.org/) — 在线查询神经元、上下游和连接权重，选择 `male-cns:v1.0`。
7. **官方服务** [Clio](https://clio.janelia.org/) — 注释中心的筛选与浏览。
8. **官方服务** [Dimorphism Explorer](https://male-cns.janelia.org/build/dimorphism_overview/) — 雄性、雌性和性二态细胞类型对照。
9. **官方展示** [MaleCNS Media Gallery](https://male-cns.janelia.org/gallery/) — 官方图像和视频素材。
10. **论文/数据** [Sexual dimorphism in the complete Drosophila male CNS connectome](https://doi.org/10.1016/j.cell.2026.08.015) — MaleCNS 主论文。

## 2. 仿真内核、分析库和研究工具

1. **研究基础** [philshiu/Drosophila_brain_model](https://github.com/philshiu/Drosophila_brain_model) — Shiu 等全脑 LIF 模型，许多社区项目的动力学来源。
2. **研究基础** [eonsystemspbc/fly-brain](https://github.com/eonsystemspbc/fly-brain) — Brian2、PyTorch、NEST GPU、GeNN 等后端的全脑模拟。
3. **研究基础** [connectome-interpreter](https://github.com/YijieYin/connectome_interpreter) — 有效连接、路径、刺激、回路操作和可微模型。
4. **研究基础** [flyconnectome/cocoa](https://github.com/flyconnectome/cocoa) — 跨 MaleCNS、FlyWire、hemibrain、MANC 的比较连接组学。
5. **研究基础** [navis-org/navis](https://github.com/navis-org/navis) — 神经元骨架、mesh、形态分析和可视化。
6. **研究基础** [navis-org/navis-flybrains](https://github.com/navis-org/navis-flybrains) — 不同果蝇模板空间之间的坐标变换。
7. **研究基础** [connectome-neuprint/neuprint-python](https://github.com/connectome-neuprint/neuprint-python) — Python 查询 neuPrint。
8. **研究基础** [Connecto](https://github.com/schlegelp/connecto) — 统一访问多个连接组后端。
9. **研究基础** [FlyBrainLab](https://github.com/FlyBrainLab) — 回路查询、可执行神经模型和交互实验平台。
10. **研究基础** [flyvis](https://github.com/TuragaLab/flyvis) — 果蝇视觉连接组约束模型、预训练模型和分析教程。
11. **研究基础** [flybody](https://github.com/TuragaLab/flybody) — MuJoCo 果蝇身体、行走/飞行环境和控制示例；本身不是 MaleCNS 脑模型。
12. **研究基础** [FlyGym](https://github.com/NeLy-EPFL/flygym) — NeuroMechFly/FlyGym 身体与感知运动实验平台。
13. **开源实验** [us/connectorch](https://github.com/us/connectorch) — 把 MaleCNS 编译成稀疏、可训练的 PyTorch 网络，带生物权重和随机重连对照。
14. **开源实验** [dhakalnirajan/axonweave](https://github.com/dhakalnirajan/axonweave) — NumPy/PyTorch/TensorFlow 的可训练生物连接底座。
15. **开源实验** [alextitonis/fly.ai](https://github.com/alextitonis/fly.ai) — CPU/Numba 或 GPU/CuPy 的 MaleCNS LIF、视觉编码、储备池、双果蝇通信和浏览器导出。
16. **开源实验** [Kisame76/drosophila-brain-mlx](https://github.com/Kisame76/drosophila-brain-mlx) — Apple Silicon MLX/Metal 全脑 LIF，与 Brian2 对照并提供随机重连控制。
17. **开源实验** [seohyunjun/mps-malecns-model](https://github.com/seohyunjun/mps-malecns-model) — Apple Silicon MPS 上的 MaleCNS 模拟。
18. **开源实验** [Pronexsteam/brainlab](https://github.com/Pronexsteam/brainlab) — FlyWire/FAFB/BANC/MaleCNS 多连接组 GPU 模拟。
19. **开源实验** [franciscocarloserra/fasterfly](https://github.com/franciscocarloserra/fasterfly) — 面向全 MaleCNS 的 Triton 事件驱动 LIF 内核。
20. **开源实验** [itsyuimorii/fly-connectome-webgpu](https://github.com/itsyuimorii/fly-connectome-webgpu) — 浏览器 WebGPU 脉冲网络实验。
21. **开源实验** [freeman-1984-coder/flybrain-sdk](https://github.com/freeman-1984-coder/flybrain-sdk) — CPU LIF、游戏 API、检查点与按需数据下载。
22. **开源实验** [WhiskeyCoder/Barry](https://github.com/WhiskeyCoder/Barry) — MaleCNS 刺激、复制、多世界和实验 API。
23. **新近原型** [timfromhcs/FlyBrain](https://github.com/timfromhcs/FlyBrain) — Vulkan-first 人工生物研究框架。
24. **新近原型** [JangYeongSil69420/malecns-reservoir-computing](https://github.com/JangYeongSil69420/malecns-reservoir-computing) — 全图储备池/液态状态机和时间序列实验。
25. **新近原型** [akramahmed1/malecns-fault-lines](https://github.com/akramahmed1/malecns-fault-lines) — 损伤、最小割和结构韧性分析。
26. **新近原型** [Shih-Yu-Yeh/malecns-topology-prior](https://github.com/Shih-Yu-Yeh/malecns-topology-prior) — 测试 MaleCNS 拓扑是否携带运动检测先验。
27. **新近原型** [praveenVnktsh/flypareto](https://github.com/praveenVnktsh/flypareto) — 全连接组智能/适应度 Pareto 分析。
28. **新近原型** [mait2355n/fly-neuron-atlas](https://github.com/mait2355n/fly-neuron-atlas) — 运动神经元图谱、证据整理和可复现实验。

## 3. 游戏与“让果蝇玩东西”

1. **开源实验** [nftechie/doomfly](https://github.com/nftechie/doomfly) — MaleCNS 接 ViZDoom；视觉输入、下降神经元输出和 PPL101 惩罚。README 同时记录未通过部分学习/生存验证。
2. **开源实验** [Aur1ety/DOOM-x-Fly](https://github.com/Aur1ety/DOOM-x-Fly) — 另一条 Doom 路线，训练小型读出层，公开多次运行结果。
3. **开源实验** [eganeganegan/flydoom](https://github.com/eganeganegan/flydoom) — 连接组约束控制器与随机重连/常规网络对照；部分版本使用 FlyWire 而非 MaleCNS。
4. **开源实验** [ornata/fly](https://github.com/ornata/fly) — Fly64，把 MaleCNS 接到 Super Mario 64。
5. **开源实验** [ksanjeev284/fly-mario](https://github.com/ksanjeev284/fly-mario) — NES Mario、CUDA LIF、递质/多巴胺学习和 3D 面板。
6. **开源实验** [Jhongdlp/FlyBrain](https://github.com/Jhongdlp/FlyBrain) — MaleCNS 驱动游戏 Boss，含逃生反射、Rust 引擎和 Three.js 可视化。
7. **开源实验** [cobanov/flyjump](https://github.com/cobanov/flyjump) — 80 个 MaleCNS 神经元子回路玩原版 Chromium Dino，训练小读出并做静默/保留集测试。
8. **开源实验** [dzhng/fly-escape](https://github.com/dzhng/fly-escape) — 浏览器 3D 房间逃生，Rust/WASM + MaleCNS 子回路。
9. **开源实验** [Yusuftmle/FlyBrain-HalfLife](https://github.com/Yusuftmle/FlyBrain-HalfLife) — Half-Life、60×60 视网膜和 DirectInput。
10. **开源实验** [liuzihe02/fly-craftax](https://github.com/liuzihe02/fly-craftax) — Craftax 生存环境、下降神经元读出与 PPO。
11. **开源实验** [seanphan/flyt3](https://github.com/seanphan/flyt3) — 井字棋、全图 LIF、训练读出、3D Web UI，并扩展到野火图像分类。
12. **开源实验** [charbelkassab/flybrain-snake](https://github.com/charbelkassab/flybrain-snake) — MaleCNS 玩 Snake，强调公开输入输出映射与控制实验。
13. **开源实验** [arjunkshah12345-hash/fly-flappy-bird](https://github.com/arjunkshah12345-hash/fly-flappy-bird) — Flappy Bird、工程适配器和录制结果。
14. **开源实验** [ykakade/flappy-fly-connectome](https://github.com/ykakade/flappy-fly-connectome) — 冻结真实拓扑、PPO 读出与浏览器推理。
15. **新近原型** [ns2250225/fly-flappy](https://github.com/ns2250225/fly-flappy) — 中文 Flappy Bird 训练项目。
16. **新近原型** [Thespaceblade/flappy-fly](https://github.com/Thespaceblade/flappy-fly) — 另一版 MaleCNS Flappy Bird。
17. **新近原型** [rothilion26/flytris](https://github.com/rothilion26/flytris) — 蘑菇体、多巴胺门控可塑性与 Tetris。
18. **新近原型** [on7jya/brain_fly](https://github.com/on7jya/brain_fly) — Tetris + MaleCNS/FAFB 活动可视化。
19. **新近原型** [Kaos599/fly-brain-minesweeper](https://github.com/Kaos599/fly-brain-minesweeper) — 扫雷、PyTorch 和 Three.js HUD。
20. **新近原型** [Aananda-giri/fly-chess](https://github.com/Aananda-giri/fly-chess) — 冻结 MaleCNS + 可训练皮层读出下棋。
21. **新近原型** [lduo8438-max/Chessfly](https://github.com/lduo8438-max/Chessfly) — MaleCNS 脉冲网络对 Stockfish。
22. **新近原型** [nyoki-mtl/fly-shogi](https://github.com/nyoki-mtl/fly-shogi) — 果蝇连接组下将棋。
23. **新近原型** [BOHUYESHAN-APB/flygo](https://github.com/BOHUYESHAN-APB/flygo) — 两个连接组大脑下五子棋。
24. **新近原型** [roymina/Fly_Gomoku](https://github.com/roymina/Fly_Gomoku) — MaleCNS 与 FlyWire 五子棋对照。
25. **新近原型** [KremlevLev/flydurak](https://github.com/KremlevLev/flydurak) — 果蝇连接组玩 Durak 纸牌。
26. **新近原型** [pikabell/fly-tictactoe](https://github.com/pikabell/fly-tictactoe) — 98 细胞 MaleCNS 子回路玩井字棋，带静默与重连控制。
27. **新近原型** [hcsolakoglu/fruit-fly-plays-fruit-ninja](https://github.com/hcsolakoglu/fruit-fly-plays-fruit-ninja) — Fruit Ninja、闭环和轨迹视频。
28. **新近原型** [lntegrals/flycube-public](https://github.com/lntegrals/flycube-public) — 把 MaleCNS 放进魔方求解决策环。
29. **新近原型** [shovon/malecns-v1-dinosaur-game](https://github.com/shovon/malecns-v1-dinosaur-game) — Chrome Dino 教学实验。
30. **新近原型** [Yi-111-a/FlyCraft](https://github.com/Yi-111-a/FlyCraft) — Minecraft 战斗/逃跑 NPC。
31. **新近原型** [shivareddy42/flyway-surfer](https://github.com/shivareddy42/flyway-surfer) — 1,072 神经元子回路驱动 3D 跑酷。
32. **新近原型** [Lak106/flybrain-pilot](https://github.com/Lak106/flybrain-pilot) — 飞行模拟器控制。
33. **新近原型** [tolga-ileri/FlyCoder](https://github.com/tolga-ileri/FlyCoder) — 166,700 个神经元尝试把网页 `div` 居中。
34. **新近原型** [michaelpersonal/flytype](https://github.com/michaelpersonal/flytype) — 打砖块和打字，画面输入驱动连接组。
35. **新近原型** [josepha-mayo/fly-experiment](https://github.com/josepha-mayo/fly-experiment) — 活体果蝇与保留的 MaleCNS 模型共同驱动 Doom/国际象棋的统一接口实验。
36. **新近原型** [Pizzawookiee/catch_the_fly](https://github.com/Pizzawookiee/catch_the_fly) — 你控制青蛙捕捉 MaleCNS 果蝇。
37. **新近原型** [charbelkassab/flybrain-intransitive](https://github.com/charbelkassab/flybrain-intransitive) — 用接近/逃跑回路玩石头剪刀布式对抗。
38. **新近原型** [nikolasandwich/fly-sudoku-expert](https://github.com/nikolasandwich/fly-sudoku-expert) — MaleCNS-inspired 数独演示；“inspired” 不等于完整接入。
39. **新近原型** [Griff1018/MaleCNS-snake-game-training](https://github.com/Griff1018/MaleCNS-snake-game-training) — Snake 框架，作者明确标注训练尚未完成。

## 4. 虚拟身体、机器人、汽车、无人机与世界

1. **开源实验** [Dorian Todd / Fly Brain Bridge](https://www.doriantodd.com/projects/fly-brain-bridge/) — MaleCNS 在 Mac 上运行，通过 Wi-Fi 给 Sesame 机器人发送前进/转向指令。
2. **开源实验** [monomyth/fly-brain-codex](https://github.com/monomyth/fly-brain-codex) — MaleCNS 派生视觉/本体感觉控制器驱动六轴机械臂模拟器；作者明确声明不是生物学验证的果蝇脑。
3. **开源实验** [monomyth/fly-brain-grok](https://github.com/monomyth/fly-brain-grok) — 同一机械臂方向的另一实验分支。
4. **新近原型** [AlexNoyanov/MaleCNS-Driving-Robot](https://github.com/AlexNoyanov/MaleCNS-Driving-Robot) — MaleCNS 驾驶机器人。
5. **计划接入** [Frankweb33/flybrain-robot-bridge](https://github.com/Frankweb33/flybrain-robot-bridge) — 当前已有视觉流、IMU、UDP 机器人桥，但仓库说明 MaleCNS 接入仍是计划。
6. **新近原型** [SpikeCalls/FlyDrones](https://github.com/SpikeCalls/FlyDrones) — 摄像头→复眼→脉冲脑→下降神经元→无人机。
7. **新近原型** [powerOFMAX/fly-parking-lab](https://github.com/powerOFMAX/fly-parking-lab) — 果蝇开 Mini Cooper、MuJoCo WASM 和 3D 停车。
8. **新近原型** [hotocoo/malecns](https://github.com/hotocoo/malecns) — MaleCNS 驾驶 F1 赛车跑摩纳哥赛道。
9. **新近原型** [Robocoprophage](https://github.com/YeshuaGod22/Robocoprophage) — 测试真实连接拓扑是否帮助飞行控制，强调随机重连对照。
10. **新近原型** [binivin/drosophila-connectome-odor-navigation](https://github.com/binivin/drosophila-connectome-odor-navigation) — 气味源导航。
11. **新近原型** [djmango/flyverse](https://github.com/djmango/flyverse) — Rust 全连接组、虚拟房间和浏览器观察器。
12. **新近原型** [artem-x-meta/fly-arena](https://github.com/artem-x-meta/fly-arena) — MaleCNS + FlyGym/MuJoCo，两只果蝇竞争食物。
13. **新近原型** [JayceeB1/flybox](https://github.com/JayceeB1/flybox) — 全连接组和 NeuroMechFly 身体实验平台。
14. **新近原型** [Doga0/flycns-sim](https://github.com/Doga0/flycns-sim) — Brian2 LIF + FlyGym/MuJoCo，仍在开发。
15. **新近原型** [2510034127qq-wq/malecns](https://github.com/2510034127qq-wq/malecns) — Arbor、MuJoCo、Rerun 的全尺度身体实验。
16. **新近原型** [Sylviali-Maker/flybrain-sim](https://github.com/Sylviali-Maker/flybrain-sim) — 中文脑-身体闭环实验台，食物/天敌刺激和果蝇主视角。
17. **新近原型** [Leon-Av/virtual-fly-lab](https://github.com/Leon-Av/virtual-fly-lab) — Godot 4 沙盒中的全 CNS 虚拟果蝇。
18. **新近原型** [tiredbooy/Fruit-Fly](https://github.com/tiredbooy/Fruit-Fly) — 觅食、学习、Gym 实验和 WebGPU 观察站。
19. **新近原型** [AntonioCoppe/flyciv](https://github.com/AntonioCoppe/flyciv) — 果蝇殖民地模拟、冻结大脑与进化适配器。
20. **新近原型** [TingjiaInFuture/malecns-language-world](https://github.com/TingjiaInFuture/malecns-language-world) — 本地 3D 观察世界和完整结构图。
21. **新近原型** [WilliamJones/pet-fly](https://github.com/WilliamJones/pet-fly) — 网页宠物果蝇，自述完整 MaleCNS 实时运行。
22. **新近原型** [VaheOfficial/FLY](https://github.com/VaheOfficial/FLY) — GPU 桌面宠物，键盘、鼠标和窗口成为感官。
23. **新近原型** [So2K/musca-desktop-fly](https://github.com/So2K/musca-desktop-fly) — Windows 桌面果蝇。
24. **新近原型** [fengruochen8/cyberfly](https://github.com/fengruochen8/cyberfly) — macOS 自主桌面果蝇。
25. **新近原型** [Furina-star/mkdir-fly-companion](https://github.com/Furina-star/mkdir-fly-companion) — 对鼠标、打字和空闲状态做反应的小型桌面生物。
26. **新近原型** [PtPavloTkachenko/fly-brain-spectacles](https://github.com/PtPavloTkachenko/fly-brain-spectacles) — Snap Spectacles 上的全息果蝇，Mac 运行 Metal 内核。
27. **新近原型** [MindExtendAI/mindfly](https://github.com/MindExtendAI/mindfly) — EEG 控制果蝇步行、Rust/WASM。
28. **新近原型** [Decentricity/mindmeld-with-fly](https://github.com/Decentricity/mindmeld-with-fly) — Muse EEG 与 MaleCNS 储备池；README 中部分 EEG 接口仍属后续阶段。
29. **新近原型** [whiteram/fly-man-bci](https://github.com/whiteram/fly-man-bci) — 把 MaleCNS 模拟放进人头球体并生成 EEG 的实验。
30. **新近原型** [TailsProwerWorks/PersonConnectome](https://github.com/TailsProwerWorks/PersonConnectome) — People Playground mod，用 MaleCNS 控制人形角色。

## 5. 视觉、互动实验室和可视化

1. **开源实验** [mingdianliu/flybrain-playground](https://github.com/mingdianliu/flybrain-playground) — 可移动刺激、简化脉冲神经元和 3D 活动。
2. **开源实验** [HEREISCB/flybrain](https://github.com/HEREISCB/flybrain) — 浏览器里运行、观察和刺激整只果蝇脑。
3. **开源实验** [PouyanJay/drosophila-lab](https://github.com/PouyanJay/drosophila-lab) — 3D 脑图谱、连接组训练和 PyTorch 实验。
4. **开源实验** [ashemag/fly-brain-atlas](https://github.com/ashemag/fly-brain-atlas) — MaleCNS 区域和神经元重建图谱。
5. **开源实验** [shyoon-devops/fly-connectome-lab](https://github.com/shyoon-devops/fly-connectome-lab) — MaleCNS + NeuroMechFly 浏览器实验室。
6. **开源实验** [juancristobalgd1/flybrain-lab](https://github.com/juancristobalgd1/flybrain-lab) — 实时训练与神经活动可视化。
7. **开源实验** [mertozbas/fruitfly-hashtag](https://github.com/mertozbas/fruitfly-hashtag) — 本地 Neural Lab、回路可视化和指导训练。
8. **开源实验** [NullLabTests/flybrain](https://github.com/NullLabTests/flybrain) — 按钮向真实连接组注入电流并观察电压/放电场。
9. **开源实验** [nathannguyen-coder/fly-arena](https://github.com/nathannguyen-coder/fly-arena) — Colab 和解剖活动浏览器。
10. **开源实验** [Decentricity/connectome-headless-viz](https://github.com/Decentricity/connectome-headless-viz) — 无头 MaleCNS 活动可视化。
11. **新近原型** [AbijahKaj/fruit-fly-brain-research](https://github.com/AbijahKaj/fruit-fly-brain-research) — WebGPU 视叶、1,771 眼柱方向和翅膀输出。
12. **新近原型** [aliozen0/malecns-virtual-brain-lab](https://github.com/aliozen0/malecns-virtual-brain-lab) — LIF、感知运动桥和 WebGL 实验室。
13. **新近原型** [Knaifu0030/fruitfly-simulation](https://github.com/Knaifu0030/fruitfly-simulation) — 数据预处理、可视化和虚拟果蝇基础工程。
14. **新近原型** [rzgrozt/Flybrain-Computer-Interface](https://github.com/rzgrozt/Flybrain-Computer-Interface) — 连接组计算机接口研究平台。
15. **新近原型** [flywatt-live/watt-the-fly](https://github.com/flywatt-live/watt-the-fly) — 用一部分 MaleCNS 放电驱动灯泡和微瓦表。

## 6. 语言、艺术、音乐、社交与奇怪作品

1. **开源实验** [nftechie/flm](https://github.com/nftechie/flm) — 冻结语言模型与完整 MaleCNS 图耦合；语言能力来自语言模型，不是果蝇脑。
2. **新近原型** [alexbuildstech/fly-connectome-lm](https://github.com/alexbuildstech/fly-connectome-lm) — MaleCNS 作为 token-in/token-out 连接组语言模型并与 Transformer 对照。
3. **新近原型** [pbomaster/Fruitfly-reviewer](https://github.com/pbomaster/Fruitfly-reviewer) — 无预训练 LLM 的抽取式论文审阅实验。
4. **新近原型** [crimconsortium/fruitfly](https://github.com/crimconsortium/fruitfly) — 果蝇在 OpenAlex 犯罪学引文图中觅食。
5. **新近原型** [xyzzyapps/faiku](https://github.com/xyzzyapps/faiku) — 蘑菇体强化学习写日英俳句与果蝇字体。
6. **新近原型** [tegnike/fly-typist](https://github.com/tegnike/fly-typist) — 虚拟果蝇打字、日文输入与录像。
7. **新近原型** [andrewevmiller/flybeats](https://github.com/andrewevmiller/flybeats) — 训练 MaleCNS 打鼓。
8. **新近原型** [anloren/fly-dj-malecns](https://github.com/anloren/fly-dj-malecns) — 冻结 MaleCNS LIF + RL DJ 混音器。
9. **新近原型** [radiotedu/radiotedu-djfly](https://github.com/radiotedu/radiotedu-djfly) — 自主音乐体验。
10. **新近原型** [sukoji/flyboard](https://github.com/sukoji/flyboard) — 把 84 首歌曲播放给全 MaleCNS 模拟并生成音乐榜。
11. **新近原型** [gustavz/FLYcasso](https://github.com/gustavz/FLYcasso) — 连接组条件图像扩散与模拟果蝇绘画。
12. **新近原型** [jtc268/fruit-fly-fashion](https://github.com/jtc268/fruit-fly-fashion) — 用 MaleCNS spike 向量控制服装图案位置、旋转和大小。
13. **新近原型** [oskarmalmwiklund/swat-or-buy](https://github.com/oskarmalmwiklund/swat-or-buy) — 把广告创意输入视叶，做前注意显著性评分。
14. **新近原型** [ML-Chen/fruit-fly-utopia](https://github.com/ML-Chen/fruit-fly-utopia) — 给果蝇持续满足刺激的“乌托邦”和享乐指数。
15. **新近原型** [JacobEGarcia/fruit-fly-purgatory](https://github.com/JacobEGarcia/fruit-fly-purgatory) — 无限候诊室艺术装置。
16. **新近原型** [InstarCage/instar](https://github.com/InstarCage/instar) — 多只完整 MaleCNS 果蝇组成持久世界并连接 Solana。
17. **新近原型** [alextitonis/fly.ai](https://github.com/alextitonis/fly.ai) — 还包含双果蝇通过翅膀歌声通信、Flybook 社交 feed 和 3D 世界。
18. **新近原型** [anzal1/samesmell](https://github.com/anzal1/samesmell) — MaleCNS 与 FlyWire 对相同信息素产生不同反应。
19. **新近原型** [amyleesterling/banc_malecns](https://github.com/amyleesterling/banc_malecns) — 雄性 MaleCNS 与雌性 BANC 的“约会”。
20. **新近原型** [hsgwktb/fly-character](https://github.com/hsgwktb/fly-character) — 连接组驱动的数字角色、阈值语音和可观测 Web UI。
21. **新近原型** [Gakpey/MaleCNS_human](https://github.com/Gakpey/MaleCNS_human) — “Fly brain in human”概念实验。

## 7. 金融、交易、市场与区块链（只建议纸上实验）

1. **开源实验** [nftechie/stonkfly](https://github.com/nftechie/stonkfly) — K 线输入、买卖输出、多巴胺奖励；未证明盈利学习。
2. **开源实验** [marketcalls/openfly](https://github.com/marketcalls/openfly) — MaleCNS 接 NIFTY 期权/OpenAlgo；不应视为有效交易策略。
3. **新近原型** [fruitflycap/fruitflycapital](https://github.com/fruitflycap/fruitflycapital) — 多只果蝇、受控 3D 飞行和加密市场世界，README 对尚未完成的自主飞行有明确边界。
4. **新近原型** [Flyextractor/extractor](https://github.com/Flyextractor/extractor) — 美股锁定回测与随机重连对照。
5. **新近原型** [EVERYTHINGAICO/malecns-market-lab](https://github.com/EVERYTHINGAICO/malecns-market-lab) — 预注册 MaleCNS vs 匹配随机储备池、样本外评估。
6. **新近原型** [abigubi/fruit-fly-options-lab](https://github.com/abigubi/fruit-fly-options-lab) — 股息感知看涨期权实验。
7. **新近原型** [armanbabazadeh6/fruit-fly-fund](https://github.com/armanbabazadeh6/fruit-fly-fund) — 两只 MaleCNS 果蝇在同一纸上市场竞赛，一只带实验记忆更新。
8. **新近原型** [davidmcarati/chonchurik](https://github.com/davidmcarati/chonchurik) — Coinbase 守护交易循环，README 明确未展示盈利学习。
9. **新近原型** [Rob-bio4/degeneretfly](https://github.com/Rob-bio4/degeneretfly) — Polymarket 盘口数据驱动 MaleCNS 可视化。
10. **新近原型** [Bgihe/stonkfly-dashboard](https://github.com/Bgihe/stonkfly-dashboard) — Stonkfly 只读实时面板。
11. **新近原型** [paappraiser/stonkfly-lab](https://github.com/paappraiser/stonkfly-lab) — 受 Stonkfly 启发的蘑菇体纸上 BTC 实验，但不是完整 MaleCNS 图。
12. **新近原型** [iyz2013/flywire-live](https://github.com/iyz2013/flywire-live) — 代币事件驱动的果蝇观察器；不要把它理解成链上神经元。

## 8. X、Reddit、YouTube 和新闻里的病毒式实验

这些条目往往只有视频或社交帖子，科学与复现证据弱于开源仓库。

1. **社媒展示** [Alex Wormuth：MaleCNS 玩 Doom](https://x.com/nftechie_/status/2096409780961059119) — 帧→视觉神经元，下降神经元→按键，伤害→PPL101 惩罚。
2. **社媒展示** [Jessica Paquette：MaleCNS 玩 Super Mario 64](https://x.com/barrelshifter/status/2097004115826200898) — 对应 Fly64/`ornata/fly`。
3. **社媒展示** [Lyra：果蝇脑玩 Beat Saber](https://x.com/_lyraaaa_/status/2097527368919470162) — 后续说明包含录制动作序列与 RL 训练，不能解读成自然即时反应。
4. **社媒展示** [Alex Wormuth：给果蝇脑 100 美元交易比特币](https://x.com/nftechie_/status/2098012107652391357) — 对应 Stonkfly；不代表有盈利能力。
5. **社媒展示** [evnsnclr：MaleCNS 进入 Minecraft](https://x.com/evnsnclr/status/2095975490708291948) — 全保留连接组驱动角色运动的 v1 展示。
6. **社媒展示** [Ro0oney：Minecraft 视频](https://www.youtube.com/results?search_query=Ro0oney+fruit+fly+brain+Minecraft) — 标题中的“conscious brain”是创作者说法，不是科学结论。
7. **社媒展示** Breg Grockman `@alright_mark`：果蝇脑平行停车 — 主要为 X 视频，方法细节有限。
8. **社媒展示** `@linguinelabs`：Bad Apple 神经活动视频 — 更接近视觉/艺术叠加，不能证明行为学习。
9. **社媒展示** `@derpchud`：Overwatch 等游戏片段 — 方法和代码公开程度有限。
10. **社媒展示** Nick Walton：果蝇脑解魔方 — 社媒传播很广，代码线索为 `flycube-public`，需把训练读出与真实连接组贡献分开。
11. **社媒展示** [果蝇脑通过 Wi-Fi 控制机器人](https://www.reddit.com/r/robotics/comments/1wgbszm/a_fruit_fly_brain_is_now_controlling_my_robot/) — MacBook 模拟输出高层前进/左右指令，机器人固件仍负责 12 个舵机。
12. **社媒展示** [把果蝇脑导入 s&box](https://www.reddit.com/r/sandbox/comments/1wdtvk3/you_can_import_a_fruit_flys_brain_into_sbox/) — 虚拟房间、避障和后续条件学习计划。
13. **社媒展示** [DOOM-x-Fly Reddit 说明](https://www.reddit.com/r/ClaudeCode/comments/1wgq7vc/we_got_a_whole_neural_scan_of_a_fly_and_we_wont/) — 作者报告 12 次中 7 次完成第一关，并公开读出层边界。
14. **社媒展示** [Chrome Dino 小型连接组实验](https://www.reddit.com/r/SideProject/comments/1webn97/chrome_dino_controlled_by_a_small_fly_connectome/) — 80 神经元、1,296 条测量连接。
15. **社媒展示** [果蝇脑“做临床研究”](https://www.reddit.com/r/medicalschool/comments/1weywv0/i_taught_a_mapped_fruit_flys_brain_how_to_do/) — 讽刺性 PubMed/香蕉研究作品。
16. **文化记录** [PC Gamer：Doom、Mario 64、Beat Saber 汇总](https://www.pcgamer.com/hardware/after-google-mapped-an-adult-male-fruit-flys-brain-software-engineers-made-it-play-doom-mario64-and-beat-saber/) — 嵌入原始帖子并指出 Beat Saber 的工程训练边界。
17. **文化记录** [Fruit Fly Brain Simulations 趋势页](https://meme.com/memes/fruit-fly-brain-simulations) — 记录 Minecraft、交易、平行停车和短视频传播；属于文化时间线而非论文。
18. **教程/评论** [How to Run the Fruit Fly Brain Simulation Yourself](https://projedefteri.com/en/blog/fruit-fly-brain-simulation/) — 解释 LIF、Doom 回路、社媒时间线与复现入口。

## 9. 最值得优先复现的 12 个

按“代码公开度、科学边界、与本地三张数据表的匹配度、趣味性”综合排序：

1. `alextitonis/fly.ai` — 最适合作为 MaleCNS 仿真基线。
2. `Kisame76/drosophila-brain-mlx` — 最适合当前 Apple Silicon 机器做性能基线。
3. `nftechie/doomfly` — 最完整的病毒式游戏回路之一，同时有失败验证记录。
4. `cobanov/flyjump` — 小回路、浏览器可运行、对照比较清楚。
5. `Jhongdlp/FlyBrain` — 游戏 Boss、逃生反射和 3D 展示。
6. `us/connectorch` — 连接组约束机器学习和随机重连对照。
7. `monomyth/fly-brain-codex` — 机器人控制，但边界说明较诚实。
8. `dzhng/fly-escape` — 视觉效果和交互性强。
9. `akramahmed1/malecns-fault-lines` — 最适合做真正的结构科学实验。
10. `Shih-Yu-Yeh/malecns-topology-prior` — 直接回答“真实布线是否带来优势”。
11. `mingdianliu/flybrain-playground` — 适合参考交互式神经实验室。
12. `flyconnectome/2025malecns` — 所有娱乐项目前都应先看的官方分析基准。

## 10. 重要科学边界

1. MaleCNS 是连接图，不是被冻结的意识、记忆或完整脑状态。
2. “用了 166,700 个神经元”不等于行为来自完整果蝇脑；输入编码、神经动力学、阈值、连接符号和输出读出大多是工程假设。
3. 游戏能动起来，可能主要来自训练过的读出层、脚本运动、预录动作或身体控制器。
4. 必须查看是否有随机重连、相同稀疏度网络、去除连接组和简单基线等对照。
5. 交易项目一律应按艺术/研究原型看待，除非有严格样本外、成本后、预注册结果；目前不应据此投入真钱。
6. FlyWire 是雌性脑，MaleCNS 是雄性完整 CNS；很多网络文章把两者混称为“完整果蝇脑”。
