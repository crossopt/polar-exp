import unittest
from polar import polarize, sort_gates, get_n_best_gates


class TestPolarize(unittest.TestCase):
    def test_oneStep_prob3(self):
        self.assertEqual([0.09, 0.51], polarize([0.3]))

    def test_oneStep_prob5(self):
        self.assertEqual([0.25, 0.75], polarize([0.5]))

    def test_severalSteps_prob3(self):
        expected = [6.560999999999999e-05, 0.01613439, 0.02954961, 0.31425039, 0.06765201, 0.45254799, 0.57744801, 0.94235199]
        actual = polarize(polarize(polarize([0.3])))
        self.assertEqual(expected, actual)

    def test_severalSteps_prob5(self):
        expected = [0.00390625, 0.12109375, 0.19140625, 0.68359375, 0.31640625, 0.80859375, 0.87890625, 0.99609375]
        actual = polarize(polarize(polarize([0.5])))
        self.assertEqual(expected, actual)


class TestSortGates(unittest.TestCase):
    def test_twoGates_prob3(self):
        self.assertEqual([(1, 0.51), (0, 0.09)], sort_gates(1, 0.3))

    def test_twoGates_prob5(self):
        self.assertEqual([(1, 0.75), (0, 0.25)], sort_gates(1, 0.5))

    def test_severalGates_prob3(self):
        only_gates = [gate[0] for gate in sort_gates(4, 0.3)]
        self.assertEqual([15, 14, 13, 11, 7, 12, 10, 9, 6, 5, 3, 8, 4, 2, 1, 0], only_gates)

    def test_severalGates_prob5(self):
        only_gates = [gate[0] for gate in sort_gates(3, 0.5)]
        self.assertEqual([7, 6, 5, 3, 4, 2, 1, 0], only_gates)


class TestNBestGates(unittest.TestCase):
    def test_twoGates_prob1(self):
        self.assertEqual([1], get_n_best_gates(1, 0.00001, 1))

    def test_severalGates_prob3(self):
        self.assertEqual([15, 14, 13, 11, 7], get_n_best_gates(4, 0.3, 5))

    def test_severalGates_prob5(self):
        self.assertEqual([7, 6, 5, 3, 4, 2, 1], get_n_best_gates(3, 0.5, 7))


if __name__ == '__main__':
    unittest.main()