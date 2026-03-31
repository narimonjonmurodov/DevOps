from ScalarP3D import ScalarP3D as sp3d

def main():
    a = list(map(float, input().split()))
    b = list(map(float, input().split()))
    result = sp3d(a, b)
    print(result)

if __name__ == "__main__":
    main()
