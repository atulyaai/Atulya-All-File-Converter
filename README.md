# Atulya-All-File-Converter

> **Private offline conversion for daily documents, scans and business files.** 📄📱

![Atulya-All-File-Converter banner](assets/atulya-hero.png)

![Status](https://img.shields.io/badge/status-roadmap-f59e0b)
![Privacy](https://img.shields.io/badge/privacy-offline--first-10b981)
![Platforms](https://img.shields.io/badge/planned-Android%20%7C%20desktop-2563eb)

Atulya-All-File-Converter is planned as a free converter for phone and desktop users who want practical PDF, scan, image and structured-data tools without uploading private files to a remote conversion service.

> 🚧 This README is the product roadmap. Format fidelity and supported conversions will be documented only as they are tested.

## 📱 First Useful Toolbox

| Category | Planned tools |
|---|---|
| PDF | Merge, split, reorder, compress, watermark and sign |
| Scan | Camera scan, crop, cleanup, OCR and searchable PDF |
| Images | Resize, compress and convert JPG/PNG/WebP |
| Data | Excel/CSV/JSON conversion for practical business data |
| Business capture | Invoice/receipt image to reviewable spreadsheet fields |
| Sharing | Save or share exported files through device controls |

## 🏗️ Architecture

```mermaid
flowchart LR
    FILE["Local File / Camera Scan"] --> ENGINE["On-Device Conversion Engine"]
    ENGINE --> PREVIEW["Preview & Correct"]
    PREVIEW --> EXPORT["PDF · Image · Spreadsheet"]
    EXPORT --> SHARE["Save / Share / Print"]
```

## 💻 Delivery Plan

| Platform | Experience |
|---|---|
| Android | Offline-first application for scan, PDF and quick conversion |
| Windows / macOS / Linux | Drag-and-drop desktop conversion queue |
| CLI | Optional batch conversion for desktop power users |

## 🗺️ Roadmap

| Phase | Delivery |
|---|---|
| 1 | Image-to-PDF, PDF merge/split and image compression |
| 2 | OCR scans and searchable document export |
| 3 | CSV/Excel/JSON conversions and batch work |
| 4 | Invoice/receipt capture with review screen |
| 5 | Desktop/mobile sync through user-controlled storage |

## 🔒 Privacy Promise

Offline conversion is the default design goal. Any optional cloud or AI processing must be clearly disclosed and opt-in.

## 📜 License

MIT planned for Atulya-authored source; bundled converter dependencies retain their licenses.
