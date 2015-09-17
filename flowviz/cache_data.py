from waterkit import rasterflow
import functools32

@functools32.lru_cache(maxsize=32)
def read_usgs_data(identifier, start_date, end_date, target, multiplier):
    return rasterflow.read_usgs_data(identifier, start_date, end_date, target,
        multiplier=multiplier)

@functools32.lru_cache(maxsize=32)
def read_excel_data(data_file, date_column_name, attribute_column_name,
    sheet_name, target_column_name, multiplier):
    return rasterflow.read_excel_data(
        data_file,
        date_column_name,
        attribute_column_name,
        sheet_name,
        target_column_name,
        multiplier=multiplier
    )
