# -*- coding: utf-8 -*-
"""CSV data representation classes.
"""
# Logging support
import logging
logger = logging.getLogger(__name__)

# Time handling support
import time

from brace.ontology import regions_dict
from brace.ontology import pollutants_dict

class DataRow(object):
    """An abstraction on raw data.
    """

    def __init__(self, *args, **kwargs):

        if args:
            raise ValueError("Unexpected unnamed parameter")

        for (k, v) in kwargs.items():

            if (k == "region"):
                self._region = unicode(v)

            elif (k == "station"):
                self._station = unicode(v)

            elif (k == "pollutant"):
                self._pollutant = pollutants_dict.get_pk(v)

            elif (k == "timestamp"):
                self._timestamp = time.strptime(v, "%d-%m-%Y %H")

            elif (k == "quantity"):
                self._quantity = float(v)

            else:
                raise ValueError(
                    "Unexpected named parameter: '%s'" % k)

    @property
    def region(self):
        """Get the region."""
        return self._region

    @property
    def station(self):
        """Get the station."""
        return self._station

    @property
    def pollutant_formula(self):
        """Get the pollutant formula."""
        return pollutants_dict.get_formula(self._pollutant)

    @property
    def pollutant_descr(self):
        """Get the pollutant description."""
        return pollutants_dict.get_name(self._pollutant)

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def quantity(self):
        return self._quantity

    def __repr__(self):
        """csv representation of a single data row.
        """
        ctx = {
            'region': self.region,
            'station': self.station,
            'pollutant': pollutants_dict.get_formula(self._pollutant) + \
                " (" + pollutants_dict.get_name(self._pollutant) + ")",
            'timestamp': time.strftime("%Y-%m-%d %H:%M", self.timestamp),
            'quantity': self.quantity,
            }

        return "%(region)s, %(station)s, %(pollutant)s, " \
                    "%(timestamp)s, %(quantity)s" % ctx

