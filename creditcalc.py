import argparse
import math


class CreditCalculator:
    ANNUITY = 'annuity'
    DIFF = 'diff'

    def __init__(self, principal: int, periods: int, percentage: float, payment: float, type: str):
        self.principal = principal
        self.periods = periods
        self.percentage = percentage
        self.payment = payment
        self.type = type
        self.interest = None
        self.print = None

    def calculate_annuity_monthly_payment(self):
        if self.percentage is None:
            raise RuntimeError

        if self.periods < 0:
            raise RuntimeError

        pow_value = math.pow(1 + self.interest, self.periods)
        payment = self.principal * (
                (self.interest * pow_value)
                / (pow_value - 1)
        )
        self.payment = math.ceil(payment)
        accumulate = self.payment * self.periods

        print(f"Your annuity payment = {self.payment}!")
        print("Overpayment = %s" % (accumulate - self.principal))

    def calculate_diff_monthly_payment(self):
        if self.principal is None or self.periods is None or self.payment is not None:
            raise RuntimeError

        accumulate = 0
        for month in range(1, self.periods + 1):
            payment = (self.principal / self.periods) \
                      + self.interest \
                      * (self.principal - (self.principal * (month - 1)) / self.periods)
            payment = math.ceil(payment)
            accumulate += payment
            print(f"Month {month}: paid out {payment}")

        print("Overpayment = %s" % (accumulate - self.principal))

    def calculate_interest(self):
        if self.percentage is None:
            raise RuntimeError

        if self.percentage < 0:
            raise RuntimeError

        self.interest = (self.percentage / 100) / 12

    def calculate_principal(self):
        if self.principal is not None:
            if self.principal < 0:
                raise RuntimeError
            return

        if self.percentage is None or self.periods is None:
            raise RuntimeError

        self.print = 'principal'
        self.principal = self.payment / ((self.interest * math.pow(1 + self.interest, self.periods)) / (math.pow(1 + self.interest, self.periods) - 1))

    def calculate_periods(self):
        if self.periods is not None:
            if self.periods < 0:
                raise RuntimeError
            return

        if self.payment is None or self.principal is None:
            raise RuntimeError

        self.print = 'periods'
        total = math.log(self.payment / (self.payment - self.interest * self.principal), 1 + self.interest)
        self.periods = int(math.ceil(total))

    def calculate_overpayment_with_principal(self):
        accumulate = self.payment * self.periods
        print(f"Your credit principal {self.principal}")
        print("Overpayment %s" % (accumulate - self.principal) )

    def calculate_overpayment_with_periods(self):
        accumulate = self.payment * self.periods
        years = self.periods // 12
        word_years = "years" if years > 1 else "year"

        months = self.periods - years * 12
        word_months = "months" if years > 1 else "month"

        if years > 0 and months > 0:
            print(f"You need {years} {word_years} and {months} {word_months} to repay this credit!")
        elif years > 0:
            print(f"You need {years} {word_years} to repay this credit!")
        else:
            print(f"You need {months} {word_months} to repay this credit!")
        print("Overpayment %s" % (accumulate - self.principal) )

    def run(self):
        try:
            self.calculate_interest()
            self.calculate_principal()
            self.calculate_periods()

            if self.type == CreditCalculator.ANNUITY:
                if self.payment is None:
                    self.calculate_annuity_monthly_payment()
                elif self.print == 'principal':
                    self.calculate_overpayment_with_principal()
                elif self.print == 'periods':
                    self.calculate_overpayment_with_periods()
            elif self.type == CreditCalculator.DIFF:
                self.calculate_diff_monthly_payment()
            else:
                raise RuntimeError
        except RuntimeError:
            print('Incorrect parameters')


parser = argparse.ArgumentParser()
parser.add_argument('--principal', type=int)
parser.add_argument('--periods', type=int)
parser.add_argument('--interest', type=float)
parser.add_argument('--payment', type=float)
parser.add_argument('--type', type=str)

args = parser.parse_args()

calculator = CreditCalculator(args.principal, args.periods, args.interest, args.payment, args.type)
calculator.run()
