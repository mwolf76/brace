# -*- coding: utf-8 -*-
"""Source data dictionaries for pollutants and italian regions.
"""
# Logging support
import logging
logger = logging.getLogger("brace")

# localization services
from gettext import gettext as _


class PollutantsDictionary(object):
    """Provides loookup services for pollutants. All of the get_xxx
    methods below take a generic identifier. The given identifier is
    used to perform look-up using key, formula and name in this order.
    """

    # List of known pollutants (code, identifier, name)
    pollutants = [
        (1, "SO2", _(u"Sulfur Dioxide")),
        (8, "NO2", _(u"Nitrogen Dioxide")),
        (9, "NOx", _(u"Nitrogen Oxides")),
        (38, "NO", _(u"Nitrogen Oxide")),
        (7, "O3", _(u"Ozone")),
        (10, "CO", _(u"Carbon Oxide")),
        (5, "PM10", _(u"Particulates < 10 μm")),
        (6001, "PM25", _(u"Particulates < 2.5 μm")),
        (4, "PTS", _(u"Particulates")),
        (20, "C6H6", _(u"Benzene")),
    ]

    # case insensitive find
    def _find_tuple(self, ident):

        if isinstance(ident, unicode) or \
                isinstance(ident, str):
            ident = ident.lower()

        for (pk, formula, name) in self.pollutants:
            if ident in (pk, formula.lower(), name.lower()):
                return (pk, formula, name)

        raise KeyError("key '%s' not found" % ident)

    def get_pk(self, ident):
        """Given a chemical identifier, returns its pk in the
        pollutants database. Raises a KeyError if no element could be
        retrieved.
        """
        (pk, formula, name) = self._find_tuple(ident)
        return pk

    def get_formula(self, ident):
        """Given a chemical identifier, returns its formula in the
        pollutants database. Raises a KeyError if no element could be
        retrieved.
        """
        (pk, formula, name) = self._find_tuple(ident)
        return formula

    def get_name(self, ident):
        """Given a chemical, returns its name in the pollutants
        database.  Raises a KeyError if no element could be retrieved.
        """
        (pk, formula, name) = self._find_tuple(ident)
        return name

    def all(self):
        """Return the list of all known pollutants.
        """
        return self.pollutants

pollutants_dict = PollutantsDictionary()


class ItalianRegionsDictionary(object):
    """Provides loookup services for italian regions. All of the get_xxx
    methods below take a generic identifier. The given identifier is
    used to perform look-up using key and name in this order.
    """

    # List of Italian regions (code, name, latitude, longitude)
    regions = [
        (13, u"Abruzzo", 42.366111, 13.394444),
        (21, u"Alto Adige", 46.5, 11.35),
        (17, u"Basilicata", 40.639166, 15.805278),
        (18, u"Calabria", 38.8918, 16.5995),
        (15, u"Campania", 40.833333, 14.25),
        (8, u"Emilia Romagna", 44.510556, 10.956944),
        (6, u"Friuli Venezia Giulia", 45.636111, 13.804167),
        (12, u"Lazio", 41.893055, 12.482778),
        (7, u"Liguria", 44.455556, 8.734722),
        (3, u"Lombardia", 45.585555, 9.930278),
        (11, u"Marche", 43.616945, 13.516667),
        (14, u"Molise", 41.566667, 14.666667),
        (1, u"Piemonte", 45.066667, 7.7),
        (16, u"Puglia", 41.125278, 16.866667),
        (20, u"Sardegna", 39.216667, 9.116667),
        (19, u"Sicilia", 38.115556, 13.361389),
        (9, u"Toscana", 43.771389, 11.254167),
        (4, u"Trentino", 46.066667, 11.116667),
        (10, u"Umbria", 43.1121, 12.3888),
        (2, u"Valle d'Aosta", 45.737222, 7.320556),
        (5, u"Veneto", 45.439722, 12.331945),
    ]

    # case insensitive find
    def _find_tuple(self, ident):

        if isinstance(ident, unicode) or \
                isinstance(ident, str):
            ident = ident.lower()

        for (pk, name, latitude, longitude) in self.regions:
            if ident in (pk, name.lower()):
                return (pk, name, latitude, longitude)

        raise KeyError("key '%s' not found" % ident)

    def get_pk(self, ident):

        (pk, _, _, _) = self._find_tuple(ident)
        return pk

    def get_name(self, ident):

        (_, name, _, _) = self._find_tuple(ident)
        return name

    def get_latitude(self, ident):
        (_, _, latitude, _) = self._find_tuple(ident)
        return latitude

    def get_longitude(self, ident):
        (_, _, _, longitude) = self._find_tuple(ident)
        return longitude

    def all(self):
        return self.regions

regions_dict = ItalianRegionsDictionary()


