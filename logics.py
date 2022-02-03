import random
import copy


def get_position_from_index(i, j):
    '''finds position of the cell in array 4x4 with starting position 1'''
    return i*4 + j + 1


def get_index_from_position(pos):
    '''finds coordinates of the position of the cell in array 4x4 (reverse to get_position_from_index)'''
    pos -= 1
    i, j = pos//4, pos % 4
    return i, j


def add_2_or_4(array, i, j):
    '''fills the cell with either 2 or 4'''
    if random.random() <= 0.75:  # 0.75 because 2 should be filled with higher probability
        array[i][j] = 2
    else:
        array[i][j] = 4
    return array


def get_empty_cells(array):
    '''searches empty cells (cell value == 0) in the array'''
    empty_cells = []
    for i in range(4):
        for j in range(4):
            if array[i][j] == 0:
                pos = get_position_from_index(i, j)
                empty_cells.append(pos)
    return empty_cells


def is_zero_in_array(array):
    '''defines if the array can be filled or already filled with 2 or 4'''
    for row in array:
        if 0 in row:
            return True
    return False


def move_left(array):
    '''describes the move to the left'''
    original = copy.deepcopy(array)  # to save the original state of the array
    delta = 0
    for row in array:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if array[i][j] == array[i][j + 1] and array[i][j] != 0:
                array[i][j] *= 2
                delta += array[i][j]
                array[i].pop(j+1)
                array[i].append(0)

    return array, delta, not original == array


def move_right(array):
    '''describes the move to the right'''
    delta = 0
    original = copy.deepcopy(array)
    for row in array:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if array[i][j] == array[i][j - 1] and array[i][j] != 0:
                array[i][j] *= 2
                delta += array[i][j]
                array[i].pop(j-1)
                array[i].insert(0, 0)
    return array, delta, not original == array


def move_up(array):
    '''describes the move up'''
    delta = 0
    original = copy.deepcopy(array)
    for j in range(4):
        column = []
        for i in range(4):
            if array[i][j] != 0:
                column.append(array[i][j])
        while len(column) != 4:
            column.append(0)
        for i in range(3):
            if column[i] == column[i + 1] and column != 0:
                column[i] *= 2
                delta += column[i]
                column.pop(i + 1)
                column.append(0)
        for i in range(4):
            array[i][j] = column[i]
    return array, delta, not original == array


def move_down(array):
    '''describes the move down'''
    original = copy.deepcopy(array)
    delta = 0
    for j in range(4):
        column = []
        for i in range(4):
            if array[i][j] != 0:
                column.append(array[i][j])
        while len(column) != 4:
            column.insert(0, 0)
        for i in range(3, 0, -1):
            if column[i] == column[i - 1] and column != 0:
                column[i] *= 2
                delta += column[i]
                column.pop(i - 1)
                column.insert(0, 0)
        for i in range(4):
            array[i][j] = column[i]
    return array, delta, not original == array


def can_move(array):
    '''defines if there are any moves left'''
    for i in range(3):
        for j in range(3):
            if array[i][j] == array[i][j + 1] or array[i][j] == array[i + 1][j]:
                return True

    for i in range(1, 4):
        for j in range(1, 4):
            if array[i][j] == array[i - 1][j] or array[i][j] == array[i][j - 1]:
                return True
    return False
