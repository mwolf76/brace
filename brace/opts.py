# -*- coding: utf-8 -*-
"""Command line getopt-like options management
"""

# System services
import sys

# Logging support
import logging
logger = logging.getLogger("brace")

# Options handling
import getopt

# custom modules
from brace.ontology import pollutants_dict
from brace.ontology import regions_dict

DEFAULT_FROM_YEAR = 2002
DEFAULT_TO_YEAR = 2009

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
  analysis (e.g. 2003). This is equivalent to --from=<year>
  --to=<year>.

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

  Here follows the complete list of italian regions:

  %(regions)s

  --pollutant=<formula>, (case-insensitive) determines which pollutant
  data set is to be processed. If specified more than once, output is
  produced for all of the given pollutants. If no pollutant is given,
  all of them will be taken into account.

  Here follows the complete list of known pollutants: 

  %(pollutants)s

  --help, prints this message.

  --verbosity=<level>, adjusts the level of verbosity of the
  tool. This is a number between 0(quiet) and 3(extremely
  verbose). This is manly for debugging purposes.

  --format=<format>, determines the output format for the dataset.
  Currently the tool supports only DSPL (Dataset publishing Language).

arguments:

  filename, the filename to write the output to.
""" % {
    'regions': "\n  ".join ([regions_dict.get_name(r[0]) 
                             for r in regions_dict.all()]),

    'pollutants': "\n  ".join ([ "%(formula)s (%(name)s)" % {
            'formula': pollutants_dict.get_formula(p[0]),
            'name': pollutants_dict.get_name(p[0]),
            } for p in pollutants_dict.all() ]),
}


class OptionsManager(object):
    """Provides options management.
    """

    long_options = [
        "help",
        "keep",
        "verbosity=",
        "from=",
        "to=",
        "year=",
        "pollutant=",
        "region=",
    ]

    def __init__(self):
        self.from_year = DEFAULT_FROM_YEAR
        self.to_year = DEFAULT_TO_YEAR
        self.verbosity = 1  # Normal
        self.keep = False

        self.regions = []
        self.pollutants = []

    def __call__(self, args):

        opts, args = getopt.getopt(args, "",
                                   self.long_options)

        for o, a in opts:

            if o == "--year":
                year = int(a)
                if year < DEFAULT_FROM_YEAR:
                    raise getopt.GetoptError(
                        "No data available before %d" % DEFAULT_FROM_YEAR)

                self.from_year = year
                logger.debug("Setting starting year to %d", year)

                self.to_year = year
                logger.debug("Setting ending year to %d", year)

            elif o == "--from":
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

            elif o == "--keep":
                self.keep = True

            elif o == "--help":
                print usage
                sys.exit()

            else:
                assert False, "unhandled option"


opts_mgr = OptionsManager()
