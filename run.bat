@ECHO OFF
REM PFT_Channel_List - Philips Flat TV Series 5500 Channel List Sort via CSV
REM Copyright (C) 2019  https://github.com/monkeymia/PFT_Channel_List
REM 
REM This program is free software: you can redistribute it and/or modify
REM it under the terms of the GNU General Public License as published by
REM the Free Software Foundation, either version 3 of the License, or
REM (at your option) any later version.
REM 
REM This program is distributed in the hope that it will be useful,
REM but WITHOUT ANY WARRANTY; without even the implied warranty of
REM MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
REM GNU General Public License for more details.
REM 
REM You should have received a copy of the GNU General Public License
REM along with this program.  If not, see <https://www.gnu.org/licenses/>.
cd /d %~dp0
setlocal enabledelayedexpansion
SET "MYPYTHON=c:\Python26\python.exe"
@ECHO INFO:Channel_2_CSV...
CALL %MYPYTHON% Channel_2_CSV.py DVBS.xml channel_output.csv --delimiter=;
IF %ERRORLEVEL% NEQ 0 GOTO labelerror
pause
@ECHO INFO:My_Channels...
CALL %MYPYTHON% My_Channels.py channel_output.csv my_channels.csv channel_output_sorted.csv --delimiter=;
IF %ERRORLEVEL% NEQ 0 GOTO labelerror
pause
@ECHO INFO:CSV_2_Channel...
CALL %MYPYTHON% CSV_2_Channel.py channel_output_sorted.csv DVBS_sorted.xml --delimiter=;
IF %ERRORLEVEL% NEQ 0 GOTO labelerror
pause
@ECHO INFO:Debug_XML...
CALL %MYPYTHON% Debug_XML.py
IF %ERRORLEVEL% NEQ 0 GOTO labelerror
pause
GOTO labelfini
:labelerror
endlocal
@ECHO ERROR:Something wrong (return-code:%ERRORLEVEL%). Stop.
EXIT /B 1

:labelfini
endlocal
@ECHO Info:Done. Please review result!
EXIT /B 0


