#!/usr/bin/env python3
import subprocess
import json
import select

command = "/usr/bin/gpspipe -w".split()

process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

try:
    while True:
        # wait for available data on stdout with a one second timeout
        rlist, _, _ = select.select([process.stdout], [], [], 1)
        if process.stdout in rlist:
            # read one line, strip it and parse the json
            line = process.stdout.readline().strip()
            line = json.loads(line)
            # dismiss everything that's not of class "SKY"
            if line.get("class") == "SKY":
                # see https://docs.checkmk.com/latest/en/localchecks.html for documentation
                print(f'P "GPSD" satellites_used={line.get("uSat")};4:;2:|satellites_visible={line.get("nSat")} '
                      f'Used Satellites: {line.get("uSat")}, Visible Satellites: {line.get("nSat")}')
                # we're done.
                exit(0)
        else:
            # we get here only when there was a timeout which means no data from gpsd
            print('P "GPSD" satellites_used=0;4:;2:|satellites_visible=0 No data from GPSD!')
            exit(1)

except KeyboardInterrupt:
    pass
