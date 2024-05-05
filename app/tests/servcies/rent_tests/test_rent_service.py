import unittest
import locale
from datetime import datetime

import pandas as pd
from pandas import DatetimeIndex, DataFrame, Timestamp
from app.domain.entities.rent_request import RentRequest
from app.domain.services.rent.rent_service import RentService
from app.use_cases.rent.rent_use_case import RentUseCase


class TestRentService(unittest.TestCase):

    START_DATE = Timestamp(2024, 1, 1)
    END_DATE = datetime(2024, 12, 31)

    def test_valid_input(self):
        rent_request = RentRequest(start_date=START_DATE, end_date='2024-12-31', monthly_rent=1000, annual_increase=2)
        result = RentService.create_rent(rent_request)
        self.assertIsInstance(result, DataFrame)
        self.assertCountEqual(result.columns, ['Year', 'Monthly Rent', 'Sum'])
        self.assertEqual(len(result), 12)  # Assuming one year rental
        # Add more assertions for specific values if needed

    def test_no_rent(self):
        rent_request = RentRequest(start_date='2024-01-01', end_date='2024-12-31', monthly_rent=0, annual_increase=2)
        result = RentService.create_rent(rent_request)
        self.assertTrue((result['Monthly Rent'] == 0).all())
        self.assertEqual(result['Sum'].iloc[-1], 0)

    # Add other test methods following similar patterns for other cases


if __name__ == '__main__':
    unittest.main()