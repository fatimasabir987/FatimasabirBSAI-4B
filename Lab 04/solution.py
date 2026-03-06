def solve_n_queens(n):
    board = [-1] * n      
    solutions = []

    def is_safe(row, col):
        for i in range(row):
            if board[i] == col:
                return False
            if abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def backtrack(row):
        if row == n:                
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(row, col):
                board[row] = col     
                backtrack(row + 1)   
                board[row] = -1      
    backtrack(0)
    return solutions

n = int(input("Enter value of N: "))
solutions = solve_n_queens(n)
print(f"\nTotal Solutions for {n}-Queens:", len(solutions))
for sol in solutions:
    print("\nSolution:")
    for row in sol:
        print("." * row + "Q" + "." * (n - row - 1))