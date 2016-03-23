from waterkit.flow import rasterflow
import functools32

import logging
logger = logging.getLogger(__name__)
import threading

def synchronized(f):
    """Decorator to make sure a function is only called by one thread at a
    time.
    """
    lock = threading.Lock()
    def sync(*args, **kwargs):
        with lock:
            return f(*args, **kwargs)
    return sync

@synchronized
def read_usgs_data(identifier, start_date, end_date, target, multiplier):
    """Read from a USGS data source.

    This function is synchronized because requests for the same data are often
    made in close proximity to one another, for instance when loading multiple
    images on the same page. In such cases all threads waiting for data that
    may be cached in the not too distant future is cheaper than all threads
    doing the same work.
    """
    data = read_usgs_data_impl(identifier, start_date, end_date, target, multiplier)
    logger.info("USGS data cache: %s", read_usgs_data_impl.cache_info())
    return data

@functools32.lru_cache(maxsize=64)
def read_usgs_data_impl(identifier, start_date, end_date, target, multiplier):
    return rasterflow.read_usgs_data(identifier, start_date, end_date, target,
        multiplier=multiplier)

@synchronized
def read_excel_data(data_file, date_column_name, attribute_column_name,
    sheet_name, target_column_name, multiplier):
    """Read from an Excel data source.

    This function is synchronized because requests for the same data are often
    made in close proximity to one another, for instance when loading multiple
    images on the same page. In such cases all threads waiting for data that
    may be cached in the not too distant future is cheaper than all threads
    doing the same work.
    """
    data = read_excel_data_impl(data_file, date_column_name, attribute_column_name,
        sheet_name, target_column_name, multiplier)
    logger.info("Excel data cache: %s", read_excel_data_impl.cache_info())
    return data

@functools32.lru_cache(maxsize=64)
def read_excel_data_impl(data_file, date_column_name, attribute_column_name,
    sheet_name, target_column_name, multiplier):
    return rasterflow.read_excel_data(
        data_file,
        date_column_name,
        attribute_column_name,
        sheet_name,
        target_column_name,
        multiplier=multiplier
    )
