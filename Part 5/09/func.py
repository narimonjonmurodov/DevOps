def input_():
    n, p = input().split()
    list_ = []
    for _ in range(int(n)+1):
        list_.append(float(input()))
    return (list_, float(p))

def det_p(cof, p):
    res=0
    n=len(cof)-1
    for i in range(0, n):
        res+=(n-i)*cof[i]*p**(n-i-1)
    print(f"{res:.3f}")
    