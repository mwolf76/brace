A tool for surveying air quality in italian cities
==================================================

Phase 1 of the process consists in fetching raw data, available to the
public on ISPRA (Superior Institute for the Environmental Protection
and Research). To perform this task a command-line tool, called "brace"
(italian for "embers") has been realized.

The tool source code, which is released under GPL, is hosted on the Social Coding
platform GitHub at this address:

https://github.com/mwolf76/brace

Anybody can analyze, modify and republish the source code, in order to meet
her needs or anybody else's.

The tool is fully documented, one can read the inline documentation invoking the
program with --help option. Typing the following message at the command line prompt:

$ brace.py --help

The following message will be shown:
--------------------------------------------------------------------------------
brace.py - a tool for public data knowledge sharing.

usage:

    brace.py [ --from=<from_year> ][ --to=<to_year> ]
             --region=<region> --pollutant=<formula>
             [ --help ] [ --verbosity=<level> ]
             filename

options:

  --from=<from_year>, determines the starting year for the analysis
  (e.g. 2003). If not specified the earliest year for which data is
  available is picked. (currently this is 2002).

  --to=<to_year>, determines the ending year for the analysis
  (e.g. 2003). If not specified the latest year for which data is
  available is picked. (currently this is 2009).

  --region=<region>, (case-insensitive) determines which localized
  data set is to be processed. This is a mandatory argument.  If not
  specified, the list of italian regions is displayed. If specified
  more than once, output is produced for all of the given regions.

  --pollutant=<formula>, (case-insensitive) determines which pollutant
  data set is to be processed. This is a mandatory argument. If not
  specified, the list of known pollutants is displayed. If specified
  more than once, output is produced for all of the given pollutants.

  --help, prints this message.

  --verbosity=<level>, adjusts the level of verbosity of the
  tool. This is a number between 0(quiet) and 3(extremely
  verbose). This is manly for debugging purposes.

arguments:

  filename, the filename to write the output to.
--------------------------------------------------------------------------------

This message lists all the available options currenlty supported by
the tool. This sections shows a few example runs, along with a short
explanation of the options and paramters used.

$ brace.py

Fetches the *entire* dataset, from year 2002 to year 2009, regarding all the pollutants, in every
italian region. This takes quite a while to execute.


$ brace.py --pollutant=C6H6

Fetches the dataset, from year 2002 to year 2009, regarding only C6H6
(Benzene), in every italian region.


$ brace.py --pollutant=NO2 --pollutant=NO --pollutant=SO2 --region=lombardia --region=piemonte

Fetches the dataset, from year 2002 to year 2009, regarding NO2
(Nitrogen Dioxide), NO (Nitrogen Oxide) and SO2 (Sulphur Dioxide), in
Lombardia and Piemonte.


$ brace.py --pollutant=NO2 --pollutant=NO --pollutant=SO2 --region=lombardia --region=piemonte --year=2009

Fetches the dataset for year 2009, regarding NO2 (Nitrogen Dioxide),
NO (Nitrogen Oxide) and SO2 (Sulphur Dioxide), in Lombardia and
Piemonte.


$ brace.py --region=toscana --from 2005

Fetches the dataset from year 2005, regarding all the pollutants in
Toscana.

Uploading data on Google Public Data Explorer
=============================================

Once the data processing phase has been completed you are now ready to
upload you datasets on the Google Public Data Explorer service, this
requires a Google account, if you don't have one you can obtain a new
account here: https://accounts.google.com/Login.

Once logged into you google account,open the browser at this address:
http://www.google.com/publicdata/home

Click on "My Datasets" and then on the "Upload Dataset" button. When asked to provide the Dataset
click on "Choose File", then browser you hard-drive and locate the newly created zip archive.

After submission, the dataset is automatically checked by Google. 





