# YAESU-FT-991a-Radio-Backup-and-Restore
YAESU FT-991a Radio Backup and Restore, reads and writes all radio settings


Assumes that the baud rate is 38400

read_settings.py (exe) will prompt for the Enhanced Comm Port. Select by entering the item number from the list.
A file is created "File_date.txt" that contains all 157 parameters from the FT-991a

To restore the FT-991a to these saved settings, write_settings.py (exe), select the Comm Port, then select the file.
(There can be multiple files saved for various setups, so choose from the list by date.

Hope you find this helpful,
73
WR9R
