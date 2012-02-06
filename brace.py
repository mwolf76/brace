#!/usr/bin/env python
# -*- coding: utf-8 -*-

# brace.py is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# TODO:
# better abstraction
# output by plugins
# code cleanup
# ... more ...

__author__ = "Marco Pensallorto"
__copyright__ = "Copyright 2011-2012, The Brace Project"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Marco Pensallorto"
__email__ = "marco.pensallorto@gmail.com"
__status__ = "Development"

# Basic services and utilities
import os
import sys

# Time services
from time import time
start = time()

# Zip archives management
import zipfile
import shutil

# opts handling
from brace.opts import opts_mgr

# ontology
from brace.ontology import pollutants_dict
from brace.ontology import regions_dict
from brace.ontology import stations_dict

# core modules
from brace.network import download, query
from brace.csvio import UnicodeReader
from brace.data import DataRow, DataManager

# output module
from brace.out.dspl import DsplDumper

# logging, (set BRACE_DEBUG from the calling env to activate extra logging)
import logging
DEBUG_MODE = os.environ.get("BRACE_DEBUG", False) and True  # a boolean cast
FORMAT = not DEBUG_MODE and '-- %(message)s' or \
         "%(asctime)-15s [%(module)s.%(funcName)s:%(lineno)d] - %(message)s"

logging.basicConfig(format=FORMAT)

logger = logging.getLogger("brace")
logger.setLevel(logging.INFO)

# Temporary storage prefix
TMP_DIR = "tmp/"
OUT_DIR = "out/"

try:
    opts_mgr(sys.argv[1:])

except Exception, e:
    print (e)
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

                if not opts_mgr.local:
                    # fetch remote archive
                    logger.info(
                        "Trying to fetch data for year %d, pollutant '%s' (%s), "
                        "region '%s'", year, pollutant_formula, pollutant_name,
                        region_name)
                    archive = query(region_code, pollutant_code, year)

                else:
                    # use local archive
                    logger.info(
                        "Using local data for year %d, pollutant '%s' (%s), "
                        "region '%s'", year, pollutant_formula, pollutant_name,
                        region_name)
                    backup_name = '%s_%s_%s.zip' % (
                        region_code, pollutant_code, year)
                    archive = open(backup_name, "rt")

                # copy it to local resource for later use
                if (opts_mgr.keep):
                    backup_name = '%s_%s_%s.zip' % (
                        region_code, pollutant_code, year)

                    bf = open(backup_name, "wt")
                    shutil.copyfileobj(archive, bf)
                    bf.close()

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

                            assert row[1] == pollutant_formula

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

                except Exception, e:
                    logger.warning("Data unavailable [reason: %s]." % str(e))

                archive.close()  # temp file will be removed automatically

        # disk cleanup
        if (os.path.exists(TMP_DIR)):
            shutil.rmtree(TMP_DIR, True)  # TODO add something for errors

    # Phase 2. Dump output
    logger.info("Dumping output files...")
    dumper = DsplDumper(data_mgr, "out.zip" )

    # try:
    #     dumper()
    #     logger.info("Execution completed successfully.")

    # except Exception, e:
    #     logger.warning("An error has occurred during dumping [%s].\n"
    #                    "Output may be incomplete or missing.", str(e))
    dumper()  # avoid exception suppresion for development (pdb)

    # Phase 3. Show run stats
    logger.info(
        "Processed %d rows in %s", total_rows, "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
               [(time() - start, ), 1, 60, 60]))
