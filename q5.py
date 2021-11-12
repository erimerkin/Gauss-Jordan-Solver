import sys
import copy
from fractions import Fraction

# This function interchanges row on given indexes for given matrix
def interchange_rows(matrix: list, row_index1: int, row_index2: int):
    temp_row = matrix[row_index1]
    matrix[row_index1] = matrix[row_index2]
    matrix[row_index2] = temp_row

# This function multiplies given row in a matrix with given factor
def multiply_row(matrix: list, row_index: int, factor):
    current_row = matrix[row_index]

    # Multiplying elements in a row one by one with factor and saving it
    for column_index in range(0, len(current_row)):
        if (current_row[column_index] != 0):
            current_row[column_index] *= factor

# This function adds a row multiplied by a constant to a target row in given matrix
def add_rows(matrix: list, target_row_index: int, operand_row_index: int, factor):
    operand_row = matrix[operand_row_index]
    target_row = matrix[target_row_index]

    # Adds elements of operand row multiplied with given constant to elements of target row
    for column_index in range(0, len(target_row)):
        target_row[column_index] += operand_row[column_index]*factor


# This function applies Gauss-Jordan Method to solve/simplify a matrix to row reduced echelon form
def gauss_jordan(matrix: list, size: int):

    row_index = 0
    column_index = 0

    # Iterates over till it checks every column and row of matrix
    while (row_index < size and column_index < size):
        isZero = True
        i = row_index

        # Loops till it finds an element that is not zero
        while(isZero):

            # If an element is not zero, it checks the row and column indexes of the element.
            # If the column and row index is equal, then there is no need to move the row,
            # otherwise it interchanges rows at supposed row index and current index
            if (matrix[i][column_index] != 0):
                if (i != row_index):
                    interchange_rows(matrix, i, row_index)
                isZero = False
                break
            
            # If element is not 0, it increases the temp row index by 1, checking other rows for a nonzero element
            else:
                i += 1

                # If all rows are iterated for current column, increases the column index by 1 and returns to starting row index
                if (i >= size):
                    i = row_index
                    column_index += 1

                    # If all columns are iterated, it quits from loop
                    if (column_index >= size):
                        break

        # If a nonzero element is found, pivoting operations for that element starts
        # It first divides the row by found element to make pivot value 1,
        # then it substracts from every row trying to make other elements in the column of pivot 0.
        if not(isZero):
            multiply_row(matrix, row_index, 1/matrix[row_index][column_index])

            # Substracts current column from other columns, making above and below of pivot 0
            for m in range(0, size):
                if (m != row_index):
                    factor = matrix[m][column_index]
                    if (factor != 0):
                        add_rows(matrix, m, row_index, -1*factor)

        row_index += 1
        column_index += 1

# This function inverts given matrix using Gauss-Jordan Method and prints the inverted matrix
def invert(matrix: list) -> list:
    limit = len(matrix)

    # Makes given A matrix an augmented matrix [A|I] by adding identity matrix
    for row_index in range(0, limit):
        for column_index in range(0, limit):
            if (row_index == column_index):
                matrix[row_index].append(1)
            else:
                matrix[row_index].append(0)

    # Applies Gauss-Jordan method to simplify and find pivots for A part,
    # while also finding the inverse by
    gauss_jordan(matrix, limit)

    # Split augmented matrix [A'|I'] to get inverse matrix
    inverse_matrix = []
    for row in matrix:
        inverse_matrix.append(row[limit:])

    # Prints formatted inverted matrix as output
    print('Inverted A:')
    for row in inverse_matrix:
        line = "\t\t"
        for element in row:
            if (element >= 0):
                line += " "
            line += format(float(element), '.6f') + "\t"
        print(line)

