#!/usr/bin/env python
# -*- coding: utf-8 -*-

# brace.py is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# TODO:
# cleanup of download files
# better scaling (use named tuples?)
# refactoring in several modules
# better abstraction
# ... more ...

__author__ = "Marco Pensallorto, Davide Setti"
__copyright__ = "Copyright 2011, The Brace Project"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Marco Pensallorto"
__email__ = "marco.pensallorto@gmail.com"
__status__ = "Development"

usage = """
brace.py - a tool for public data knowledge sharing.

usage:

    brace.py [ --from=<from_year> ]
             [ --to=<to_year> ]
             [ --region=<region_1>  [--region=<region_2> ... ] ]
             [ --pollutant=<formula_1> [--pollutant=<formula_2> ... ] ]
             [ --verbosity=<level> ] [ --help ]
             [ --format<format> ]
             filename

options:

  --from=<from_year>, determines the starting year for the analysis
  (e.g. 2003). If not specified the earliest year for which data is
  available is picked. (currently this is 2002).

  --to=<to_year>, determines the ending year for the analysis
  (e.g. 2003). If not specified the latest year for which data is
  available is picked. (currently this is 2009).

  --region=<region>, (case-insensitive) determines which localized
  data set is to be processed. If specified more than once, output is
  produced for all of the given region. If no region is given, all of
  them will be taken into account.

  --pollutant=<formula>, (case-insensitive) determines which pollutant
  data set is to be processed. If specified more than once, output is
  produced for all of the given pollutants. If no pollutant is given,
  all of them will be taken into account.

  --help, prints this message.

  --verbosity=<level>, adjusts the level of verbosity of the
  tool. This is a number between 0(quiet) and 3(extremely
  verbose). This is manly for debugging purposes.

  --format=<format>, determines the output format for the dataset.
  Currently the tool supports only DSPL (Dataset publishing Language).

arguments:

  filename, the filename to write the output to.
"""

# Basic services and utilities
import os
import sys
import csv
import time

# Options handling
import getopt

# Zip archives management
import zipfile

# Temporary files support
import tempfile

# Network I/O services
import urllib

# localization services
from gettext import gettext as _

# logging
import logging
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# HTML parsing
from BeautifulSoup import BeautifulSoup

# The URL of the website that provides pollutants data
URL_PREFIX = "http://www.brace.sinanet.apat.it/zipper/"

DEFAULT_FROM_YEAR = 2002
DEFAULT_TO_YEAR = 2009

# Maximum number of attempts to download a single file
DOWNLOAD_MAX_RETRIES = 6
DOWNLOAD_DELAY_TIME_BETWEEN_ATTEMPTS = 10

# global data var
samples = []

import csv
import codecs
import cStringIO


# unicode-related csv helper classes (from Python 2.7 docs)
class UTF8Recoder:
    """Iterator that reads an encoded stream and reencodes the input to UTF-8.
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter:
    """A CSV writer which will write rows to CSV file "f", which is
    encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


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


class OptionsHandler(object):
    """Provides options management.
    """

    long_options = [
        "help",
        "verbosity=",
        "from=",
        "to=",
        "pollutant=",
        "region=",
    ]

    def __init__(self):
        self.from_year = DEFAULT_FROM_YEAR
        self.to_year = DEFAULT_TO_YEAR
        self.verbosity = 1  # Normal

        self.regions = []
        self.pollutants = []

    def __call__(self, args):

        opts, args = getopt.getopt(args, "",
                                   self.long_options)

        for o, a in opts:

            if o == "--from":
                from_year = int(a)
                if from_year < DEFAULT_FROM_YEAR:
                    raise getopt.GetoptError(
                        "No data available before %d" % DEFAULT_FROM_YEAR)

                self.from_year = from_year
                logger.debug("Setting starting year to %d", from_year)

            elif o == "--to":
                to_year = int(a)
                if DEFAULT_TO_YEAR < to_year:
                    raise getopt.GetoptError(
                        "No data available after %d" % DEFAULT_TO_YEAR)

                self.to_year = to_year
                logger.debug("Setting ending year to %d", to_year)

            elif o == "--region":
                region_name = regions_dict.get_name(a)
                region_code = regions_dict.get_pk(a)

                self.regions.append(region_code)
                logger.debug("Adding region '%s'", region_name)

            elif o == '--pollutant':
                pollutant_formula = pollutants_dict.get_formula(a)
                pollutant_name = pollutants_dict.get_name(a)
                pollutant_code = pollutants_dict.get_pk(a)

                self.pollutants.append(pollutant_code)
                logger.debug("Adding pollutant '%s' (%s)",
                             pollutant_formula, pollutant_name)

            elif o == "--verbosity":
                level = int(a)
                self.verbosity = level

                if level == 0:
                    logger.setLevel(logging.ERROR)
                elif level == 1:
                    logger.setLevel(logging.WARNING)
                elif level == 2:
                    logger.setLevel(logging.INFO)
                elif level == 3:
                    logger.setLevel(logging.DEBUG)

                else:
                    assert False, "Unsupported verbosity level"

                logger.debug("Setting verbosity level to %s",
                             ["ERROR", "WARNING", "INFO", "DEBUG"][level])

            elif o == "--help":
                print usage
                sys.exit()

            else:
                assert False, "unhandled option"


