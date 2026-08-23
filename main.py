#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import hashlib
import os
import shutil
import sys
import time


TARGET_NAME = "shopList.slt"
DEFAULT_FACILITY_DIR = "facility"
LANG_ENV = "MHWI_SHOPLIST_LANG"
COLOR_ENABLED = False

CURRENT_LANG = "zh"


# 界面文案翻译表。zh 为默认语言，en 为英文。
TRANSLATIONS = {
    "zh": {
        "app.title": "MHWI 商店列表管理工具",
        "app.author": "by @SMIXLY",
        "menu.path": "文件目录：",
        "status.enabled.match": "状态：已启用 -> {}",
        "status.enabled.unknown": "状态：已启用（哈希不匹配任何候选文件）",
        "status.disabled": "状态：未启用",
        "list.title": "可用 .slt 文件：",
        "list.empty": "  （无）",
        "list.enabled_marker": " [已启用]",
        "list.no_files": "未找到可用的 .slt 文件（目录：{}）。",
        "operation.actions": "操作：",
        "operation.hint": "输入序号启用 / D 禁用 / R 刷新 / L 切换语言 / Q 退出",
        "error.invalid_index": "序号无效，请输入 1~{} 之间的数字。",
        "error.unknown_action": "无法识别的操作：{}",
        "scan.dir": "扫描目录：",
        "scan.count": "可用 .slt 文件：",
        "scan.count_suffix": " 份",
        "scan.enabled": "当前已启用：",
        "scan.enabled.unknown": "当前已启用：{}（哈希不匹配任何候选文件）",
        "scan.disabled": "当前状态：未启用（不存在 shopList.slt）",
        "enable.confirm": "当前已启用一份 shopList.slt，替换它？(y/N) ",
        "enable.cancelled": "已取消。",
        "enable.ok": "已启用：{}",
        "enable.file": "生成文件：{}",
        "enable.no_files": "未找到可用的 .slt 文件，无法启用。",
        "enable.not_found": "找不到指定的文件：{}",
        "enable.available": "可用文件：",
        "disable.none": "当前没有 shopList.slt，无需禁用。",
        "disable.confirm": "确定删除 {} 吗？(y/N) ",
        "disable.cancelled": "已取消。",
        "disable.ok": "已禁用：{}",
        "prompt": "> ",
        "help.desc": "扫描并管理 facility 目录下的 .slt 文件",
        "help.path": ".slt 文件所在目录（默认 ./facility）",
        "help.lang": "界面语言（zh 或 en，默认 zh）",
        "help.scan": "扫描并显示 .slt 文件列表",
        "help.enable": "将某个 .slt 文件复制为 shopList.slt",
        "help.enable.source": "文件序号或文件名",
        "help.enable.yes": "已存在时不再询问，直接替换",
        "help.disable": "删除当前 shopList.slt",
        "help.disable.yes": "不再询问，直接删除",
    },
    "en": {
        "app.title": "MHWI Shop List Manager",
        "app.author": "by @SMIXLY",
        "menu.path": "Directory: ",
        "status.enabled.match": "Status: enabled -> {}",
        "status.enabled.unknown": "Status: enabled (hash does not match any candidate file)",
        "status.disabled": "Status: disabled",
        "list.title": "Available .slt files:",
        "list.empty": "  (none)",
        "list.enabled_marker": " [enabled]",
        "list.no_files": "No .slt files found (directory: {}).",
        "operation.actions": "Actions: ",
        "operation.hint": "Enter a number to enable / D disable / R refresh / L toggle language / Q quit",
        "error.invalid_index": "Invalid number, please enter a number between 1~{}.",
        "error.unknown_action": "Unrecognized action: {}",
        "scan.dir": "Scanning directory: ",
        "scan.count": "Available .slt files: ",
        "scan.count_suffix": " file(s)",
        "scan.enabled": "Currently enabled: ",
        "scan.enabled.unknown": "Currently enabled: {} (hash does not match any candidate file)",
        "scan.disabled": "Status: disabled (shopList.slt does not exist)",
        "enable.confirm": "A shopList.slt is already enabled, replace it? (y/N) ",
        "enable.cancelled": "Cancelled.",
        "enable.ok": "Enabled: {}",
        "enable.file": "Created file: {}",
        "enable.no_files": "No .slt files found, cannot enable.",
        "enable.not_found": "Cannot find the specified file: {}",
        "enable.available": "Available files: ",
        "disable.none": "No shopList.slt is currently enabled, nothing to disable.",
        "disable.confirm": "Are you sure you want to delete {}? (y/N) ",
        "disable.cancelled": "Cancelled.",
        "disable.ok": "Disabled: {}",
        "prompt": "> ",
        "help.desc": "Scan and manage .slt files in the facility directory",
        "help.path": "Directory containing .slt files (default ./facility)",
        "help.lang": "UI language (zh or en, default zh)",
        "help.scan": "Scan and list .slt files",
        "help.enable": "Copy a .slt file to shopList.slt",
        "help.enable.source": "File number or filename",
        "help.enable.yes": "Replace existing shopList.slt without asking",
        "help.disable": "Delete the current shopList.slt",
        "help.disable.yes": "Delete without asking",
    },
}