# This function first applies Gauss-Jordan Elimination to the given matrix and then checks the rank of resulting matrix
# According to the rank of the matrix, it tries to solve the matrix and print relevant information about solution
def solve(input_matrix: list):

    # Deep-copies matrix since python lists are passed by reference so any change done in a
    # shallow copied list will also result in a change for main list
    augmented_matrix = copy.deepcopy(input_matrix)
    n = len(augmented_matrix)

    # Uses Gauss-Jordan method to achieve row-reduced echelon form for given matrix
    gauss_jordan(augmented_matrix, n)

    # Calculates rank of matrix by iterating over row of augmented matrix column by column.
    # As the Gauss-Jordan method is applied to matrix beforehand pivots are expected to be starting from
    # first row in matrix. If it is not in the first column of first row, then it

    # If a row has no pivots(filled with zeroes) it checks b part of augmented matrix [A|b].
    # If that row of b is not 0, the is no solution for matrix.
    # If row of b is 0 when the other columns are 0, then it has infinitely many solutions.
    # If every row has a pivot such that rank = matrix, the matrix has an unique solution.
    rank = 0
    for row in augmented_matrix:
        pivot_found = False
        column_index = 0

        # Checks if a row has pivot, if a pivot is found loop is done. Increases rank for every pivot found
        while (not(pivot_found) and column_index < n):
            if (row[column_index] != 0):
                pivot_found = True
                rank += 1
            column_index += 1

        # If all columns in current row of A is 0, checks current column for b.
        # If row of b is not 0, it prints Inconsistent problem and finishes running for solution.
        if not(pivot_found):
            if (row[n] != 0):
                print("Inconsistent problem")
                return

    # Case of rank = n, which means matrix has an unique solution and inverting matrix is possible
    # Prints the solution of matrix and its inverse
    if (rank == n):

        # Creates string to store unique solution variables which will be printed and prints them
        print("Unique solution:")
        unique_sol = "\t\t"
        for row in augmented_matrix:
            if (row[n] >= 0):
                unique_sol += " "
            unique_sol += format(float(row[n]), '.6f') + '\t'
        print(unique_sol)

        # As we have an augmented matrix of [A|b], this seperates A matrix and finds inverse of matrix A.
        a_matrix = []
        for row in input_matrix:
            a_matrix.append(row[:-1])

        invert(a_matrix)    # inverts and prints the inverted matrix

    else:

        # Starting from row 1, it checks every row column by column to find a pivot which should have value 1.
        # We used Gauss-Jordan Elimination method, so results of our algorithm should have pivots in top rows. 
        # Meaning that if a pivot is not found in top row, it doesn't exits.
        row_index = 0
        column_index = 0
        unknown_matrix = []
        while (column_index < n):

            # Checks if the current element is pivot, if not it moves 1 column to right
            # It adds 0 for every arbitrary value (pivot not found for column), and 1 for every pivot to a list.
            if (augmented_matrix[row_index][column_index] == 1):
                unknown_matrix.append(1)
                row_index += 1
            else:
                unknown_matrix.append(0)
        
            column_index += 1

        # Prints arbitrary variables found in upper loop according to unknown_matrix list.
        # If value is equal to 0, it is a arbitrary value
        print("Arbitrary variables:")
        arbitrary_variables = "\t\t\t"
        for variable_number in range(0, n):
            if (unknown_matrix[variable_number] == 0):
                arbitrary_variables += "x_" + str(variable_number+1) + "\t"
        print(arbitrary_variables)

        # Using found arbitrary variables, this loop calculates the solution by giving 0 to arbitrary variables.
        # Which is already done in unkown_matrix list.
        multiplied_matrix = []
        for row in augmented_matrix:
            arb_sol = [row[len(row)-1]]
            for i in range(0, len(row)-1):
                arb_sol.append(row[i]*unknown_matrix[i])
            multiplied_matrix.append(arb_sol)

        # Prints the found arbitrary solutions to the matrix
        print("Arbitrary solutions:")
        arbitrary_solution = "\t\t\t"
        for index in range(0, len(multiplied_matrix)):
            result = multiplied_matrix[index][0]

            for variable in range(1, len(multiplied_matrix[index])):
                result -= multiplied_matrix[index][variable]

            arbitrary_solution += "x_" + str(index+1) + ": " + format(float(result), '.6f') + "\t"
        print(arbitrary_solution)


def main():

    file_locations = sys.argv

    # Reads data from files given as arguments, solves and prints the result for them.
    # Does this for every given argument 
    for i in range(1, len(file_locations)):
        print(f"\nINPUT {i} (from {file_locations[i]}):")

        try:
            file = open(file_locations[i], 'r')

            # Reads from file and tokenizes it
            inputs = []
            for line in file:
                inputs.append(line.split())

            # gets the size of matrix
            size = int(inputs.pop(0)[0])

            # adds tokens to created matrix as fractions (this will reduce inaccurracy of float operations)
            input_matrix = []
            for k in range(0, size):
                row = []
                for l in range(0, size+1):
                    row.append(Fraction(float(inputs[k][l])))
                input_matrix.append(row)

            file.close()

            # Solves the matrix
            solve(input_matrix)
            print("\n------------------------------\n")

        except IOError:
            print(f"Error: Given file doesn't seem to exist. ({file_locations[i]})")



if (__name__ == "__main__"):
    main()
