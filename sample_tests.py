
import datetime

import pytest

from application import create_customers, process_event_history
from contract import TermContract, MTMContract, PrepaidContract
from customer import Customer
from filter import DurationFilter, CustomerFilter, ResetFilter
from phoneline import PhoneLine


def create_single_customer_with_all_lines() -> Customer:
    """ Create a customer with one of each type of PhoneLine
    """
    contracts = [
        TermContract(start=datetime.date(year=2017, month=12, day=25),
                     end=datetime.date(year=2019, month=6, day=25)),
        MTMContract(start=datetime.date(year=2017, month=12, day=25)),
        PrepaidContract(start=datetime.date(year=2017, month=12, day=25),
                        balance=100)
    ]
    numbers = ['867-5309', '273-8255', '649-2568']
    customer = Customer(cid=7777)

    for i in range(len(contracts)):
        customer.add_phone_line(PhoneLine(numbers[i], contracts[i]))

    customer.new_month(12, 2017)
    return customer


test_dict = {'events': [
    {"type": "sms",
     "src_number": "867-5309",
     "dst_number": "273-8255",
     "time": "2018-01-01 01:01:01",
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "sms",
     "src_number": "273-8255",
     "dst_number": "649-2568",
     "time": "2018-01-01 01:01:02",
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "sms",
     "src_number": "649-2568",
     "dst_number": "867-5309",
     "time": "2018-01-01 01:01:03",
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "273-8255",
     "dst_number": "867-5309",
     "time": "2018-01-01 01:01:04",
     "duration": 10,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "867-5309",
     "dst_number": "649-2568",
     "time": "2018-01-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "649-2568",
     "dst_number": "273-8255",
     "time": "2018-01-01 01:01:06",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]}
],
    'customers': [
        {'lines': [
            {'number': '867-5309',
             'contract': 'term'},
            {'number': '273-8255',
             'contract': 'mtm'},
            {'number': '649-2568',
             'contract': 'prepaid'}
        ],
            'id': 7777}
    ]
}

test_dict2 = {
    'events': [],
    'customers': [
        {'id': 7777, 'lines': [{'number': '867-5309', 'contract': 'term'}]},
        {'id': 8888, 'lines': [{'number': '123-4567', 'contract': 'mtm'}]},
        {'id': 9999, 'lines': [{'number': '555-7890', 'contract': 'prepaid'}]}
    ]
}

import unittest
class TestFilters(unittest.TestCase):
    def setUp(self):
        """Set up test data for customers and calls."""
        self.customer1 = Customer(1001, ["123-4567", "890-1234"])
        self.customer2 = Customer(2002, ["555-5555"])
        self.customers = [self.customer1, self.customer2]

        self.call1 = Call("123-4567", "555-5555", (43.7, -79.4), (43.6, -79.5), 120)
        self.call2 = Call("555-5555", "890-1234", (43.9, -79.3), (44.0, -79.2), 300)
        self.call3 = Call("999-9999", "777-7777", (43.5, -79.6), (43.4, -79.7), 180)
        self.calls = [self.call1, self.call2, self.call3]

    def test_customer_filter_valid_id(self):
        """Test CustomerFilter with a valid customer ID."""
        filter_ = CustomerFilter()
        result = filter_.apply(self.customers, self.calls, "1001")
        self.assertEqual(result, [self.call1, self.call2])  # Only calls involving 1001

    def test_customer_filter_invalid_id(self):
        """Test CustomerFilter with an invalid customer ID."""
        filter_ = CustomerFilter()
        result = filter_.apply(self.customers, self.calls, "9999")
        self.assertEqual(result, self.calls)  # No change expected

    def test_customer_filter_non_numeric(self):
        """Test CustomerFilter with a non-numeric input."""
        filter_ = CustomerFilter()
        result = filter_.apply(self.customers, self.calls, "abc")
        self.assertEqual(result, self.calls)  # No change expected

    def test_location_filter_valid_range(self):
        """Test LocationFilter with a valid range covering call1."""
        filter_ = LocationFilter()
        result = filter_.apply(self.customers, self.calls, "-79.5, 43.5, -79.3, 43.8")
        self.assertEqual(result, [self.call1])  # Only call1 falls within range

    def test_location_filter_outside_range(self):
        """Test LocationFilter with a range that excludes all calls."""
        filter_ = LocationFilter()
        result = filter_.apply(self.customers, self.calls, "-80.0, 42.0, -79.8, 42.5")
        self.assertEqual(result, [])  # No calls should match

    def test_location_filter_invalid_input(self):
        """Test LocationFilter with an invalid format."""
        filter_ = LocationFilter()
        result = filter_.apply(self.customers, self.calls, "invalid input")
        self.assertEqual(result, self.calls)  # No change expected

