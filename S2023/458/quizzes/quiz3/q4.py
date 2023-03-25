import sys
 
 
# Function to find the most efficient way to multiply
# a given sequence of matrices
def matrixChainMultiplication(dims):
 
    n = len(dims)
 
    # c[i, j] = minimum number of scalar multiplications (i.e., cost)
    # needed to compute matrix `M[i] M[i+1] … M[j] = M[i…j]`
    # The cost is zero when multiplying one matrix
    c = [[0 for x in range(n + 1)] for y in range((n + 1))]
 
    for length in range(2, n + 1):        # subsequence lengths
 
        for i in range(1, n - length + 2):
 
            j = i + length - 1
            c[i][j] = sys.maxsize
 
            k = i
            while j < n and k <= j - 1:
                cost = c[i][k] + c[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
 
                if cost < c[i][j]:
                    c[i][j] = cost
 
                k = k + 1
 
    return c[1][n - 1]
 
 
if __name__ == '__main__':
 
    # Matrix `M[i]` has dimension `dims[i-1] × dims[i]` for `i=1…n`
    # input is 10 × 30 matrix, 30 × 5 matrix, 5 × 60 matrix
    dims = [5, 10, 15, 50, 20, 100]
 
    print('The minimum cost is', matrixChainMultiplication(dims))