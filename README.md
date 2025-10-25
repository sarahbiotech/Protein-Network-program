 Protein Network Viewer:

A Python program for building and visualizing connections between two or more proteins.  
Users can input protein names separated by commas, click the "Generate Network" button, and the program identifies and highlights the most connected proteins (hubs) within the network.


 Features: 
 
- Build protein interaction networks from Python.
- Highlight highly connected proteins (main proteins are shown in red).
- Export results as PNG (network image) and CSV (interaction data).
- Select different network layouts: spring, circular, shell.

 Requirements: 
 
- Python 3.x
- Required Python libraries:
  
  pip install requests networkx matplotlib

- Operating system: Windows, Mac, or Linux (depending on your Python setup)

Usage: 

- Download the source code from this repository.

- Run the program using Python:

   python src/proteinnet.py

- Input protein names separated by commas.

- Click "Generate Network" to visualize interactions.

- Save the network as PNG or save the report as CSV.

Example:

- Input: ProteinA, ProteinB, ProteinC

- Output: A network visualization highlighting interactions and showing the most connected proteins.

⚠️ Copyright & Usage

- This code  developed by Sarah Ali.

- You are welcome to study, use, or modify the code for personal or educational purposes, but you must give credit to the original author.

Notes:

- Main proteins (the ones you entered) are shown in red in the network.

- The report includes the top interactions, node counts, edge counts, and the most connected protein.

