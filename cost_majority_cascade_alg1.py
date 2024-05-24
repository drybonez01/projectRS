import networkx as nx

def load_graph(filename):
    # Carica il grafo dal file .gml usando networkx con label='id'
    G = nx.read_gml(filename, label='id')
    return G

def load_costs(filename):
    costs = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 2:
                continue  # Ignora le righe non valide
            try:
                node = parts[0]
                cost = float(parts[1])
                costs[node] = cost
            except ValueError as e:
                print(f"Errore nella conversione dei dati: {e}")
                continue
    return costs

def f1(S, V, N):
    result = 0
    for v in V:
        N_v_intersection_S = len(N[v].intersection(S))
        result += min(N_v_intersection_S, len(N[v]) // 2)
    return result

def cost_seeds_greedy(G, k, c):
    Sp = set()
    Sd = set()
    total_cost = 0

    N = {v: set(G.neighbors(v)) for v in G.nodes}  # Dizionario dei vicini per ogni nodo

    while True:
        # Trova il nodo che massimizza il beneficio per costo
        u = max((v for v in G.nodes if v not in Sd),
                key=lambda v: (f1(Sd.union({v}), G.nodes, N) - f1(Sd, G.nodes, N)) / c[str(v)])

        # Calcola il costo totale se aggiungiamo questo nodo
        node_cost = c[str(u)]

        # Verifica se l'aggiunta di questo nodo supera il budget
        if total_cost + node_cost > k:
            break

        # Aggiungi il nodo al seed set
        Sp.add(u)
        Sd.add(u)
        total_cost += node_cost

    return Sp

def main():
    graph_file = input("Inserisci il percorso del file del grafo (.gml): ")
    cost_file = input("Inserisci il percorso del file dei costi (.txt): ")
    k = float(input("Inserisci il valore di k: "))

    G = load_graph(graph_file)
    c = load_costs(cost_file)

    Sp = cost_seeds_greedy(G, k, c)

    print("Seed set massimale trovato:", Sp)

if __name__ == "__main__":
    main()