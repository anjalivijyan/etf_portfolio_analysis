#Maximum drawdown

def Max_Drawdown(wealth_series):
    # wealth_series: 1D Series
    roll_max = wealth_series.cummax()
    dd = wealth_series / roll_max - 1
    return dd.min()  # negative number
