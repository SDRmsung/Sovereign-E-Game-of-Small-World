#!/usr/bin/env python3
"""
Sovereign-E-Game-of-Small-World: Headless CLI Engine.
Usage:
    python cli.py --audit
    python cli.py --run --scenario MANUFACTURING --draws 20
"""
import argparse
import sys
from src.contracts import COMPONENTS_SSOT
from src.linter import validate_topology
from src.deck import create_deck, execute_simulation_batch

def main():
    parser = argparse.ArgumentParser(description="A47 Game of Small World CLI Engine")
    parser.add_argument("--audit", action="store_true", help="Run topology linter audit")
    parser.add_argument("--run", action="store_true", help="Run 20-card simulation")
    parser.add_argument("--scenario", default="MANUFACTURING", choices=["MANUFACTURING", "SERVICE"])
    parser.add_argument("--draws", type=int, default=20, help="Number of cards to draw")
    args = parser.parse_args()

    comp_map = {c.id: c for c in COMPONENTS_SSOT}

    # Standard safe baseline configuration
    contracts = [comp_map['W1']]
    s1 = [comp_map['K1'], comp_map['A1'], comp_map['C4'], comp_map['C5']]
    s2 = [comp_map['K1'], comp_map['W3'], comp_map['A3'], comp_map['C2'], comp_map['C3']]

    linter = validate_topology(s1, s2, contracts)

    if args.audit or not args.run:
        print("=== A47 SOVEREIGN TOPOLOGY AUDIT ===")
        print(f"Topology Valid: {linter.valid}")
        print(f"ACT Cost Multiplier: {linter.act_cost_multiplier}x")
        print(f"Reverse Quality Detected: {linter.is_reverse_quality}")
        if linter.errors:
            print("Errors:", linter.errors)
        if linter.warnings:
            print("Warnings:", linter.warnings)

    if args.run:
        print(f"\n=== EXECUTING SIMULATION ({args.scenario}) ===")
        deck = create_deck(args.scenario)
        if args.draws < len(deck):
            deck = deck[:args.draws]
        final_capital, status, matrix = execute_simulation_batch(deck, s1, s2, linter)
        print(f"Execution Status: {status}")
        print(f"Final Capital: ${final_capital:,}")
        print(f"Confusion Matrix: Passed={matrix['passed']}, Intercepted={matrix['intercepted']}, Type1={matrix['type1']}, Type2={matrix['type2']}")

if __name__ == "__main__":
    main()
