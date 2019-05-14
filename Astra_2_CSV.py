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
import copy
import csv
import string
import sys
import os
import os.path
import Mixin_CSV_TXT_XML

class Astra_2_CSV (Mixin_CSV_TXT_XML.Mixin_CSV_TXT_XML) : 

    DEFAULT_CSV = "astra_output.csv"
    DELIMITER_ASTRA = " "

    def __call__ \
        ( self
        , input_txt  = None
        , output_csv = None
        , delimiter  = None
        ) :
        self.change_delimiter (delimiter)  
        if not output_csv : 
            output_csv = self.DEFAULT_CSV
        txt_file = self.find_input_file \
            ( filename  = input_txt
            , extension = ".txt"
            , default   = "astra.txt"
            )
        lines = self.txt_read_file (txt_file)
        rows = self.astra_convert (lines)
        self.csv_write_file (output_csv, rows) 
    # end def 

    def astra_convert (self, lines) : 
        header = []
        rows = []
        for i, line_txt_lf in enumerate (lines) : 
            line_txt = line_txt_lf.strip ()
            if line_txt.startswith ("Updated on:") : 
                continue
            row = {}
            line_org = line_txt.split (self.DELIMITER_ASTRA) 
            if header and all (x in line_org for x in header) : 
                continue
            line = copy.deepcopy (line_org)
            line.reverse () 
            if not i : 
                header = line_org
                for k in header : 
                    row [k] = k
                    print ("Info:read header field:'%s'" % k) 
            else : 
                for k in header : 
                    row [k] = ""
                for k in \
                    ( "Encoding"
                    , "Pay"
                    , "Frequency"
                    , "SR"
                    , "Pol."
                    , "Transponder"
                    , "Satellite"
                    , "Quality"
                    , "Encryption"
                    , "Orb"
                    , "Language"
                    ) : 
                    v = line [0]
                    if k == "Quality" and v == "astra" : 
                        line.remove (v)
                        v = line [0]
                    if k not in row : 
                        print ("Error:Unknown file format;k:'%s';v='%s';row=%s" % (k, v, row))
                        sys.exit (10)
                    if k == "Encoding" and not v.startswith ("mpeg-") : 
                        continue  # ignore empty
                    if k == "Quality" and v == "none" : 
                        continue  # ignore empty
                    row [k] = v
                    line.remove (v)
                for k in \
                    ( "Name"
                    , "Genre"
                    , "Type"
                    ) : 
                    if k not in row : 
                        print ("Error:Unknown file format;k:'%s';v='%s'" % (k, v))
                remaining = " ".join (line)
                # in case of no genre or name :
                if remaining.startswith ("tv ") :
                    k = "Type"
                    row [k] = "tv"
                    k = "Name"
                    row [k] = remaining [3:]
                elif remaining.startswith ("radio ") :
                    k = "Type"
                    row [k] = "radio"
                    k = "Name"
                    row [k] = remaining [6:]
                elif remaining.endswith (" tv") :
                    k = "Type"
                    row [k] = "tv"
                    k = "Genre"
                    row [k] = remaining [:-3]
                elif remaining.endswith (" radio") :
                    k = "Type"
                    row [k] = "radio"
                    k = "Genre"
                    row [k] = remaining [:-6]
                elif remaining == "tv" :
                    k = "Type"
                    row [k] = "tv"
                elif remaining == "radio" :
                    k = "Type"
                    row [k] = "radio"
                else : 
                    t1 = " tv "
                    t2 = " radio "
                    if remaining.count (t1) == 1 : 
                        head, sep, tail = remaining.partition (t1)
                    elif remaining.count (t2) == 1 : 
                        head, sep, tail = remaining.partition (t2)
                    else : 
                        print \
                            ( "Error:cannot extract name/type/genre:'%s'; line_txt='%s';line_nr=%d" 
                            % (remaining, line_txt, i)
                            )
                        sys.exit (11)
                    k = "Genre"
                    row [k] = head.strip ()
                    k = "Type"
                    row [k] = sep.strip ()
                    k = "Name"
                    row [k] = tail.strip ()
            if i : 
                rows.append (row)
        return rows 
    # end def     

    def usage (self) :
        print \
            ( "Error: Please specify input file ! Usage %s <input_txt> [output_csv]" 
            % sys.argv [0]
            )
    # end def     

# end class

if __name__ == "__main__" : 
    csv_file = None
    txt_file = None
    if len (sys.argv) > 2 : 
        txt_file = sys.argv [1]
        csv_file = sys.argv [2]
    elif len (sys.argv) > 1 : 
        txt_file = sys.argv [1]
    else : 
        pass
    delimiter = None
    for a in sys.argv : 
        if a.startswith ("--delimiter=") : 
            delimiter = a.replace ("--delimiter=", "", 1)
    ce = Astra_2_CSV ()
    ce  ( input_txt  = txt_file
        , output_csv = csv_file
        , delimiter  = delimiter
        )
# END

