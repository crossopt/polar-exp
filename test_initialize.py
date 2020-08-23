import unittest
from initialize import get_endpoints, get_gates, get_all_possible_configs


class TestGetGates(unittest.TestCase):
    def test_power2_prob1(self):
        self.assertEqual(['*', '?', '?', '?'], get_gates(2, 0.1))

    def test_power2_prob5(self):
        self.assertEqual(['*', '*', '?', '?'], get_gates(2, 0.5))

    def test_power3_prob2(self):
        self.assertEqual(['*', '*', '?', '?', '?', '?', '?', '?'], get_gates(3, 0.2))

    def test_power3_prob3(self):
        self.assertEqual(['*', '*', '*', '?', '?', '?', '?', '?'], get_gates(3, 0.3))

    def test_power3_prob5(self):
        self.assertEqual(['*', '*', '*', '?', '*', '?', '?', '?'], get_gates(3, 0.5))


class TestGetEndpoints(unittest.TestCase):
    def test_amountIsCorrect_power2_prob1(self):
        self.assertEqual(['*', '*', '*', '?'], sorted(get_endpoints(2, 0.1)))

    def test_amountIsCorrect_power2_prob5(self):
        self.assertEqual(['*', '*', '?', '?'], sorted(get_endpoints(2, 0.5)))

    def test_amountIsCorrect_power3_prob5(self):
        self.assertEqual(['*', '*', '*', '*', '?', '?', '?', '?'], sorted(get_endpoints(3, 0.5)))


class TestGetAllPossibleConfigs(unittest.TestCase):
    def test_configListIsCorrect_power2_prob1(self):
        self.assertEqual([['*', '*', '*', '?'],
                          ['*', '*', '?', '*'],
                          ['*', '?', '*', '*'],
                          ['?', '*', '*', '*']], sorted(get_all_possible_configs(2, 0.1)))

    def test_configListIsCorrect_power2_prob5(self):
        self.assertEqual([['*', '*', '?', '?'],
                          ['*', '?', '*', '?'],
                          ['*', '?', '?', '*'],
                          ['?', '*', '*', '?'],
                          ['?', '*', '?', '*'],
                          ['?', '?', '*', '*']], sorted(get_all_possible_configs(2, 0.5)))


if __name__ == '__main__':
    unittest.main()
