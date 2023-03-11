from datetime import datetime
from math import exp, log, sqrt


# TODO: check docstrings

def elapsed_time(initial_date, final_date):
    """Returns the elapsed time between two dates and its uncertainty.

    The unit of the elapsed time is day.
    Standard uncertainty of the elapsed time is assumed to be 1 day.

    Parameters
    ----------
    initial_date : str
        Initial date to compute the elapsed time.
    final_date : str
        Final date to compute the elapsed time.

    Returns
    -------
    int
        Elapsed time between the initial and final dates.
    """
    initial_date = datetime.strptime(initial_date, '%Y/%m/%d')
    final_date = datetime.strptime(final_date, '%Y/%m/%d')
    t = final_date - initial_date
    t = t.days
    return t


def decay_factor_value(t, t12):
    """Returns the value of source decay factor.

    The decay factor is non-dimensional.
    The units of decay time and half life must be the same.

    Parameters
    ----------
    t : int or float
        Value of source decay time.
    t12 : int or float
        Value of source half life.

    Returns
    -------
    float
        Value of source decay factor.
    """
    return exp(-log(2) * t / t12)


def decay_factor_uncertainty(t, t12, ur_t, ur_t12):
    """Returns the relative uncertainty of source decay factor.

    The units of decay time and half life must be the same.
    Standard uncertainty of the elapsed time is assumed to be 1 day.

    Parameters
    ----------
    t : int or float
        Value of source decay time.
    t12 : int or float
        Value of source half life.
    ur_t : int or float
        Relative uncertainty of source decay time.
    ur_t12 : int or float
        Relative uncertainty of source half life.

    Returns
    -------
    float
        Relative uncertainty of source decay factor.
    """
    return sqrt((log(2) * t / t12) ** 2 * (ur_t ** 2 + ur_t12 ** 2))
