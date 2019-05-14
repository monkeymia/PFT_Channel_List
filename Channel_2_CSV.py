# -*- coding: iso-8859-1 -*-

from __future__ import print_function
import csv
import string
import sys
import os
import os.path
import xml.etree.ElementTree as ET
import Mixin_CSV_TXT_XML

class Channel_2_CSV (Mixin_CSV_TXT_XML.Mixin_CSV_TXT_XML) : 

    DEFAULT_CSV = "channel_output.csv"

    def __call__ \
        ( self
        , input_xml  = None
        , output_csv = None
        , delimiter  = None
        ) :
        self.change_delimiter (delimiter)  
        if not output_csv : 
            output_csv = self.DEFAULT_CSV
        xml = self.find_input_file (filename = input_xml)
        tree = self.xml_read_file (xml)
        rows = self.xml_convert_from_philips_5500 (tree)
        self.csv_write_file (output_csv, rows) 
    # end def 

    def usage (self) :
        print \
            ( "Error: Please specify input file ! Usage %s <input_xml> [output_csv]" 
            % sys.argv [0]
            )
    # end def     

    def xml_convert_from_philips_5500 (self, tree) :
        root = tree.getroot ()
        print ("Info:Found %d elements" % len (root))
        rows = []
        value = root.tag 
        if value != "ChannelMap" :
            print ("Error:Unknown XML file format;Root-tag:'%s'" % value)
            sys.exit (10)
        for child_index, channel  in enumerate (root) :
            value = channel.tag 
            if value != "Channel" :
                print ("Error:Unknown XML file format;Channel-tag:'%s'" % value)
                sys.exit (11)
            value = root.attrib
            if  value :
                print ("Error:Unknown XML file format;Channel-tag has attribs:'%s'" % value)
                sys.exit (12)
            row = {}
            for channel_child_index, child in enumerate (channel) : 
                tag = child.tag
                col_prefix = ""
                if tag == "Setup" : 
                    col_prefix = "S_"
                elif tag == "Broadcast" : 
                    col_prefix = "B_"
                else : 
                    print ("Error:Unknown XML file format;Channel-Child-tag:'%s'" % tag)
                    sys.exit (13)
                for k, v in child.attrib.items () : 
                    col_name = "%s%s" % (col_prefix, k) 
                    if col_name in row : 
                        print ("Error:Unknown XML file format;Duplicate attribute name:'%s'" % k)
                        sys.exit (14)
                    row [col_name] = v
                    if "0x" in v : 
                        v_ascii = ""
                        has_error = False
                        for i in v.split (" ") : 
                            if i : 
                                d = int (i, 16)
                                if d < 0  or d > 0xFF : 
                                    has_error = True
                                else : 
                                    c = chr (d)
                                    if c in string.printable :
                                        v_ascii += c
                        if not v_ascii : 
                            has_error = True
                        if not has_error :
                            row ["%s_ascii" % col_name] = v_ascii
            if not row : 
                print ("Error:Unknown XML file format;No channel infos")
                sys.exit (15)
            else : 
                row ["H_New_ChannelNumber"] = row ["S_ChannelNumber"]
            rows.append (row)        
        return rows 
    # end def     

    def xml_read_file (self, input_xml) : 
        print ("Info:Parse xml file '%s'" % input_xml) 
        tree = ET.parse (input_xml)
        return tree
    # end def     

# end class

if __name__ == "__main__" : 
    csv_file = None
    xml_file = None
    if len (sys.argv) > 2 : 
        xml_file = sys.argv [1]
        csv_file = sys.argv [2]
    elif len (sys.argv) > 1 : 
        xml_file = sys.argv [1]
    else : 
        pass
    delimiter = None
    for a in sys.argv : 
        if a.startswith ("--delimiter=") : 
            delimiter = a.replace ("--delimiter=", "", 1)
    ce = Channel_2_CSV ()
    ce  ( input_xml  = xml_file
        , output_csv = csv_file
        , delimiter  = delimiter
        )
# END

