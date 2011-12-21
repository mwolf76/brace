# -*- coding: utf-8 -*-
"""DSPL (Dataset Publishing Language) output services
"""

# os services
import os

# time services
import time
import datetime

# Temporary files support
import tempfile

# Logging support
import logging
logger = logging.getLogger("brace")

# custom modules
from brace.opts import opts_mgr

from brace.ontology import pollutants_dict
from brace.ontology import regions_dict
from brace.ontology import stations_dict

# zipfile
import zipfile
import shutil

# TODO: this code is *very* raw, at some point in time this should use
# some decent templating engine (e.g. Genshi)


# -- concepts
def build_dspl_aggregates_concept_xml():
    """
    """
    return """<concept id="aggregate" extends="entity:entity">
  <info>
    <name>
      <value>Aggregation</value>
    </name>
    <description>
      <value>Max or Avg</value>
    </description>
  </info>
  <type ref="string"/>
  <table ref="aggregates_table"/>
</concept>
"""


def build_dspl_regions_concept_xml():
    """Builds the xml node for a specific city in Italy
    """

    return """<!-- Concept for regions (geo). -->
<concept id="region" extends="geo:location">
      <info>
        <name>
            <value>Regions</value>
        </name>
        <description>
            <value>Italian regions</value>
        </description>
      </info>
      <type ref="string"/>
      <property id="name">
          <info>
              <name>
                  <value>Name</value>
              </name>
              <description>
                  <value>The official name of the region</value>
              </description>
          </info>
          <type ref="string" />
      </property>
      <table ref="regions_table" />
</concept>
"""


def build_dspl_stations_concept_xml():
    """Builds the xml node for a specific city in Italy
    """

    return """<!-- Concept for stations (geo) -->
<concept id="station" extends="geo:location">
      <info>
          <name>
              <value>Station</value>
          </name>
          <description>
              <value>Pollution sampling station</value>
          </description>
      </info>
      <property concept="region" isParent="true" />
      <table ref="stations_table" />
 </concept>
"""


def build_dspl_pollutant_concept_xml(pollutant):
    """Builds the xml node for a specific pollutant
    """
    return """<!-- Concept for %(id)s %(name)s. -->
<concept id="%(id)s">
    <info>
        <name>
            <value>%(name)s</value>
        </name>
    </info>
    <type ref="float" />
</concept>
""" % {
        'id': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
}


# -- tables
def build_dspl_aggregates_table_xml():
    """
    """
    return """<!-- Table for aggregate types. -->
<table id="aggregates_table">
    <column id="aggregate" type="string"/>
    <column id="description" type="string"/>
    <data>
        <file format="csv" encoding="utf-8">aggregates.csv</file>
    </data>
</table>
"""


def build_dspl_regions_table_xml():
    """ Builds the dspl italian regions table
    """

    return """<!-- Table for regions. -->
<table id="regions_table">
    <column id="region" type="string"/>
    <column id="latitude" type="float"/>
    <column id="longitude" type="float"/>
    <data>
        <file format="csv" encoding="utf-8">regions.csv</file>
    </data>
</table>
"""


def build_dspl_stations_table_xml():
    """ Builds the dspl stations table
    """

    return """<!-- Table for stations. -->
<table id="stations_table">
    <column id="station" type="string"/>
    <column id="region" type="string" />
    <column id="latitude" type="float"/>
    <column id="longitude" type="float"/>
    <data>
        <file format="csv" encoding="utf-8">stations.csv</file>
    </data>
</table>
"""


def build_dspl_pollutant_slice_table_xml(pollutant):
    """Builds the dspl pollutant slice table for a given pollutant.
    """

    return """<!-- Slice table for %(formula)s (%(name)s). -->
<table id="%(formula)s_slice_table">
    <column id="region" type="string" />
    <column id="station" type="string" />
    <column id="aggregate" type="string" />
    <column id="day" type="date" format="yyyy-MM-dd" />
    <column id="%(formula)s" type="float"/>
    <data><file format="csv" encoding="utf-8">%(formula)s.csv</file></data>
</table>
""" % {
        'formula': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
}


