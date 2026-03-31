# Python Bootcamp Project 01

## 📌 Overview
This project is a collection of fundamental Python programming tasks designed to strengthen core programming skills. It covers basic concepts such as data types, control structures, algorithms, file handling, and problem-solving.

Each task is implemented as an independent Python script, following the project requirements.

---

## 🧠 What I Learned
During this project, I practiced and improved my understanding of:

- Python syntax and structure
- Input/Output handling
- Conditional statements and loops
- Functions and modular code
- Working with lists, dictionaries, and sets
- File handling and JSON processing
- Basic algorithms and problem-solving
- Error handling and input validation

---

## Task 1. Scalar product

Calculate the scalar product of two vectors in three dimensional space. Use standard input stream and standard output stream for data input and output, respectively. Do not check the correctness of the input data.

- Input: Real numbers, coordinates of two vectors on two lines respectively.
- Output: Real number, scalar product of given vectors.

<table>
    <tr>
        <th>Input</th>
        <th>Output</th>
    </tr>
    <tr>
        <td>1.0 2.0 3.0<br>4.0 5.0 6.0</td>
        <td>32.0</td>
    </tr>
</table>

## Task 2. Palindrome

Determine whether the number is a palindrome or not. Use standard input stream and standard output stream for data input and output, respectively. Do not use strings. Negative numbers are not considered palindromes. Do not check the correctness of the input data.

- Input: Integer.
- Output: True if this number is a palindrome. False if this number is not a palindrome.

<table>
    <tr>
        <th>Input</th>
        <th>Output</th>
    </tr>
    <tr>
        <td>1143411</td>
        <td>True</td>
    </tr>
</table>

## Task 3. Figures

Process a square matrix of zeros and ones, count the number of "squares" and "circles" in it. There are no other figures in the matrix. The figures cannot be beyond the boundaries of the matrix. There is an empty space between any two figures. Identified figures contain more than one unit. Use the input.txt file to enter data. Use the standard output stream to output data. Do not check the correctness of the input data.

- Input: The rows of a square matrix, each containing zeros/units separated by a space.
- Output: Two natural numbers separated by a space are the number of "squares" and the number of "circles" in the matrix, respectively.

<table>
    <tr>
        <th>Input</th>
        <th>Output</th>
    </tr>
    <tr>
        <td>0 0 0 0 0 0 0 0 1 0<br>0 1 1 1 0 0 0 1 1 1<br>0 1 1 1 0 0 0 0 1 0<br>
        0 1 1 1 0 0 0 0 0 0<br>0 0 0 0 0 0 0 0 0 0<br>0 1 1 0 0 1 1 0 0 0<br>
        0 1 1 0 1 1 1 1 0 0<br>0 0 0 0 1 1 1 1 0 0<br>1 1 0 0 0 1 1 0 0 0<br>1 1 0 0 0 0 0 0 0 0</td>
        <td>3 2</td>
    </tr>
</table>

## Task 4. Pascal's triangle

Output N first rows of Pascal's triangle by the given number N of rows. Use standard input stream and standard output stream for data input and output, respectively. Check the correctness of the input data.

- Input: Integer, number of rows.
- Output: Integer numbers, Pascal's triangle.

<table>
    <tr>
        <th>Input</th>
        <th>Output</th>
    </tr>
    <tr>
        <td>5</td>
        <td>1<br>1 1<br>1 2 1<br>1 3 3 1<br>1 4 6 4 1</td>
    </tr>
    <tr>
        <td>f</td>
        <td>Natural number was expected</td>
    </tr>

</table>

## Task 5. String to number conversion

Convert a string to a real number as if it were processed by the `float()` function . It, as well as any similar functions, should not be used in the implementation. Multiply the resulting real number by 2. Print the result with three digits after the dot. Use standard input stream and standard output stream for data input and output, respectively. Check the correctness of the input data.

- Input: A string
- Output: A real number if the input is correct. An error message if the input is incorrect.


| Input          | Output          |
|----------------|-----------------|
| -14.97         | -29.940         |
| +19.2          | 38.400          |

## Task 6. Movies

Join two lists of movies sorted by the `year` field so that the resulting list remains sorted. The input data is in json format. Output the joined list also in json format. Use the input.txt text file to enter data. Use the standard output stream to output data. Check the correctness of the input data. If the input file is empty, display the message “Empty file”.

- Input: Two sorted lists of movies in json format.
- Output: The joined sorted list in json format if the input is correct. An error message if the input is incorrect.

### Input

