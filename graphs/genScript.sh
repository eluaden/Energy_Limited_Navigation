# BASH GERADOR DOS GRAFOS DE TESTE
# USO: bash genScript.sh

# Gerar os grafos de teste
# N = número de vértices
# M = número de arestas
# Wmax = peso máximo das arestas
# Pmax = peso máximo dos vértices
# Hper = percentual de arestas pesadas (peso  >= (9 / 10) * Wmax)
# Lper = percentual de arestas leves (peso <= (1 / 10) * Wmax)
# Pper = percentual de vértices que são pontos de recarga
#           N     M     Wmax    Pmax    Hper    Lper    Pper
./generator 10    15    5       10      0       0       40   >  grafo1.txt
./generator 10    15    50      20      0       0       10   >  grafo2.txt
./generator 100   300   100     50      0       0       20   >  grafo3.txt
./generator 100   300   100     50      10      10      20   >  grafo4.txt
./generator 100   300   100     50      40      40      20   >  grafo5.txt
./generator 100   300   100     50      80      10      20   >  grafo6.txt
./generator 100   300   100     50      10      80      20   >  grafo7.txt
./generator 100   300   100     50      0       0       100  >  grafo8.txt
./generator 100   300   100     50      0       0       50   >  grafo9.txt

echo "Grafos de teste gerados com sucesso!"