#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Copyright 2010-2015 Jose Riguera Lopez <jriguera@gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from __future__ import print_function

import sys
import os.path
import datetime
import time

import gpx



def get_closed_tracksegs(gpxdata, tdate, delta):
    tracksegs = []
    for track in gpxdata.tracks:
        if not track.status:
            continue
        tracksegs += track.closest(tdate, delta)
    return tracksegs


def match(gpxdata, datetimes, tdelta, keep=True):
    result = []
    tracksegs = []
    result = []
    for dt in datetimes:
        if not tracksegs:
            tracksegs = get_closed_tracksegs(gpxdata, dt, tdelta)
        if not tracksegs:
            print("* Erro: non hai segmentos para tempo <%s> con delta <%s>!" % (dt, tdelta), file=sys.stderr)
            if keep:
                result.append((dt, None, None))
            continue
        else:
            min_tdiff = datetime.timedelta.max
            closed_point = None
            closed_tragseg = 0
            for index, tragseg in enumerate(tracksegs):
                point = tragseg.closest(dt)
                delta = abs(point.time - dt)
                if delta < min_tdiff:
                    min_tdiff = delta
                    closed_point = point
                    closed_tragseg = index
            # closed_point.time
            if min_tdiff > max_delta:
                # Resetease todo para forzar a busqueda no seguinte punto
                closed_tragseg = 0
                tracksegs = []
                print("* Erro: non se atopou un punto en <%s> con delta <%s>!", file=sys.stderr)
                if keep:
                    result.append((dt, None, None))
            else:
                # A lista the tracksegs mantense
                tracksegs = tracksegs[closed_tragseg:]
                result.append((dt, closed_point, min_tdiff))
    return result


# Formatos: https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
# https://docs.python.org/2/library/string.html#format-examples
def print_output(result, fd, separator=',', dt_format="%Y-%m-%d %H:%M:%S", point_format="{lat} {lon} {time}", print_diff=True):
    for item in result:
        tdate, point, tdiff = item
        printed = []
        printed.append(tdate.strftime(dt_format))
        if point:
            printed.append(point_format.format(lat=point.lat, lon=point.lon, ele=point.ele, time=point.time.strftime(dt_format)))
            if print_diff:
                printed.append("%d" % tdiff.total_seconds())
        print(separator.join(printed), file=fd)


def read_gpx(fgpx):
    gpxdata = None
    with open(fgpx, "r") as fd:
        gpxparse = gpx.GPXParser(fd, fgpx)
        gpxdata = gpxparse.gpx
    print("* Lin datos GPX de %s" % fgpx, file=sys.stderr)
    return gpxdata


def read_datetimes(fcsv, tzdiff, dt_format='%d/%m/%y,%H:%M:%S'):
    index = 1
    result = None
    with open(fcsv, "r") as fd:
        result = []
        for line in fd:
            try:
                ttime = time.strptime(line.strip(), dt_format)
                dtime = datetime.datetime.fromtimestamp(time.mktime(ttime))
                dtime = dtime + tzdiff
            except Exception as e:
                print("* Non entendo a linha %d no CSV: %s" % (index, str(e)), file=sys.stderr)
            else:
                result.append(dtime)
            finally:
                index += 1
    print("* Lin %d linhas no CSV %s" % (index, fcsv), file=sys.stderr)
    return result


# cambia estes 2 numeros para variar o maximo tempo que busca e a differencia
# de tempo entre o GPX (normalmente en UTC) e o teu CSV (que creo que e local, noutro caso pon 0)
def main(fgpx, fcsv, maxdiffseconds=300, utcdiffminutes=-120):
    delta = datetime.timedelta(seconds=maxdiffseconds)
    tzdiff = datetime.timedelta(minutes=utcdiffminutes)
    gpxdata = read_gpx(fgpx)
    datetimes = read_datetimes(fcsv, tzdiff)
    resultado = match(gpxdata, datetimes, delta, True)
    print_output(resultado, sys.stdout)


# O programa executase asi: ./match.py Track_2016-09-10-165617.gpx  proba.csv > saida.csv
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

