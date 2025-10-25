import requests
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import csv

G = None
data_global = []
main_proteins_global = []
selected_layout = "spring"

def get_string_interactions(protein_names, species=9606, score_threshold=400):
    all_data = []
    for protein_name in protein_names:
        url = "https://string-db.org/api/json/network"
        params = {
            "identifiers": protein_name,
            "species": species,
            "required_score": score_threshold
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if "error" not in data:
                all_data.extend(data)
        except:
            continue
    return all_data

def get_layout(G):
    global selected_layout
    if selected_layout == "spring":
        return nx.spring_layout(G, seed=42)
    elif selected_layout == "circular":
        return nx.circular_layout(G)
    elif selected_layout == "shell":
        return nx.shell_layout(G)
    else:
        return nx.spring_layout(G, seed=42)

def build_network(data, protein_names):
    global G, data_global, main_proteins_global
    G = nx.Graph()
    main_proteins = set([p.strip() for p in protein_names])
    main_proteins_global = main_proteins
    data_global = data

    for interaction in data:
        a = interaction['preferredName_A']
        b = interaction['preferredName_B']
        G.add_node(a)
        G.add_node(b)
        G.add_edge(a, b, weight=interaction['score'])

    node_colors = ['red' if node in main_proteins else 'lightblue' for node in G.nodes()]
    pos = get_layout(G)

    plt.figure(figsize=(10,8))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=10, edge_color='gray')
    plt.show()

    generate_report(G, main_proteins, data)

def generate_report(G, main_proteins, data, save_path=None):
    if not save_path:
        save_path = "protein_network_report.txt"
    with open(save_path, "w") as f:
        f.write("=== Protein Network Report ===\n\n")
        f.write(f"Main proteins: {', '.join(main_proteins)}\n")
        f.write(f"Number of nodes: {G.number_of_nodes()}\n")
        f.write(f"Number of edges: {G.number_of_edges()}\n\n")

        degrees = dict(G.degree())
        max_deg_node = max(degrees, key=degrees.get)
        f.write(f"Most connected protein: {max_deg_node} ({degrees[max_deg_node]} connections)\n\n")

        sorted_edges = sorted(data, key=lambda x: x['score'], reverse=True)[:5]
        f.write("Top 5 interactions:\n")
        for edge in sorted_edges:
            f.write(f"{edge['preferredName_A']} - {edge['preferredName_B']}, score: {edge['score']}\n")
        f.write("\n")

        scores = [edge['score'] for edge in data]
        if scores:
            f.write(f"Max score: {max(scores)}\n")
            f.write(f"Min score: {min(scores)}\n")
            f.write(f"Average score: {sum(scores)/len(scores):.2f}\n\n")

        f.write("Protein list:\n")
        for node in G.nodes():
            tag = "(Main)" if node in main_proteins else ""
            f.write(f"{node} {tag}\n")
    print(f"Report saved to {save_path}")
    os.startfile(save_path)

def save_network_png():
    if G is None:
        messagebox.showerror("Error", "Network has not been generated yet!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files","*.png")])
    if not file_path:
        return
    node_colors = ['red' if node in main_proteins_global else 'lightblue' for node in G.nodes()]
    pos = get_layout(G)
    plt.figure(figsize=(10,8))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=10, edge_color='gray')
    plt.savefig(file_path)
    messagebox.showinfo("Saved", f"Network saved as image: {file_path}")

def save_report_csv():
    if not data_global:
        messagebox.showerror("Error", "Network has not been generated yet!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if not file_path:
        return
    with open(file_path, "w", newline='') as csvfile:
        fieldnames = ['Protein A', 'Protein B', 'Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for edge in data_global:
            writer.writerow({'Protein A': edge['preferredName_A'], 'Protein B': edge['preferredName_B'], 'Score': edge['score']})
    messagebox.showinfo("Saved", f"Report saved as CSV: {file_path}")

def generate_network():
    proteins_input = entry.get().strip()
    if not proteins_input:
        messagebox.showerror("Error", "Please enter protein names!")
        return
    protein_names = [p.strip() for p in proteins_input.split(",")]
    data = get_string_interactions(protein_names)
    if not data:
        messagebox.showinfo("No Data", f"No interactions found for: {proteins_input}")
    else:
        build_network(data, protein_names)

def set_layout():
    global selected_layout
    selected_layout = layout_var.get()

# Tkinter GUI
root = tk.Tk()
root.title("Protein Network Viewer- Developed by: Sarah")
root.geometry("600x400")
root.resizable(False,False)

tk.Label(root, text="Enter protein names").pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Generate Network", command=generate_network).pack(pady=5)

tk.Button(root, text="Save Network as PNG", command=save_network_png).pack(pady=5)
tk.Button(root, text="Save Report as CSV", command=save_report_csv).pack(pady=5)

# Layout selection
layout_var = tk.StringVar(value="spring")
tk.Label(root, text="Select network layout:").pack(pady=5)
tk.OptionMenu(root, layout_var, "spring", "circular", "shell", command=lambda x: set_layout()).pack(pady=5)

root.mainloop()





