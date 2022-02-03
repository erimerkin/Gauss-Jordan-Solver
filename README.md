# Q5 Report

This program solves given matrixes with the help of Gauss-Jordan Elimination Method. We used Fractions library of Python to reduce inaccuracy in floating point operations. To achieve this all the inputs read from files is saved as a Fraction instead of float/integer to matrix. Then the operations are done on Fraction format. After the solution completes, Fractions are converted to a floating point number with an accuracy of 6 digits after period (ex. 0,666667).

The outline of program’s working is:
	Read matrix from file -> Gauss-Jordan Elimination -> Determining rank of matrix -> Calculating the solution -> Printing the solution

So we will explain the methods used in given order:

### Gauss-Jordan Elimination

In this step, we tried to replicate Gauss-Jordan Elimination. To explain the method, showing a pseudocode of algorithm works much better.

Pseudocode of Gauss Jordan Elimination implemented in program for an augmented matrix with given n size:
1. Start from first row and column (row_index=0, column_index=0).
2. Make sure column index and row index are within the bounds. Otherwise quit.
3. Check the element in current index. If it is not 0 go to step 10, otherwise continue.
4. Let i = row index, j= column index
5. Check if j < n, otherwise quit.
6. Increase i by 1.
7. Check if i < n. Otherwise increase column index by 1 and go to step 4.
8. Check if the element a_ij != 0, otherwise go to step 6.
9. Check if i = row index, otherwise interchange i’th row with the row at row index. 
10. Divide the row by current element to make pivot 1.
11. Add or subtract a factor of current row from other rows to remove elements on the same column as pivot.
12. Increase column and row index by 1. 
13. Go to step 2.


### Determining rank of matrix

After our implementation of Gauss-Jordan Elimination is completed, the resulting matrix have all 0 in bottom rows and pivots at the top rows, preferably starting with a_1,1=1. 
	
So rank checking algorithm starts with first element in the first row of index. As we know pivots are in top rows, if the first element of first row has no pivot, algorithm checks other columns till it finds a 1(pivot). It increases rank for every pivot found. 

If a a row of A is filled with 0’s, algorithm checks if element of b for that index is also 0. If it is not 0, matrix has no solution; so the program prints “Inconsistent problem” quits. Otherwise it continues on looping till all pivots are found or all of matrix is iterated.



### Calculating Solution

**For rank (A) = n:** program simply prints elements of b which is the solution in [A|b] augmented matrix. 
To find an inverse a new augmented matrix [A|I] (I: Identity matrix) is created and Gauss-Jordan Elimination applied to this new matrix with a fixed size of n which is the size of A matrix. So that the program doesn’t try to eliminate the inverse we got on identity matrix side.

**For rank(A) < rank (A|b) (No solution):”** This case is handled when determining the rank of a matrix. So no extra operation needed for this case.

**For rank(A) < n (Arbitrary Solution):** Starting from first row, it checks every row column by column to find a pivot which should have a value of 1. We used Gauss-Jordan Elimination method, so results of our algorithm should have pivots in top rows. Meaning that if a pivot is not found in top row, it doesn’t exits, then according to this corresponding x variable’s value is set as 0 and stored in a list.  Solution is obtained by multiplied this list with A matrix like Ax=b. 



## Output
Program will output solutions for given files. All elements are printed as floating point numbers with an accuracy of 6 digits after period (ex. 0.333333, 0.000000) to create a more readable and tabular output.  



## Running the program
Python 3 is required.  Usage command is:

	`python q5.py "file1" "file2" ....`

The program will read and solve every matrix given in files. It can take single or multiple arguments.
