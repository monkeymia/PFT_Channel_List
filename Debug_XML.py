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
import string
import sys
import os
import os.path
import xml.etree.ElementTree as ET
import Mixin_CSV_TXT_XML

class Debug_XML (Mixin_CSV_TXT_XML.Mixin_CSV_TXT_XML) : 

    def __call__ (self) :
        cwd = os.getcwd ()
        for fname in os.listdir (cwd) : 
            if fname.lower ().endswith (".xml") : 
                tree = self.xml_read_file \
                    (os.path.join (cwd, fname))
                text = self.convert (tree)
                self.txt_write_file \
                    ( os.path.join (cwd, "%s.debug" % fname)
                    , text
                    )
                
    # end def 

    def convert (self, tree) :
        e0 = tree.getroot ()
        lines = []
        indent = ""
        lines.append ("%s%s" % (indent, e0.tag))
        indent = " " * 1
        for k, v in sorted (e0.attrib.items ()) :
            lines.append ("%s%s='%s'" % (indent, k, v))
        for e1 in e0 : 
            indent = " " * 2
            lines.append ("%s%s" % (indent, e1.tag))
            indent = " " * 3
            for k, v in sorted (e1.attrib.items ()) :
                lines.append ("%s%s='%s'" % (indent, k, v))
            for e2 in e1 : 
                indent = " " * 4
                lines.append ("%s%s" % (indent, e2.tag))
                indent = " " * 5
                for k, v in sorted (e2.attrib.items ()) :
                    lines.append ("%s%s='%s'" % (indent, k, v))
                for e3 in e2 : 
                    indent = " " * 6
                    lines.append ("%s%s" % (indent, e3.tag))
                    indent = " " * 7
                    for k, v in sorted (e3.attrib.items ()) :
                        lines.append ("%s%s='%s'" % (indent, k, v))
        return "\n".join (lines)
    # end def     

# end class

if __name__ == "__main__" : 
    ce = Debug_XML ()
    ce ()
# END

