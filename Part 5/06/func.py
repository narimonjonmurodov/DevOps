import json

def marge_str(str):
   data = json.loads(str)
   marge=[]
   for value in data.values():
      marge += value
   is_valid(marge)
   marge.sort(key=lambda movie: movie["year"])
   dict = {"list0" : marge}
   output = json.dumps(dict, indent=2)
   print(output)

def is_valid(lst):
   required_keys = ["title", "year"]
   for movie in lst:
      if not ( all(key in movie for key in required_keys) and len(movie) == 2 ):
         raise ValueError("Missing value in json")
