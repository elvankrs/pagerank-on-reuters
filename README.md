# PageRank on Reuters

This project implements PageRank algorithm using the power iteration method on a social network constructed from co-occurrences of people in news articles. The data used is derived from a subset of the [Reuters-21578](https://archive.ics.uci.edu/dataset/137/reuters+21578+text+categorization+collection) corpus.  

The social network is built from a dataset of news articles, where each node represents a person, and edges between nodes represent co-occurrences of these people within the same article. The PageRank algorithm iteratively calculates the importance (rank) of each person based on their connections to others in the network. A teleportation factor is applied to ensure convergence of the algorithm.

## Usage

- Python version: 3.9.13

No external libraries are required. The project is implemented using only the Python Standard Library.

To run the PageRank algorithm on your data, use the following command:

```
python main.py data_path
```

- `data_path` is the file path containing the edge and vertex information for the network.