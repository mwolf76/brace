# -*- coding: utf-8 -*-
"""DSPL (Dataset Publishing Language) output services
"""

# os services
import os

# time services
import time

# Logging support
import logging
logger = logging.getLogger("brace")

# custom modules
from brace.opts import opts_mgr
from brace.ontology import pollutants_dict
from brace.ontology import regions_dict


# TODO: following code is *very* raw
def build_dspl_pollutant_concept_xml(pollutant):
    """Builds the xml node for a specific pollutant
    """
    return """<concept id="%(id)s">
      <info>
        <name>
          <value>%(name)s</value>
        </name>
      </info>
      <type ref="float"/>
      <table ref="%(id)s_table" />
    </concept>
    """ % {
        'id': pollutants_dict.get_formula(pollutant),
        'name': pollutants_dict.get_name(pollutant),
    }


def build_dspl_regions_concept_xml():
    """Builds the xml node for a specific city in Italy
    """

    return """<concept id="region" extends="geo:location">
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
    </concept>"""


def build_dspl_regions_table_xml():
    """ Builds the dspl italian regions table
    """

    return """<table id="regions_table">
        <column id="region" type="string"/>
        <column id="latitude" type="float"/>
        <column id="longitude" type="float"/>
        <data>
            <file format="csv" encoding="utf-8">regions.csv</file>
        </data>
        </table>"""


def build_dspl_pollutant_table_xml(pollutant):
    """Builds the dspl pollutant table for a given pollutant.
    """

    return """
<table id="%(id)s_table">
    <column id="station" type="string"/>
    <column id="timestamp" type="timestamp"/>
    <column id="quantity" type="float"/>
    <data><file format="csv" encoding="utf-8">%(id)s.csv</file></data>
</table>""" % {
        'id': pollutants_dict.get_formula(pollutant),
    }


def build_dspl_tables_xml():
    """
    """

    return \
        build_dspl_regions_table_xml() + \
        "\n" + \
        "\n".join(map(build_dspl_pollutant_table_xml, opts_mgr.pollutants))


def build_dspl_concepts_xml():
    """Builds the dspl ontology for pollutants.
    """
    return \
        "\n".join(map(build_dspl_pollutant_concept_xml,
                      opts_mgr.pollutants)) + \
        "\n" + \
        build_dspl_regions_concept_xml()

def build_dspl_xml():
    """Builds the dspl file.
    """

    return """<?xml version="1.0" encoding="UTF-8"?>
<dspl targetNamespace="https://www.github.org/mwolf76/brace"
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

  <concepts>
  %(concepts)s
  </concepts>

  <tables>
  %(tables)s
  </tables>

</dspl>
""" % {
        'concepts':  build_dspl_concepts_xml(),
        'tables': build_dspl_tables_xml(),
}



class DsplDumper(object):
    """
    """

    def __init__(self, data_mgr, outname):
        self._data_mgr = data_mgr
        self._outname = outname

    def __call__(self):
        
        # write output to file
        logger.info("Dumping DSPL files...")

        xml = open(self._filename, "wt")
        xml.write(build_dspl_xml())
        xml.close()

        # write regions csv file
        logger.debug("Dumping regions csv")
        regcsv = open("regions.csv", "wt")
        for r in opts_mgr.regions:
            entry = u"%(region)s, %(longitude)s, %(latitude)s\n" % {
                'region': regions_dict.get_name(r),
                'latitude': regions_dict.get_latitude(r),
                'longitude': regions_dict.get_longitude(r),
            }
            regcsv.write(entry)
        regcsv.close()

        # write pollutants csv files
        for pollutant in opts_mgr.pollutants:

            formula = pollutants_dict.get_formula(pollutant)
            logger.debug("Dumping csv for %s", formula)

            polcsv = open("%s.csv" % formula, "wt")
            for row in self._data_mgr.filter_by_formula(formula):

                entry = u"%(region)s, %(station)s, %(pollutant)s, %(timestamp)s, %(quantity)s\n" % {
                    'region': row.region,
                    'station': row.station,
                    'pollutant': pollutants_dict.get_formula(row.pollutant) + \
                        " (" + pollutants_dict.get_name(row.pollutant) + ")",
                    'timestamp': time.strftime("%Y-%m-%d %H:%M", row.timestamp),
                    'quantity': row.quantity,
                }
                polcsv.write(entry)

            polcsv.close()


