# -*- coding: utf-8 -*-
"""Source data dictionaries for pollutants and italian regions.
"""
# Logging support
import logging
logger = logging.getLogger("brace")

# localization services
from gettext import gettext as _

# TODO: improve these classes for performance

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
        (5, "PM10", _(u"Particulates < 10 micrometers")),
        (6001, "PM25", _(u"Particulates < 2.5 micrometers")),
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

        raise KeyError (
            "%s is not a known pollutant." % ident)

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

    def __contains__(self, ident):
        try:
            (_, _, _, _) = self._find_tuple(ident)
            return True

        except:
            pass

        return False


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

        raise KeyError(
            "'%s' is not an italian region" % ident)

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

    def __contains__(self, ident):
        try:
            (_, _, _, _) = self._find_tuple(ident)
            return True

        except:
            pass

        return False

    def all(self):
        return self.regions

regions_dict = ItalianRegionsDictionary()


class StationsDictionary(object):
    """Provides loookup services for the pulltant stations. All of the
    get_xxx methods below take a generic identifier. The given
    identifier is used to perform look-up using key and name in this
    order.
    """

    # List of sampling stations (region_code, station_name, latitude, longitude)
    # TODO: as of now the ontology holds only the stations for Lombardy, extracting
    # these indeed is a PITA. This list comes from a lot of Emacs macro wizardry and
    # a certain amount of nerve.

    stations = [

        # TODO fix coordinates
        (3, u"ABBADIA CERRETO", 45.5855555, 9.930278),
        (3, u"ARCONATE", 45.5855555, 9.930278),
        (3, u"ARESE", 45.5855555, 9.930278),
        (3, u"BERGAMO - VIA GARIBALDI", 45.5855555, 9.930278),
        (3, u"BERGAMO - VIA GOISIS", 45.5855555, 9.930278),
        (3, u"BERGAMO - VIA MEUCCI", 45.5855555, 9.930278),
        (3, u"BERTONICO", 45.5855555, 9.930278),
        (3, u"BORGOFRANCO", 45.5855555, 9.930278),
        (3, u"BORMIO", 45.5855555, 9.930278),
        (3, u"BRESCIA - BROLETTO", 45.5855555, 9.930278),
        (3, u"BRESCIA - VIA ZIZIOLA", 45.5855555, 9.930278),
        (3, u"BRESCIA VIA CANTORE", 45.5855555, 9.930278),
        (3, u"BRESCIA VILLAGGIO SERENO", 45.5855555, 9.930278),
        (3, u"BUSTO ARSIZIO - ACCAM", 45.5855555, 9.930278),
        (3, u"CALUSCO", 45.5855555, 9.930278),
        (3, u"CANTU - VIA MEUCCI", 45.5855555, 9.930278),
        (3, u"CARBONARA DI PO", 45.5855555, 9.930278),
        (3, u"CASIRATE D'ADDA", 45.5855555, 9.930278),
        (3, u"CASSANO VIA DI VONA", 45.5855555, 9.930278),
        (3, u"CASSANO VIA MILANO", 45.5855555, 9.930278),
        (3, u"CHIAVENNA", 45.5855555, 9.930278),
        (3, u"CITTADELLA", 45.5855555, 9.930278),
        (3, u"CODOGNO", 45.5855555, 9.930278),
        (3, u"COLICO", 45.5855555, 9.930278),
        (3, u"COMO", 45.5855555, 9.930278),
        (3, u"CORMANO", 45.5855555, 9.930278),
        (3, u"CORNALE", 45.5855555, 9.930278),
        (3, u"CORTE DEI CORTESI", 45.5855555, 9.930278),
        (3, u"CREMA - VIA INDIPENDENZA", 45.5855555, 9.930278),
        (3, u"CREMA - VIA XI FEBBRAIO", 45.5855555, 9.930278),
        (3, u"CREMONA - P.ZZA CADORNA", 45.5855555, 9.930278),
        (3, u"CREMONA - PIAZZA LIBERTA", 45.5855555, 9.930278),
        (3, u"CREMONA VIA FATEBENEFRATELLI", 45.5855555, 9.930278),
        (3, u"DARFO_2", 45.5855555, 9.930278),
        (3, u"ERBA", 45.5855555, 9.930278),
        (3, u"ERBA- Via Battisti", 45.5855555, 9.930278),
        (3, u"FERNO", 45.5855555, 9.930278),
        (3, u"FERRERA ERBOGNONE - Eni", 45.5855555, 9.930278),
        (3, u"FILAGO", 45.5855555, 9.930278),
        (3, u"GALLARATE S.LORENZO", 45.5855555, 9.930278),
        (3, u"GAMBARA", 45.5855555, 9.930278),
        (3, u"LACCHIARELLA", 45.5855555, 9.930278),
        (3, u"LALLIO", 45.5855555, 9.930278),
        (3, u"LECCO VIA AMENDOLA", 45.5855555, 9.930278),
        (3, u"LECCO VIA SORA", 45.5855555, 9.930278),
        (3, u"LEGNANO S.MAGNO", 45.5855555, 9.930278),
        (3, u"LIMITO", 45.5855555, 9.930278),
        (3, u"LODI", 45.5855555, 9.930278),
        (3, u"LODI S.ALBERTO", 45.5855555, 9.930278),
        (3, u"LONATO", 45.5855555, 9.930278),
        (3, u"MAGENTA VF", 45.5855555, 9.930278),
        (3, u"MANTOVA - LUNETTA", 45.5855555, 9.930278),
        (3, u"MANTOVA - TRIDOLINO", 45.5855555, 9.930278),
        (3, u"MANTOVA - VIA ARIOSTO", 45.5855555, 9.930278),
        (3, u"MANTOVA GRAMSCI", 45.5855555, 9.930278),
        (3, u"MANTOVA SANT'AGNESE", 45.5855555, 9.930278),
        (3, u"MARMIROLO - BOSCO FONTANA", 45.5855555, 9.930278),
        (3, u"MEDA", 45.5855555, 9.930278),
        (3, u"MERATE", 45.5855555, 9.930278),
        (3, u"MILANO - JUVARA", 45.5855555, 9.930278),
        (3, u"MILANO - P.CO LAMBRO", 45.5855555, 9.930278),
        (3, u"MILANO - SENATO", 45.5855555, 9.930278),
        (3, u"MILANO - V.LE MARCHE", 45.5855555, 9.930278),
        (3, u"MILANO - VERZIERE", 45.5855555, 9.930278),
        (3, u"MILANO - VIA MESSINA", 45.5855555, 9.930278),
        (3, u"MILANO VIA PASCAL", 45.5855555, 9.930278),
        (3, u"MILANO VIA ZAVATTARI", 45.5855555, 9.930278),
        (3, u"MOGGIO", 45.5855555, 9.930278),
        (3, u"MONTANASO", 45.5855555, 9.930278),
        (3, u"MONZA", 45.5855555, 9.930278),
        (3, u"MONZA via MACHIAVELLI", 45.5855555, 9.930278),
        (3, u"MONZAMBANO", 45.5855555, 9.930278),
        (3, u"MORBEGNO2", 45.5855555, 9.930278),
        (3, u"MOTTA VISCONTI", 45.5855555, 9.930278),
        (3, u"Mortara", 45.5855555, 9.930278),
        (3, u"ODOLO", 45.5855555, 9.930278),
        (3, u"OLGIATE COMASCO", 45.5855555, 9.930278),
        (3, u"OSIO SOTTO", 45.5855555, 9.930278),
        (3, u"OSPITALETTO", 45.5855555, 9.930278),
        (3, u"OSTIGLIA S.G.", 45.5855555, 9.930278),
        (3, u"PARONA", 45.5855555, 9.930278),
        (3, u"PAVIA - P.ZZA MINERVA", 45.5855555, 9.930278),
        (3, u"PAVIA - VIA FOLPERTI", 45.5855555, 9.930278),
        (3, u"PERO", 45.5855555, 9.930278),
        (3, u"PORTO MANTOVANO", 45.5855555, 9.930278),
        (3, u"REZZATO", 45.5855555, 9.930278),
        (3, u"RIVOLTA D'ADDA", 45.5855555, 9.930278),
        (3, u"S.GIORGIO", 45.5855555, 9.930278),
        (3, u"S.NAZZARO", 45.5855555, 9.930278),
        (3, u"SAN ROCCO AL PORTO", 45.5855555, 9.930278),
        (3, u"SAREZZO - VIA MINELLI", 45.5855555, 9.930278),
        (3, u"SARONNO - SANTUARIO", 45.5855555, 9.930278),
        (3, u"SCHIVENOGLIA", 45.5855555, 9.930278),
        (3, u"SERIATE", 45.5855555, 9.930278),
        (3, u"SERMIDE TOGLIATTI", 45.5855555, 9.930278),
        (3, u"SOMMA LOMBARDO - MXP", 45.5855555, 9.930278),
        (3, u"SONDRIO - VIA MERIZZI", 45.5855555, 9.930278),
        (3, u"SONDRIO PARIBELLI", 45.5855555, 9.930278),
        (3, u"SORESINA", 45.5855555, 9.930278),
        (3, u"TAVAZZANO", 45.5855555, 9.930278),
        (3, u"TREVIGLIO", 45.5855555, 9.930278),
        (3, u"TREZZO D'ADDA", 45.5855555, 9.930278),
        (3, u"TURANO", 45.5855555, 9.930278),
        (3, u"TURBIGO", 45.5855555, 9.930278),
        (3, u"VALMADRERA", 45.5855555, 9.930278),
        (3, u"VARENNA", 45.5855555, 9.930278),
        (3, u"VARESE - VIA COPELLI", 45.5855555, 9.930278),
        (3, u"VARESE - VIA VIDOLETTI", 45.5855555, 9.930278),
        (3, u"VIA TURATI", 45.5855555, 9.930278),
        (3, u"VIGEVANO", 45.5855555, 9.930278),
        (3, u"VIMERCATE", 45.5855555, 9.930278),
        (3, u"VOGHERA - VIA POZZONI", 45.5855555, 9.930278),
    ]

    # case insensitive find
    def _find_tuple(self, ident):

        if isinstance(ident, unicode) or \
                isinstance(ident, str):
            ident = ident.lower()

        for (regcode, name, latitude, longitude) in self.stations:
            if ident in (name.lower(), ):
                return (regcode, name, latitude, longitude)

        raise KeyError(
            "'%s' is not a registered sampling station" % ident)

    def get_regcode(self, ident):

        (regcode, _, _, _) = self._find_tuple(ident)
        return regcode

    def get_name(self, ident):

        (_, name, _, _) = self._find_tuple(ident)
        return name

    def get_latitude(self, ident):
        (_, _, latitude, _) = self._find_tuple(ident)
        return latitude

    def get_longitude(self, ident):
        (_, _, _, longitude) = self._find_tuple(ident)
        return longitude

    def __contains__(self, ident):
        try:
            (_, _, _, _) = self._find_tuple(ident)
            return True

        except:
            pass

        return False

    def all(self):
        return self.stations



stations_dict = StationsDictionary()