opts_mgr = OptionsHandler()
try:
    opts_mgr(sys.argv[1:])

except Exception, e:
    print str(e)
    print usage
    sys.exit(-1)

# hackish :-/
if not opts_mgr.pollutants:
    opts_mgr.pollutants = [
        p[0] for p in pollutants_dict.all()]
if not opts_mgr.regions:
    opts_mgr.regions = [
        r[0] for r in regions_dict.all()]


def download(url, max_retries=DOWNLOAD_MAX_RETRIES,
             delay=DOWNLOAD_DELAY_TIME_BETWEEN_ATTEMPTS):
    """Download a remote url to a newly created temporary file.
    The file will be destroyed when the object is closed.
    """
    res = None

    # try downloading file up to a given number of attempts
    (attempts, success) = (0, False)
    while (not success and attempts < max_retries):

        attempts += 1

        try:
            logger.debug("Downloading url '%s', attempt %d",
                         url, attempts)

            urlfile = urllib.urlopen(url)
            if urlfile is None:
                raise Exception(
                    "Could not access to remote url '%s'" % url)

            res = tempfile.TemporaryFile()

            while True:
                packet = urlfile.read()
                if not packet:
                    break

                res.write(packet)

            urlfile.close()
            success = True

        except IOError, ioe:
            logger.warning(str(ioe))
            time.sleep(delay)  # wait before next attempt

    return res


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


# TODO: following code is *very* raw
def build_dspl_pollutant_concept_xml(pollutant):
    """Builds the xml node for a specific pollutant
    """
    return """<concept id="%(id)s">
      <info>
        <name>
          <value>%(name)s</value>
        </name>
      </info>
      <type ref="float"/>
      <table ref="%(id)s_table" />
    </concept>
    """ % {
        'id': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
    }


def build_dspl_regions_concept_xml():
    """Builds the xml node for a specific city in Italy
    """

    return """<concept id="region" extends="geo:location">
      <info>
        <name><value>Regions</value></name>
        <description>
          <value>Italian regions</value>
        </description>
      </info>
      <type ref="string"/>
      <property id="name">
        <info>
          <name><value>Name</value></name>
          <description>
            <value>The official name of the region</value>
          </description>
        </info>
        <type ref="string" />
      </property>
      <table ref="regions_table" />
    </concept>"""


def build_dspl_regions_table_xml():
    """ Builds the dspl italian regions table
    """

    return """<table id="regions_table">
        <column id="region" type="string"/>
        <column id="latitude" type="float"/>
        <column id="longitude" type="float"/>
        <data>
            <file format="csv" encoding="utf-8">regions.csv</file>
        </data>
        </table>"""


def build_dspl_pollutant_table_xml(pollutant):
    """Builds the dspl pollutant table for a given pollutant.
    """

    return """
<table id="%(id)s_table">
    <column id="station" type="string"/>
    <column id="timestamp" type="timestamp"/>
    <column id="quantity" type="float"/>
    <data><file format="csv" encoding="utf-8">%(id)s.csv</file></data>
</table>""" % {
        'id': pollutants_dict.get_formula(pollutant),
    }


def build_dspl_tables_xml():
    """
    """

    return \
        build_dspl_regions_table_xml() + \
        "\n" + \
        "\n".join(map(build_dspl_pollutant_table_xml, opts_mgr.pollutants))


def build_dspl_concepts_xml():
    """Builds the dspl ontology for pollutants.
    """
    return \
        "\n".join(map(build_dspl_pollutant_concept_xml,
                      opts_mgr.pollutants)) + \
        "\n" + \
        build_dspl_regions_concept_xml()

