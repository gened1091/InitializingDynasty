import os
import numpy as np

from flask import redirect, render_template, session
from functools import wraps


def get_normal_in_range(mean, stdev, lower=0, upper=100):
    value = np.random.normal(loc=mean, scale=stdev)
    while value > upper or value < lower:
        value = np.random.normal(loc=mean, scale=stdev)
    return round(value)

def cap_0_100(value):
    if value > 100:
        return 100
    elif value < 0:
        return 0
    return round(value)
