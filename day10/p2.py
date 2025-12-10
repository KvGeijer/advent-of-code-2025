from z3 import *
import json

with open("parsed.txt", "r") as f:
    machines = json.load(f)

def solve_joltage(buttons, joltages):
    opt = Optimize()
    
    # Set up each line
    lines = [IntVal(0) for i in range(len(joltages))]
    press_vec = [Int(f"press_button{i}") for i in range(len(buttons))]
    
    # Create Lhs
    for i, (button, presses) in enumerate(zip(buttons, press_vec)):
        opt.add(presses >= 0)
        for ind in button:
            lines[ind] += presses

    # Specify lhs = rhs
    for ind in range(len(joltages)):
        opt.add(lines[ind] == joltages[ind])

    opt.minimize(Sum(press_vec))

    result = opt.check()
    if result.r != 1:
        print("Could not solve model!")
        exit(-1)
    else:
        m = opt.model()
        return sum(int(m[p].as_long()) for p in press_vec)

# Oh how I long for the Zote pipes :)
print(sum(solve_joltage(ind_buttons, joltages) for (_, _, ind_buttons, joltages) in machines))