def build_dspl_xml():
    """Builds the dspl file.
    """

    return """<?xml version="1.0" encoding="UTF-8"?>
<dspl targetNamespace="https://www.github.org/mwolf76/brace"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns="http://schemas.google.com/dspl/2010"
   xmlns:time="http://www.google.com/publicdata/dataset/google/time"
   xmlns:geo="http://www.google.com/publicdata/dataset/google/geo"
   xmlns:entity="http://www.google.com/publicdata/dataset/google/entity"
   xmlns:quantity="http://www.google.com/publicdata/dataset/google/quantity">

  <import namespace="http://www.google.com/publicdata/dataset/google/time"/>
  <import namespace="http://www.google.com/publicdata/dataset/google/entity"/>
  <import namespace="http://www.google.com/publicdata/dataset/google/geo"/>
  <import namespace="http://www.google.com/publicdata/dataset/google/quantity"/>

  <info>
    <name>
      <value>Air quality in Italian cities</value>
    </name>
    <description>
      <value>Pollutants measurements in metropolitan areas in Italy</value>
    </description>
    <url>
      <value>https://www.github.org/mwolf76/brace</value>
    </url>
    </info>

  <provider>
    <name>
      <value>BRACE database</value>
    </name>
    <url>
      <value>http://www.brace.sinanet.apat.it/web/struttura.html</value>
    </url>
  </provider>

  <concepts>
  %(concepts)s
  </concepts>

  <tables>
  %(tables)s
  </tables>

</dspl>
""" % {
        'concepts':  build_dspl_concepts_xml(),
        'tables': build_dspl_tables_xml(),
}


# main body
if __name__ == "__main__":

    for year in range(opts_mgr.from_year,
                      1 + opts_mgr.to_year):

        for pollutant_code in opts_mgr.pollutants:

            pollutant_formula = pollutants_dict.get_formula(pollutant_code)
            pollutant_name = pollutants_dict.get_name(pollutant_code)

            for region_code in opts_mgr.regions:

                region_name = regions_dict.get_name(region_code)

                logger.info(
                    "Processing year %d, pollutant '%s' (%s), region '%s'",
                    year, pollutant_formula, pollutant_name, region_name)

                name = '%sdownload/%s_%s_%s.zip' % (
                    URL_PREFIX,
                    region_name.upper(),
                    pollutant_formula.upper(),
                    year
                )

                query = urllib.urlencode({
                    'p_comp': pollutant_code,
                    'p_comp_name': pollutant_formula.upper(),
                    'p_reg': region_code,
                    'p_reg_name': region_name.upper(),
                    'p_anno': year,
                })

                genfile = "%(prefix)sservlet/zipper?%(query)s" % {
                    'prefix': URL_PREFIX,
                    'query': query,
                }

                link = download(genfile)
                if link is None:
                    logger.warning("Could not fetch '%s'. Skipping...", genfile)
                    continue  # failed to download

                link.seek(0)
                soup = BeautifulSoup(link)

                location = \
                    soup.find('script').contents[0].split('"')[1].\
                    replace("../download/", "")

                link.close()

                archive = download(
                    "%(prefix)sdownload/%(location)s" % {
                        'prefix': URL_PREFIX,
                        'location': location})

                if archive is None:
                    logger.warning("Could not fetch '%s'. Skipping...", location)
                    continue  # failed to download

                # calculate size of the downloaded file, rewind it
                size = archive.tell()
                archive.seek(0)

                logger.info("Downloaded %d bytes.", size)

                if size:
                    zf = zipfile.ZipFile(archive)
                    for entry in zf.namelist():

                        logger.info("Extracting '%s' ...", entry)
                        zf.extract(entry)

                        i = 0

                        # data appears to be encoded using iso-8859-1,
                        # it needs to be recoded to UTF-8.
                        for row in UnicodeReader(open(entry),
                                                 encoding="iso-8859-1"):

                            data = {
                                'region': region_name,
                                'station': row[0],
                                'pollutant': row[1] or pollutant_formula,
                                'timestamp': row[2],
                                'quantity': row[3]
                                }

                            row = DataRow(**data)
                            samples.append(row)
                            logger.debug("-- " + unicode(row))

                            i += 1

                        logger.info("Processed %d rows", i)
                        os.remove(entry)

                    archive.close()

                else:
                    logger.warning("Data unavailable.")

    # write output to file
    logger.debug("Dumping xml file")
    xml = open("brace.xml", "wt")
    xml.write(build_dspl_xml(), encoding='utf-8')
    xml.close()

    # write regions csv file
    logger.debug("Dumping regions csv")
    regcsv = open("regions.csv", "wt")
    for r in opts_mgr.regions:
        entry = "%(region)s, %(longitude)s, %(latitude)s\n" % {
            'region': regions_dict.get_name(r),
            'longitude': regions_dict.get_longitude(r),
            'latitude': regions_dict.get_latitude(r),
        }
        regcsv.write(entry, encoding='utf-8')

    regcsv.close()

    # write pollutants csv files
    for pollutant in opts_mgr.pollutants:

        formula = pollutants_dict.get_formula(pollutant)
        logger.debug("Dumping csv for %s", formula)

        polcsv = open("%s.csv" % formula, "wt")
        for row in samples:
            if row.pollutant_formula == formula:
                polcsv.write(unicode(row) + "\n", encoding='utf-8')
        polcsv.close()
