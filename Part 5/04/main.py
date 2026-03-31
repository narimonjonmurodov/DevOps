from func import Pascal_t as pt

def main():
   try:
      n = int(input())
      pt(n)
   except:
      print("Natural number was expected")


if __name__ == "__main__":
    main()