_ANSI_CODES = {
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
}


def tr(key, *args):
    """Return the translated string for the current language.

    Falls back to Chinese when a key is missing, then to the key itself.
    Positional args are used to format ``{}`` placeholders when present.
    """
    table = TRANSLATIONS.get(CURRENT_LANG) or TRANSLATIONS["zh"]
    template = table.get(key) or TRANSLATIONS["zh"].get(key, key)
    if args:
        try:
            return template.format(*args)
        except (IndexError, KeyError):
            return template
    return template


def set_lang(lang):
    """Set the current UI language, falling back to Chinese for invalid input."""
    global CURRENT_LANG
    lang = (lang or "").strip().lower()
    if lang in ("zh", "chinese"):
        CURRENT_LANG = "zh"
    elif lang in ("en", "english"):
        CURRENT_LANG = "en"
    else:
        CURRENT_LANG = "zh"


def toggle_lang():
    """Flip between Chinese and English."""
    global CURRENT_LANG
    CURRENT_LANG = "en" if CURRENT_LANG == "zh" else "zh"


def _find_lang_arg(argv):
    """Detect ``--lang`` / ``-l`` from raw argv, wherever it appears."""
    for i, arg in enumerate(argv):
        if arg in ("--lang", "-l") and i + 1 < len(argv):
            return argv[i + 1]
        if arg.startswith("--lang="):
            return arg.split("=", 1)[1]
    return None


def initial_lang(argv):
    """Resolve the UI language: CLI argument wins, then env var, then zh."""
    cli = _find_lang_arg(argv)
    if cli:
        return cli
    env = os.environ.get(LANG_ENV)
    if env:
        return env
    return "zh"


def setup_color():
    """Enable ANSI colors only when stdout is a real terminal."""
    global COLOR_ENABLED
    if not sys.stdout.isatty():
        COLOR_ENABLED = False
        return
    if os.name == "nt":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            COLOR_ENABLED = False
            return
    COLOR_ENABLED = True


def style(text, color=None, bold=False, dim=False):
    """Wrap text in ANSI escape codes when color output is available."""
    if not COLOR_ENABLED:
        return text
    codes = []
    if bold:
        codes.append("1")
    if dim:
        codes.append("2")
    if color in _ANSI_CODES:
        codes.append(_ANSI_CODES[color])
    return "\033[{}m{}\033[0m".format(";".join(codes), text)


def facility_dir(path_arg):
    """Return the folder holding the .slt files.

    Defaults to ./facility, but also accepts the folder itself or the
    current directory when run from inside it. When frozen as an exe,
    also look next to the executable so double-clicking works anywhere.
    """
    if path_arg:
        return path_arg
    candidates = [DEFAULT_FACILITY_DIR]
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        candidates.insert(0, os.path.join(exe_dir, DEFAULT_FACILITY_DIR))
    for candidate in candidates:
        if os.path.isdir(candidate):
            return candidate
    return "."


