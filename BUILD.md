# Build Guide

Build Atulya-All-File-Converter for all platforms from a single Python codebase.

## Prerequisites

```bash
pip install -e ".[all]"
```

Individual extras: `pip install atulya-convert[pdf]` or `[docx]` or `[all]`.

## Windows EXE (PyInstaller)

```batch
build_exe.bat
```

Produces `dist/atulya-convert.exe` — single-file, no Python required.

## Android APK (Buildozer)

Requires Linux (or WSL). Install Buildozer, then:

```bash
build_apk.sh
```

Produces `bin/atulya_convert_*.apk`. Works on Android 8+ via Termux.

## Linux (pip / .deb / AppImage)

### pip install (all distros)

```bash
pip install atulya-all-file-converter
```

### .deb package (Debian/Ubuntu)

```bash
fpm -s python -t deb .
```

### AppImage (portable Linux)

```bash
pip install pyinstaller
pyinstaller --onefile --name atulya-convert src/atulya_all_file_converter/cli.py
```

## Cross-platform notes

- All core operations are pure Python — no platform-specific code
- Android: uses `termux-open` for file access; clipboard via termux-clipboard-set
- Windows EXE includes all dependencies via PyInstaller hooks
- Linux AppImage works on any distro with FUSE
