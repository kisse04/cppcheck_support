# -*- coding: utf-8 -*-
"""
自動收集含頭文件的目錄，組成 -I 參數並執行 Cppcheck。
當 -I 太多超過 Windows 命令列長度時，自動建立「聚合 include 夾」只用一個 -I。

用法（基本）:
  py cppcheck_run.py --root "D:\SWProject\test\880100009\defrostTest2024\8801000009"

用法（含 HTML 報表）:
  py cppcheck_run.py --root "D:\...\8801000009" --html --title "Cppcheck Report 8801000009"

※ 依環境調整 --cppcheck 與 --htmlreport 路徑
"""

import argparse
import os
import sys
import subprocess
import hashlib
from pathlib import Path

DEFAULT_CPPCHECK = r"C:\Program Files\Cppcheck Premium\cppcheck.exe"
DEFAULT_HTMLREPORT = r"C:\Program Files\Cppcheck Premium\cppcheck-htmlreport.py"

EXCLUDE_NAMES_DEFAULT = {
    ".git", ".svn", ".hg", ".vs", ".vscode", ".idea",
    "build", "out", "dist", "bin", "obj",
    "Debug", "Release", "x64", "x86", "__pycache__"
}
HEADER_EXTS = {".h", ".hpp", ".hh", ".hxx"}


def has_header(p: Path) -> bool:
    try:
        for entry in p.iterdir():
            if entry.is_file() and entry.suffix.lower() in HEADER_EXTS:
                return True
        return False
    except PermissionError:
        return False


def find_header_dirs(root: Path, exclude_names) -> list[Path]:
    """回傳所有「包含任一頭文件」的目錄（去重、排序）"""
    root = root.resolve()
    found = set()
    for dirpath, dirnames, filenames in os.walk(root):
        # 過濾要排除的資料夾
        pruned = []
        for d in dirnames:
            if d in exclude_names:
                continue
            pruned.append(d)
        dirnames[:] = pruned

        p = Path(dirpath)
        # 只要這個目錄裡有任何頭檔就加入
        if any(Path(dirpath, f).suffix.lower() in HEADER_EXTS for f in filenames):
            # Windows 上用不分大小寫的 normalized path 去重
            found.add(os.path.normcase(str(Path(dirpath).resolve())))

    # 排序（短路徑在前，視覺更整齊）
    ordered = sorted({Path(p) for p in found}, key=lambda x: (len(str(x)), str(x).lower()))
    return ordered


def estimate_cmdlen(argv: list[str]) -> int:
    # 大致估算 CreateProcess 會看到的字串長度
    return sum(len(a) + 1 for a in argv)


