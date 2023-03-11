from datetime import datetime
from math import exp, log, sqrt


def elapsed_time(initial_date, final_date):
    """Compute the elapsed time between two dates in days.

    Parameters
    ----------
    initial_date : str
        Initial date to compute the elapsed time.
    final_date : str
        Final date to compute the elapsed time.

    Returns
    -------
    float
        Elapsed time between two dates in days.
    """
    initial_date = datetime.strptime(initial_date, '%Y/%m/%d')
    final_date = datetime.strptime(final_date, '%Y/%m/%d')
    t = final_date - initial_date
    t = t.days
    return t


def decay_factor_value(t, t12):
    """Compute the value of the source's decay factor on a date from the calibration date.

    Its value is computed as:

    .. math::
        f=e^{-\\frac{\\ln(2)t}{t_{12}}}

    where :math:`t` the source's decay time from the source's calibration date and
    :math:`t_{1/2}` if the source's half life.

    Parameters
    ----------
    t : int or float
        Value of source's decay time.
    t12 : int or float
        Value of source's half life.

    Returns
    -------
    float
        Value of source's decay factor on a date from the calibration date.
    """
    return exp(-log(2) * t / t12)


def decay_factor_uncertainty(t, t12, ur_t, ur_t12):
    """Compute relative standard uncertainty of the source's decay factor on a date from the calibration date.

    Its relative standard uncertainty is computed as:

    .. math::
        u_r(f)=\\sqrt{\\left(\\frac{\\ln(2)t}{t_{12}}\\right)^2\\left(u_r^2(t)+u_r^2(t_{1/2})\\right)}

    Parameters
    ----------
    t : int or float
        Value of source's decay time.
    t12 : int or float
        Value of source's half life.
    ur_t : int or float
        Relative uncertainty of source's decay time.
    ur_t12 : int or float
        Relative uncertainty of source's half life.

    Returns
    -------
    float
        Relative standard uncertainty of source's decay factor on a date from the calibration date.
    """
    return sqrt((log(2) * t / t12) ** 2 * (ur_t ** 2 + ur_t12 ** 2))
