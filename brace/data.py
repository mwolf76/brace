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
from brace.ontology import stations_dict
from brace.ontology import pollutants_dict

from brace.exceptions import OntologyException

# Ordered dict
try:
    from collections import OrderedDict

except ImportError, ioe:
    from ordereddict import OrderedDict

# named tuple for lighteweight data storage
DataRow = collections.namedtuple('DataRow',
    'region, station, pollutant, timestamp, quantity')

class DataManager(object):
    """DataManager class
    """

    def __init__(self):
        self._data = []

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

        if station not in stations_dict:
            raise OntologyException("Station '%s' not found in the ontology." %
                                    station)

        if region not in regions_dict:
            raise OntologyException("Station '%s' not found in the ontology." %
                                    station)

    def filter_by_formula(self, formula):

        for row in self._data:
            if pollutants_dict.get_formula(row.pollutant) == formula:
                yield row

    @property
    def data(self):
        return iter(self._data)
