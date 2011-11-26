"""Command line getopt-like options management
"""
# Options handling
import getopt


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
