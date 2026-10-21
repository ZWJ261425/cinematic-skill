# 工程适配

## 建项目

脚本使用 Python 3.11+ 标准库。bootstrap 校验随包工程 SHA256，解压到新的空目录，写入新 brief。不要在 Skill 自身、旧成片目录或现有工程上执行。

```powershell
python '<skill-dir>/scripts/bootstrap_project.py' --target './work/history-film' --topic '天文学发展史'
cd './work/history-film'
npm ci
npm run studio
```

选 `EchoMotion`。`Echo` 是原版，`MotionPreview` 是旧30秒样片，不会自动变成新主题预览。公开模板默认静音；`--reference` 只保留原例叙事和画面。需要音乐时自行提供有权使用的音轨。

## 同时修改的内容

| 文件 | 适配 |
|---|---|
| src/story.ts | 全部事实、日期、字幕、章节起止；不能只改片名 |
| src/Film.tsx | 片名、章节图形、谱系节点、结语、字幕布局、画作标注；检查当前合成所有文字 |
| src/FullMotion.tsx | 素材路径、遮罩、人物边界、相机、切图支点；运动按原画坐标标定 |
| src/MotionPreview.tsx | 眨眼、烛火、湖面、字形模块；两处 fillText('ChatGPT',...)、采样区域、结尾时序与旧预览 |
| src/Root.tsx | 新总帧数、尺寸、fps，与 timeline 一致；另定义新短预览 |
| src/Film.tsx 中的波形 | 当前为非音乐驱动的示意动画；加入音乐后按新曲重新采样 |
| public/art、public/motion-assets | 决定保留画作与新素材；换图片后重新标定遮罩 |
| render-motion-film.mjs | 输出名称、抽帧时刻、短片段范围、实际适合的并发数 |
| 字幕/来源/提示词/核验 | 区分原例记录与新记录，旧的通过状态不能证明新片 |

案例全画幅1920×1080，上下各70px留黑，背景 Canvas 为1920×940。换画幅时不只改 Root，还要适配画布、相机、遮罩、字体位置和构图。检索所有硬编码标题与图形节点；2026年节点只是原例的有日期快照，按新请求再次核验。

## 音乐

公开工程不包含案例音乐。新曲从有权使用的原始音频开始；需要变速且保持音高时可使用 atempo。

FFmpeg滤镜示例：`atempo=0.8,atrim=duration=178,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1.5,afade=t=out:st=172:d=6`。数值来自新 brief，不照抄固定长度。需要响度归一时先测量，再两遍 loudnorm，不能拿旧曲的 measured_I 等数值处理新曲。

波形从处理后音频按每帧窗计算 RMS，再平滑/缩放。可按 globalFrame 索引每帧波形数组；帧窗大小=音频采样率/fps。当前公开模板是示意波形，加入音乐后请更新。

## 导出

使用本机已有 Node/npm 和 package-lock。不要把 node_modules、build、浏览器缓存和中间帧装入交付工程。

```powershell
npm run typecheck
$env:REMOTION_BROWSER_EXECUTABLE = '<本机 Chrome 或 Edge 可执行文件路径>'
$env:REMOTION_OUTPUT_DIR = '<项目输出目录>'
npm run stills:motion -- '3,41,87.2,87.6,118.6,146,176.3,177.9'
npm run render:motion
```

抽帧时刻仅对应原案例。新片按自己的 storyboard 选择。H.264、yuv420p、CRF17、JPEG93、AAC320k是案例高质量起点；按设备负载调整并发。

若没有默认浏览器或FFmpeg，定位已有工具并传完整路径。verify_video.py 支持 FFMPEG_BINARY、FFPROBE_BINARY 或显式参数，不需要 API Key。新 bitmap 用环境已有图像工具，不假定视频生成服务已连接。

## 检查

每章看实际帧；眨眼看闭合与恢复，走路看脚步落点，水和树看遮罩边，转场看相邻镜头，结尾看成字和最后一帧。复杂或新动作需要连续帧或短视频，单帧不证明流畅。

verify_video.py 可加 --expected-frames 精确比对总帧数；无音乐的 brief 用 --allow-silent。报告自动证明技术检查，视觉与史料另行记录。新视频与工程另存。

工程包保留 src/public、package文件、渲染脚本、字幕、来源、提示词、新核验。公开模板不附带原例音乐。用户要成片时，说明与源码不能替代 MP4。
