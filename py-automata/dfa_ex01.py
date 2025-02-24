import dfa

def refuse(A):
    """Constructs a DFA A0 that accepts exactly the words that A refuses and vice versa."""
    Q0 = A.Q
    Sigma0 = A.Sigma
    delta0 = A.delta
    q0_0 = A.q0
    F0 = Q0 - A.F  # Complement of the accepting states

    return dfa.DFA(Q0, Sigma0, delta0, q0_0, F0)


# generate words for testing
def generate_words():
    words = []
    alphabet = ['a', 'b']
    for first in alphabet:
        for second in alphabet:
            for third in alphabet:
                words.append(first + second + third)
    return words

def __main__() :

    # Define DFA A
    Q = {1,2,3,4}
    Sigma = {'a','b'}
    delta = {(1,'a'):2, (1,'b'):4, (2,'a'):3, (2,'b'):4, (3,'a'):3, (3,'b'):3, (4,'a'):2, (4,'b'):3}
    q0 = 1
    F = {4}
    A = dfa.DFA(Q, Sigma, delta, q0, F)

    # Generate DFA A0
    A0 = refuse(A)
    
    # DFA A1
    Q = {1,2,3,4}
    Sigma = {'a','b'}
    delta = {(1,'a'):2, (1,'b'):4, (2,'a'):2, (2,'b'):3, (3,'a'):2, (3,'b'):2, (4,'a'):4, (4,'b'):4}
    q0 = 1
    F = {3}
    A1 = dfa.DFA(Q, Sigma, delta, q0, F)
    
    # DFA A2
    Q = {1,2,3}
    Sigma = {'a','b'}
    delta = {(1,'a'):2, (1,'b'):1, (2,'a'):3, (2,'b'):1, (3,'a'):3, (3,'b'):1}
    q0 = 1
    F = {3}
    A2 = dfa.DFA(Q, Sigma, delta, q0, F)
    
    words = generate_words()
    automata = [A1, A2, A, A0]

    words += ['aaaaaaaaabbbbbb','babbbbbbbbbbbbbbb']
    
    # test words on automata
    for X in automata:
         print(f"{X.__repr__()}")
         for w in words:
            print(f"{w}: {X.run(w)}")
         print("\n")

__main__()