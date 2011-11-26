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

  --year=<year>, determines the starting and ending year for the
  analysis (e.g. 2003). If not specified the earliest year for which
  data is available is picked. (currently this is 2002). This is
  equivalent to --from=<year> --to=<year>.

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

# Time services
from time import time
start = time()

# Zip archives management
import zipfile
import shutil

# custom modules
from brace.opts import opts_mgr
from brace.ontology import pollutants_dict
from brace.ontology import regions_dict
from brace.network import download, query
from brace.csvio import UnicodeReader
from brace.data import DataRow, DataManager
from brace.out.dspl import DsplDumper

# logging
import logging
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger("brace")
logger.setLevel(logging.INFO)

# Temporary storage prefix
TMP_DIR = "tmp/"

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


# main body
if __name__ == "__main__":

    data_mgr = DataManager()

    # Phase 1. Fetch data
    total_rows = 0
    for pollutant_code in opts_mgr.pollutants:
        pollutant_formula = pollutants_dict.get_formula(pollutant_code)
        pollutant_name = pollutants_dict.get_name(pollutant_code)

        for region_code in opts_mgr.regions:
            region_name = regions_dict.get_name(region_code)

            for year in range(opts_mgr.from_year,
                              1 + opts_mgr.to_year):
                logger.info(
                    "Trying to fetch data for year %d, pollutant '%s' (%s), region '%s'",
                    year, pollutant_formula, pollutant_name, region_name)

                archive = query(region_code, pollutant_code, year)
                try:
                    zf = zipfile.ZipFile(archive)
                    for entry in zf.namelist():

                        logger.info("Extracting '%s' ...", entry)
                        zf.extract(entry, TMP_DIR)

                        i = 0
                        fullpath = os.path.join(TMP_DIR, entry)

                        # data appears to be encoded using iso-8859-1,
                        # it needs to be recoded to UTF-8.
                        for row in UnicodeReader(open(fullpath),
                                                 encoding="iso-8859-1"):

                            data = {
                                'region': region_name,
                                'station': row[0],
                                'pollutant': row[1] or pollutant_formula,
                                'timestamp': row[2],
                                'quantity': row[3]
                                }

                            data_mgr.append(**data)

                            logger.debug("-- " + unicode(row))

                            i += 1; total_rows += 1

                        logger.info("Processed %d rows", i)

                except Exception, e:  # TODO which expception
                    logger.warning("Data unavailable.")
                    
                archive.close()

        # disk cleanup
        if (os.path.exists(TMP_DIR)):
            shutil.rmtree(TMP_DIR, True)  # TODO add something for errors

    # Phase 2. Dump output
    dumper = DsplDumper(data_mgr, "braces.xml")
    dumper()

    # Phase 3. Show run stats
    logger.info("Processed %d rows in %s", total_rows, "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:], [(time() - start, ), 1, 60, 60]))
    
    