def scan_slt_files(folder):
    """List all .slt files in folder, excluding shopList.slt itself."""
    if not os.path.isdir(folder):
        return [], None
    entries = []
    for name in sorted(os.listdir(folder)):
        if not name.lower().endswith(".slt"):
            continue
        if name.lower() == TARGET_NAME.lower():
            continue
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            st = os.stat(path)
            entries.append(
                {
                    "name": name,
                    "path": path,
                    "size": st.st_size,
                    "mtime": st.st_mtime,
                }
            )
    return entries, folder


def active_shoplist(folder):
    path = os.path.join(folder, TARGET_NAME)
    if os.path.isfile(path):
        st = os.stat(path)
        return {
            "path": path,
            "size": st.st_size,
            "mtime": st.st_mtime,
            "hash": file_sha256(path),
        }
    return None


def file_sha256(path):
    """Compute the SHA-256 hash of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_matching_entry(entries, active):
    """Find which listed .slt file matches the enabled shopList.slt by hash."""
    if active is None:
        return None
    for entry in entries:
        if file_sha256(entry["path"]) == active["hash"]:
            return entry
    return None


def format_size(size):
    for unit in ("B", "KB", "MB"):
        if size < 1024 or unit == "MB":
            return "{:.1f} {}".format(size, unit)
        size /= 1024.0
    return "{:.1f} GB".format(size)


def format_time(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def resolve_entry(entries, selector):
    """Resolve a numeric index (1-based) or an exact filename."""
    if selector is None:
        return None
    if isinstance(selector, str) and selector.isdigit():
        index = int(selector)
        if 1 <= index <= len(entries):
            return entries[index - 1]
        return None
    for entry in entries:
        if entry["name"] == selector:
            return entry
    return None


def enable_entry(folder, entry, yes=False):
    """Copy one .slt file to shopList.slt."""
    target = os.path.join(folder, TARGET_NAME)
    if os.path.exists(target):
        if not yes:
            answer = input(tr("enable.confirm")).strip().lower()
            if answer not in ("y", "yes"):
                print(style(tr("enable.cancelled"), color="yellow"))
                return False
    shutil.copy2(entry["path"], target)
    print(style(tr("enable.ok", entry["name"]), color="green", bold=True))
    print(style(tr("enable.file", target), color="cyan", dim=True))
    return True


def disable_shoplist(folder, yes=False):
    """Delete only shopList.slt in the target folder."""
    target = os.path.join(folder, TARGET_NAME)
    if not os.path.exists(target):
        print(style(tr("disable.none"), color="yellow"))
        return True
    if not yes:
        answer = input(tr("disable.confirm", target)).strip().lower()
        if answer not in ("y", "yes"):
            print(style(tr("disable.cancelled"), color="yellow"))
            return False
    os.remove(target)
    print(style(tr("disable.ok", TARGET_NAME), color="green", bold=True))
    return True


def print_list(entries, folder):
    if not entries:
        print(style(tr("list.no_files", folder), color="yellow"))
        return
    for i, entry in enumerate(entries, 1):
        print(
            "{} {}  [{}  {}]".format(
                style("{:>2}.".format(i), bold=True),
                entry["name"],
                style(format_size(entry["size"]), color="yellow"),
                style(format_time(entry["mtime"]), dim=True),
            )
        )


def clear_screen():
    """Clear the terminal when supported; otherwise print a separator."""
    if os.name == "nt" and sys.stdout.isatty():
        os.system("cls")
        return
    print("\n" + "-" * 60)


def run_scan(args):
    folder = facility_dir(args.path)
    entries, folder = scan_slt_files(folder)
    print(style(tr("scan.dir"), color="cyan", bold=True) + folder)
    print(
        style(tr("scan.count"), color="cyan", bold=True)
        + style(str(len(entries)), bold=True)
        + tr("scan.count_suffix")
    )
    active = active_shoplist(folder)
    if active:
        match = find_matching_entry(entries, active)
        if match:
            print(
                style(tr("scan.enabled"), color="green", bold=True)
                + match["name"]
                + style("  [{}]".format(format_size(active["size"])), color="yellow")
            )
        else:
            print(style(tr("scan.enabled.unknown", TARGET_NAME), color="yellow"))
    else:
        print(style(tr("scan.disabled"), color="yellow"))
    print_list(entries, folder)


def run_enable(args):
    folder = facility_dir(args.path)
    entries, folder = scan_slt_files(folder)
    if not entries:
        print(style(tr("enable.no_files"), color="red"))
        return 1
    entry = resolve_entry(entries, args.source)
    if entry is None:
        print(style(tr("enable.not_found", args.source or ""), color="red"))
        print(style(tr("enable.available"), color="cyan", bold=True))
        print_list(entries, folder)
        return 1
    return 0 if enable_entry(folder, entry, yes=args.yes) else 1


def run_disable(args):
    folder = facility_dir(args.path)
    return 0 if disable_shoplist(folder, yes=args.yes) else 1


def run_interactive(path_arg):
    folder = facility_dir(path_arg)
    while True:
        clear_screen()
        print(style(tr("app.title"), color="cyan", bold=True))
        print(style(tr("app.author"), dim=True))
        print(style(tr("menu.path"), color="cyan", bold=True) + os.path.abspath(folder))
        print()
        entries, folder = scan_slt_files(folder)
        active = active_shoplist(folder)
        match = find_matching_entry(entries, active)
        if match:
            print(style(tr("status.enabled.match", match["name"]), color="green", bold=True))
        elif active:
            print(style(tr("status.enabled.unknown"), color="yellow"))
        else:
            print(style(tr("status.disabled"), color="yellow"))
        print()
        print(style(tr("list.title"), color="cyan", bold=True))
        if not entries:
            print(style(tr("list.empty"), dim=True))
        else:
            for i, entry in enumerate(entries, 1):
                marker = (
                    style(tr("list.enabled_marker"), color="green", bold=True)
                    if match and entry["path"] == match["path"]
                    else ""
                )
                print(
                    "  {}{}{}".format(
                        style("{:>2}.".format(i), bold=True),
                        entry["name"],
                        marker,
                    )
                )
        print(style(tr("operation.actions"), color="cyan", bold=True) + tr("operation.hint"))
        try:
            raw = input(style(tr("prompt"), bold=True)).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        choice = raw.lower()
        if choice in ("q", "quit", "exit"):
            break
        if choice in ("r", "refresh"):
            continue
        if choice in ("l", "lang"):
            toggle_lang()
            continue
        if choice in ("d", "disable"):
            disable_shoplist(folder)
            run_interactive(folder)
            return
        if choice.isdigit():
            entry = resolve_entry(entries, raw)
            if entry is None:
                print(style(tr("error.invalid_index", len(entries)), color="red"))
                continue
            enable_entry(folder, entry)
            run_interactive(folder)
            return
        entry = resolve_entry(entries, raw)
        if entry is not None:
            enable_entry(folder, entry)
            run_interactive(folder)
            return
        else:
            print(style(tr("error.unknown_action", raw), color="red"))


def add_lang_arg(parser):
    """Attach the ``--lang`` option so it works before or after subcommands."""
    parser.add_argument("--lang", "-l", help=tr("help.lang"))


def build_parser():
    parser = argparse.ArgumentParser(description=tr("help.desc"))
    parser.add_argument("--path", help=tr("help.path"))
    add_lang_arg(parser)
    sub = parser.add_subparsers(dest="command")

    scan_parser = sub.add_parser("scan", help=tr("help.scan"))
    add_lang_arg(scan_parser)

    enable_parser = sub.add_parser("enable", help=tr("help.enable"))
    enable_parser.add_argument("source", nargs="?", help=tr("help.enable.source"))
    enable_parser.add_argument("--yes", action="store_true", help=tr("help.enable.yes"))
    add_lang_arg(enable_parser)

    disable_parser = sub.add_parser("disable", help=tr("help.disable"))
    disable_parser.add_argument("--yes", action="store_true", help=tr("help.disable.yes"))
    add_lang_arg(disable_parser)

    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    set_lang(initial_lang(argv))
    setup_color()
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "scan":
        run_scan(args)
    elif args.command == "enable":
        return run_enable(args)
    elif args.command == "disable":
        return run_disable(args)
    else:
        run_interactive(args.path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
