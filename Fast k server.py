import time
import random
from math import inf

# Weighted Median Finder
def find_weighted_median(i, j, W):
    # i, j: interval boundaries (1-based index)
    # W: prefix-sum array where W[x] = sum of w[1..x]       
    # return: weighted median index m 
    
    totalW = W[j] - W[i - 1]                          # total weight on interval 
    target = W[i - 1] + (totalW + 1) // 2             # first position >= half

    # Linear scan (O(n)) for simplicity
    m = i
    for pos in range(i, j + 1):
        if W[pos] >= target:
            m = pos
            break
    return m


# Fast Response k-Server Algorithm(STEP1 ~ STEP4)

def fast_response_k_server(n, k, w): 
    # n: number of clients (1..n) / k: number of servers / w: traffic array, w[1..n], w[0] unused
       
    # STEP 1: Prefix Sums
    # W[i]  = sum of w[1..i] → traffic prefix sum
    # XW[i] = sum of i*w[i] → location × traffic prefix sum
    W = [0] * (n + 1)
    XW = [0] * (n + 1)
    for i in range(1, n + 1):
        W[i] = W[i - 1] + w[i]        # prefix sum
        XW[i] = XW[i - 1] + i * w[i]  # weighted prefix sum

    
    # STEP 2: Precompute cost(i, j)
    # cost(i, j):
    #  - minimum total weighted distance when ONE server covers interval [i..j]
    # best_server[i][j]:
    #  - optimal server location for interval [i..j]
        
    # Initialize cost table (n+1) x (n+1)
    cost = []
    for i in range(n + 1):
        row = []
        for j in range(n + 1):
            row.append(0)
        cost.append(row)

    # Initialize best_server table (n+1) x (n+1)
    best_server = []
    for i in range(n + 1):
        row = []
        for j in range(n + 1):
            row.append(0)
        best_server.append(row)


    for i in range(1, n + 1):
        for j in range(i, n + 1):

            # (1) Find weighted median m 
            m = find_weighted_median(i, j, W)
            best_server[i][j] = m

            # (2) Compute cost for interval [i..j] / 
            # Left side cost 
            if i <= m - 1:
                WL = W[m - 1] - W[i - 1]        # sum of w[i..m-1]
                XL = XW[m - 1] - XW[i - 1]      # sum of t*w[t] over i..m-1
                Left = m * WL - XL
            else:
                Left = 0

            # Right side cost
            if m + 1 <= j:
                WR = W[j] - W[m]
                XR = XW[j] - XW[m]
                Right = XR - m * WR
            else:
                Right = 0

            cost[i][j] = Left + Right           # total cost / 총 비용

    
    # STEP 3: Dynamic Programming for k servers
    # DP[t][j] = minimum cost to cover clients [1..j] using t servers
    # Recurrence:
    # DP[t][j] = min over i < j of { DP[t-1][i] + cost(i+1, j) }
    
    # Initialize DP table (k+1) x (n+1)
    DP = []
    for t in range(k + 1):
        row = []
        for j in range(n + 1):
            row.append(inf)  
        DP.append(row)

    # Initialize choice table (k+1) x (n+1)
    choice = []
    for t in range(k + 1):
        row = []
        for j in range(n + 1):
            row.append(-1)   
        choice.append(row)

    DP[0][0] = 0  # Base case 

    # Case: Using 1 server → cost(1, j)
    for j in range(1, n + 1):
        DP[1][j] = cost[1][j]
        choice[1][j] = 0

    # Case: t >= 2
    for t in range(2, k + 1):
        for j in range(1, n + 1):
            if j < t:
                continue  # cannot cover 
            best_val = inf
            best_i = -1
            for i in range(t - 1, j):
                val = DP[t - 1][i] + cost[i + 1][j]
                if val < best_val:
                    best_val = val
                    best_i = i
            DP[t][j] = best_val
            choice[t][j] = best_i

    min_total_cost = DP[k][n]

    # STEP 4: Backtracking to find actual server locations
    # Using choice[][] reconstruct:
    #   - how segments were split
    #   - the optimal server position in each segment
    # choice[t][j] tells where the last split occurred.
    segments = []
    t = k
    j = n
    while t > 0:
        i = choice[t][j]
        L = i + 1
        R = j
        segments.append((L, R))  # server t covers [L..R]
        j = i
        t -= 1

    segments.reverse()  # make it server 1..k order 

    # Compute final server positions (weighted median)
    server_positions = []
    for (L, R) in segments:
        if L <= R:
            server_positions.append(best_server[L][R])
        else:
            server_positions.append(None)

    return min_total_cost, server_positions, segments


# ---------------------------------------
# Random Input Generator / max_w is 10
# ---------------------------------------
def make_weights(n, max_w=10):
    # Generate random traffic values.
    w = [0] * (n + 1)
    for i in range(1, n + 1):
        w[i] = random.randint(1, max_w)
    return w

# Running Time Measurement (Median of reps)
def get_time_k_server(n, k, reps=9):
    # Return median running time over 'reps' runs.    
    
    w = make_weights(n)
    times = []

    for _ in range(reps):
        t1 = time.perf_counter_ns()
        fast_response_k_server(n, k, w)
        t2 = time.perf_counter_ns()
        times.append(t2 - t1)

    times.sort()
    return times[len(times) // 2]  # Median 


# Main experiment loop 
if __name__ == "__main__":
    data_list = [10, 50, 100, 150, 200]   # n values for testing
                                       
    k = 3  # number of servers

    print("n,time(ns)")
    for n in data_list:
        t = get_time_k_server(n, k)
        print(f"{n},{t}")

    
    # w = make_weights(10)
    # min_cost, server_pos, segs = fast_response_k_server(10, k, w)
    # print("\nExample result for n = 10:")
    # print("weights:", w[1:])
    # print("min_cost:", min_cost)
    # print("server positions:", server_pos)
    # print("segments:", segs)
