"""
Sovereign-E-Game-of-Small-World: Contracts and Schema Definitions (SSOT)
Aligned with DLOS v22.0, A43 13/15 Elements, A45 Small World Lattice, and SDP12 9-Position Map.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class AgentComponent:
    id: str
    code: str
    name: str
    pillar: str  # 'KNOW', 'WANT', 'ACT', 'CONTROL'
    cost: int
    latency: int
    allowed_slots: List[str]
    requires: List[str]
    description: str
    reverse_risk: str = "無"

@dataclass
class LintResult:
    valid: bool = True
    errors: List[Dict[str, str]] = field(default_factory=list)
    warnings: List[Dict[str, str]] = field(default_factory=list)
    act_cost_multiplier: float = 1.0
    is_reverse_quality: bool = False
    reverse_components: List[str] = field(default_factory=list)

@dataclass
class Card:
    id: str
    card_type: str  # 'ROUTINE', 'LEFT_TAIL', 'RIGHT_TAIL'
    title: str
    content: str
    base_margin: int = 0
    hazard_penalty: int = 0
    reward: int = 0
    requires_in_s2: List[str] = field(default_factory=list)

COMPONENTS_SSOT: List[AgentComponent] = [
    AgentComponent('K1', 'KNOW.1', 'Context (即時工單/現場邊界)', 'KNOW', 10, 1, ['SYSTEM_1_SLOT_5', 'SYSTEM_2_SLOT_6'], [], '急單數量、交期、料號或航班取消代碼'),
    AgentComponent('K2', 'KNOW.2', 'Memory (長期記憶/常故障機台)', 'KNOW', 20, 1, ['SYSTEM_1_SLOT_5', 'SYSTEM_2_SLOT_6'], ['K1'], '上次哪家有現貨、熟客偏好，減少重複搜尋', '記憶未更新會導致參數漂移'),
    AgentComponent('K3', 'KNOW.3', 'RAG (API規格書/法規手冊檢索)', 'KNOW', 50, 3, ['SYSTEM_2_SLOT_6'], ['K1'], '檢索 ERP 規格、IATA 退改規則或 IFRS 條文', '放進 ⑤ 快篩區會拖慢日常查詢速度'),
    AgentComponent('W1', 'WANT.1', 'Goal (意圖契約: 毛利>15%)', 'WANT', 0, 0, ['GLOBAL_CONTRACT'], [], '最高決策層鎖定的硬性目標與邊界條件', '未設定則系統無方向亂跑'),
    AgentComponent('W2', 'WANT.2', 'Prompt (角色邊界契約)', 'WANT', 10, 1, ['SYSTEM_1_SLOT_5', 'SYSTEM_2_SLOT_6'], ['W1'], '定義採購/管家權限，嚴禁直接刪庫或無授權下單'),
    AgentComponent('W3', 'WANT.3', 'Reasoning (深度邏輯推演)', 'WANT', 200, 10, ['SYSTEM_2_SLOT_6'], ['K1', 'W1'], '判斷資訊缺口、動態選工具、跨系統取捨', '若放入 ⑤ 快篩區處理 ⑨ 日常案件，直接觸發 ④ 反向品質'),
    AgentComponent('A1', 'ACT.1', 'Tools (ERP庫存/GDS機位API)', 'ACT', 30, 2, ['SYSTEM_1_SLOT_5', 'SYSTEM_2_SLOT_6'], ['K1'], '確定性執行工具，改變或查詢物理世界', '未配 C5 MCP 時串接成本暴增 3 倍'),
    AgentComponent('A2', 'ACT.2', 'Skills (急單毛利速算SOP包)', 'ACT', 50, 3, ['SYSTEM_1_SLOT_5', 'SYSTEM_2_SLOT_6'], ['A1'], '將多個 Tools 封裝成標準作業流程'),
    AgentComponent('A3', 'ACT.3', 'Plugin (外協現貨網/即時匯率)', 'ACT', 100, 5, ['SYSTEM_2_SLOT_6'], ['A1', 'C5'], '外部生態轉接器，捕捉 ③ 魅力品質右尾機會的關鍵', '外部 API 不穩定，未加 C1 Harness 易卡死'),
    AgentComponent('C1', 'CTRL.1', 'Harness (預算裝甲/防無限迴圈)', 'CONTROL', 20, 1, ['SYSTEM_1_SLOT_5', 'SYSTEM_2_SLOT_6'], [], '限制 API 呼叫上限與單次授權金額上限'),
    AgentComponent('C2', 'CTRL.2', 'Loop (動態重試迴圈)', 'CONTROL', 120, 6, ['SYSTEM_2_SLOT_6'], ['W3', 'C1'], '查無庫存或機位客滿時，自動換關鍵字重試', '若未搭配 C1，抽中左尾卡時觸發無限迴圈破產'),
    AgentComponent('C3', 'CTRL.3', 'Graph (DAG 工具鏈編排)', 'CONTROL', 30, 1, ['SYSTEM_1_SLOT_5', 'SYSTEM_2_SLOT_6'], ['A1'], '查庫存 -> 查產能 -> 算毛利的條件分流管線'),
    AgentComponent('C4', 'CTRL.4', 'Hook (安全攔截/毛利<15%熔斷)', 'CONTROL', 15, 1, ['SYSTEM_1_SLOT_5', 'SYSTEM_2_SLOT_6'], ['W1'], '守住 ① 基本品質底線！危險操作或低毛利強制攔截轉 HITL', '不放會導致 ⑧ Type 2 漏放而死'),
    AgentComponent('C5', 'CTRL.5', 'MCP (標準模型上下文協議)', 'CONTROL', 25, 1, ['SYSTEM_1_SLOT_5', 'SYSTEM_2_SLOT_6'], [], '統一結構化呼叫 ERP/MES/GDS，避免私有代碼失控')
]
