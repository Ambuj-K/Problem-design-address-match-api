import unittest
from ..api_functions.supporter import *


class TestSupporterFunctions(unittest.TestCase):

    # test functionality rejection
    def test_calculate_loan_prerequisites(self):
        assert calculate_loan_prerequisites(28, 40000, 700, 800, 30,
                                            90) == ['Accepted', ""]

        assert calculate_loan_prerequisites(28, 40000, 200, 800, 30,
                                            90) == ['Rejected', "Bureau "
                                                                "Score LT 600"]

        assert calculate_loan_prerequisites(48, 400, 700, 800, 30,
                                            90) == ['Rejected',
                                                    "TotalLoanAmount LT 1000"]

        assert calculate_loan_prerequisites(98, 40000, 700, 800, 30,
                                            90) == ['Accepted', ""]

    # test matching score
    def test_matching(self):
        assert matching("aa","aa")==100

        assert matching("aa", "aa") == 100
