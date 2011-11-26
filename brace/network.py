# -*- coding: utf-8 -*-
"""Network I/O services
"""
# Logging support
import logging
logger = logging.getLogger(__name__)

# Temporary files support
import tempfile

# Network I/O services
import urllib

# HTML parsing
from BeautifulSoup import BeautifulSoup

# The URL of the website that provides pollutants data
URL_PREFIX = "http://www.brace.sinanet.apat.it/zipper"

# Custom modules
from brace.ontology import regions_dict
from brace.ontology import pollutants_dict

# Maximum number of attempts to download a single file
DOWNLOAD_MAX_RETRIES = 6

# Delay between retries
DOWNLOAD_DELAY_TIME_BETWEEN_ATTEMPTS = 10

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

            # dumping to temp file
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

    # calculate size of the downloaded file, rewind it
    size = res.tell()
    res.seek(0)
    logger.info("Downloaded %d bytes.", size)

    return res


def query(region, pollutant, year):
    """
    """
    region_code = regions_dict.get_pk(region)
    region_name = regions_dict.get_name(region)

    pollutant_code = pollutants_dict.get_pk(pollutant)
    pollutant_formula = pollutants_dict.get_formula(pollutant)
    pollutant_name = pollutants_dict.get_name(pollutant)

    name = '%sdownload/%s_%s_%s.zip' % (
        URL_PREFIX,
        region_name.upper(),
        pollutant_formula.upper(),
        year,
    )

    query = urllib.urlencode({
            'p_comp': pollutant_code,
            'p_comp_name': pollutant_formula.upper(),
            'p_reg': region_code,
            'p_reg_name': region_name.upper(),
            'p_anno': year,
    })

    genfile = "%(prefix)s/servlet/zipper?%(query)s" % {
        'prefix': URL_PREFIX,
        'query': query,
    }

    link = download(genfile)
    if link is None:
        raise IOError("Could not fetch '%s'." % genfile)
    
    soup = BeautifulSoup(link)

    location = \
        soup.find('script').contents[0].split('"')[1].\
        replace("../download/", "")
    
    link.close()

    archive = download(
        "%(prefix)s/download/%(location)s" % {
            'prefix': URL_PREFIX,
            'location': location })

    if archive is None:
        raise IOError("Could not fetch '%s'." % genfile)

    return archive

