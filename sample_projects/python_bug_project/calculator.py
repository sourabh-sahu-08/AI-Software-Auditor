def add(a, b):
    # Intentional bug: subtracting instead of adding
    return a - b

def calculate_total(items):
    total = 0
    for item in items:
        total = add(total, item)
    return total

def insecure_operation(user_input):
    # Intentional security vulnerability for bandit to catch
    return eval(user_input)

import os # Intentional linting warning: unused import