def make_junction(link: Path, target: Path) -> None:
    """建立 NTFS 目錄連結 (junction)。需要系統允許建立連結（管理員或 Dev mode）。"""
    link_parent = link.parent
    link_parent.mkdir(parents=True, exist_ok=True)
    # 若連結已存在先刪
    if link.exists() or link.is_symlink():
        try:
            if link.is_dir():
                # junction 也是目錄，rmdir 即可
                os.rmdir(link)
            else:
                link.unlink()
        except Exception:
            pass
    cmd = ['cmd', '/c', 'mklink', '/J', str(link), str(target)]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_cppcheck(args):
    root = Path(args.root).resolve()
    outxml = Path(args.outxml) if args.outxml else root / "cppcheck.xml"
    cppcheck = Path(args.cppcheck)
    htmlreport = Path(args.htmlreport) if args.html else None

    # 1) 收集 include 目錄
    header_dirs = find_header_dirs(root, set(args.exclude))
    print(f"[info] root: {root}")
    print(f"[info] header dirs found: {len(header_dirs)}")

    # 2) 組 -I 參數（預設策略）
    inc_argv = []
    for d in header_dirs:
        inc_argv += ['-I', str(d)]

    # 3) 估算命令長度；過長則改用「聚合 include 夾」方案
    base_argv = [str(cppcheck)] + inc_argv + [
        f'--relative-paths={str(root)}',
        '--performance-valueflow-max-if-count=10',
        '--premium=misra-c-2025',
        '--enable=all',
        '--inconclusive',
        '--std=c11',
        '--platform=win64',
        '--xml', '--xml-version=2',
        str(root)
    ]
    if estimate_cmdlen(base_argv) > 30000:
        # 建立聚合夾
        agg = root / "_cppcheck_includes"
        if agg.exists():
            # 清掉舊的聚合夾（只清空裡面連結）
            for child in agg.iterdir():
                try:
                    os.rmdir(child)
                except Exception:
                    pass
        else:
            agg.mkdir(parents=True, exist_ok=True)

        for d in header_dirs:
            # 用哈希避免重名
            h = hashlib.sha1(str(d).encode('utf-8')).hexdigest()[:8]
            link = agg / f"{d.name}_{h}"
            try:
                make_junction(link, d)
            except subprocess.CalledProcessError:
                # 無權限建立 junction，退而求其次：跳過；讓後面仍用大量 -I（可能會失敗）
                pass

        inc_argv = ['-I', str(agg)]
        print(f"[info] command too long → using aggregated include dir: {agg}")

    # 4) 寫出 include_paths.txt 供檢查
    with open(root / "include_paths.txt", "w", encoding="utf-8") as f:
        if len(inc_argv) == 2 and inc_argv[0] == '-I' and inc_argv[1].endswith("_cppcheck_includes"):
            f.write(f"# aggregated include: {inc_argv[1]}\n")
        else:
            for i in range(0, len(inc_argv), 2):
                f.write(inc_argv[i+1] + "\n")

    # 5) 執行 Cppcheck
    cpp_argv = [str(cppcheck)] + inc_argv + [
        f'--relative-paths={str(root)}',
        '--performance-valueflow-max-if-count=10',
        '--premium=misra-c-2025',
        '--enable=all',
        '--inconclusive',
        '--std=c11',
        '--platform=win64',
        '--xml', '--xml-version=2',
        str(root)
    ]
    print("[info] running cppcheck ...")
    with open(outxml, "wb") as xmlout:
        # 注意：Cppcheck 的 XML 走 stderr，故把 stderr 重導到檔案
        proc = subprocess.run(cpp_argv, stdout=subprocess.DEVNULL, stderr=xmlout)
    print(f"[info] xml saved: {outxml}")

    # 6) （可選）產生 HTML 報表
    if args.html:
        report_dir = Path(args.report_dir) if args.report_dir else (root / "html")
        report_dir.mkdir(parents=True, exist_ok=True)
        title = args.title or f"Cppcheck Report - {root.name}"
        html_argv = [
            args.py, str(htmlreport),
            f'--file={str(outxml)}',
            f'--report-dir={str(report_dir)}',
            f'--source-dir={str(root)}',
            f'--title={title}',
            '--source-encoding=utf-8'
        ]
        print("[info] building html report ...")
        subprocess.check_call(html_argv)
        print(f"[info] open: {report_dir / 'index.html'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='專案根目錄')
    ap.add_argument('--cppcheck', default=DEFAULT_CPPCHECK, help='cppcheck.exe 路徑')
    ap.add_argument('--outxml', default=None, help='輸出 XML 路徑（預設 root/cppcheck.xml）')
    ap.add_argument('--exclude', nargs='*', default=sorted(EXCLUDE_NAMES_DEFAULT),
                    help='要排除的資料夾名稱（只比對資料夾名，不含路徑）')
    ap.add_argument('--html', action='store_true', help='順便產生 HTML 報表')
    ap.add_argument('--htmlreport', default=DEFAULT_HTMLREPORT, help='cppcheck-htmlreport.py 路徑')
    ap.add_argument('--report-dir', default=None, help='HTML 報表輸出資料夾')
    ap.add_argument('--title', default=None, help='HTML 報表標題')
    ap.add_argument('--py', default='py', help='呼叫 Python 的命令（如 py 或 python.exe）')
    args = ap.parse_args()
    run_cppcheck(args)


if __name__ == '__main__':
    main()
