"""
Module to prepopulate data from online datasets with unreliable API
connectivity.
"""

from econ.models import ConsumerPriceIndexData

from waterkit.econ import analysis

from datetime import datetime

def populate_cpi_data(api_key):
    """Populate consumer price index data."""
    begin = 1990
    end = datetime.now().year
    data = analysis.read_annual_cpi(api_key, begin, end)
    for year, value in data.iteritems():
        print "Inserting or updating data for %d" % year
        ConsumerPriceIndexData.objects.update_or_create(
            year = year, value = value)

