#!/usr/bin/env python3
"""
Análise dos resultados do TP1 - Questão 1
Uso: python3 analise.py resultados.csv
"""

import sys, csv, math
from collections import defaultdict

def ler_csv(path):
    dados = defaultdict(list)
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = int(row['threads'])
            dados[t].append(float(row['tempo_s']))
    return dados

def estatisticas(valores):
    n    = len(valores)
    med  = sum(valores) / n
    var  = sum((x - med)**2 for x in valores) / (n - 1) if n > 1 else 0
    dp   = math.sqrt(var)
    cv   = (dp / med * 100) if med > 0 else 0
    return med, dp, cv

def main():
    path      = sys.argv[1] if len(sys.argv) > 1 else "resultados.csv"
    plataforma = sys.argv[2] if len(sys.argv) > 2 else "Plataforma"

    dados = ler_csv(path)
    threads_ord = sorted(dados.keys())

    print(f"\n{'='*60}")
    print(f" Resultados — {plataforma}")
    print(f"{'='*60}")
    print(f"{'Threads':>8} {'Média (s)':>12} {'Desv.Pad':>10} {'CV (%)':>8}  {'Status'}")
    print(f"{'-'*60}")

    medias = {}
    for t in threads_ord:
        med, dp, cv = estatisticas(dados[t])
        medias[t]   = med
        status = "OK" if cv <= 5 else "⚠ CV alto — refazer"
        print(f"{t:>8} {med:>12.4f} {dp:>10.4f} {cv:>8.2f}%  {status}")

    print(f"\n{'='*60}")
    print(" Speedup e Eficiência")
    print(f"{'='*60}")
    t1 = medias.get(1, None)
    if t1:
        print(f"{'Threads':>8} {'Speedup':>10} {'Eficiência':>12}")
        print(f"{'-'*40}")
        for t in threads_ord:
            sp  = t1 / medias[t]
            eff = sp / t * 100
            print(f"{t:>8} {sp:>10.3f} {eff:>11.1f}%")

    print(f"\n{'='*60}")
    print(" Tempo Normalizado (T_n / T_1)")
    print(f"{'='*60}")
    if t1:
        for t in threads_ord:
            print(f"  {t:>2} threads: {medias[t]/t1:.4f}")

    # Tenta gerar gráfico se matplotlib estiver disponível
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Gráfico 1: Tempo médio
        ax = axes[0]
        ax.plot(threads_ord, [medias[t] for t in threads_ord], 'o-', color='steelblue')
        ax.set_xlabel("Número de Threads")
        ax.set_ylabel("Tempo médio (s)")
        ax.set_title(f"Tempo de Execução — {plataforma}")
        ax.grid(True, alpha=0.3)

        # Gráfico 2: Tempo normalizado
        if t1:
            ax2 = axes[1]
            norm = [medias[t]/t1 for t in threads_ord]
            ax2.plot(threads_ord, norm, 'o-', color='darkorange', label=plataforma)
            ax2.axhline(1.0, color='gray', linestyle='--', alpha=0.5)
            ax2.set_xlabel("Número de Threads")
            ax2.set_ylabel("Tempo normalizado (T_n / T_1)")
            ax2.set_title("Curva Normalizada")
            ax2.legend()
            ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        out = f"grafico_{plataforma.replace(' ','_')}.png"
        plt.savefig(out, dpi=150)
        print(f"\nGráfico salvo: {out}")
    except ImportError:
        print("\n(matplotlib não instalado — gráficos não gerados)")

if __name__ == "__main__":
    main()