def build_dspl_tables_xml():
    """
    """

    return \
        build_dspl_aggregates_table_xml() + \
        "\n" + \
        build_dspl_regions_table_xml() + \
        "\n" + \
        build_dspl_stations_table_xml() + \
        "\n" + \
        "\n".join(map(build_dspl_pollutant_slice_table_xml,
                      opts_mgr.pollutants))


def build_dspl_concepts_xml():
    """Builds the dspl ontology for pollutants.
    """

    return \
        "\n" + \
        build_dspl_aggregates_concept_xml() + \
        "\n" + \
        build_dspl_regions_concept_xml() + \
        "\n" + \
        build_dspl_stations_concept_xml() + \
        "\n".join(map(build_dspl_pollutant_concept_xml,
                      opts_mgr.pollutants))


def build_dspl_pollutant_slice_xml(pollutant):
    """
    """
    return """<!-- Slice for %(formula)s (%(name)s). (max) -->
<slice id="%(formula)s_slice">
    <dimension concept="region" />
    <dimension concept="station" />
    <dimension concept="aggregate" />
    <dimension concept="time:day" />
    <metric concept="%(formula)s" />
    <table ref="%(formula)s_slice_table"/>
</slice>
""" % {
        'formula': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
}

def build_dspl_slices_xml():
    """Builds the dspl slices for pollutants.
    """
    return \
        "\n".join(map(build_dspl_pollutant_slice_xml,
                      opts_mgr.pollutants))

def build_dspl_xml():
    """Builds the dspl file.
    """

    return """<?xml version="1.0" encoding="UTF-8"?>
<!-- Autogenerated on %(now)s by brace.py -->
<dspl
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

<!-- Concepts -->
<concepts>
%(concepts)s
</concepts>

<!-- Slices -->
<slices>
%(slices)s
</slices>

<!-- Tables -->
<tables>
%(tables)s
</tables>

</dspl>
""" % {
        'now': datetime.datetime.now().strftime("%a, %d %b %Y - %H:%M"),
        'concepts': build_dspl_concepts_xml(),
        'tables': build_dspl_tables_xml(),
        'slices': build_dspl_slices_xml(),
}



