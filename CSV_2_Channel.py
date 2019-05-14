# -*- coding: iso-8859-1 -*-
# PFT_Channel_List - Philips Flat TV Series 5500 Channel List Sort via CSV
# Copyright (C) 2019  https://github.com/monkeymia/PFT_Channel_List
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import print_function
import csv
import string
import sys
import os
import os.path
import xml.etree.ElementTree as ET
import Mixin_CSV_TXT_XML

class CSV_2_Channel (Mixin_CSV_TXT_XML.Mixin_CSV_TXT_XML) : 

    DEFAULT_XML = "channel_output.xml"

    def __call__ \
        ( self
        , input_csv  = None
        , output_xml = None
        , delimiter  = None
        ) :     
        self.change_delimiter (delimiter)  
        if not output_xml : 
            output_xml = self.DEFAULT_XML
        xml = self.find_input_file \
            ( filename  = input_csv
            , extension = ".csv"
            , default = "channel_output.csv"
            )
        rows = self.csv_read_file (xml)
        tree = self.xml_convert_to_philips_5500 (rows)
        self.xml_write_file (output_xml, tree) 
    # end def 

    def usage (self) :
        print \
            ( "Error: Please specify input file ! Usage %s <input_csv> [output_xml]" 
            % sys.argv [0]
            )
    # end def     
    
    def xml_convert_to_philips_5500 (self, rows) :
        print ("Info:Found %d lines" % len (rows))
        root = ET.Element ("ChannelMap", attrib = {})
        tree = ET.ElementTree (root)
        channel_numbers = set ()
        for row in sorted \
            ( rows
            , key = lambda x : 
                ( int (x ["H_New_ChannelNumber"])
                , int (x ["S_ChannelNumber"])
                )
            ) : 
            channel = ET.Element ("Channel", attrib = {})
            root.append (channel)
            for prefix, tag in \
                ( ("S_", "Setup")
                , ("B_", "Broadcast")
                ) : 
                a = {}
                for k, v in row.items () : 
                    if k.endswith ("_ascii") : 
                        continue
                    if k.startswith (prefix) : 
                        a_name  = k.replace (prefix, "", 1)
                        a [a_name] = v
                if "ChannelNumber" in a : 
                    a ["ChannelNumber"] = row ["H_New_ChannelNumber"]
                    n = int (a ["ChannelNumber"]) 
                    if (n != 1) and (not channel_numbers) : 
                        print ("Error:First Channel_Number must be 1! n=%s" % n) 
                    if n in channel_numbers : 
                        print ("Error:Duplicate Channel_Number detected! n=%s" % n) 
                        sys.exit (100)
                    if (n > 1) and ((n - 1) not in channel_numbers) : 
                        print ("Error:Gap in Channel_Numbers is not allowed! n=%s" % n) 
                        sys.exit (101)
                    if n < 1 :
                        print ("Error:Invalid Channel_Number! n=%s" % n) 
                        sys.exit (102)
                    channel_numbers.add (n)    
                child = ET.Element (tag, attrib = a)
                channel.append (child)
        return tree 
    # end def     

# end class

if __name__ == "__main__" : 
    csv_file = None
    xml_file = None
    if len (sys.argv) > 2 : 
        csv_file = sys.argv [1]
        xml_file = sys.argv [2]
    elif len (sys.argv) > 1 : 
        csv_file = sys.argv [1]
    else : 
        pass
    delimiter = None
    for a in sys.argv : 
        if a.startswith ("--delimiter=") : 
            delimiter = a.replace ("--delimiter=", "", 1)
    ce = CSV_2_Channel ()
    ce  ( input_csv  = csv_file
        , output_xml = xml_file
        , delimiter  = delimiter
        )
# END

