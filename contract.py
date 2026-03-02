
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This is an abstract class and should not be directly instantiated.

    Only subclasses should be instantiated.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]
    end: datetime.date
    balance: float

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.bill = None
        self.start = start

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class TermContract(Contract):
    """
     >>> contract = TermContract(start=datetime.date(2023, 1, 1), end=datetime.date(2024, 1, 1))
     >>> call = Call("056-7577", "285-3740", "2018-01-02 02:03:15", 163, [-79.24422244488586, 43.77413520361959], [-79.33181640187328, 43.75083004709019])
     >>> bill = Bill()
     >>> contract.new_month(2, 2023, bill)
     >>> contract.bill_call(call)
     >>> contract.cancel_contract()
     280.0
    """

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        super().__init__(start)
        self.end = end

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("TERM", TERM_MINS_COST)
        if self.start.year == year and self.start.month == month:
            self.bill.add_fixed_cost(TERM_DEPOSIT)
        self.bill.add_fixed_cost(TERM_MONTHLY_FEE)

    def bill_call(self, call: Call) -> None:
        call_minutes = ceil(call.duration / 60.0)
        if call_minutes > TERM_MINS:
            self.bill.add_free_minutes(TERM_MINS)
            billed_minutes = call_minutes - TERM_MINS
            self.bill.add_billed_minutes(billed_minutes)
        else:
            self.bill.free_min += call_minutes

    def cancel_contract(self) -> float:
        if datetime.date.today() >= self.end:
            refund = TERM_DEPOSIT - self.bill.get_cost()
        else:
            refund = self.bill.billed_min + TERM_MONTHLY_FEE
        return refund


class MTMContract(Contract):
    """
         >>> contract = MTMContract(start=datetime.date(2023, 1, 1))
         >>> call = Call("938-6680", "674-6199", "2023-01-02 11:05:55", 305, [-79.49877597785999, 43.60212042242521], [-79.44914130508965, 43.758957913726896])
         >>> bill = Bill()
         >>> contract.new_month(2, 2023, bill)
         >>> contract.bill_call(call)
         >>> contract.cancel_contract()
         50.3
    """

    def __init__(self, start: datetime.date) -> None:
        super().__init__(start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.add_fixed_cost(MTM_MONTHLY_FEE)
        self.bill.set_rates("MTM", MTM_MINS_COST)


class PrepaidContract(Contract):
    """
             >>> contract = PrepaidContract(start=datetime.date(2023, 1, 1), balance=50.0)
             >>> call = Call("938-6680", "674-6199", "2023-01-02 11:05:55", 305, [-79.49877597785999, 43.60212042242521], [-79.44914130508965, 43.758957913726896])
             >>> bill = Bill()
             >>> contract.new_month(2, 2023, bill)
             >>> contract.bill_call(call)
             >>> contract.cancel_contract()
             0.0
        """

    def __init__(self, start: datetime.date, balance: float) -> None:
        super().__init__(start)
        self.balance = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("PREPAID", PREPAID_MINS_COST)
        if self.balance > 10:
            self.balance -= 25
        self.bill.add_fixed_cost(self.balance)

    def cancel_contract(self) -> float:
        if self.balance > 0:
            return self.balance
        return 0.0


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
