Fast Response k-Server Problem (1D k-Median)
📌 Project Overview

This repository solves the Fast Response k-Server Problem on a linear network. The objective is to place $k$ servers to minimize the total weighted traffic cost, where the cost is the sum of each client's traffic ($w[i]$) multiplied by its distance (number of hops) to the nearest server.

The algorithm uses Dynamic Programming (DP) and leverages the fact that the optimal single-server placement for any contiguous client segment is its weighted median.

Overall Time Complexity: $O(n^3)$ for fixed $k$.

⚙️ How to Run the Code

The main file for this project is fast k server.py.

1. Prerequisites

Python 3 installed on your system.

The implementation uses standard Python libraries; no external packages are required.

2. Execution

Download fast k server.py to your local machine.

Open your terminal or command prompt.

Navigate to the directory containing fast k server.py.

Run the script:

python "fastkserver.py"

3. Inputs

The script uses the function:

fast_response_k_server(N, K, W)

N – number of clients

K – number of servers

W – traffic array (weights for each client)

You can modify these values inside the main block of the script to test different cases.

4. Expected Output

The script will print:

minCost: Minimum total weighted traffic cost

serverLocations: List of $k$ optimal server positions

📖 Theoretical Approach

The algorithm partitions the client sequence into k contiguous segments. For each segment, the optimal cost is computed based on the weighted median. The dynamic programming relation is:

DP[t][j]= min⁡0 ≤ p < j{DP[t−1][p] + Cost(p+1,j)}
DP[t][j]= 0≤p<j
min {DP[t−1][p]+Cost(p+1,j)}

Where:

DP[t][j] = minimum cost of serving the first j clients with t servers

Cost(p+1, j) = cost of serving clients p+1 to j with one server placed optimally

This approach ensures that the total cost is minimized across all possible server placements.
