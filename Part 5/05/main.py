from func import string_to_float

def main():
   s = input().strip()
   num = string_to_float(s)

   if num is None:
       print("Error")
   else:
       result = num * 2
       print(f"{result:.3f}")

if __name__ == "__main__":
    main()
