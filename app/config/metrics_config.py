"""
Configuration file for financial metrics and analysis parameters
"""

# Financial metrics to fetch
METRICS_TO_FETCH = [
    "total revenues",
    "operating cash flow",
    "net income",
    "earnings per share",
    "operating margin",
    "capital expenditures",
    "return on invested capital",
    "Diluted Weighted Avg Shares"
]

# Metrics that should include CAGR calculation
CAGR_METRICS = {
    "total revenues",
    "operating cash flow",
    "net income",
    "earnings per share"
}

# Analysis parameters
ANALYSIS_DEFAULTS = {
    'lookback_days': 365,
    'crossover_days': 180
}
