# -*- coding: utf-8 -*-
"""CSV data representation classes.
"""
# Logging support
import logging
logger = logging.getLogger("brace")

# Standard collections
import collections

# Time handling support
import time

from brace.ontology import regions_dict
from brace.ontology import pollutants_dict

# named tuple for lighteweight data storage
DataRow = collections.namedtuple('DataRow',
    'region, station, pollutant, timestamp, quantity')

class DataManager(object):
    """DataManager class
    """

    def __init__(self):
        self._data = []
        self._stations = {}

    def append(self, *args, **kwargs):

        """Data validation and normalization
        """
        if args:
            raise ValueError("Unexpected unnamed parameter")

        cleaned = {}

        for (k, v) in kwargs.items():

            if (k == "region"):
                cleaned["region"] = unicode(v)

            elif (k == "station"):
                cleaned["station"] = unicode(v)

            elif (k == "pollutant"):
                cleaned["pollutant"] = pollutants_dict.get_pk(v)

            elif (k == "timestamp"):
                cleaned["timestamp"] = time.strptime(v, "%d-%m-%Y %H")

            elif (k == "quantity"):
                cleaned["quantity"] = float(v)

            else:
                raise ValueError(
                    "Unexpected named parameter: '%s'" % k)

        # normalized, cleaned up data
        row = DataRow(**cleaned)
        self._data.append(row)

        station, region = cleaned["station"], cleaned["region"]  # aliases
        if not station in self._stations:
            self._stations[station] = region
        else:
            assert self._stations[station] == region  # ensure integrity

    def filter_by_formula(self, formula):

        for row in self._data:
            if pollutants_dict.get_formula(row.pollutant) == formula:
                yield row

    @property
    def data(self):
        return iter(self._data)

    @property
    def stations(self):
        return self._stations.iteritems()

# class DataRow(object):
#     """An abstraction on raw data.
#     """

#     def __init__(self, *args, **kwargs):


#     def __repr__(self):
#         """csv representation of a single data row.
#         """
#         ctx = {
#             'region': self.region,
#             'station': self.station,
#             'pollutant': pollutants_dict.get_formula(self._data.pollutant) + \
#                 " (" + pollutants_dict.get_name(self._data.pollutant) + ")",
#             'timestamp': time.strftime("%Y-%m-%d %H:%M", self.timestamp),
#             'quantity': self.quantity,
#             }

#         return "%(region)s, %(station)s, %(pollutant)s, " \
#                     "%(timestamp)s, %(quantity)s" % ctx
