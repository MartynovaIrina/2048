import unittest
from logics import get_position_from_index, get_empty_cells, get_index_from_position,\
    is_zero_in_array, move_left, move_up, move_down, can_move


class Test_2048(unittest.TestCase):

    def test_1(self):
        self.assertEqual(get_position_from_index(1, 2), 7)

    def test_2(self):
        self.assertEqual(get_position_from_index(3, 3), 16)

    def test_3(self):
        array = [[0]*4 for _ in range(4)]
        lst = list(range(1, 17))
        self.assertEqual(get_empty_cells(array), lst)

    def test_4(self):
        array = [[1]*4] + [[0]*4 for _ in range(3)]
        lst = list(range(5, 17))
        self.assertEqual(get_empty_cells(array), lst)

    def test_5(self):
        array = [[2]*4 for _ in range(4)]
        self.assertEqual(get_empty_cells(array), [])

    def test_6(self):
        self.assertEqual(get_index_from_position(7), (1, 2))

    def test_7(self):
        self.assertEqual(get_index_from_position(16), (3, 3))

    def test_8(self):
        self.assertEqual(get_index_from_position(1), (0, 0))

    def test_9(self):
        array = [[2]*4 for _ in range(4)]
        self.assertEqual(is_zero_in_array(array), False)

    def test_10(self):
        array = [[0]*4 for _ in range(4)]
        self.assertEqual(is_zero_in_array(array), True)

    def test_11(self):
        array = [[0] * 4] + [[2]*4 for _ in range(3)]
        self.assertEqual(is_zero_in_array(array), True)

    def test_12(self):
        array = [[2, 2, 0, 0], [0, 4, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        res = [[4, 0, 0, 0], [8, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(move_left(array), (res, 12, True))

    def test_13(self):
        array = [[2, 4, 4, 2], [4, 0, 0, 2], [0, 0, 0, 0], [8, 8, 4, 4]]
        res = [[2, 8, 2, 0], [4, 2, 0, 0], [0, 0, 0, 0], [16, 8, 0, 0]]
        self.assertEqual(move_left(array), (res, 32, True))

    def test_14(self):
        array = [[2, 4, 0, 2], [2, 0, 2, 0], [4, 0, 2, 4], [4, 4, 0, 0]]
        res = [[4, 8, 4, 2], [8, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(move_up(array), (res, 24, True))

    def test_15(self):
        array = [[2, 4, 0, 2], [2, 0, 2, 0], [4, 0, 2, 4], [4, 4, 0, 0]]
        res = [[0, 0, 0, 0], [0, 0, 0, 0], [4, 0, 0, 2], [8, 8, 4, 4]]
        self.assertEqual(move_down(array), (res, 24, True))

    def test_16(self):
        array = [[2, 4, 0, 2], [2, 0, 2, 0], [4, 0, 2, 4], [4, 4, 0, 0]]
        self.assertEqual(can_move(array), True)

    def test_17(self):
        array = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        self.assertEqual(can_move(array), False)


if __name__ == '__main__':
    unittest.main()
