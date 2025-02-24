# DFA Implementation and Usage

## Implementation

This Python implementation defines a **Deterministic Finite Automaton (DFA)** using the `DFA` class. A DFA is initialized with:
- `Q`: Set of states.
- `Σ`: Input alphabet.
- `δ`: Transition function (dict mapping `(state, input) → next state`).
- `q0`: Start state.
- `F`: Accepting states.

### Key Functions
- `run(w)`: Returns `True` if `w` is accepted, else `False`.
- `refuse(A)`: Constructs a DFA that accepts words rejected by `A`.
- `generate_words()`: Generates test words.

## Usage

### Defining a DFA
```python
import dfa

Q = {1, 2, 3}
Σ = {'a', 'b'}
δ = {(1, 'a'): 2, (1, 'b'): 1, (2, 'a'): 3, (2, 'b'): 1, (3, 'a'): 3, (3, 'b'): 1}
q0 = 1
F = {3}

A = dfa.DFA(Q, Σ, δ, q0, F)

```
### Generating The Compliment
```python
A0 = refuse(A)
```
### Running a DFA on a String
```python
print(A.run("aba"))  # Output: True or False
```
