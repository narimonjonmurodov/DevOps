from functions import txt_matrix as t_m, sum_row_1 as sr1, sum_coulmn_1 as sc1, delete

def main():
   square, circle = 0, 0
   arr = t_m()

   for row in range(len(arr)):
      for col in range(len(arr[row])):

         if arr[row][col] == 0:
            continue
         r_sum = sr1(row, col, arr)
         c_sum = sc1(row, col, arr)

         if r_sum == c_sum:
            square+=1
            arr = delete(row, col, c_sum, arr)
         else:
            circle+=1
            arr = delete(row, int(col - (c_sum - r_sum)/2), c_sum, arr)

   print(square, circle)

if __name__ == "__main__":
    main()
