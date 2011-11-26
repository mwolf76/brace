"""Network I/O services
"""

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


