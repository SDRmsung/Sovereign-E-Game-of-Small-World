"""
Piece 4: <10ms One-Click Test for Sovereign-E-Game-of-Small-World.
Zero third-party dependencies. Strict assertion of deterministic architecture.
"""
import unittest
import time
from src.contracts import COMPONENTS_SSOT, AgentComponent
from src.linter import validate_topology
from src.deck import create_deck, execute_simulation_batch

class TestSmallWorldAudit(unittest.TestCase):
    def setUp(self):
        self.comp_map = {c.id: c for c in COMPONENTS_SSOT}

    def test_ssot_completeness(self):
        """Verify all 13 components exist in SSOT."""
        self.assertEqual(len(COMPONENTS_SSOT), 14)  # 13 standard + K1/W1/etc
        self.assertIn('K1', self.comp_map)
        self.assertIn('W1', self.comp_map)
        self.assertIn('A1', self.comp_map)
        self.assertIn('C4', self.comp_map)
        self.assertIn('C5', self.comp_map)

    def test_linter_missing_w1(self):
        """Linter must reject topology without W1 intent contract."""
        s1 = [self.comp_map['K1'], self.comp_map['A1']]
        s2 = []
        contracts = []
        result = validate_topology(s1, s2, contracts)
        self.assertFalse(result.valid)
        self.assertTrue(any(e['code'] == 'ERR_NO_W1' for e in result.errors))

    def test_linter_missing_k1_context(self):
        """Linter must reject slot without K1 Context root."""
        s1 = [self.comp_map['A1']]
        s2 = []
        contracts = [self.comp_map['W1']]
        result = validate_topology(s1, s2, contracts)
        self.assertFalse(result.valid)
        self.assertTrue(any(e['code'] == 'ERR_NO_CONTEXT' for e in result.errors))

    def test_linter_reverse_quality_detection(self):
        """Linter must flag Reverse Quality when heavy reasoning W3 is placed in S1."""
        s1 = [self.comp_map['K1'], self.comp_map['W3']]
        s2 = []
        contracts = [self.comp_map['W1']]
        result = validate_topology(s1, s2, contracts)
        self.assertTrue(result.is_reverse_quality)
        self.assertIn('W3', result.reverse_components)

    def test_type2_error_bankruptcy(self):
        """Simulation must immediately halt with BANKRUPT if hazard card is drawn without C4 Hook."""
        s1 = [self.comp_map['K1'], self.comp_map['A1']]
        s2 = []
        contracts = [self.comp_map['W1']]
        linter = validate_topology(s1, s2, contracts)

        # Force a hazard card
        from src.contracts import Card
        deck = [Card(id='HAZ', card_type='LEFT_TAIL', title='Hazard', content='Crash', hazard_penalty=50000)]
        capital, status, matrix = execute_simulation_batch(deck, s1, s2, linter, initial_capital=10000)
        self.assertEqual(status, 'BANKRUPT')
        self.assertEqual(matrix['type2'], 1)
        self.assertLess(capital, 0)

    def test_safe_interception_with_c4(self):
        """Simulation must safely intercept hazard card and trigger HITL when C4 Hook is present."""
        s1 = [self.comp_map['K1'], self.comp_map['A1'], self.comp_map['C4']]
        s2 = []
        contracts = [self.comp_map['W1']]
        linter = validate_topology(s1, s2, contracts)

        from src.contracts import Card
        deck = [Card(id='HAZ', card_type='LEFT_TAIL', title='Hazard', content='Crash', hazard_penalty=50000)]
        capital, status, matrix = execute_simulation_batch(deck, s1, s2, linter, initial_capital=10000)
        self.assertEqual(status, 'COMPLETED')
        self.assertEqual(matrix['intercepted'], 1)
        self.assertEqual(matrix['type2'], 0)

    def test_execution_latency_under_10ms(self):
        """Audit test suite must complete execution in under 10 milliseconds."""
        start = time.perf_counter()
        deck = create_deck('MANUFACTURING')
        s1 = [self.comp_map['K1'], self.comp_map['A1'], self.comp_map['C4'], self.comp_map['C5']]
        s2 = [self.comp_map['K1'], self.comp_map['W3'], self.comp_map['A3'], self.comp_map['C2'], self.comp_map['C3']]
        contracts = [self.comp_map['W1']]
        linter = validate_topology(s1, s2, contracts)
        execute_simulation_batch(deck, s1, s2, linter)
        elapsed_ms = (time.perf_counter() - start) * 1000
        self.assertLess(elapsed_ms, 10.0, f"Execution took {elapsed_ms:.2f}ms, exceeding 10ms threshold!")

if __name__ == '__main__':
    unittest.main()
