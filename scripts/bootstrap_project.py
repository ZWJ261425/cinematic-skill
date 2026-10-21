"""Copy the verified Echo project into a new, empty work directory."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import shutil
import stat
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--topic')
    parser.add_argument('--reference', action='store_true', help='Reproduce the original ChatGPT example.')
    args = parser.parse_args()
    if args.reference and args.topic:
        parser.error('--reference reproduces the original topic; use --topic without --reference for a new theme.')
    if not args.reference and not (args.topic and args.topic.strip()):
        parser.error('New-topic mode requires --topic.')
    skill = Path(__file__).resolve().parents[1]
    target = args.target.resolve()
    if target == skill or target.is_relative_to(skill):
        parser.error('The project must be outside the skill directory.')
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        parser.error('Target must be a new or empty directory; existing files will not be overwritten.')
    manifest = json.loads((skill / 'assets/template-manifest.json').read_text(encoding='utf-8'))
    template = skill / 'assets' / manifest['archive']
    with template.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    if digest != manifest['sha256']:
        parser.error('Template checksum mismatch; no project was written.')
    with zipfile.ZipFile(template) as archive:
        entries = []
        for info in archive.infolist():
            parts = PurePosixPath(info.filename).parts
            if not parts or parts[0] != manifest['archive_root']:
                parser.error('Unexpected template root.')
            if PurePosixPath(info.filename).is_absolute() or '..' in parts or '\\' in info.filename:
                parser.error('Unsafe template member.')
            if stat.S_ISLNK(info.external_attr >> 16):
                parser.error('Template symlinks are not supported.')
            if len(parts) == 1:
                continue
            dest = target.joinpath(*parts[1:]).resolve()
            if not dest.is_relative_to(target):
                parser.error('Template member would escape target.')
            entries.append((info, dest))
        target.mkdir(parents=True, exist_ok=True)
        for info, dest in entries:
            if info.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, dest.open('xb') as output:
                shutil.copyfileobj(source, output)
    topic = args.topic or 'ChatGPT的发展史（回声参考案例）'
    brief = {
        'topic': topic, 'mode': 'reference' if args.reference else 'new-topic',
        'preset': {'width': 1920, 'height': 1080, 'fps': 30, 'suggested_max_seconds': 180},
        'audio': 'No audio included; supply licensed music if needed.',
        'adaptation_required': not args.reference,
        'reference_verifications': 'Original example results, not evidence for new output.',
        'template_sha256': digest,
    }
    (target / 'project-settings.json').write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding='utf-8')
    text = (
        f'# 本次制作\n\n主题：{topic}\n\n'
        '这是《回声》工程的副本。新主题需改写 story、章节图形、标题/结语和目标字形，'
        '重新核验史料并按所用画作标定遮罩、支点与运镜。旧核验记录仅证明原例。\n\n'
        + '公开模板默认静音。若需音乐，请加入有权使用的音轨及 Remotion Audio 组件，并重新生成波形。\n'
        + '\n使用 npm ci、npm run studio，选择 EchoMotion。依本次 storyboard 更新总帧数、抽帧时间与输出文件名。\n'
    )
    (target / 'PROJECT_BRIEF.md').write_text(text, encoding='utf-8')
    print(json.dumps({'project': str(target), 'files_copied': len(entries), 'topic': topic,
                      'audio_included': False, 'reference_ready': args.reference,
                      'new_topic_content_needs_adaptation': not args.reference}, ensure_ascii=False))


if __name__ == '__main__':
    main()
