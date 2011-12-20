# -*- coding: utf-8 -*-
"""DSPL (Dataset Publishing Language) output services
"""

# os services
import os

# time services
import time
import datetime

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

# TODO: following code is *very* raw
def build_dspl_pollutant_concept_xml_max(pollutant):
    """Builds the xml node for a specific pollutant
    """
    return """<!-- Concept for %(id)s %(name)s (max). -->
<concept id="%(id)s_max">
    <info>
        <name>
            <value>%(name)s</value>
        </name>
    </info>
    <type ref="float"/>
</concept>
""" % {
        'id': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
}


def build_dspl_pollutant_concept_xml_avg(pollutant):
    """Builds the xml node for a specific pollutant
    """
    return """<!-- Concept for %(id)s %(name)s (avg). -->
<concept id="%(id)s_avg">
    <info>
        <name>
            <value>%(name)s</value>
        </name>
    </info>
    <type ref="float"/>
</concept>
""" % {
        'id': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
}


def build_dspl_regions_concept_xml():
    """Builds the xml node for a specific city in Italy
    """

    return """<!-- Concept for regions (geo). -->
<concept id="region" extends="geo:location">
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
</concept>
"""


def build_dspl_stations_concept_xml():
    """Builds the xml node for a specific city in Italy
    """

    return """<!-- Concept for stations (geo) -->
<concept id="station" extends="geo:location">
      <info>
          <name>
              <value>Measurement station</value>
          </name>
          <description>
              <value>Measurement station</value>
          </description>
      </info>
      <property concept="region" isParent="true" />
      <table ref="stations_table" />
 </concept>
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


def build_dspl_pollutant_slice_table_xml_max(pollutant):
    """Builds the dspl pollutant slice table for a given pollutant (max).
    """

    return """<!-- Slice table for %(formula)s (%(name)s). -->
<table id="%(formula)s_slice_table_max">
    <column id="region" type="string"/>
    <column id="station" type="string"/>
    <column id="day" type="date" format="yyyy-MM-dd"/>
    <column id="%(formula)s_max" type="float"/>
    <data><file format="csv" encoding="utf-8">%(formula)s_max.csv</file></data>
</table>
""" % {
        'formula': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
}


def build_dspl_pollutant_slice_table_xml_avg(pollutant):
    """Builds the dspl pollutant slice table for a given pollutant (avg).
    """

    return """<!-- Slice table for %(formula)s (%(name)s). -->
<table id="%(formula)s_slice_table_avg">
    <column id="region" type="string"/>
    <column id="station" type="string"/>
    <column id="day" type="date" format="yyyy-MM-dd"/>
    <column id="%(formula)s_avg" type="float"/>
    <data><file format="csv" encoding="utf-8">%(formula)s_avg.csv</file></data>
</table>
""" % {
        'formula': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
}


def build_dspl_tables_xml():
    """
    """

    return \
        build_dspl_regions_table_xml() + \
        "\n" + \
        build_dspl_stations_table_xml() + \
        "\n" + \
        "\n".join(map(build_dspl_pollutant_slice_table_xml_max,
                      opts_mgr.pollutants)) + \
        "\n" + \
        "\n".join(map(build_dspl_pollutant_slice_table_xml_avg,
                      opts_mgr.pollutants))


def build_dspl_concepts_xml():
    """Builds the dspl ontology for pollutants.
    """

    return \
        "\n".join(map(build_dspl_pollutant_concept_xml_max,
                      opts_mgr.pollutants)) + \
        "\n" + \
        "\n".join(map(build_dspl_pollutant_concept_xml_avg,
                      opts_mgr.pollutants)) + \
        "\n" + \
        build_dspl_regions_concept_xml() + \
        "\n" + \
        build_dspl_stations_concept_xml()

def build_dspl_pollutant_slice_xml_max(pollutant):
    """
    """
    return """<!-- Slice for %(formula)s (%(name)s). (max) -->
<slice id="%(formula)s_max_slice">
    <dimension concept="region"/>
    <dimension concept="station"/>
    <dimension concept="time:day"/>
    <metric concept="%(formula)s_max"/>
    <table ref="%(formula)s_slice_table_max"/>
</slice>
""" % {
        'formula': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
}

def build_dspl_pollutant_slice_xml_avg(pollutant):
    """
    """
    return """<!-- Slice for %(formula)s (%(name)s). (avg) -->
<slice id="%(formula)s_avg_slice">
    <dimension concept="region"/>
    <dimension concept="station"/>
    <dimension concept="time:day"/>
    <metric concept="%(formula)s_avg"/>
    <table ref="%(formula)s_slice_table_avg"/>
</slice>
""" % {
        'formula': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
}

def build_dspl_slices_xml():
    """Builds the dspl slices for pollutants.
    """
    return \
        "\n".join(map(build_dspl_pollutant_slice_xml_max,
                      opts_mgr.pollutants)) + \
        "\n".join(map(build_dspl_pollutant_slice_xml_avg,
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
    """
    """

    def __init__(self, data_mgr, out):
        self._data_mgr = data_mgr
        self._out = out
        self._tmpdir = "zip/"

    def _yield(self, formula):
        """Yields aggregate data for this output plugin.
        """
        fk = pollutants_dict.get_pk(formula)

        curr_reg = None
        curr_stat = None
        curr_day = None

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

                    # initialization occurs here
                    max_ = 0.0   # (aggregate max)
                    cum_ = 0.0   # (aggregate cum sum)
                    samples = 0  # (number of samples, needed for avg)

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

            avg_ = cum / samples
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
        for pollutant in opts_mgr.pollutants:
            formula = pollutants_dict.get_formula(pollutant)

            fullpath_max = os.path.join(self._tmpdir, "%(formula)s_max.csv" % {
                'formula': formula
            })
            polcsv_max = open(fullpath_max, "wt")
            polcsv_max.write("region, station, day, %(formula)s_max\n" % {
                'formula': formula,
            })

            fullpath_avg = os.path.join(self._tmpdir, "%(formula)s_avg.csv" % {
                'formula': formula
            })
            polcsv_avg = open(fullpath_avg, "wt")
            polcsv_avg.write("region, station, day, %(formula)s_avg\n" % {
                'formula': formula,
            })

            # generate aggregate data
            for (region, station, day, max_, avg_) in self._yield(formula):

                entry_max = u"%(region)s, %(station)s, %(day)s, %(max)s\n" % {
                    'region': region,
                    'station': station,
                    'day': time.strftime("%Y-%m-%d", day +(0, ) * 6),
                    'max': max_,
                }
                polcsv_max.write(entry_max)

                entry_avg = u"%(region)s, %(station)s, %(day)s, %(avg)s\n" % {
                    'region': region,
                    'station': station,
                    'day': time.strftime("%Y-%m-%d", day +(0, ) * 6),
                    'avg': avg_,
                }
                polcsv_avg.write(entry_avg)


            polcsv_max.close()
            azip.write(fullpath_max)

            polcsv_avg.close()
            azip.write(fullpath_avg)

        # disk cleanup
        if (os.path.exists(self._tmpdir)):
            shutil.rmtree(self._tmpdir, True)  # TODO add something for errors
