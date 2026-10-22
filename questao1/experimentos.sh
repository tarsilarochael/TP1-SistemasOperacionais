#!/bin/bash
# Executa os experimentos do TP1 - Questão 1
# Uso: ./experimentos.sh [num_termos]
# Gera: resultados.csv  (threads, medicao, tempo_s)

export LC_NUMERIC=C   # força ponto como separador decimal no output do time

TERMOS=${1:-1000000000}   # default: 1 bilhão
MEDICOES=5
THREADS="1 2 4 8 16 32"
OUT="resultados.csv"

echo "threads,medicao,tempo_s" > "$OUT"
echo "Experimentos com $TERMOS termos, $MEDICOES medições cada"
echo "Salvando em $OUT"
echo "---"

for T in $THREADS; do
    echo -n "Threads=$T: "
    TEMPOS=()

    for M in $(seq 1 $MEDICOES); do
        # Captura apenas o tempo real (wall-clock) do shell built-in time
        TEMPO=$( { TIMEFORMAT='%R'; time ./piThreads "$T" "$TERMOS" > /dev/null; } 2>&1 )
        TEMPOS+=("$TEMPO")
        echo "$T,$M,$TEMPO" >> "$OUT"
        echo -n "$TEMPO s  "
    done
    echo ""
done

echo "---"
echo "Arquivo gerado: $OUT"
echo ""
echo "Para calcular médias e CVs, execute:"
echo "  python3 analise.py $OUT"
