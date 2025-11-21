import time       # for timing how long the algorithm takes
import random     # for generating random traffic weights
from math import inf  # for representing an infinitely large cost

def find_weighted_median(i, j, W):
    """
    Finds the weighted median of clients in the interval [i..j].
    W is a prefix-sum array of traffic weights.
    Weighted median = the client such that the sum of weights on the left
                      is <= total/2 and on the right is also <= total/2.
    """
    totalW = W[j] - W[i - 1]  # total weight in interval [i..j]
    target = W[i - 1] + (totalW + 1) // 2  # halfway point, rounded up
    m = i
    for pos in range(i, j + 1):
        if W[pos] >= target:
            m = pos
            break
    return m  # best server location for this interval

def fast_response_k_server(n, k, w): 
    """
    Main function to find optimal server positions for k servers.
    n = number of clients
    k = number of servers
    w = traffic array (1-indexed, w[0] unused)
    Returns: minimum total weighted distance, server positions, segments
    """
    
    W = [0] * (n + 1)
    XW = [0] * (n + 1)
    for i in range(1, n + 1):
        W[i] = W[i - 1] + w[i]        # accumulate traffic
        XW[i] = XW[i - 1] + i * w[i]  # accumulate traffic*position
    
    # cost[i][j] = minimal total weighted distance for interval [i..j]
    # best_server[i][j] = position of the optimal server in [i..j]
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    best_server = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            m = find_weighted_median(i, j, W)
            best_server[i][j] = m
            
            if i <= m - 1:
                WL = W[m - 1] - W[i - 1]     # sum of weights to the left
                XL = XW[m - 1] - XW[i - 1]   # sum of positions*weights to the left
                Left = m * WL - XL           # total distance cost left
            else:
                Left = 0  # no clients to the left
            
            if m + 1 <= j:
                WR = W[j] - W[m]            # sum of weights to the right
                XR = XW[j] - XW[m]          # sum of positions*weights to the right
                Right = XR - m * WR          # total distance cost right
            else:
                Right = 0  # no clients to the right
            
            cost[i][j] = Left + Right       # total cost for this interval
    
    # DP[t][j] = min cost to cover clients [1..j] with t servers
    DP = [[inf] * (n + 1) for _ in range(k + 1)]
    choice = [[-1] * (n + 1) for _ in range(k + 1)]  # remembers where last split was
    DP[0][0] = 0  # base case: 0 cost for 0 clients with 0 servers
    
    for j in range(1, n + 1):
        DP[1][j] = cost[1][j]  # one server covering first j clients
        choice[1][j] = 0       # first server covers all
    
    for t in range(2, k + 1):
        for j in range(1, n + 1):
            if j < t:
                continue  # cannot place more servers than clients
            best_val = inf
            best_i = -1
            for i in range(t - 1, j):
                val = DP[t - 1][i] + cost[i + 1][j]
                if val < best_val:
                    best_val = val
                    best_i = i
            DP[t][j] = best_val
            choice[t][j] = best_i
    
    min_total_cost = DP[k][n]  # final minimal total cost
    
    # Backtrack to find segments
    segments = []
    t = k
    j = n
    while t > 0:
        i = choice[t][j]  # where last segment starts
        L = i + 1
        R = j
        segments.append((L, R))  # server t covers [L..R]
        j = i  # move to previous segment
        t -= 1
    segments.reverse()  # segments in order of server 1..k
    
    # Compute final server positions (weighted medians of segments)
    server_positions = []
    for (L, R) in segments:
        if L <= R:
            server_positions.append(best_server[L][R])
        else:
            server_positions.append(None)  # empty segment (should not happen)
    
    return min_total_cost, server_positions, segments

def make_weights(n, max_w=10):
    """
    Generate a random traffic array of size n (1-indexed).
    w[0] is unused.
    """
    w = [0] * (n + 1)
    for i in range(1, n + 1):
        w[i] = random.randint(1, max_w)
    return w

def get_time_k_server(n, k, reps=9):
    """
    Returns median execution time (in ns) of fast_response_k_server
    over 'reps' random runs for given n, k.
    """
    w = make_weights(n)
    times = []
    for _ in range(reps):
        t1 = time.perf_counter_ns()
        fast_response_k_server(n, k, w)
        t2 = time.perf_counter_ns()
        times.append(t2 - t1)
    times.sort()
    return times[len(times) // 2]  # median time

if __name__ == "__main__":
    data_list = [10, 50, 100, 150, 200]  # different client sizes to test
    k = 3  # number of servers

    print("n,time(ns)")
    for n in data_list:
        t = get_time_k_server(n, k)
        print(f"{n},{t}")
    
    # Example run for n = 10
    # w = make_weights(10)
    # min_cost, server_pos, segs = fast_response_k_server(10, k, w)
    # print("\nExample result for n = 10:")
    # print("weights:", w[1:])
    # print("min_cost:", min_cost)
    # print("server positions:", server_pos)
    # print("segments:", segs)
