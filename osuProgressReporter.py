from math import ceil
import sys
import os
import argparse
import logging
import time
from win10toast import ToastNotifier

APP_NAME = "osuProgressReporter"
VERSION = 0
WORKING_DIR = r"C:\Users\AZM\Documents\Python\osuProgressReporter"
LOG_FILE = f'{APP_NAME}v{VERSION}log.txt'
DESCRIPTION = "osu progress reporter", "checks the output from the progress tracker to provide reports"

CSV_PATH = r"C:\Users\AZM\Documents\Python\progresstracker\5197321.csv"
CSV_COLUMNS = {
	"logtime":0,
	"totalhits":1,
	"hitsperplay":2,
	"hitspersecond":3,
	"averageplaylength":4,
	"userid":5,
	"username":6,
	"count300":7,
	"count100":8,
	"count50":9,
	"playcount":10,
	"rankedscore":11,
	"totalscore":12,
	"pprank":13,
	"level":14,
	"ppraw":15,
	"accuracy":16,
	"countss":17,
	"countssh":18,
	"counts":19,
	"countsh":20,
	"counta":21,
	"totalsecondsplayed":22,
	"ppcountryrank":23,
}

def sendWindowsToast(msg):
	toaster = ToastNotifier()
	toaster.show_toast("Osu Progress Report", msg, duration=4)

def getDiffFroTo(latest, earliest, csv):
	output = {}
	for key in CSV_COLUMNS:
		if key in ["username", "userid"]:
			output[key] = csv[-latest-1][CSV_COLUMNS[key]]
			continue
		if key in ["logtime", "hitsperplay", "hitspersecond", "averageplaylength", "level", "ppraw", "accuracy"]:
			output[key] = float(csv[-latest-1][CSV_COLUMNS[key]]) - float(csv[-earliest-1][CSV_COLUMNS[key]])
			continue
		output[key] = int(csv[-latest-1][CSV_COLUMNS[key]]) - int(csv[-earliest-1][CSV_COLUMNS[key]])
	return output

def main(args):
	with open(CSV_PATH) as f:
		csv = [s.strip().split(", ") for s in f.readlines()]

	diff = getDiffFroTo(0, args.datapointsback, csv)
	#print(diff)

	hitsperplay = float(csv[-1][CSV_COLUMNS["hitsperplay"]])
	hitsperplayrange = diff["totalhits"]/diff["playcount"]

	_pc = int(csv[-1][CSV_COLUMNS["playcount"]])
	_th = int(csv[-1][CSV_COLUMNS["totalhits"]])
	playsto1000 = (1000*_pc-_th)/(hitsperplayrange-1000)
	playsto800 = (800*_pc-_th)/(hitsperplayrange-800)

	msg = f"""
You're at {round(hitsperplay,2)} hits per play.
In the past {args.datapointsback} data points you have:
{round(hitsperplayrange,2)} average hits per play
{diff["playcount"]} plays submitted
{round(diff["totalsecondsplayed"]/3600, 2)} hours played 
{diff["totalhits"]} objects clicked
Hits per play changed by {round(diff["hitsperplay"], 2)}
At this rate it'll take {ceil(playsto800)} plays to reach 800 hits per play
and {ceil(playsto1000)} plays to reach 1000 hits per play
"""
	if args.toasted:
		sendWindowsToast(msg)
	print(msg)
	return 1

if __name__ == '__main__':
	t0 = time.time()
	os.chdir(WORKING_DIR)

	# parse input
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	parser.add_argument("-log", type=str, default="INFO", help="set log level for console output, WARNING/INFO/DEBUG")
	parser.add_argument("-logfile", type=str, default="DEBUG", help="sets file logging level, 0/CRITICAL/ERROR/WARNING/INFO/DEBUG, set to 0 to disable")
	parser.add_argument("-datapointsback", type=int, default=7, help="how many data points back to go to from the latest data point")
	parser.add_argument("-toasted", type=bool, default=False, help="whether to send a windows toaster notification with the results")
	args = parser.parse_args()

	# setting up logger to info on terminal and debug on file
	log_format=logging.Formatter(f'%(asctime)s {APP_NAME} v{VERSION} %(levelname)s:%(name)s:%(funcName)s %(message)s')
	
	if args.logfile != "0":
		file_handler = logging.FileHandler(filename=LOG_FILE, mode="a")
		file_handler.setLevel(getattr(logging, args.logfile.upper()))
		file_handler.setFormatter(log_format)
		logging.getLogger().addHandler(file_handler)
	
	stream_handler = logging.StreamHandler(sys.stdout)
	stream_handler.setLevel(getattr(logging, args.log.upper()))
	logging.getLogger().addHandler(stream_handler)

	if args.logfile != "0":
		logging.getLogger().setLevel(getattr(logging, args.logfile.upper()))
	else:
		logging.getLogger().setLevel(getattr(logging, args.log.upper()))

	logging.debug(f"Started with arguments: {sys.argv}")

	main(args)

	logging.info(f"Exited. Ran for {round(time.time() - t0, 3)}s")