def test_customer_creation() -> None:
    """ Test for the correct creation of Customer, PhoneLine, and Contract
    classes
    """
    customer = create_single_customer_with_all_lines()
    bill = customer.generate_bill(12, 2017)

    assert len(customer.get_phone_numbers()) == 3
    assert len(bill) == 3
    assert bill[0] == 7777 
    assert bill[1] == 270.0
    assert len(bill[2]) == 3
    assert bill[2][0]['total'] == 320
    assert bill[2][1]['total'] == 50
    assert bill[2][2]['total'] == -100

    # Check for the customer creation in application.py
    customer = create_customers(test_dict)[0]
    customer.new_month(12, 2017)
    bill = customer.generate_bill(12, 2017)

    assert len(customer.get_phone_numbers()) == 3
    assert len(bill) == 3
    assert bill[0] == 7777
    assert bill[1] == 270.0
    assert len(bill[2]) == 3
    assert bill[2][0]['total'] == 320
    assert bill[2][1]['total'] == 50
    assert bill[2][2]['total'] == -100

def test_customer_creation_extended() -> None:
    customer = create_single_customer_with_all_lines()
    assert len(customer.get_phone_numbers()) == 3
    assert customer.get_id() == 7777
    assert all(isinstance(num, str) for num in customer.get_phone_numbers())

def test_contract_start_dates_extended() -> None:
    customers = create_customers(test_dict)
    for c in customers:
        for pl in c._phone_lines:
            assert pl.contract.start == datetime.date(2017, 12, 25)
            if hasattr(pl.contract, 'end'):
                assert pl.contract.end == datetime.date(2019, 6, 25)

def test_events_extended() -> None:
    customers = create_customers(test_dict)
    customers[0].new_month(1, 2018)
    process_event_history(test_dict, customers)
    bill = customers[0].generate_bill(1, 2018)
    assert bill[0] == 7777
    assert isinstance(bill[1], float)
    assert bill[1] >= 0  # Ensuring bill is non-negative

def test_customer_creation_extended() -> None:
    customer = create_single_customer_with_all_lines()
    assert len(customer.get_phone_numbers()) == 3
    assert customer.get_id() == 7777
    assert all(isinstance(num, str) for num in customer.get_phone_numbers())

def test_contract_start_dates_extended() -> None:
    customers = create_customers(test_dict)
    for c in customers:
        for pl in c._phone_lines:
            assert pl.contract.start == datetime.date(2017, 12, 25)
            if hasattr(pl.contract, 'end'):
                assert pl.contract.end == datetime.date(2019, 6, 25)

def test_events_extended() -> None:
    customers = create_customers(test_dict)
    customers[0].new_month(1, 2018)
    process_event_history(test_dict, customers)
    bill = customers[0].generate_bill(1, 2018)
    assert bill[0] == 7777
    assert isinstance(bill[1], float)
    # assert bill[1] >= 0  # Ensuring bill is non-negative

    # Check individual contract contributions
    term_total = bill[2][0]['total']
    mtm_total = bill[2][1]['total']
    prepaid_total = bill[2][2]['total']
    print(term_total)
    print(mtm_total)
    print(prepaid_total)

    assert isinstance(term_total, (int, float))
    assert isinstance(mtm_total, (int, float))
    assert isinstance(prepaid_total, (int, float))

    assert term_total >= 0  # Term contract should always be non-negative
    assert mtm_total >= 0  # MTM contract should be non-negative
    assert prepaid_total <= 0  # Prepaid can be negative due to deductions

    history = customers[0].get_call_history()
    assert isinstance(history, list)
    assert len(history) > 0
    assert all(hasattr(h, 'incoming_calls') and hasattr(h, 'outgoing_calls') for h in history)

