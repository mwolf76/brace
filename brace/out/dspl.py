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

from xml.sax.saxutils import escape

# TODO: this code is *very* raw, at some point in time this should use
# some decent templating engine (e.g. Genshi)


# -- concepts
def build_dspl_aggregates_concept_xml():
    """
    """
    return """<!-- Concept for aggregates. -->
<concept id="aggregate" extends="entity:entity">
    <info>
         <name>
            <value>Aggregation</value>
         </name>
         <description>
             <value>Max or Avg</value>
         </description>
    </info>
    <type ref="string" />

    <property id="name">
        <info>
            <name>
                <value>Aggregate</value>
            </name>
            <description>
                <value>Aggregation function (max or avg)</value>
            </description>
        </info>
        <type ref="string" />
  </property>
  <table ref="aggregates_table"/>
</concept>
"""


def build_dspl_pollutants_concept_xml():
    """
    """
    return """<!-- Concept for pollutants. -->
<concept id="pollutant" extends="entity:entity">
    <info>
         <name>
            <value>Aggregation</value>
         </name>
         <description>
             <value>Max or Avg</value>
         </description>
    </info>
    <type ref="string" />

    <property id="name">
        <info>
            <name>
                <value>Formula</value>
            </name>
            <description>
                <value>Pollutant agent canonical name</value>
            </description>
        </info>
        <type ref="string" />
  </property>
  <table ref="pollutants_table"/>
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
      <type ref="string" />

      <property id="name">
          <info>
              <name>
                  <value>Station</value>
              </name>
              <description>
                  <value>The official name of the region (italian)</value>
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
      <type ref="string" />

      <property id="name">
          <info>
              <name>
                  <value>Station</value>
              </name>
              <description>
                  <value>Pollution sampling station</value>
              </description>
          </info>
          <type ref="string" />
      </property>
      <property concept="region" isParent="true" />
      <table ref="stations_table" />
 </concept>
"""

"""
<concepts>
    <concept id="population">
      <info>
        <name>
          <value>Population</value>
        </name>
      </info>
      <type ref="integer"/>
    </concept>
  ...
  </concepts>
  """

def build_dspl_measurement_concept_xml():
    """Builds the xml node for a specific city in Italy
    """
    return """<!-- Concept for measurement -->
<concept id="measurement">
      <info>
          <name>
              <value>Measurement</value>
          </name>
      </info>
      <type ref="float" />
 </concept>
"""


def build_dspl_pollutant_concept_xml(pollutant):
    """Builds the xml node for a specific pollutant
    """
    return """<!-- Concept for %(id)s %(name)s. -->
<concept id="pollutant">
    <info>
        <name>
            <value>Pollutants</value>
        </name>
        <description>
            <value>Chemicals and waste</value>
        </description>
      </info>
      <type ref="string"/>

      <property id="name">
          <info>
              <name>
                  <value>Pollutant</value>
              </name>
              <description>
                  <value>Chemicals and waste</value>
              </description>
          </info>
          <type ref="string" />
      </property>
      <table ref="pollutants_table" />
</concept>
"""


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


def build_dspl_pollutants_table_xml():
    """
    """
    return """<!-- Table for aggregate types. -->
<table id="pollutants_table">
    <column id="pollutant" type="string"/>
    <column id="description" type="string"/>
    <data>
        <file format="csv" encoding="utf-8">pollutants.csv</file>
    </data>
</table>
"""


def build_dspl_regions_table_xml():
    """ Builds the dspl italian regions table
    """

    return """<!-- Table for regions. -->
<table id="regions_table">
    <column id="region" type="string"/>
    <column id="name" type="string"/>
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
    <column id="name" type="string"/>
    <column id="region" type="string" />
    <column id="latitude" type="float"/>
    <column id="longitude" type="float"/>
    <data>
        <file format="csv" encoding="utf-8">stations.csv</file>
    </data>
</table>
"""


def build_dspl_pollutants_slice_table_xml():
    """Builds the dspl pollutants slice table.
    """

    return """<!-- Slice table for pollutants. -->
<table id="pollutants_slice_table">
    <column id="region" type="string" />
    <column id="station" type="string" />
    <column id="aggregate" type="string" />
    <column id="pollutant" type="string" />
    <column id="day" type="date" format="yyyy-MM-dd" />

    <column id="measurement" type="float" />
    <data>
        <file format="csv" encoding="utf-8">data.csv</file>
    </data>
</table>
"""


def build_dspl_tables_xml():
    """
    """

    return \
        build_dspl_aggregates_table_xml() + \
        "\n" + \
        build_dspl_pollutants_table_xml() + \
        "\n" + \
        build_dspl_regions_table_xml() + \
        "\n" + \
        build_dspl_stations_table_xml() + \
        "\n" + \
        build_dspl_pollutants_slice_table_xml()


def build_dspl_concepts_xml():
    """Builds the dspl ontology for pollutants.
    """

    return \
        "\n" + \
        build_dspl_aggregates_concept_xml() + \
        "\n" + \
        build_dspl_pollutants_concept_xml() + \
        "\n" + \
        build_dspl_regions_concept_xml() + \
        "\n" + \
        build_dspl_stations_concept_xml() + \
        "\n" + \
        build_dspl_measurement_concept_xml()


