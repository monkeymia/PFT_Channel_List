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
import xml.etree.ElementTree as ET
import Mixin_CSV_TXT_XML

class My_Channels (Mixin_CSV_TXT_XML.Mixin_CSV_TXT_XML) : 

    MY_CHANNEL_COL_NAME = "Channel"
    MY_SID_COL_NAME     = "SID"

    def __call__ (self, ch_csv, my_csv, ch_new, delimiter = None) :
        self.change_delimiter (delimiter)  
        c = self.csv_read_file (ch_csv) 
        m  = self.csv_read_file (my_csv) 
        rows = self.convert (c, m)
        self.csv_write_file (ch_new, rows) 
    # end def 

    def convert (self, c, m) :
        rows   = []
        channel_numbers = []
        my_dct = {}
        for r in m : 
            if self.MY_CHANNEL_COL_NAME not in r : 
                print \
                    ( "Error:Column '%s' not found in my channels.keys=%s" 
                    % (self.MY_CHANNEL_COL_NAME, sorted (r))
                    )
                sys.exit (1)
            if self.MY_SID_COL_NAME not in r : 
                print \
                    ( "Error:Column '%s' not found in my channels.keys=%s" 
                    % (self.MY_SID_COL_NAME, sorted (r))
                    )
                sys.exit (1)
            k = r [self.MY_SID_COL_NAME]
            v = r [self.MY_CHANNEL_COL_NAME]
            if k in my_dct : 
                print ("Error:Duplicate value SID=%s" % k)
                sys.exit (1)
            my_dct [str (k)] = str (v)
            channel_numbers.append (int (str (v)))
        print ("Info:Found %s rows in my_file"  % len (channel_numbers))
        if len (channel_numbers) != len (set (channel_numbers)) : 
            print ("Error:Duplicate Channel Number detected.")
            sys.exit (1)
        if 0 in channel_numbers : 
            print ("Error:Invalid Channel Number 0 detected.")
            sys.exit (1)
        for i in range (1, len (channel_numbers)) : 
            if i not in channel_numbers : 
                print ("Error:Gap in Channel Number detected. (%s)" % i)
                sys.exit (1)
        count = 0
        for r in c : 
            row = copy.deepcopy (r)
            name = "B_Frequency"
            if name not in row : 
                print ("Error: Column '%s' not found." % name)
            name = "B_Sid"
            if name not in row : 
                print ("Error: Column '%s' not found." % name)
            sid = str (row [name])
            name = "H_New_ChannelNumber"
            if name not in row : 
                print ("Error: Column '%s' not found." % name)
            value = my_dct.get (sid, "")
            row [name] = value
            if value : 
                count += 1 
            rows.append (row)
        print ("Info:%s rows are taken in to acount from my_file"  % count)
        last_channel_nr = max ([0] + channel_numbers)
        for i, r in enumerate \
            ( sorted 
                ( rows
                , key = lambda x : (str (x ["S_ChannelName_ascii"]), str (x ["B_Frequency"]))
                )
            ) : 
            if not r ["H_New_ChannelNumber"] : 
                last_channel_nr += 1
                r ["H_New_ChannelNumber"] = str (last_channel_nr)
        return rows
    # end def     

# end class

if __name__ == "__main__" : 
    ch_file     = "channel_output.csv"
    ch_new_file = "channel_output_sorted.csv"
    my_file     = "my_channels.csv"
    if len (sys.argv) > 3 : 
        ch_file     = sys.argv [1]
        my_file     = sys.argv [2]
        ch_new_file = sys.argv [3]
    else : 
        print ("Usage: %s <channel_file> <my_file> <channel_new>" % sys.argv [0])
    delimiter = None
    for a in sys.argv : 
        if a.startswith ("--delimiter=") : 
            delimiter = a.replace ("--delimiter=", "", 1)
    ce = My_Channels ()
    ce  ( ch_file
        , my_file
        , ch_new_file
        , delimiter = delimiter
        )
# END



