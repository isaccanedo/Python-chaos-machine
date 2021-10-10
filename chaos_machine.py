"""example of simple chaos machine"""
"""exemplo de máquina de caos simple"""

# Chaos Machine (K, t, m)
K = [0.33, 0.44, 0.55, 0.44, 0.33]
t = 3
m = 5

# Buffer Space (with Parameters Space)
# Espaço de buffer (com espaço de parâmetros)
buffer_space: list[float] = []
params_space: list[float] = []

# Machine Time
# Tempo Máquina
machine_time = 0


def push(seed):
    global buffer_space, params_space, machine_time, K, m, t

    # Choosing Dynamical Systems (All)
    # Escolha de sistemas dinâmicos (todos)
    for key, value in enumerate(buffer_space):
        # Evolution Parameter
        # Parâmetro de evolução
        e = float(seed / value)

        # Control Theory: Orbit Change
        # Teoria de controle: Mudança de órbita
        value = (buffer_space[(key + 1) % m] + e) % 1

        # Control Theory: Trajectory Change
        # Teoria de controle: Mudança de trajetória
        r = (params_space[key] + e) % 1 + 3

        # Modification (Transition Function) - Jumps
        # Modificação (função de transição) - saltos
        buffer_space[key] = round(float(r * value * (1 - value)), 10)
        params_space[key] = r  # Saving to Parameters Space # Salvando no espaço de parâmetros

    # Logistic Map
    # Mapa Logístico
    assert max(buffer_space) < 1
    assert max(params_space) < 4

    # Machine Time
    # Tempo Máquina
    machine_time += 1


def pull():
    global buffer_space, params_space, machine_time, K, m, t

    # PRNG (Xorshift by George Marsaglia)
    # PRNG (Xorshift de George Marsaglia)
    def xorshift(X, Y):
        X ^= Y >> 13
        Y ^= X << 17
        X ^= Y >> 5
        return X

    # Choosing Dynamical Systems (Increment)
    # Escolha de sistemas dinâmicos (incremento)
    key = machine_time % m

    # Evolution (Time Length)
    # Evolução (duração do tempo)
    for i in range(0, t):
        # Variables (Position + Parameters)
        # Variáveis (Posição + Parâmetros)
        r = params_space[key]
        value = buffer_space[key]

        # Modification (Transition Function) - Flow
        # Modificação (Função de Transição) - Fluxo
        buffer_space[key] = round(float(r * value * (1 - value)), 10)
        params_space[key] = (machine_time * 0.01 + r * 1.01) % 1 + 3

    # Choosing Chaotic Data
    # Escolhendo Dados Caóticos
    X = int(buffer_space[(key + 2) % m] * (10 ** 10))
    Y = int(buffer_space[(key - 2) % m] * (10 ** 10))

    # Machine Time
    # Tempo Máquina
    machine_time += 1

    return xorshift(X, Y) % 0xFFFFFFFF


def reset():
    global buffer_space, params_space, machine_time, K, m, t

    buffer_space = K
    params_space = [0] * m
    machine_time = 0


if __name__ == "__main__":
    # Initialization
    reset()

    # Pushing Data (Input)
    import random

    message = random.sample(range(0xFFFFFFFF), 100)
    for chunk in message:
        push(chunk)

    # for controlling
    # para controlar
    inp = ""

    # Pulling Data (Output)
    # Extração de dados (saída)
    while inp in ("e", "E"):
        print("%s" % format(pull(), "#04x"))
        print(buffer_space)
        print(params_space)
        inp = input("(e)exit? ").strip()
