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
import sys
import os.path
import datetime

import gpx




# #############
# Funcion noela
# #############

def noela(di, persoa="pedro"):
    print("Noela di> %s %s." % (di, persoa))
    # Outra forma
    print("Noela repite> " + di + " " + persoa + ".")
    print("Esta dito.")


# ###############
# Test Code !!!!!
# ###############

def test(f):
    print "\n* GPX TestCase (This is an example!!)\n"

    print "Loading GPX file %s ..." % f
    fd = open(f)
    gpxparse = gpx.GPXParser(fd, f)
    gpxdata = gpxparse.gpx
    print gpxdata
    tracks = gpxdata.tracks
    for track in tracks:
        print "* Length: " 
        print track.lengthMinMaxTotal()
        print "* Times: "
        print track.timeMinMaxDuration()
        print "* Speed: " 
        print track.speedMinAvgMax()
    print "\n* End Tests!\n"

# Agora so tes que comentar o anterior e centrarte neste trozo de codio aqui
# ten coidado ca identacion, python e moi quisquilloso

#    max_delta = 300
#    tempo = "tempo a buscar"
#
#    tracksegs = []
#    for track in self.gpxdata.tracks:
#        if not track.status:
#            continue
#        tracksegs += track.closest(tempo, max_delta)
#    if len(tracksegs) == 0:
#        print("GPX non ten tracks!!")
#    else:
#        min_tdiff = datetime.timedelta.max
#        closed_point = None
#        for tragseg in tracksegs:
#            point = tragseg.closest(tempo)
#            delta = abs(point.time - tempo)
#            if delta < min_tdiff:
#                min_tdiff = delta
#                closed_point = point
#        self.dgettext['point_time'] = closed_point.time
#        if min_tdiff > max_delta:
#            print("Imposible atopar un punto preto de %s con delta %s" % (tempo, max_delta))
#        else:
#            print("Punto atopado!")
#            print(closed_point)



if __name__ == "__main__":
    test(sys.argv[1])

    # Usamos a funcion noela
    noela("Hola")
    noela("Hello", "jose")

    # Para usar a funcion esta, descomenta a seguinte liña e executa o programa: ./test.py  ruta.gpx  "olaaaaa"
    #noela(sys.argv[2])


#EOF
