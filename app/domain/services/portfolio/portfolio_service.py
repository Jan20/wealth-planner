import locale

import pandas as pd
from pandas import DatetimeIndex, DataFrame

from app.domain.entities.portfolio_request import PortfolioRequest
from app.use_cases.portfolio.portfolio_use_case import PortfolioUseCase

locale.setlocale(locale.LC_ALL, 'de_DE')


class PortfolioService(PortfolioUseCase):

    @staticmethod
    def create_portfolio(portfolio_request: PortfolioRequest) -> DataFrame:
        """
        Calculate monthly rent payments based on the provided RentRequest and return as a DataFrame.

        Args:
        request (RentRequest): RentRequest object containing rental details.

        Returns:
        pd.DataFrame: DataFrame containing monthly rent payments.
        """
        date_range: DatetimeIndex = pd.date_range(
            start=portfolio_request.start_date,
            end=portfolio_request.end_date,
            freq='Y'
        )

        portfolio_values = [portfolio_request.initial_portfolio]
        portfolio_growth = []

        for i in range(len(date_range)):
            portfolio_growth.append(portfolio_values[i] * portfolio_request.yearly_return)
            portfolio_values.append(portfolio_values[i] + portfolio_growth[i] + portfolio_request.yearly_contribution)

        contributions = [portfolio_request.yearly_contribution for _ in range(len(date_range))]

        portfolio_values = portfolio_values[:-1]
        # Create DataFrame from calculated data
        df: DataFrame = DataFrame(
            {
                'Year': date_range,
                'Portfolio': portfolio_values,
                'Growth': portfolio_growth,
                'Contribution': contributions,
            }
        )

        df["Year"] = df["Year"].map(lambda date: date.strftime("%Y"))
        df["Growth"] = df["Growth"].map(lambda x: locale.currency(x, symbol=True, grouping=True, international=True))
        df["Contribution"] = df["Contribution"].map(lambda x: locale.currency(x, symbol=True,  grouping=True, international=True))

        return df
