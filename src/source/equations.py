from datetime import datetime
from math import exp, log, sqrt, pi

u_t_days = 1
years_to_days = 365.242
psv_s_to_usv_h = 0.0036


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
    t = final_date - initial_date
    t = t.days
    u_t = u_t_days
    ur_t = percentage_uncertainty(t, u_t)
    return t, u_t, ur_t


def percentage_uncertainty(m, u_m):
    """Returns the percentage uncertainty of a magnitude from its absolute uncertainty.

    Parameters
    ----------
    m : int or float
        Value of the magnitude.
    u_m : int or float
        Absolute uncertainty of the magnitude.

    Returns
    -------
    float
        Percentage uncertainty of the magnitude.
    """
    return u_m / m * 100


def absolute_uncertainty(m, ur_m):
    """Returns the percentage uncertainty of a magnitude from its absolute uncertainty.

    Parameters
    ----------
    m : int or float
        Value of the magnitude.
    ur_m : int or float
        Percentage uncertainty of the magnitude.

    Returns
    -------
    float
        Absolute uncertainty of the magnitude.
    """
    return m * ur_m / 100


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


def strength_value(b0, t, t12):
    """Returns the value of the source strength at a specific time.

    The unit of the strength is 1/s.
    The unit of the calibration strength is 1/s.
    The units of decay time and half life must be the same.

    Parameters
    ----------
    b0: int or float
        Value of source calibration strength.
    t : int or float
        Value of source decay time.
    t12 : int or float
        Value of source half life.

    Returns
    -------
    float
        Value of the source strength at a specific time.
    """
    return b0 * exp(-log(2) * t / t12)


def strength_relative_uncertainty(t, t12, ur_b0, ur_t, ur_t12):
    """Returns the relative uncertainty of the source strength at a specific time.

    The units of decay time and half life must be the same.

    Parameters
    ----------
    t : int or float
        Value of source decay time.
    t12 : int or float
        Value of source half life.
    ur_b0: int or float
        Relative uncertainty of source calibration strength.
    ur_t : int or float
        Relative uncertainty of source decay time.
    ur_t12 : int or float
        Relative uncertainty of source half life.
    Returns
    -------
    float
        Value of the source strength at a specific time.
    """
    return sqrt(ur_b0 ** 2 + (log(2) * t / t12) ** 2 * (ur_t ** 2 + ur_t12 ** 2))


def fluence_rate_value(b, fi, l):
    # TODO
    return b * fi / 4 / pi / l ** 2


def fluence_rate_relative_uncertainty(ur_b, ur_fi, ur_l):
    # TODO
    return sqrt(ur_b ** 2 + ur_fi ** 2 + 4 * ur_l ** 2)


def ambient_dose_equivalent_value(f, hf):
    # TODO
    return hf * f * psv_s_to_usv_h


def ambient_dose_equivalent_relative_uncertainty(ur_hf, ur_f):
    # TODO
    return sqrt(ur_hf ** 2 + ur_f ** 2)


def magnitude_product():
    # TODO
    pass


def magnitude_division():
    # TODO
    pass


def magnitude_summation():
    # TODO
    pass


def magnitude_difference():
    # TODO
    pass


def magnitude_product_uncertainty():
    # TODO
    pass


def magnitude_division_uncertainty():
    # TODO
    pass


def magnitude_summation_uncertainty():
    # TODO
    pass


def magnitude_difference_uncertainty():
    # TODO
    pass
