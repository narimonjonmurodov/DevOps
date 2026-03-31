from func import marge_str as md

def main():
   try:
      with open("input.txt", "r") as f:
         data = f.read().strip()

      if not data:
         print("Empty file")
         return

      md(data)

   except Exception:
      print("Error(JSON format): in input.txt")

if __name__ == "__main__":
   main()
