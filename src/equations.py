from datetime import datetime
from math import exp, log, sqrt

u_t_days = 1


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
    tuple
        Elapsed time between the initial and final dates (value, uncertainty, percentage uncertainty).
    """
    initial_date = datetime.strptime(initial_date, '%Y/%m/%d')
    final_date = datetime.strptime(final_date, '%Y/%m/%d')
    time = final_date - initial_date
    time = time.days
    uncertainty = u_t_days
    percentage = percentage_uncertainty(time, uncertainty)
    return time, uncertainty, percentage


def percentage_uncertainty(m, u_m):
    """Returns the percentage uncertainty of a magnitude from its absolute uncertainty.

    Parameters
    ----------
    m : num
        Value of the magnitude.
    u_m : num
        Absolute uncertainty of the magnitude.

    Returns
    -------
    num
        Percentage uncertainty of the magnitude.
    """
    return u_m / m * 100


def absolute_uncertainty(m, ur_m):
    """Returns the percentage uncertainty of a magnitude from its absolute uncertainty.

    Parameters
    ----------
    m : num
        Value of the magnitude.
    ur_m : num
        Percentage uncertainty of the magnitude.

    Returns
    -------
    num
        Absolute uncertainty of the magnitude.
    """
    return m * ur_m / 100


def decay_factor_value(t, t12):
    """Returns the value of source decay factor.

    The value of decay factor is non-dimensional.
    The units of decay time and half life must be the same.

    Parameters
    ----------
    t : num
        Value of source decay time.
    t12 : num
        Value of source half life.

    Returns
    -------
    num
        Value of source decay factor.
    """
    return exp(-log(2) * t / t12)


def decay_factor_uncertainty(t, t12, ur_t, ur_t12):
    """Returns the relative uncertainty of source decay factor.

    The value of decay factor is non-dimensional.
    The units of decay time and half life must be the same.

    Parameters
    ----------
    t : num
        Value of source decay time.
    t12 : num
        Value of source half life.
    ur_t : num
        Relative uncertainty of source decay time.
    ur_t12 : num
        Relative uncertainty of source half life.

    Returns
    -------
    num
        Relative uncertainty of source decay factor.
    """
    return sqrt((log(2) * t / t12) ** 2 * (ur_t ** 2 + ur_t12 ** 2))
