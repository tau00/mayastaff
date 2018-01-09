# -------------------------------------------------------------------------------
# Name:        ply_importer
# Purpose:
#
# Author:      tau
#
# Created:     06-10-2015
# Copyright:   (c) tau 2015
# Licence:     copyrights
# -------------------------------------------------------------------------------
import math, struct, time
import numpy as np
import pymel.core as pm
import maya.mel as mel


def main():
    # read fileX:\CAMERA-DEPTH\vr\media\part_02\Right
    ply_file = open('Y:\REKONSTRUKCJA\LAS\LAS.ply', 'rb')
    #ply_file = open('X:\CAMERA_DEPTH\vr\media\part_02\Right\face.ply', 'rb')
    # przez header
    for num in range(0, 13):
        bytes_read = ply_file.readline()
    print (bytes_read)

    pos_xyz = np.array([[0, 0, 0]])
    color_rgb = np.array([[0, 0, 0]])

    licz = 0
    pos_xyz_str = ""
    # wczytywanie danych
    t0 = time.clock()
    while bytes_read:
        if licz % 100 == 0:
            bytes_read = ply_file.read(4)
            if bytes_read:
                x = struct.unpack('f', bytes_read)

            bytes_read = ply_file.read(4)
            if bytes_read:
                y = struct.unpack('f', bytes_read)

            bytes_read = ply_file.read(4)
            if bytes_read:
                z = struct.unpack('f', bytes_read)

            bytes_read = ply_file.read(4)
            if bytes_read:
                nx = struct.unpack('f', bytes_read)

            bytes_read = ply_file.read(4)
            if bytes_read:
                ny = struct.unpack('f', bytes_read)

            bytes_read = ply_file.read(4)
            if bytes_read:
                nz = struct.unpack('f', bytes_read)

            bytes_read = ply_file.read(1)
            if bytes_read:
                r = struct.unpack('B', bytes_read)

            bytes_read = ply_file.read(1)
            if bytes_read:
                g = struct.unpack('B', bytes_read)

            bytes_read = ply_file.read(1)
            if bytes_read:
                b = struct.unpack('B', bytes_read)

            pos_xyz_str = pos_xyz_str + " -p " + str(x[0]) + " " + str(y[0]) + " " + str(z[0]) + " "
            pos_xyz = np.append(pos_xyz, [[x[0], y[0], z[0]]], 0)
            color_rgb = np.append(color_rgb, [[r[0], g[0], b[0]]], 0)
        else:
            bytes_read = ply_file.read(27)
        licz += 1

    # print ("{0:.2f}".format(pos_xyz[19686][0]))
    expr = ""
    ilosc_elementow = len(pos_xyz)
    # print pos_xyz, ilosc_elementow
    print (time.clock() - t0)
    # print (float(color_rgb[222][0]/255.0), float(color_rgb[222][1]/255.0) ,float(color_rgb[222][2]/255.0) )
    # CREATE PARTICLE
    mel.eval("particle -n pointcloud " + pos_xyz_str)
    pm.mel.eval('addAttr -ln "rgbPP" -dt vectorArray pointcloudShape')
    pm.mel.eval('addAttr -ln "rgbPP0" -dt vectorArray pointcloudShape')
    # COLORIZE
    for id in range(1, ilosc_elementow):
        pm.select('pointcloudShape.pt[' + str(id - 1) + ']')
        r = color_rgb[id][0] / 255.0
        g = color_rgb[id][1] / 255.0
        b = color_rgb[id][2] / 255.0
        pm.setParticleAttr(at='rgbPP', vv=(r, g, b))
        # expr = "particle -e -id "+str(id)+" -at rgbPP -vv 0 0 1 pointcloud;"+expr
        expr = "setParticleAttr -at rgbPP -vv 1 0 1 pointcloudShape.pt[" + str(id) + "];" + expr
    expr = "\"" + expr + "\""
    mel.eval("dynExpression -c  -s " + expr + "  pointcloudShape")

    print ("total time " + str(time.clock() - t0))

    """
    print (pos_xyz)
    pm.particle( n=('Tetst') ,p=[ pos_str] )
    pm.mel.eval('addAttr -ln "rgbPP" -dt vectorArray TetstShape' )
    pm.mel.eval('addAttr -ln "rgbPP0" -dt vectorArray TetstShape')
    pm.select( 'TetstShape.pt[2]' )
    for
        pm.setParticleAttr( at='rgbPP', vv=(1, 0,0) )
    """
    ply_file.close()


if __name__ == '__main__':
    main()
