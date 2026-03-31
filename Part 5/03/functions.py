def txt_matrix():
   with open("input.txt", "r") as f:
       matrix = [list(map(int, line.split())) for line in f]

   return matrix

def sum_row_1(row, coulmn, matrix):
   sum = 0
   while True:
      sum += 1
      coulmn += 1
      if coulmn >= len(matrix[row]):
         return sum
      if matrix[row][coulmn] == 0:
         return sum

def sum_coulmn_1(row, coulmn, matrix):
   sum = 0
   while True:
      sum += 1
      row += 1
      if row >= len(matrix):
         return sum
      if matrix[row][coulmn] == 0:
         return sum

def delete(row, coulmn, size, matrix):
   for i in range(size):
      for j in range(size):
         matrix[row+i][coulmn+j] = 0
   return matrix
