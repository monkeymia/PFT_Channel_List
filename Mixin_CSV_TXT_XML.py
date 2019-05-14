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

class Mixin_CSV_TXT_XML (object) : 

    DELIMITER_CSV   = ";"
    
    def change_delimiter (self, delimiter = None) :
        if delimiter :
            self.DELIMITER_CSV = str (delimiter) [0]
    # end def 
    
    def csv_read_file (self, input_csv) : 
        if sys.version_info [0] == 2 : 
            mode = "rb"
        else : 
            mode = "r"
        csv_rows = []
        print \
            ( "Info:Read csv file '%s' with delimiter '%s'. If it is different then unexpected errors will happen!" 
            % (input_csv, self.DELIMITER_CSV)
            )
        f = open (input_csv, mode) 
        try :
            reader = csv.DictReader \
                ( f
                , dialect   = "excel"
                , delimiter = self.DELIMITER_CSV
                , quoting   = csv.QUOTE_ALL
                )
            for row in reader : 
                csv_rows.append (row)
        finally : 
            f.close ()
        return csv_rows 
    # end def     

    def csv_write_file (self, output_csv, csv_rows) :     
        d = os.path.dirname (output_csv) 
        if d and not os.path.exists (d) : 
            os.makedirs (d)
        fieldnames = set ()
        for row in csv_rows : 
            for k in row.keys () : 
                fieldnames.add (k)
        fieldnames_lst = list (fieldnames)
        fieldnames_lst.sort ()
        header = {}
        for k in fieldnames_lst : 
            header [k] = k
        if sys.version_info [0] == 2 : 
            mode = "wb"
        else : 
            mode = "w"
        print ("Info:Write csv file '%s'" % output_csv) 
        f = open (output_csv, mode) 
        try :
            writer = csv.DictWriter \
                ( f
                , fieldnames_lst
                , dialect   = "excel"
                , delimiter = self.DELIMITER_CSV
                , quoting   = csv.QUOTE_ALL
                )
            writer.writerow (header)
            for row in csv_rows :
                writer.writerow (row)
        finally : 
            f.close ()
    # end def 
        
    def find_input_file \
        ( self
        , filename  = None
        , extension = ".xml"
        , default   = None
        ) : 
        if not filename  : 
            cwd = os.getcwd ()
            fnames = set ()
            for fname in os.listdir (cwd) : 
                if fname.lower ().endswith (extension) : 
                    fnames.add (fname) 
            if len (fnames) > 1 :
                if default in fnames : 
                    filename = default
                else : 
                    print ("Error:cannot detect input file:fnames=%s" % sorted (fnames))
                    self.usage ()
                    sys.exit (1)
        if not filename : 
            print ("Error:cannot detect input file:extension=%s" % extension)
            self.usage ()
            sys.exit (2)
        if filename and not os.path.exists (filename) : 
            print \
                ( "Error:Input_file '%s' not found." 
                % filename
                )
            sys.exit (3)
        return filename
    # end def     

    def usage (self) :
        print ("Usage:%s" % sys.argv [0])
    # end def     
    
    def txt_read_file (self, input_txt) : 
        print ("Info:Read txt file '%s'" % input_txt) 
        lines = []
        f = open (input_txt, "r") 
        try :
            lines = f.readlines () 
        finally : 
            f.close 
        return lines
    # end def     
    
    def txt_write_file (self, output_txt, text) :     
        d = os.path.dirname (output_txt) 
        if d and not os.path.exists (d) : 
            os.makedirs (d)
        mode = "w"
        print ("Info:Write txt file '%s'" % output_txt) 
        f = open (output_txt, mode) 
        try :
            f.write (text)
        finally : 
            f.close ()
    # end def 
    
    def xml_read_file (self, input_xml) : 
        print ("Info:Parse xml file '%s'" % input_xml) 
        tree = ET.parse (input_xml)
        return tree
    # end def     
    
    def xml_write_file (self, output_xml, tree) :     
        d = os.path.dirname (output_xml) 
        if d and not os.path.exists (d) : 
            os.makedirs (d)
        mode = "w"
        print ("Info:Write xml file '%s'" % output_xml) 
        f = open (output_xml, mode) 
        f.write ("""<?xml version="1.0" encoding="utf-8"?>\n""")
        try :
            tree.write (f, encoding = "utf-8")
        finally : 
            f.close ()
    # end def 

# end class

# END