def test_filters_extended() -> None:
    customers = create_customers(test_dict)
    process_event_history(test_dict, customers)
    calls = []
    hist = customers[0].get_history()
    calls.extend(hist[0])

    filters = [
        DurationFilter(),
        CustomerFilter(),
        ResetFilter()
    ]

    filter_strings = [
        ["L050", "G010", "L000", "50", "AA", ""],
        ["7777", "1111", "9999", "aaaaaaaa", ""],
        ["rrrr", ""]
    ]

    expected_return_lengths = [
        [1, 2, 0, 3, 3, 3],
        [3, 3, 3, 3, 3],
        [3, 3]
    ]

    for i in range(len(filters)):
        for j in range(len(filter_strings[i])):
            result = filters[i].apply(customers, calls, filter_strings[i][j])
            assert isinstance(result, list)
            assert len(result) == expected_return_lengths[i][j]

def test_events() -> None:
    """ Test the ability to make calls, and ensure that the CallHistory objects
    are populated
    """
    customers = create_customers(test_dict)
    customers[0].new_month(1, 2018)

    process_event_history(test_dict, customers)

    # Check the bill has been computed correctly
    bill = customers[0].generate_bill(1, 2018)
    assert bill[0] == 7777
    assert bill[1] == pytest.approx(-29.925)
    assert bill[2][0]['total'] == pytest.approx(20)
    assert bill[2][0]['free_mins'] == 1
    assert bill[2][1]['total'] == pytest.approx(50.05)
    assert bill[2][1]['billed_mins'] == 1
    assert bill[2][2]['total'] == pytest.approx(-99.975)
    assert bill[2][2]['billed_mins'] == 1

    # Check the CallHistory objects are populated
    history = customers[0].get_call_history('867-5309')
    assert len(history) == 1
    assert len(history[0].incoming_calls) == 1
    assert len(history[0].outgoing_calls) == 1

    history = customers[0].get_call_history()
    assert len(history) == 3
    assert len(history[0].incoming_calls) == 1
    assert len(history[0].outgoing_calls) == 1


def test_contract_start_dates() -> None:
    """ Test the start dates of the contracts.

    Ensure that the start dates are the correct dates as specified in the given
    starter code.
    """
    customers = create_customers(test_dict)
    for c in customers:
        for pl in c._phone_lines:
            assert pl.contract.start == datetime.date(
                year=2017, month=12, day=25)
            if hasattr(pl.contract, 'end'):  # only check if there is an end date (TermContract)
                assert pl.contract.end == datetime.date(
                    year=2019, month=6, day=25)


def test_filters() -> None:
    """ Test the functionality of the filters.

    We are only giving you a couple of tests here, you should expand both the
    dataset and the tests for the different types of applicable filters
    """
    customers = create_customers(test_dict)
    process_event_history(test_dict, customers)

    # Populate the list of calls:
    calls = []
    hist = customers[0].get_history()
    # only consider outgoing calls, we don't want to duplicate calls in the test
    calls.extend(hist[0])

    # The different filters we are testing
    filters = [
        DurationFilter(),
        CustomerFilter(),
        ResetFilter()
    ]

    # These are the inputs to each of the above filters in order.
    # Each list is a test for this input to the filter
    filter_strings = [
        ["L050", "G010", "L000", "50", "AA", ""],
        ["7777", "1111", "9999", "aaaaaaaa", ""],
        ["rrrr", ""]
    ]

    # These are the expected outputs from the above filter application
    # onto the full list of calls
    expected_return_lengths = [
        [1, 2, 0, 3, 3, 3],
        [3, 3, 3, 3, 3],
        [3, 3]
    ]

    for i in range(len(filters)):
        for j in range(len(filter_strings[i])):
            result = filters[i].apply(customers, calls, filter_strings[i][j])
            assert len(result) == expected_return_lengths[i][j]


if __name__ == '__main__':
    pytest.main(['sample_tests.py'])
    unittest.main()
