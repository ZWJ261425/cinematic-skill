# Cinematic History Remotion / 电影感历史短片 Skill

[中文](#中文) · [English](#english)

## 中文

将历史主题、技术发展简史或一段已有影片制作成可编辑的电影感短片。Skill 指导 Codex 编写时间线、核验事实、设计古典画作场景、实现画面内部运动与克制运镜，并用 Remotion 渲染和检查成片。

它附带《回声》公开版参考工程，展示烛火、风雪、水面、树梢、人物脚步、机械部件和星光汇字等实现。参考工程是可改写的技术案例，原片内容与旧验证结果不代表新主题已完成。

### 安装

需要 Codex、Python 3.11+、Node.js/npm。制作和验证视频还需要浏览器及 FFmpeg/FFprobe。Remotion 依赖由参考工程中的 `package-lock.json` 锁定；使用 Remotion 时请遵守其[单独的许可条款](https://www.remotion.dev/docs/license/pricing)。

```bash
git clone https://github.com/ZWJ261425/cinematic-skill.git ~/.codex/skills/cinematic-history-remotion
```

Windows PowerShell：

```powershell
git clone https://github.com/ZWJ261425/cinematic-skill.git "$HOME/.codex/skills/cinematic-history-remotion"
```

重启 Codex 或开启新会话后，使用 `$cinematic-history-remotion` 调用。若本机已安装同名 Skill，无需再次克隆。

### 使用

在 Codex 中输入：

> 使用 $cinematic-history-remotion，制作一部约 2 分钟的天文学发展史短片。先核验关键日期，再为每幕设计画作、内部动作、运镜和字幕，最后交付 MP4 与可编辑工程。

直接复制参考工程：

```bash
python ~/.codex/skills/cinematic-history-remotion/scripts/bootstrap_project.py --target ./my-history-film --topic "天文学发展史"
cd my-history-film
npm ci
npm run studio
```

在 Studio 中选择 `EchoMotion`。新主题需要改写 `src/story.ts`、镜头与素材；只替换片名不会完成适配。公开参考工程默认静音，使用系统衬线字体。若需音乐，请提供有权使用的音轨并在 Remotion 工程中加入 `Audio` 组件。

### 目录

| 路径 | 用途 |
| --- | --- |
| `SKILL.md` | Codex 工作流入口 |
| `agents/openai.yaml` | Skill 显示信息与默认提示 |
| `references/` | 画面动作、案例和工程适配说明 |
| `scripts/bootstrap_project.py` | 校验并复制参考工程到空目录 |
| `scripts/verify_video.py` | 检查视频元数据与整片解码 |
| `assets/echo-remotion.zip` | 已清理的可编辑 Remotion 工程 |
| `assets/template-manifest.json` | 压缩包校验值与元数据 |

### 素材与许可

仓库已排除原片个人音乐、复制的系统字体、品牌矢量图、第三方参考 HTML、个人路径与旧核验记录。作者原创的 Skill 文本、脚本、参考工程源码与生成场景按 [MIT License](LICENSE) 发布（以作者实际享有的权利为限）。名画保留原有公有领域/CC0 状态；素材来源见 [素材说明](ASSET-CREDITS.md)。

## English

This Codex skill helps create or revise cinematic history films in Remotion. It covers source checking, storyboards, painterly scenes, motion inside each frame, restrained camera moves, rendering, and final verification. An editable, sanitized *Echo* project is included as a technical reference.

### Install

Requirements: Codex, Python 3.11+, Node.js/npm, a browser for Remotion, and FFmpeg/FFprobe for video verification. Remotion has [its own license](https://www.remotion.dev/docs/license/pricing).

```bash
git clone https://github.com/ZWJ261425/cinematic-skill.git ~/.codex/skills/cinematic-history-remotion
```

Restart Codex or start a new session, then invoke `$cinematic-history-remotion`.

### Example

> Use $cinematic-history-remotion to make a two minute film about the history of astronomy. Check the key dates, design motion and camera movement for each scene, then deliver an MP4 and editable project.

Bootstrap the example with `scripts/bootstrap_project.py --target ./my-history-film --topic "History of astronomy"`, run `npm ci` in the new directory, and select `EchoMotion` in Remotion Studio. Replace the original narrative, artwork, and motion coordinates for your topic. The public project is silent and uses system serif fonts. Add music only when you have the rights to use it.

### Layout

`SKILL.md` is the skill entry point; `agents/` holds display metadata; `references/` contains focused production guidance; `scripts/` contains the bootstrap and video verifier; `assets/` contains the checked Remotion archive and its SHA-256 manifest.

The original personal track, copied fonts, brand vectors, third-party sample HTML, private paths, and historical verification files are excluded. Author-created skill text, scripts, reference project source code, and generated scenes are released under the [MIT License](LICENSE), to the extent the author holds rights in them. Museum images retain their public-domain/CC0 status; see [asset credits](ASSET-CREDITS.md).
