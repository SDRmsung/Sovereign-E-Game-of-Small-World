"""
Probability Deck Engine & Scenario Definitions.
Position ⑨ (18 cards) + Left Tail Hazard (1 card) + Right Tail Opportunity (1 card).
"""
import random
from typing import List, Tuple
from src.contracts import Card, AgentComponent, LintResult

def create_deck(scenario: str = 'MANUFACTURING') -> List[Card]:
    deck: List[Card] = []
    # 18 Routine cards
    for i in range(18):
        deck.append(Card(
            id=f'ROUTINE_{i+1}',
            card_type='ROUTINE',
            title=f'常態日常工單 #{i+1}',
            content='庫存充足，機台順暢，適合 System 1 快篩推進。',
            base_margin=1200
        ))
    # 1 Left-Tail card (Hazard - Snake)
    deck.append(Card(
        id='CARD_HAZARD',
        card_type='LEFT_TAIL',
        title='左尾黑天鵝・毒蛇',
        content='原料短缺！機台故障！毛利跌破 15% 邊界！',
        hazard_penalty=50000
    ))
    # 1 Right-Tail card (Opportunity - Diamond)
    deck.append(Card(
        id='CARD_OPPORTUNITY',
        card_type='RIGHT_TAIL',
        title='右尾大商機・鑽石',
        content='跨國巨頭尋求備援長約！',
        reward=30000,
        requires_in_s2=['W3', 'A3', 'C2', 'C3']
    ))
    random.shuffle(deck)
    return deck

def execute_simulation_batch(
    deck: List[Card],
    s1: List[AgentComponent],
    s2: List[AgentComponent],
    linter: LintResult,
    initial_capital: int = 100000
) -> Tuple[int, str, dict]:
    capital = initial_capital
    matrix = {'passed': 0, 'type1': 0, 'type2': 0, 'intercepted': 0}
    has_hook = any(c.id == 'C4' for c in (s1 + s2))

    for card in deck:
        if linter.is_reverse_quality and card.card_type == 'ROUTINE':
            capital -= 2000

        if card.card_type == 'ROUTINE':
            s1_ready = any(c.id == 'K1' for c in s1) and any(c.id in ('A1', 'A2', 'A2_DISTILLED') for c in s1)
            profit = card.base_margin if s1_ready else int(card.base_margin * 0.4)
            cost = sum(c.cost for c in s1)
            capital += profit - cost
            matrix['passed'] += 1

        elif card.card_type == 'LEFT_TAIL':
            if has_hook:
                matrix['intercepted'] += 1
                matrix['type1'] += 1
                capital += 3500  # HITL safe recovery
            else:
                matrix['type2'] += 1
                capital -= card.hazard_penalty
                return capital, 'BANKRUPT', matrix

        elif card.card_type == 'RIGHT_TAIL':
            s2_ok = all(req in [c.id for c in s2] for req in card.requires_in_s2)
            has_distilled = any(c.id == 'A2_DISTILLED' for c in s1)
            if s2_ok or has_distilled:
                capital += card.reward

    return capital, 'COMPLETED', matrix
