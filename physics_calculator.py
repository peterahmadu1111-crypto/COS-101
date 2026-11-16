"""
Physics Calculator
Each formula has its own calculator function. After every calculation you are
asked whether you want to keep calculating with that formula.
All values use SI units.
"""

import math

G = 6.674e-11   # gravitational constant (N·m²/kg²)
g = 9.81        # gravitational acceleration on Earth (m/s²)


# ---------- Helper functions ----------

def get_number(prompt):
    """Keep asking until the user enters a valid number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a valid number.")


def ask_yes_no(prompt):
    """Return True for yes, False for no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please type y or n.")


def choose_variable(variables):
    """Let the user pick which variable to solve for."""
    print("\nSolve for which variable?")
    for i, (name, unit) in enumerate(variables.items(), 1):
        print(f"  {i}. {name} ({unit})")
    keys = list(variables)
    while True:
        choice = input("Choose: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return keys[int(choice) - 1]
        print("  Invalid choice.")


def read_inputs(variables, target):
    """Ask for every variable except the one being solved for."""
    return {
        name: get_number(f"Enter {name} ({unit}): ")
        for name, unit in variables.items()
        if name != target
    }


def show_result(target, value, unit):
    print(f"\n  {target} = {value:.6g} {unit}")


def repeat_calculator(calculator):
    """Run a calculator, then ask whether to calculate again."""
    while True:
        try:
            calculator()
        except ZeroDivisionError:
            print("\n  Error: division by zero. Check your inputs.")
        except ValueError:
            print("\n  Error: no real solution (square root of a negative number).")
        if not ask_yes_no("\nContinue calculating with this formula? (y/n): "):
            break


# ---------- The six formula calculators ----------

def newtons_second_law():
    """F = m × a"""
    print("\nNewton's Second Law:  F = m × a")
    units = {"F": "N", "m": "kg", "a": "m/s²"}
    target = choose_variable(units)
    v = read_inputs(units, target)

    if target == "F":
        result = v["m"] * v["a"]
    elif target == "m":
        result = v["F"] / v["a"]
    else:
        result = v["F"] / v["m"]
    show_result(target, result, units[target])


def kinetic_energy():
    """KE = ½ × m × v²"""
    print("\nKinetic Energy:  KE = ½ × m × v²")
    units = {"KE": "J", "m": "kg", "v": "m/s"}
    target = choose_variable(units)
    v = read_inputs(units, target)

    if target == "KE":
        result = 0.5 * v["m"] * v["v"] ** 2
    elif target == "m":
        result = 2 * v["KE"] / v["v"] ** 2
    else:
        result = math.sqrt(2 * v["KE"] / v["m"])
    show_result(target, result, units[target])


def potential_energy():
    """PE = m × g × h"""
    print(f"\nGravitational Potential Energy:  PE = m × g × h   (g = {g} m/s²)")
    units = {"PE": "J", "m": "kg", "h": "m"}
    target = choose_variable(units)
    v = read_inputs(units, target)

    if target == "PE":
        result = v["m"] * g * v["h"]
    elif target == "m":
        result = v["PE"] / (g * v["h"])
    else:
        result = v["PE"] / (v["m"] * g)
    show_result(target, result, units[target])


def ohms_law():
    """V = I × R"""
    print("\nOhm's Law:  V = I × R")
    units = {"V": "V", "I": "A", "R": "Ω"}
    target = choose_variable(units)
    v = read_inputs(units, target)

    if target == "V":
        result = v["I"] * v["R"]
    elif target == "I":
        result = v["V"] / v["R"]
    else:
        result = v["V"] / v["I"]
    show_result(target, result, units[target])


def kinematics():
    """v = u + a × t"""
    print("\nKinematics (Final Velocity):  v = u + a × t")
    units = {"v": "m/s", "u": "m/s", "a": "m/s²", "t": "s"}
    target = choose_variable(units)
    v = read_inputs(units, target)

    if target == "v":
        result = v["u"] + v["a"] * v["t"]
    elif target == "u":
        result = v["v"] - v["a"] * v["t"]
    elif target == "a":
        result = (v["v"] - v["u"]) / v["t"]
    else:
        result = (v["v"] - v["u"]) / v["a"]
    show_result(target, result, units[target])


def universal_gravitation():
    """F = G × m1 × m2 / r²"""
    print("\nUniversal Gravitation:  F = G × m1 × m2 / r²   (G = 6.674e-11)")
    units = {"F": "N", "m1": "kg", "m2": "kg", "r": "m"}
    target = choose_variable(units)
    v = read_inputs(units, target)

    if target == "F":
        result = G * v["m1"] * v["m2"] / v["r"] ** 2
    elif target == "m1":
        result = v["F"] * v["r"] ** 2 / (G * v["m2"])
    elif target == "m2":
        result = v["F"] * v["r"] ** 2 / (G * v["m1"])
    else:
        result = math.sqrt(G * v["m1"] * v["m2"] / v["F"])
    show_result(target, result, units[target])


# ---------- Main menu ----------

MENU = {
    "1": ("Newton's Second Law      (F = ma)", newtons_second_law),
    "2": ("Kinetic Energy           (KE = ½mv²)", kinetic_energy),
    "3": ("Potential Energy         (PE = mgh)", potential_energy),
    "4": ("Ohm's Law                (V = IR)", ohms_law),
    "5": ("Kinematics               (v = u + at)", kinematics),
    "6": ("Universal Gravitation    (F = Gm₁m₂/r²)", universal_gravitation),
}


def main():
    print("=" * 44)
    print("            PHYSICS CALCULATOR")
    print("=" * 44)

    while True:
        print("\nFormulas:")
        for key, (label, _) in MENU.items():
            print(f"  {key}. {label}")
        print("  q. Quit")

        choice = input("\nSelect a formula: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        if choice in MENU:
            repeat_calculator(MENU[choice][1])
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