class DsplDumper(object):
    """(missing docs)
    """

    def __init__(self, data_mgr, out):
        self._data_mgr = data_mgr
        self._out = out
        self._tmpdir = "zip/"

    def _yield(self, formula):
        """Yields aggregate data for this output plugin.
        """
        fk = pollutants_dict.get_pk(formula)

        # initialization
        curr_reg = None
        curr_stat = None
        curr_day = None

        max_ = 0.0   # (aggregate max)
        cum_ = 0.0   # (aggregate cum sum)
        samples = 0  # (number of samples, needed for avg)

        for row in self._data_mgr.data:
            if row.pollutant == fk:
                (region, station, pollutant, timestamp, quantity) = row

                # day as a 3-tuple
                day = (timestamp.tm_year, timestamp.tm_mon, timestamp.tm_mday)

                # if dealing with another region, station or day,
                # yield result and reset the result
                if (curr_reg != region) \
                       or (curr_stat != station) \
                       or (curr_day != day):

                    if curr_reg is not None and \
                       curr_stat is not None and \
                       curr_day is not None:

                        # remeber last yield
                        (last_region, last_station, last_day) = \
                                      (region, station, day)

                        avg_ = cum_ / samples
                        yield (region, station, day, max_, avg_)

                # update
                curr_reg = region
                curr_stat = station
                curr_day = day

                # update aggregate measurement
                max_ = max(max_, quantity)
                cum_ += quantity
                samples += 1

        # yield last row if necessary
        if (region != last_region) or \
               (station != last_station) or \
               (day != last_day):

            avg_ = cum_ / samples
            yield (region, station, day, max_, avg_)

    def __call__(self):

        if '.' not in self._out:
            self._out = self._out + ".zip"

        # disk cleanup
        if (os.path.exists(self._tmpdir)):
            shutil.rmtree(self._tmpdir, True)  # TODO add something for errors
        os.mkdir(self._tmpdir)

        azip = zipfile.ZipFile(self._out, "w" )

        # write output to file
        fullpath = os.path.join(self._tmpdir, "brace.xml")
        xml = open(fullpath, "wt")
        xml.write(build_dspl_xml())
        xml.close()
        azip.write(fullpath)

        # write aggregates csv file
        fullpath = os.path.join(self._tmpdir, "aggregates.csv")
        aggrcsv = open(fullpath, "wt")
        aggrcsv.write("aggregate, description\n")
        for (id, desc) in [ ( "max", "Maximum daily concentration" ),
                            ( "avg", "Average daily concentration" ), ]:
            entry = u"%(id)s, %(description)s\n" % {
                'id': id,
                'description': desc,
            }
            aggrcsv.write(entry)
        aggrcsv.close()
        azip.write(fullpath)

        # write regions csv file
        fullpath = os.path.join(self._tmpdir, "regions.csv")
        regcsv = open(fullpath, "wt")
        regcsv.write("region, latitude, longitude\n")
        for r in opts_mgr.regions:
            entry = u"%(region)s, %(latitude)s, %(longitude)s\n" % {
                'region': regions_dict.get_name(r),
                'latitude': regions_dict.get_latitude(r),
                'longitude': regions_dict.get_longitude(r),
            }
            regcsv.write(entry)
        regcsv.close()
        azip.write(fullpath)

        # write stations csv file
        fullpath = os.path.join(self._tmpdir, "stations.csv")
        stscsv = open(fullpath, "wt")
        stscsv.write("station, region, latitude, longitude\n")
        for (regcode, name, latitude, longitude) in stations_dict.all():
            entry = u"%(station)s, %(region)s, %(latitude)s, %(longitude)s\n" % {
                'station': name,
                'region': regions_dict.get_name(regcode),
                'latitude': latitude,
                'longitude': longitude,
            }
            stscsv.write(entry)
        stscsv.close()
        azip.write(fullpath)

        # write pollutants csv files for slice tables
        # Remark: as csv file *must* be sorted according to dimensions
        # it is necessary to build two separate temp files and then
        # join them together when every row has been processed. :-/
        for pollutant in opts_mgr.pollutants:
            formula = pollutants_dict.get_formula(pollutant)

            max_file = tempfile.TemporaryFile()
            avg_file = tempfile.TemporaryFile()

            # generate aggregate data
            for (region, station, day, max_, avg_) in self._yield(formula):

                entry = u"%(region)s, %(station)s, max, %(day)s, %(qty)s\n" % {
                    'region': region,
                    'station': station,
                    'day': time.strftime("%Y-%m-%d", day +(0, ) * 6),
                    'qty': max_,
                }
                max_file.write(entry)

                entry = u"%(region)s, %(station)s, avg, %(day)s, %(qty)s\n" % {
                    'region': region,
                    'station': station,
                    'day': time.strftime("%Y-%m-%d", day +(0, ) * 6),
                    'qty': avg_,
                }
                avg_file.write(entry)

            avg_file.seek(0)


            fullpath = os.path.join(self._tmpdir, "%(formula)s.csv" % {
                'formula': formula
            })
            polcsv = open(fullpath, "wt")
            polcsv.write("region, station, aggregate, day, %(formula)s\n" % {
                'formula': formula,
            })


            # concatenate max_file and avg_file
            max_file.seek(0)
            for l in max_file:
                polcsv.write(l)
            max_file.close()  # get rid of temp file

            avg_file.seek(0)
            for l in avg_file:
                polcsv.write(l)
            avg_file.close()  # get rid of temp file

            polcsv.close()
            azip.write(fullpath)

        # disk cleanup
        if (os.path.exists(self._tmpdir)):
            shutil.rmtree(self._tmpdir, True)  # TODO add something for errors
