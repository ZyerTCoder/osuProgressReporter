@echo off
echo Starting osu!
echo.
start /b /wait C:\Users\AZM\AppData\Local\osu!\osu!.exe
python C:\Users\AZM\Documents\Python\progresstracker\osutracker.py
python C:\Users\AZM\Documents\Python\osuProgressReporter\osuProgressReporter.py -datapointsback 1
python C:\Users\AZM\Documents\Python\osuProgressReporter\osuProgressReporter.py
pause