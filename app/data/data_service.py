# src/data/data_service.py

import yfinance as yf
import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config.api_config import ROIC_API
from config.metrics_config import METRICS_TO_FETCH, CAGR_METRICS


class DataService:
    def __init__(self):
        self.METRICS = {
            "total revenues": "is_sales_and_services_revenues",
            "operating cash flow": "cf_cash_from_oper",
            "net income": "is_net_income",
            "earnings per share": "eps",
            "operating margin": "oper_margin",
            "capital expenditures": "cf_cap_expenditures",
            "return on invested capital": "return_on_inv_capital",
            "Diluted Weighted Avg Shares": "is_sh_for_diluted_eps"
        }
        self.API_KEY = "a365bff224a6419fac064dd52e1f80d9"
        self.BASE_URL = "https://api.roic.ai/v1/rql"
        self.CAGR_METRICS = CAGR_METRICS

    def get_historical_data(self, ticker, start_date, end_date):
        """Fetch historical price data using yfinance"""
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(start=start_date, end=end_date)
        if df.empty:
            raise ValueError(f"No data found for {ticker} in the specified date range")
        df.index = df.index.tz_localize(None)
        return df

    def get_financial_data(self, ticker, metric_description, start_year, end_year):
        """Fetch financial metrics data from ROIC API"""
        metric_field = self.METRICS.get(metric_description.lower())
        if not metric_field:
            print(f"Error: Unknown metric '{metric_description}'")
            return None

        query = f"get({metric_field}(fa_period_reference=range('{start_year}', '{end_year}'))) for('{ticker}')"
        url = f"{self.BASE_URL}?query={query}&apikey={self.API_KEY}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            df = pd.DataFrame(response.json())
            df.columns = df.iloc[0]
            df = df.drop(0).reset_index(drop=True)

            years = df['fiscal_year'].astype(int)
            values = df[metric_field].astype(float)

            return pd.Series(values.values, index=years, name=metric_description)
        except Exception as e:
            print(f"Error fetching {metric_description}: {str(e)}")
            return None

    def get_analysis_dates(self, end_date, lookback_type, lookback_value):
        """Calculate start date based on lookback period"""
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        if lookback_type == 'quarters':
            start_dt = end_dt - relativedelta(months=3*lookback_value)
        else:  # days
            start_dt = end_dt - relativedelta(days=lookback_value)
        return start_dt.strftime("%Y-%m-%d")

    def create_metrics_table(self, ticker, metrics, start_year, end_year):
        """Creates a combined table of all metrics with selective growth rates"""
        data = {}
        growth_rates = {}

        for metric in metrics:
            metric = metric.lower()
            series = self.get_financial_data(ticker.upper(), metric, start_year, end_year)
            if series is not None:
                data[metric] = series

                # Calculate CAGR only for specified metrics
                if metric in self.CAGR_METRICS:
                    first_value = series.iloc[0]
                    last_value = series.iloc[-1]
                    num_years = len(series) - 1
                    if num_years > 0 and first_value > 0 and last_value > 0:
                        growth_rate = ((last_value / first_value) ** (1 / num_years) - 1) * 100
                        growth_rates[metric] = growth_rate

        if data:
            # Create main DataFrame with metrics
            df = pd.DataFrame(data).T

            # Add growth rates column only for specified metrics
            df['CAGR %'] = None  # Initialize with None
            for metric in self.CAGR_METRICS:
                if metric in growth_rates and metric in df.index:
                    df.at[metric, 'CAGR %'] = growth_rates[metric]

            return df
        return None

    def add_metric(self, description, field_name):
        """Adds a new metric to the METRICS dictionary"""
        description = description.lower().strip()
        field_name = field_name.strip()

        if description in self.METRICS:
            print(f"Warning: Metric '{description}' already exists with field '{self.METRICS[description]}'")
            return False

        self.METRICS[description] = field_name
        return True