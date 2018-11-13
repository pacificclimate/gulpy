# gulpy

## Purpose
The scripts in this repository insert observations made by weather stations into PCIC's CRMP or MSC databases.

`import_bch_flat.py` reads a file containing a list of datafiles, one per line. An example filelist:

```
/home/user/data/datafile1.csv
/home/user/data/datafile2.csv
/home/user/data/datafile3.csv
```
Each datafile is a CSV where each line represents a single observation made by a weather station. The datafile has the following columns, separated by commas:
* history_id - the numerical ID of the weather station placement making the observation, corresponding to the pre-existing station history ID in the database
* obs_time - time the measurement was made, in the form "YYYY-MM-DD HH:MM:SS"
* datum - a number; the actual value of the observation 
* vars_id - a numerical id representing the type of observation (temperature, precipitation, wind speed, etc) made by the station, corresponding to that variable type's pre-existing ID in the database

An example datafile:
```
"history_id","obs_time","datum","vars_id"
5812,"2015-10-22 20:00:00",72,1301
5812,"2015-10-22 21:00:00",70,1301
5812,"2015-10-22 22:00:00",70,1301
5812,"2015-10-22 23:00:00",71,1301
5812,"2015-10-23 00:00:00",62,1301

```
The BCH package inserts observations from each datafile into the database.

## Installation

We recommend using a python virtual environment for consistency and repeatability.

```bash
git clone https://github.com/pacificclimate/gulpy
cd gulpy
virtualenv venv
source venv/bin/activate
pip install -i https://pypi.pacificclimate.org/simple/ .
```

## Use
The `import_bch_flat` script accepts the following arguments:

### -c CONNECTION, --c CONNECTION_STRING (required)
The connection string gives the address of the database to add data to, using the form `dialect://username:password@host/database`. For example, the MSC database would be `postgresql://msc_rw:PASSWORD@dbmsc.pcic.uvic.ca/msc`

### filelist (required)
The location of a filelist containing the name of one datafile per line.

### -b SIZE, --batch_size SIZE (optional)
Control how many inputs will be committed in each batch. The default is 250. Smaller batch sizes prevent running out of database resource locks when running the script in parallel; larger batch sizes allow the script to run faster if it is expected to be the only thing interacting with the database.

### -D, --diagnostic (optional)
Turn on Diagnostic Mode. In Diagnostic Mode, no data will be added to the database. Allows checking inputs without actually committing them.

### -l LEVEL, --log_level LEVEL (optional)
Control the verbosity of log output. In order from most to least verbose, the log levels are: DEBUG, INFO, WARNING, ERROR, CRITICAL

### -h, --help (optional)
Display a help message and exit without opening files or making database changes.

## Troubleshooting
Running this script using python 3 instead of python 2 may result in the following error:

```
_csv.Error: iterator should return strings, not bytes (did you open the file in text mode?)
```