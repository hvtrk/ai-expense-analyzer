import logging
import numpy as np

PRECISION = 2

# Module-level logger — importable as `from utils.math_utils import logger`
logger = logging.getLogger(__name__)


# Safe float
def safe_float(value):
    try:
        value = float(value)
        if np.isnan(value) or np.isinf(value):
            return 0.0
        return round(float(value), PRECISION)
    except (ValueError, TypeError):
        return 0.0
