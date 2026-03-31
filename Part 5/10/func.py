def input_():
    first_line = input().split()
    check(first_line, 2)
    N, T = map(int, first_line)

    machines = []

    for _ in range(N):
        line = input().split()
        check(line, 3)
        year, cost, time = map(int, line)
        machines.append((year, cost, time))
    return machines, N, T

def check(list_, leng):
    if len(list_) != leng:
        raise ValueError
    for i in list_:
        if int(i) <= 0:
            raise ValueError
    
def out(machines, N, T):
    min_cost = None

    for i in range(N):
        for j in range(i + 1, N):
            y1, c1, t1 = machines[i]
            y2, c2, t2 = machines[j]

            if y1 == y2 and (t1 + t2) >= T:
                total_cost = c1 + c2

                if min_cost is None or total_cost < min_cost:
                    min_cost = total_cost

    if min_cost is not None:
        print(int(min_cost))
    else:
        raise