"""
Deterministic DAG Linter for Agent Architecture Topology.
Ensures zero-tolerance hard gates: Context root, W1 intent contract, dependency closure, MCP protocol.
"""
from typing import List, Set
from src.contracts import AgentComponent, LintResult

def validate_topology(
    s1: List[AgentComponent],
    s2: List[AgentComponent],
    contracts: List[AgentComponent]
) -> LintResult:
    errors = []
    warnings = []
    all_placed = s1 + s2 + contracts
    all_ids: Set[str] = {c.id for c in all_placed}
    s1_ids: Set[str] = {c.id for c in s1}
    s2_ids: Set[str] = {c.id for c in s2}

    # 1. Global Contract check: must have W1
    if not any(c.id == 'W1' for c in contracts):
        errors.append({'slot': 'GLOBAL', 'code': 'ERR_NO_W1', 'message': '最高決策層未簽署 W1 意圖契約'})

    # 2. Slot dependency and orphan check
    def check_slot(slot_components: List[AgentComponent], slot_name: str, slot_ids: Set[str]):
        has_context = 'K1' in slot_ids or 'K1' in s1_ids
        if slot_components and not has_context:
            errors.append({'slot': slot_name, 'code': 'ERR_NO_CONTEXT', 'message': f'{slot_name} 缺少 K1 Context 起點'})

        for comp in slot_components:
            for req in comp.requires:
                is_satisfied = req in all_ids if req == 'K1' else req in slot_ids
                if not is_satisfied:
                    errors.append({
                        'slot': slot_name,
                        'code': 'ERR_MISSING_DEP',
                        'message': f'{comp.name} 缺少前置依賴 [{req}]'
                    })

        has_control = any(c.pillar == 'CONTROL' for c in slot_components)
        has_act = any(c.pillar == 'ACT' for c in slot_components)
        if has_control and not has_act and slot_components:
            warnings.append({
                'slot': slot_name,
                'code': 'WARN_ORPHAN_CONTROL',
                'message': f'{slot_name} 配置控制元件但無 ACT 執行工具'
            })

    check_slot(s1, 'SYSTEM_1_SLOT_5', s1_ids)
    check_slot(s2, 'SYSTEM_2_SLOT_6', s2_ids)

    # 3. MCP check
    has_act_tools = any(c.id in ('A1', 'A3') for c in all_placed)
    has_mcp = any(c.id == 'C5' for c in all_placed)
    act_mult = 3.0 if (has_act_tools and not has_mcp) else 1.0
    if has_act_tools and not has_mcp:
        warnings.append({'slot': 'GLOBAL', 'code': 'WARN_NO_MCP', 'message': '未配置 C5 MCP，ACT 成本 3x'})

    # 4. Reverse Quality check
    reverse_in_s1 = [c.id for c in s1 if c.id in ('W3', 'C2', 'K3')]
    is_reverse = len(reverse_in_s1) > 0
    if is_reverse:
        warnings.append({
            'slot': 'SYSTEM_1_SLOT_5',
            'code': 'WARN_REVERSE_QUALITY',
            'message': f'S1 誤置慢想/重度元件 {reverse_in_s1}，觸發 ④ 反向品質'
        })

    return LintResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        act_cost_multiplier=act_mult,
        is_reverse_quality=is_reverse,
        reverse_components=reverse_in_s1
    )
