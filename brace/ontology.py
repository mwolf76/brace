"""Source data dictionaries for pollutants and italian regions.
"""

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

    # List of Italian regions (code, name)
    regions = [
        (13, u"Abruzzo"),
        (21, u"Alto Adige"),
        (17, u"Basilicata"),
        (18, u"Calabria"),
        (15, u"Campania"),
        (8, u"Emilia Romagna"),
        (6, u"Friuli Venezia Giulia"),
        (12, u"Lazio"),
        (7, u"Liguria"),
        (3, u"Lombardia"),
        (11, u"Marche"),
        (14, u"Molise"),
        (1, u"Piemonte"),
        (16, u"Puglia"),
        (20, u"Sardegna"),
        (19, u"Sicilia"),
        (9, u"Toscana"),
        (4, u"Trentino"),
        (10, u"Umbria"),
        (2, u"Valle d'Aosta"),
        (5, u"Veneto"),
    ]

    # case insensitive find
    def _find_tuple(self, ident):

        if isinstance(ident, unicode) or \
                isinstance(ident, str):
            ident = ident.lower()

        for (pk, name) in self.regions:
            if ident in (pk, name.lower()):
                return (pk, name)

        raise KeyError("key '%s' not found" % ident)

    def get_pk(self, ident):

        (pk, name) = self._find_tuple(ident)
        return pk

    def get_name(self, ident):

        (pk, name) = self._find_tuple(ident)
        return name

    def get_longitude(self, ident):
        return 0.0  ## TODO

    def get_latitude(self, ident):
        return 0.0 ## TODO

    def all(self):

        return self.regions

regions_dict = ItalianRegionsDictionary()


