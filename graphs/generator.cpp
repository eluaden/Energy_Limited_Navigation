#include <bits/stdc++.h>
#include "jngen.h"

using namespace std;

int main(int argc, char *argv[]) {
    registerGen(argc, argv);
    parseArgs(argc, argv);

    int n = getOpt(0), m = getOpt(1), limWeight = getOpt(2),
     limCost = getOpt(3), heavyPercent = getOpt(4), lightPercent = getOpt(5),
     rechargePercent = getOpt(6);

    ensure(heavyPercent + lightPercent <= 100, "Heavy and light percentages must sum up to at most 100");
    ensure(rechargePercent <= 100, "Recharge percentage must be at most 100");
    ensure(heavyPercent >= 0 && lightPercent >= 0 && rechargePercent >= 0, "Percentages must be non-negative");
    ensure(n > 0, "Number of vertices must be positive");
    ensure(m >= n - 1, "Number of edges must be at least n-1 for a connected graph");
    ensure(limWeight > 0, "Limit for weights must be positive");
    ensure(limCost > 0, "Limit for costs must be positive");
    ensure(rechargePercent >= 0 && rechargePercent <= 100, "Recharge percentage must be between 0 and 100");    
    
    Graph g = Graph::random(n, m).connected().allowMulti();
    auto edges = g.edges();

    cout << n << " " << m << "\n";
    for(auto u : edges) {
        int weight;
        int randPercent = rnd.next(1, 100);
        if(randPercent <= heavyPercent) {
            weight = rnd.next(9 * limWeight / 10, limWeight);
        } else if(randPercent <= heavyPercent + lightPercent) {
            weight = rnd.next(1, limWeight / 10);
        } else {
            weight = rnd.next(1, limWeight);
        }
        cout << u.first + 1 << " " << u.second + 1 << " " << weight << "\n";
    }

    int postos = n * rechargePercent / 100;
    cout << postos << "\n";
    auto vertices = Array::randomUnique(postos, 1, n);
    for(int v : vertices) {
        int cost = rnd.next(1, limCost);
        cout << v << " " << cost << "\n";
    }
    return 0;
}