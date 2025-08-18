#!/usr/bin/env python3
"""Run simulations from command line and print JSON result."""
import argparse
import json
import os
import sys

# ensure project root is on sys.path so `src` package is importable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.usecases.game import simulate_games

parser = argparse.ArgumentParser(description='Run game simulations')
parser.add_argument('-n', '--n', type=int, default=1, help='number of simulations')
parser.add_argument('--seed', type=int, default=None, help='random seed')

if __name__ == '__main__':
    args = parser.parse_args()
    res = simulate_games(n=args.n, seed=args.seed)
    # If batch, print a compact human summary then the full JSON
    if isinstance(res, dict) and res.get('simulacoes') and res['simulacoes'] > 1:
        print('Simulações:', res['simulacoes'])
        print('Seed:', res.get('seed'))
        print('Média de rodadas:', res.get('media_rodadas'))
        print('\nVitorias:')
        wins = res.get('vitorias', {})
        perc = res.get('percentuais', {})
        for k in wins:
            print(f"  {k}: {wins[k]} ({perc.get(k, 0):.2f}%)")
        print('\n--- JSON completo ---')
    print(json.dumps(res, ensure_ascii=False, indent=2))