```json
{
  "list1": [
    {
      "title": "Titanic",
      "year": 1998
    },
    {
      "title": "Taxi 2",
      "year": 2000
    },
    {
      "title": "Avatar",
      "year": 2009
    }
  ],
  "list2": [
    {
      "title": "Terminator",
      "year": 1984
    },
    {
      "title": "Home Alone",
      "year": 1993
    },
    {
      "title": "Spider-Man",
      "year": 2002
    }
  ]
}
```
### Output

```json
{
  "list0": [
    {
      "title": "Terminator",
      "year": 1984
    },
    {
      "title": "Home Alone",
      "year": 1993
    },
    {
      "title": "Titanic",
      "year": 1998
    },
    {
      "title": "Taxi 2",
      "year": 2000
    },
    {
      "title": "Spider-Man",
      "year": 2002
    },
    {
      "title": "Avatar",
      "year": 2009
    }
  ]
}
```

## Task 7. A robot

The robot is able to move down or to the right one square of the field. The field is rectangular and filled with numbers - the number of coins in each square of the field. The robot collects coins from each square it walked on. It is initially located in the top left square, so it collects the coins located there anyway. The robot's task is to collect as many coins as possible on the way to the bottom right square of the field, so it always moves along the most successful route. Determine from the given field how many coins the robot will collect. Use standard input stream and standard output stream for data input and output, respectively. Do not check the correctness of the input data.

- Input: Two natural numbers, the number of rows N and the number of columns M of a field, respectively. N rows, each containing M non-negative numbers, the number of coins in each square of the field.
- Output: A non-negative number, the total number of coins the robot will collect.

<table>
    <tr>
        <th>Input</th>
        <th>Output</th>
    </tr>
    <tr>
        <td>3 4<br>3 0 2 1<br>6 4 8 5<br>3 3 6 0</td>
        <td>27</td>
    </tr>
</table>

## Task 8. Different numbers

Count the number of different numbers entered. Use standard input stream and standard output stream for data input and output, respectively. Do not check the correctness of the input data.

- Input: Natural number, the number of numbers is N. N lines, each containing an integer.
- Output: A natural number, the number of different numbers entered.

<table>
    <tr>
        <th>Input</th>
        <th>Output</th>
    </tr>
    <tr>
        <td>10<br>5<br>3<br>7<br>3<br>6<br>3<br>5<br>2<br>9<br>4</td>
        <td>7</td>
    </tr>
</table>

## Task 9. The derivative at a point

Calculate the derivative of a given polynomial at a given point. Print the result with three digits after the dot. Use standard input stream and standard output stream for data input and output, respectively. Do not check the correctness of the input data.

- Input: The first line contains a natural and a real numbers, the highest degree of the polynomial N and the point at which you want to find the derivative, respectively. The subsequent lines contain real numbers, coefficients at the degrees of x, starting with the highest degree.
- Output: The real number, the derivative of a polynomial at a point.

Polynomial: `5 * x**2 + 1.2 * x - 3` \
Derivative: `10 * x + 1.2` \
Derivative at a point`3.0`: `30 + 1.2 = 31.2`

<table>
    <tr>
        <th>Input</th>
        <th>Output</th>
    </tr>
    <tr>
        <td>2 3.0<br>5<br>1.2<br>-3</td>
        <td>31.200</td>
    </tr>
</table>

## Task 10. Machines

The machine has certain year of manufacture, cost and running time. You need to select two such machines that will take turns and spend a certain amount of time. At the same time, the cost of the machines should be minimal and the year of manufacture should be the same. Output the total cost of the selected machines. It is guaranteed that there is a single solution. Use standard input stream and standard output stream for data input and output, respectively. Check the correctness of the input data.

- Input: Two natural numbers separated by a space, the number of available machines N and the required total running time, respectively. N lines, each containing three natural numbers separated by a space, the year of manufacture, the cost and the running time of the machine, respectively.
- Output: A real number if the input is correct. An error message if the input is incorrect.

<table>
    <tr>
        <th>Input</th>
        <th>Output</th>
    </tr>
    <tr>
        <td>5 48<br>2023 100 14<br>2020 18 347<br>2023 10000000 34<br>2023 1000 34<br>2022 10 34</td>
        <td>1100</td>
    </tr>
</table>

---

### 📌 Notes
- Each task is independent and follows the given requirements
- Input is taken via standard input or input.txt where required
- Output is printed to standard output
- Error handling is implemented where specified

---

### 🚀 Conclusion

This project helped me build a strong foundation in Python by solving a variety of problems involving logic, algorithms, and data processing.

---