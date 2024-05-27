import locale

import pandas as pd
from pandas import DatetimeIndex, DataFrame

from app.domain.entities.rent_request import RentRequest
from app.use_cases.rent.rent_use_case import RentUseCase


class RentService(RentUseCase):

    @staticmethod
    def create_rent(rent_request: RentRequest) -> DataFrame:
        """
        Calculate monthly rent payments based on the provided RentRequest and return as a DataFrame.

        Args:
        request (RentRequest): RentRequest object containing rental details.

        Returns:
        pd.DataFrame: DataFrame containing monthly rent payments.
        """
        date_range: DatetimeIndex = pd.date_range(
            start=rent_request.start_date,
            end=rent_request.end_date,
            freq='ME'
        )

        monthly_rents = [rent_request.monthly_rent * ((1 + rent_request.annual_increase / 100) ** i) for i in
                         range(len(date_range))]

        df: DataFrame = DataFrame(
            {
                'Date': date_range,
                'Monthly Rent': monthly_rents,
            }
        )
        df.set_index('Date', inplace=True)

        df = df.resample('YE').sum()
        df['Sum'] = df['Monthly Rent'].cumsum()
        df['Year'] = df.index.year

        df["Monthly Rent"] = df["Monthly Rent"].map(lambda x: locale.currency(x, symbol=True, grouping=True, international=True))
        df["Sum"] = df["Sum"].map(lambda x: locale.currency(x, symbol=True,  grouping=True, international=True))

        return df[['Year', 'Monthly Rent', 'Sum']]
