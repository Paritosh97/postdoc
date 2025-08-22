import json
import sys
import matplotlib.pyplot as plt
import networkx as nx

# -----------------------------
# Node and Edge classes
# -----------------------------
class SceneNode:
    def __init__(self, id, attributes, temporal_states):
        self.id = id
        self.attributes = attributes
        self.temporal_states = temporal_states

class SceneEdge:
    def __init__(self, source, target, rel_type, active_intervals, description=""):
        self.source = source
        self.target = target
        self.rel_type = rel_type
        self.active_intervals = active_intervals
        self.description = description

# -----------------------------
# Load graph from JSON
# -----------------------------
def load_scene_graph(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    
    nodes = {n["id"]: SceneNode(n["id"], n["attributes"], n.get("temporal_states", [])) for n in data["nodes"]}
    edges = [
        SceneEdge(
            e["source"],
            e["target"],
            e["rel_type"],
            e.get("active_intervals", []),
            e.get("description", "")
        ) 
        for e in data["edges"]
    ]
    return nodes, edges

# -----------------------------
# Draw graph
# -----------------------------
def draw_scene_graph(nodes, edges):
    G = nx.DiGraph()

    # Add nodes
    for node_id, node_obj in nodes.items():
        if node_obj.temporal_states:
            states_str = []
            for state_entry in node_obj.temporal_states:
                interval = state_entry.get("time_interval", [0.0, 1.0])
                desc = state_entry.get("description", "")
                states_str.append(f"{interval[0]:.2f}-{interval[1]:.2f}: {desc}")
            label = f"{node_id}\n" + "\n".join(states_str)
        else:
            label = node_id
        G.add_node(node_id, label=label, color=node_obj.attributes.get("color", "grey"))

    # Add edges
    for edge in edges:
        intervals = ", ".join([f"{s:.2f}-{e:.2f}" for s, e in edge.active_intervals])
        label = f"{edge.rel_type}"
        if intervals:
            label += f"\nActive: {intervals}"
        if edge.description:
            label += f"\n{edge.description}"
        G.add_edge(edge.source, edge.target, label=label)

    # Layout & draw
    pos = nx.spring_layout(G, k=0.8, iterations=70, seed=42)
    node_colors = [G.nodes[n]['color'] for n in G.nodes]

    plt.figure(figsize=(14, 12))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1800, edgecolors="black")
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20)
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['label'] for n in G.nodes}, font_size=9)
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)},
        font_color='darkred', font_size=8
    )
    plt.title("Scene Graph")
    plt.axis('off')
    plt.show()

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python display_scene_graph.py <scene_graph.json>")
        sys.exit(1)

    filename = sys.argv[1]
    nodes, edges = load_scene_graph(filename)
    draw_scene_graph(nodes, edges)
