from func import input_, out

def main():
    try:
        machines, N, T = input_()
        out(machines, N, T)
    except:
        print("Incorrect input")


if __name__ == "__main__":
    main()