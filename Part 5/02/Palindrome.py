def p(a, rev):
   if a < 0:
      print(False)
   elif a == rev:
      print(True)
   else:
      print(False)


def rev(n):
   rev = 0
   while n > 0:
      rev = rev*10 + n%10
      n = n//10
   return rev
