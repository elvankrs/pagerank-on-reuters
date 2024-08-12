import sys

def read_data(data_path):
  vertice_dict = {}
  matrix = []
  processing_edges = False

  # Open and read the file
  with open(data_path, 'r') as file:
      for line in file:
          if line.startswith("*Vertices"):
              num_vertices = int(line.split()[1])
              # Initialize the link matrix with zeros
              matrix = [[0] * num_vertices for _ in range(num_vertices)]
          elif line.startswith("*Edges"):
              # Begin processing edges from the next line
              processing_edges = True
              continue
          elif processing_edges:  # Process edges after *Edges is encountered
              start, end = map(int, line.split())
              start, end = start - 1, end - 1
              matrix[start][end] += 1
              matrix[end][start] += 1  # for an undirected network
          else:
              # Process vertices before *Edges is encountered
              vertice_no, name = line.split()
              if vertice_no.isdigit():
                  vertice_dict[int(vertice_no)] = name[1:-1]
  return matrix, vertice_dict

def get_trans_prob_matrix(link_matrix, teleportation_rate):
  num_vertices = len(link_matrix)
  trans_prob_matrix = []
  for row in link_matrix:
    row_sum = sum(row)
    trans_prob_matrix.append([(elem / row_sum) * (1 - teleportation_rate) + teleportation_rate / num_vertices if row_sum > 0 
                              else teleportation_rate / num_vertices for elem in row])
  return trans_prob_matrix

def matrix_vector_multiply(vector, matrix):
    result = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += vector[j] * matrix[j][i]
    return result

def vector_difference_norm(vec1, vec2):
    return sum(abs(a - b) for a, b in zip(vec1, vec2))

def pagerank(link_matrix, teleportation_rate=0.10, tolerance=1e-6, max_iterations=1000):

  trans_prob_matrix = get_trans_prob_matrix(link_matrix, teleportation_rate=0.10) # transition probability matrix
  x = [1] + [0] * (len(trans_prob_matrix) - 1) # Initialize the arbitrary vector x with a 1 at the first position

  # Power iteration method
  iteration = 0
  while iteration < max_iterations:
    temp = x  # Store the current vector before updating
    x = matrix_vector_multiply(x, trans_prob_matrix)
    if vector_difference_norm(temp, x) <= tolerance: # When the vector is very close to its previous version, exit the loop
      break
    iteration += 1

  # Sort scores and indices
  sorted_indices = sorted(range(len(x)), key=lambda i: x[i], reverse=True)[:20]
  sorted_scores = [x[i] for i in sorted_indices]

  return sorted_indices, sorted_scores

def print_results(sorted_indices, sorted_scores, vertice_dict):
  
  cols = ["Rank", "Person Name", "Score"]
  print(f"{cols[0]:<6} {cols[1]:<15} {cols[2]:>10}")
  print("-" * (len(" ".join(cols)) + 13))

  for rank_idx, vertice_idx, score in zip(range(1, 21), sorted_indices, sorted_scores):
    print("{:<6d} {:<15s} {:^10.11f} ".format(rank_idx, vertice_dict[vertice_idx], score))

data_path = sys.argv[1]

link_matrix, vertice_dict = read_data(data_path)
sorted_indices, sorted_scores = pagerank(link_matrix, teleportation_rate=0.10, tolerance=1e-6, max_iterations=1000)
print_results(sorted_indices, sorted_scores, vertice_dict)