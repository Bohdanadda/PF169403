import unittest
from laboratorium1.src.insufficient_funds_error import InsufficientFundsError, BankAccount


class TestInsufficientFundsError(unittest.TestCase):
    def setUp(self):
        self.status = InsufficientFundsError()

    def test_deposite(self):
        account = BankAccount()
        account.deposit(100)
        self.assertEqual(100, account.balance)

        with self.assertRaises(ValueError):
            account.deposit(-50)

    def test_withdraw(self):
        account = BankAccount(200)
        account.withdraw(50)
        self.assertEqual(account.get_balance(), 150)

        with self.assertRaises(ValueError):
            account.withdraw(-20)

        # with self.assertRaises(InsufficientFundsError):
        #     account.withdraw(300)

    def test_get_balance(self):
        account = BankAccount(500)
        self.assertEqual(account.get_balance(), 500)
        account.deposit(250)
        self.assertEqual(account.get_balance(), 750)
        account.withdraw(100)
        self.assertEqual(account.get_balance(), 650)

    def tearDown(self):
        pass