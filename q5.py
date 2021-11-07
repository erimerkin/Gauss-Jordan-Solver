# Import math Library
import math
import copy


def interchange_rows(matrix: list, row_index1: int, row_index2: int):
    temp = matrix[row_index1]
    matrix[row_index1] = matrix[row_index2]
    matrix[row_index2] = temp


def multiply_row(matrix: list, row_index: int, factor):
    current_row = matrix[row_index]
    for column_index in range(0, len(current_row)):
        if (current_row[column_index] != 0.0):
            current_row[column_index] *= factor


def add_rows(matrix: list, target_row_index: int, operand_row_index: int, factor):
    operand_row = matrix[operand_row_index]
    target_row = matrix[target_row_index]

    for column_index in range(0, len(target_row)):
        target_row[column_index] = math.fsum(
            [target_row[column_index], factor*operand_row[column_index]])


def gauss_jordan(matrix: list, size: int):

    row_index = 0
    column_index = 0
    while (row_index < size and column_index < size):

        isZero = True
        i = row_index

        while(isZero):
            if (matrix[i][column_index] != 0.0):
                if (i != row_index):
                    interchange_rows(matrix, i, row_index)
                isZero = False
                break

            else:
                i += 1
                if (i >= size):
                    i = row_index
                    column_index += 1
                    if (column_index >= size):
                        break

        if not(isZero):
            multiply_row(matrix, row_index, 1/matrix[row_index][column_index])
            for m in range(0, size):
                if (m != row_index):
                    factor = matrix[m][column_index]
                    if (factor != 0.0):
                        add_rows(matrix, m, row_index, -1*factor)

        row_index += 1
        column_index += 1
    print(matrix)


def invert(matrix: list) -> list:
    limit = len(matrix)

    # Makes given A matrix an augmented matrix [A|I]
    for row_index in range(0, limit):
        for column_index in range(0, limit):
            if (row_index == column_index):
                matrix[row_index].append(1)
            else:
                matrix[row_index].append(0)

    gauss_jordan(matrix, limit)

    # Divides [A'|I'] to get inverse matrix
    inverse_matrix = []
    for row in matrix:
        inverse_matrix.append(row[limit:])

    # Prints formatted inverted matrix as output
    print('Inverted A:', end='')
    for row in inverse_matrix:
        line = "\t\t"
        for element in row:
            line += format(element, '.4f') + "\t"
        line += '\n\t'
        print(line, end='')


def check_rank(matrix) -> int:
    rank = 0
    gauss_jordan(matrix, len(matrix))

    for row in matrix:
        pivot_found = False
        column_index = 0
        while (not(pivot_found) and column_index < len(matrix)):
            if (row[column_index] != 0.0):
                pivot_found = True
                rank += 1
            column_index += 1

        if not(pivot_found):
            if (row[len(matrix)] != 0):
                return -1

    return rank


def solve(input_matrix: list):
    augmented_matrix = copy.deepcopy(input_matrix)

    rank = check_rank(augmented_matrix)
    if (rank == -1):
        print("Inconsistent problem")

    elif (rank < len(augmented_matrix)):
        print("arbitrary solution")
        # TODO: #1 NEEDS ARBITRARY SOLUTION

    else:
        unique_sol = "Unique solution:\t"
        for row in augmented_matrix:
            unique_sol += format(row[len(augmented_matrix)], '.4f') + '\t'
        print(unique_sol)

        a_matrix = []
        for row in input_matrix:
            a_matrix.append(row[:-1])

        print("")
        invert(a_matrix)


def main():
    test_matrix = [[0, 0, 0, 0, 0],
                   [0, 1, 5, -2, 8],
                   [1, 2, 3, 4, 0],
                   [-4, 0, 1, 3, -4]]

    #TODO: #2 Implement file operations to read matrix
    # file = open("test.txt", 'r')

    solve(test_matrix)


if (__name__ == "__main__"):
    main()
