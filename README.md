---
# 1. 身份識別層 (Identity)
id: "readme"
title: "Sovereign-E-Game-of-Small-World"
aliases:
  - "Game_of_Small_World"
  - "A47_Simulator"

# 2. 語義摘要層 (Semantic)
description: "AREA|A51|FLEET_E|SMALL_WORLD|SDP12|SIMULATOR"
tags:
  - area
  - fleet-e
  - small-world
  - sdp12
  - kano-decay
  - game-engine
type: repo-root

# 3. 生命週期層 (Lifecycle)
compiler_status: stable
created: "2026-10-14"
updated: "2026-10-14"

# 4. 知識拓撲層 (Topology)
parent: ["[[Fleet_E_Edge_Agents/m.A51.05_FLEET_E|🤖 Fleet E 艦隊 MOC]]"]
related:
  - "[[000_MOC_A47_Game_of_Small_World|A47 小世界導航總圖]]"
  - "[[000_MOC_A45_Small_World|A45 Small World 晶格導航總圖]]"
---

# 🎮 Sovereign-E-Game-of-Small-World (小世界大局觀：AI 企業防禦沙盒)
> 面向中小企業與決策主管的「SDP12 雙系統九宮格 ✕ 13 Agent 積木 ✕ Kano 動態演化」在線決策模擬器

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Live Simulator](https://img.shields.io/badge/Live_Simulator-GitHub_Pages-cyan.svg)](https://sdrmsung.github.io/Sovereign-E-Game-of-Small-World/)
[![Audit Pass](https://img.shields.io/badge/10ms_One--Click_Test-100%25_PASS-brightgreen.svg)](tests/test_audit.py)
[![Type II Error](https://img.shields.io/badge/Type_II_Error-Zero_Tolerance-red.svg)](cli.py)

---

## 🧭 核心願景：何謂「小世界大局觀」？ (Vision)

在企業 AI 落地過程中，最容易讓企業破產的不是 AI 運算太慢，而是**「混淆矩陣的不對稱代價」**：
* **Type 1 誤殺（把繩子當成毒蛇）**：系統過於敏感而叫停，轉人工確認，頂多損失幾十元行政成本。
* **Type 2 漏放（把劇毒眼鏡蛇當成繩子抓）**：系統盲目放行低毛利、原料斷貨或合規違約的急單，**一次出局，直接宣告倒閉！**

本模擬器將大語言模型架構工程（A43 13/15 元件）映射至 **SDP12 雙系統九宮格**，引導三階層人員（經營層、管理層、基層）親手配置積木，理解「小腦快篩（S1）」與「大腦慢想（S2）」的分流與動態演化。

---

## 🏛️ SDP12 九宮格功能分區架構 (Architecture)

```
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│ ① Must-be (基本及格線)  │ ② One-Dim (一維速度感)   │ ③ Attractive (魅力大紅包)│
│ (沒做到客戶掀桌)         │ (越快處理越省錢)         │ (抓到外協現貨大商機)     │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ ④ Reverse (好心做壞事)  │ ⑤ System 1 (小腦反射區) │ ⑥ System 2 (大腦精算區) │
│ (慢想塞快篩，算力爆炸)   │ (0.1秒光速防呆，佔90%)   │ (10秒深度推演抓右尾)     │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ ⑦ Type 1 誤殺 (草木皆兵) │ ⑧ Type 2 漏放 (致命地雷) │ ⑨ 常態分佈工單 (日常90%)│
│ (繩子當蛇，小成本看一眼) │ (蛇當繩子，一次暴死出局) │ (18張日常、1張蛇、1張鑽石)│
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

---

## 📦 4-Piece Judge Minimal Delivery Kit (極簡交付件)

本專案符合 A51 主權星系標準之「四件套極簡交付標準」：

1. **Clean Interface (無依賴網頁介面)**：
   * 根目錄 [`index.html`](index.html) 為純前端單檔 React 18 + Tailwind SPA，零後端依賴，雙擊即可運行，已啟用 GitHub Pages 部署。
2. **CLI (命令列模擬器)**：
   * [`cli.py`](cli.py)：提供無頭命令列拓撲檢查與 20 張卡牌批次蒙地卡羅模擬。
3. **Engine / Contracts (核心引擎與強型別契約)**：
   * [`src/contracts.py`](src/contracts.py)：13 元件 SSOT、情境與卡牌資料結構。
   * [`src/linter.py`](src/linter.py)：確定性拓撲靜態檢查器（DAG Linter，含 MCP 3x 懲罰與反向品質捕捉）。
   * [`src/deck.py`](src/deck.py)：20-Card 機率抽牌與混淆矩陣結算狀態機。
4. **<10ms One-Click Test (毫秒級一鍵驗收套件)**：
   * [`tests/test_audit.py`](tests/test_audit.py)：零第三方依賴單元測試，執行時間 < 1ms，100% 斷言通過。

---

## 🚀 快速開始 (Quick Start)

### 1. 瀏覽器在線體驗
直接訪問 GitHub Pages 部署站點：  
👉 **[https://sdrmsung.github.io/Sovereign-E-Game-of-Small-World/](https://sdrmsung.github.io/Sovereign-E-Game-of-Small-World/)**

### 2. 命令列審計與模擬
```bash
# 執行拓撲語法檢查
python cli.py --audit

# 執行 20 張卡牌批次模擬（製造業情境）
python cli.py --run --scenario MANUFACTURING --draws 20
```

### 3. 一鍵毫秒級驗收
```bash
python -m unittest tests/test_audit.py
```

---

## 📜 授權協議 (License)
本專案基於 **[Apache 2.0 License](LICENSE)** 條款開源發布。
