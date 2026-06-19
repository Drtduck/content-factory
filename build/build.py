#!/usr/bin/env python3
"""Сборщик плагина autocontent-copilot под три морды (Claude, Codex, Hermes).

Источник метода один: core/skills. Сборка кладёт скиллы в dist/<platform>/skills
(копией или симлинком) и рядом - манифест морды из adapters/<platform>, подставив
общие поля name/version/description/keywords из build/manifest.shared.json.

Чистый stdlib, без внешних зависимостей. Скрипт ничего не публикует и не качает -
только готовит локальную раскладку в dist/.

Примеры:
  python build/build.py --platform claude            # симлинки (dev, дефолт)
  python build/build.py --platform claude --copy      # реальные копии файлов
  python build/build.py --platform all --copy         # собрать все три морды
  python build/build.py --platform codex --clean       # пересобрать с нуля
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_SKILLS = REPO_ROOT / "core" / "skills"
ADAPTERS = REPO_ROOT / "adapters"
SHARED_MANIFEST = REPO_ROOT / "build" / "manifest.shared.json"
DIST = REPO_ROOT / "dist"

PLATFORMS = ("claude", "codex", "hermes")

# Куда на каждой морде кладётся манифест и какие поля из shared в него вливаются.
# rel - путь манифеста относительно корня плагина морды (adapters/<platform>).
# fmt - формат файла (json или yaml).
# merge - какие общие поля подставлять из manifest.shared.json.
PLATFORM_MANIFESTS = {
    "claude": [
        {"rel": ".claude-plugin/plugin.json", "fmt": "json",
         "merge": ("name", "version", "description")},
        {"rel": ".claude-plugin/marketplace.json", "fmt": "json",
         "merge": ()},
        {"rel": ".mcp.json", "fmt": "json", "merge": ()},
    ],
    "codex": [
        {"rel": ".codex-plugin/plugin.json", "fmt": "json",
         "merge": ("name", "version", "description")},
        {"rel": ".mcp.json", "fmt": "json", "merge": ()},
    ],
    "hermes": [
        {"rel": "plugin.yaml", "fmt": "yaml",
         "merge": ("name", "version", "description")},
        {"rel": "mcp.config.yaml", "fmt": "yaml", "merge": ()},
    ],
}


def load_shared():
    with SHARED_MANIFEST.open(encoding="utf-8") as fh:
        return json.load(fh)


def fail(msg):
    print("ошибка: " + msg, file=sys.stderr)
    sys.exit(1)


def copy_skills(dest_skills, link):
    """Положить core/skills в dest_skills копией или симлинком."""
    if dest_skills.exists() or dest_skills.is_symlink():
        if dest_skills.is_symlink() or dest_skills.is_file():
            dest_skills.unlink()
        else:
            shutil.rmtree(dest_skills)
    dest_skills.parent.mkdir(parents=True, exist_ok=True)

    if link:
        rel = os.path.relpath(CORE_SKILLS, dest_skills.parent)
        os.symlink(rel, dest_skills, target_is_directory=True)
        print("  skills -> симлинк на " + rel)
    else:
        shutil.copytree(CORE_SKILLS, dest_skills)
        n = sum(1 for _ in dest_skills.rglob("*") if _.is_file())
        print("  skills -> скопировано файлов: " + str(n))


def merge_fields(base, shared, fields):
    """Вернуть копию base с подставленными общими полями из shared."""
    out = dict(base)
    for key in fields:
        if key in shared:
            out[key] = shared[key]
    return out


def write_json(path, data):
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def emit_manifest(spec, src_root, dest_root, shared):
    """Прочитать манифест морды, при наличии merge-полей влить shared, записать в dist."""
    src = src_root / spec["rel"]
    dest = dest_root / spec["rel"]
    dest.parent.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        fail("нет файла манифеста: " + str(src))

    if spec["fmt"] == "json" and spec["merge"]:
        with src.open(encoding="utf-8") as fh:
            data = json.load(fh)
        data = merge_fields(data, shared, spec["merge"])
        write_json(dest, data)
        print("  manifest -> " + spec["rel"] + " (поля из shared: "
              + ", ".join(spec["merge"]) + ")")
        return

    # yaml-манифесты и json без merge копируем как есть: stdlib не пишет yaml,
    # а общие поля в шаблонах уже выставлены под текущую версию shared.
    shutil.copyfile(src, dest)
    if spec["fmt"] == "yaml" and spec["merge"]:
        print("  manifest -> " + spec["rel"]
              + " (скопирован как есть; синхронизируйте поля с manifest.shared.json вручную)")
    else:
        print("  manifest -> " + spec["rel"] + " (скопирован как есть)")


def build_platform(platform, link, clean, shared):
    src_root = ADAPTERS / platform
    if not src_root.exists():
        fail("нет адаптера для морды: " + platform)

    dest_root = DIST / platform
    if clean and dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    print("[" + platform + "] -> " + str(dest_root))
    copy_skills(dest_root / "skills", link)
    for spec in PLATFORM_MANIFESTS[platform]:
        emit_manifest(spec, src_root, dest_root, shared)
    print("[" + platform + "] готово")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Собрать dist/<platform> из core/skills и adapters/<platform>.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--platform", required=True,
        choices=PLATFORMS + ("all",),
        help="морда: claude | codex | hermes | all",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--link", dest="link", action="store_true", default=True,
        help="симлинковать скиллы вместо копии (дефолт, для dev)",
    )
    mode.add_argument(
        "--copy", dest="link", action="store_false",
        help="копировать скиллы файлами (для раздачи плагина)",
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="снести dist/<platform> перед сборкой",
    )
    args = parser.parse_args(argv)

    if not CORE_SKILLS.exists():
        fail("нет core/skills: " + str(CORE_SKILLS))

    shared = load_shared()
    targets = PLATFORMS if args.platform == "all" else (args.platform,)
    for platform in targets:
        build_platform(platform, args.link, args.clean, shared)


if __name__ == "__main__":
    main()
