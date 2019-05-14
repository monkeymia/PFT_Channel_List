# PFT_Channel_List
Philips Flat TV Series 5500 Channel List Sort via CSV 

License
------------------------------------------------------------------------------
See LICENSE

Introdution
------------------------------------------------------------------------------
The Phillips Flat TV (PFT) 5500 Series allows to export channel list to 
USB, but provides no software to edit it. 

The exported files is XML-format. XML is difficult to edit. This software 
(written in Python 2.6) converts it from/to Comma Separated Value (csv) file 
that could be edit in Libre Office Calc, Excel, ...

Usage
------------------------------------------------------------------------------
1) Export Channel list to USB (see User Manual).
2) Create Backup
3) Copy 
   Clone\PhilipsChannelMaps\ChannelMap_100\ChannelList\s2channellib\DVBS.xml
   (Description of the file format - see below)
4) Create a my_channels.csv file. 
   The file must contain column "SID" and "Channel". 
   SID identifies the channel and must match value in DVBS.xml
   Channel defines the new location (starting from value 1, ascending, no gaps)
5) run.bat (Please double check consistent delimiter in CSV file) 
   
   or : 
   
   a) run Channel_2_CSV.py
   b) edit colunn H_New_ChannelNumber 
   c) run CSV_2_Channel.py

6) review DVBS_sorted.xml
7) copy DVBS_sorted.xml to USB and rename it to DVBS.xml
8) Import Channel list from USB (see User Manual).
9) "repair" other sources (Cable, T) i.e search for new channels


Description of Source code 
------------------------------------------------------------------------------
Tested with python 2.6

* Channel_2_CSV.py: 
  Convert DVBS.xml to csv.
  
* CSV_2_Channel.py: 
  convert csv to DVBS.xml
  Note: Instead of the original ChannelNumber the value in 
  column "H_New_ChannelNumber" defines the position. 

* Debug_XML.py  :
  pretty print XML (insert linefeeds) - for debugging only.

* Mixin_CSV_TXT_XML.py:  
  provides functions to read/write files (for internal use)

* My_Channels.py:
  Read channel csv file and my channels csv and creates a new channel list
  based on SID and channel defined in my channels csv file. All other channels 
  are added in alphabetical order (column S_ChannelName_ascii)

Infos about the File format DVBS.xml
------------------------------------------------------------------------------

Example: 

<?xml version="1.0" encoding="utf-8"?>
<ChannelMap>
	<Channel>
		<Setup SatelliteName="0x41 0x00 0x53 0x00 0x54 0x00 0x52 0x00 0x41 0x00 0x20 0x00 0x31 0x00 0x39 0x00 0x2E 0x00 0x32 0x00 0x45 0x00 0x20 0x00 0x31 0x00 0x39 0x00 0x2E 0x00 0x32 0x00 0xC2 0x00 0xB0 0x00 0x45 0x00 " ChannelNumber="1" ChannelName="" ChannelLock="0" UserModifiedName="0" LogoID="0" UserModifiedLogo="0" LogoLock="0" UserHidden="0" FavoriteNumber="0" Scramble="0"></Setup>
		<Broadcast ChannelType="3" Onid="1" Tsid="1058" Sid="30122" Frequency="10847" Modulation="0" ServiceType="1" SymbolRate="22008" LNBNumber="52" Polarization="1" SystemHidden="0"></Broadcast>
	</Channel>
...
	</Channel>
</ChannelMap>

Obviously:

* The first line indicates standalone XML in a UTF-8 encoded text file.
* The root element is ChannelMap
* Each Channel has sub-element "Setup" and "Broadcast".
* The order of channel becomes relevant if Favorites are used. 
* It seems Text is encoded in Ascii, but after each char a 0x00 is added.
* It seems Frequency, SymbolRate might be slightly different compared to offical valus found in Internet
  Thefore the best match is Sid. 

    Setup
     ChannelLock='0'
     ChannelName='0x51 0x00 0x56 0x00 0x43 0x00 0x32 0x00 '
     ChannelNumber='1'
     FavoriteNumber='0'
     LogoID='0'
     LogoLock='0'
     SatelliteName='0x41 0x00 0x53 0x00 0x54 0x00 0x52 0x00 0x41 0x00 0x20 0x00 0x31 0x00 0x39 0x00 0x2E 0x00 0x32 0x00 0x45 0x00 '
     Scramble='0'
     UserHidden='0'
     UserModifiedLogo='0'
     UserModifiedName='0'
    Broadcast
     ChannelType='3'
     Frequency='12551'
     LNBNumber='52'
     Modulation='0'
     Onid='1'
     Polarization='1'
     ServiceType='1'
     Sid='3394'
     SymbolRate='22008'
     SystemHidden='0'
     Tsid='1108'


