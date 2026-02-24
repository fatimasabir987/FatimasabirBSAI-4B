X_CAP = 4
Y_CAP = 5
GOAL = 2


def rule1(x, y): 
    return (X_CAP, y)          # Fill X
def rule2(x, y):
    return (x, Y_CAP)          # Fill Y
def rule3(x, y): 
    return (0, y)              # Empty X
def rule4(x, y): 
    return (x, 0)              # Empty Y
def rule5(x, y): # Pour X -> Y until X is empty
    if x + y <= Y_CAP: 
        return (0, x + y)
    return (x, y) # No change if rule doesn't apply cleanly
def rule6(x, y): # Pour X -> Y until Y is full
    if x + y >= Y_CAP: return (x - (Y_CAP - y), Y_CAP)
    return (x, y)
def rule7(x, y): # Pour Y -> X until Y is empty
    if x + y <= X_CAP: return (x + y, 0)
    return (x, y)
def rule8(x, y): # Pour Y -> X until X is full
    if x + y >= X_CAP: return (X_CAP, y - (X_CAP - x))
    return (x, y)

def solve_water_jug():
    stack = [((0, 0), [])]
    visited = set()

    while stack:
        (curr_x, curr_y), path = stack.pop()

        if curr_x == GOAL or curr_y == GOAL:
            return path

        if (curr_x, curr_y) in visited:
            continue
        
        visited.add((curr_x, curr_y))

        all_rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]

        for i, rule_func in enumerate(all_rules, 1):
            state_after_rule = rule_func(curr_x, curr_y)
            
            if state_after_rule not in visited:
                stack.append((state_after_rule, path + [i]))

    return "Goal not reachable"
final_path = solve_water_jug()
print(f"Final Rule Stack: {final_path}")