def build_dspl_pollutant_slice_xml():
    """
    """
    return """<!-- Slice for pollutants -->
<slice id="pollutants_slice">
    <dimension concept="region" />
    <dimension concept="station" />
    <dimension concept="aggregate" />
    <dimension concept="pollutant" />
    <dimension concept="time:day" />

    <metric concept="measurement" />
    <table ref="pollutants_slice_table" />
</slice>
"""


def build_dspl_slices_xml():
    """Builds the dspl slices for pollutants.
    """
    # return \
    #     "\n".join(map(build_dspl_pollutant_slice_xml,
    #                   opts_mgr.pollutants))
    return build_dspl_pollutant_slice_xml()

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

    def _yield(self):
        """Yields aggregate data for this output plugin.
        """
        # initialization
        region = None
        station = None
        pollutant = None
        day = None

        max_ = 0.0   # (aggregate max)
        cum_ = 0.0   # (aggregate cum sum)
        samples = 0  # (number of samples, needed for avg)
        data = False # when True data needs to be yielded

        for row in self._data_mgr.data:
            (row_region, row_station, row_pollutant, row_timestamp, row_quantity) = row

            # day as a 3-tuple
            row_day = (row_timestamp.tm_year, row_timestamp.tm_mon, row_timestamp.tm_mday)

            # new data available ?
            data = region is not None and \
                   (row_region != region or \
                    row_station != station or \
                    row_pollutant != pollutant or \
                    row_day != day)

            # if dealing with another region, station, pollutant or day,
            # yield result and reinitialize counters
            if data:

                avg_ = cum_ / samples
                yield (region, station, day, pollutant, max_, avg_)
                max_ = 0.0
                cum_ = 0.0
                samples = 0
                data = False

            region = row_region
            station = row_station
            pollutant = row_pollutant
            day = row_day

            # update aggregate measurement
            max_ = max(max_, row_quantity)
            cum_ += row_quantity
            samples += 1

        # yield last row if necessary
        if data:
            avg_ = cum_ / samples
            yield (region, station, day, pollutant, max_, avg_)

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
        regcsv.write("region, name, latitude, longitude\n")
        for r in opts_mgr.regions:
            entry = u"%(region)s, %(region)s, %(latitude)s, %(longitude)s\n" % {
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
        stscsv.write("station, name, region, latitude, longitude\n")
        for (regcode, name, latitude, longitude) in stations_dict.all():
            entry = u"%(station)s, %(station)s, %(region)s, %(latitude)s, %(longitude)s\n" % {
                'station': name,
                'region': regions_dict.get_name(regcode),
                'latitude': latitude,
                'longitude': longitude,
            }
            stscsv.write(entry)
        stscsv.close()
        azip.write(fullpath)

        # write pollutants csv file
        fullpath = os.path.join(self._tmpdir, "pollutants.csv")
        csv = open(fullpath, "wt")
        csv.write("pollutant, description\n")
        for (_, formula, description) in pollutants_dict.all():
            entry = u"%(formula)s, %(description)s\n" % {
                'formula': formula,
                'description': escape(description),
                }
            csv.write(entry)
        csv.close()
        azip.write(fullpath)

        # write pollutants csv files for slice tables
        # Remark: as csv file *must* be sorted according to dimensions
        # it is necessary to build two separate temp files and then
        # join them together when every row has been processed. :-/
        data_fullpath = os.path.join(self._tmpdir, "data.csv")
        data_csv = open(data_fullpath, "wt")
        data_csv.write("region, station, aggregate, pollutant, day, measurement\n")

        max_file = tempfile.TemporaryFile()
        avg_file = tempfile.TemporaryFile()

        # generate aggregated data
        for (region, station, day, pollutant, max_, avg_) in self._yield():

            formula = pollutants_dict.get_formula(pollutant)

            entry = u"%(region)s, %(station)s, max, %(formula)s, %(day)s, %(qty).3f\n" % {
                'region': region,
                'station': station,
                'formula': formula,
                'day': time.strftime("%Y-%m-%d", day +(0, ) * 6),
                'qty': max_,
            }
            max_file.write(entry)

            entry = u"%(region)s, %(station)s, avg, %(formula)s, %(day)s, %(qty).3f\n" % {
                'region': region,
                'station': station,
                'formula': formula,
                'day': time.strftime("%Y-%m-%d", day +(0, ) * 6),
                'qty': avg_,
            }
            avg_file.write(entry)

        # concatenate max_file and avg_file files
        max_file.seek(0)
        for l in max_file:
            data_csv.write(l)
        max_file.close()  # get rid of temp file

        avg_file.seek(0)
        for l in avg_file:
            data_csv.write(l)
        avg_file.close()  # get rid of temp file

        data_csv.close()
        azip.write(data_fullpath)

        # disk cleanup
        if (os.path.exists(self._tmpdir)):
            shutil.rmtree(self._tmpdir, True)  # TODO add something for errors
