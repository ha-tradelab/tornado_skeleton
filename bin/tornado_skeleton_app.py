# coding: utf-8
"""
Launch the TornadoSkeleton API.
"""

import os
import sys
from optparse import OptionParser

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path + '/../')
os.chdir(path + '/../')
from tornado_skeleton.api import TornadoSkeletonAPI


parser = OptionParser()

parser.add_option("-e", "--env",
                  dest="env", default='',
                  help="Specify the environment (dictates the configuration file name)")

parser.add_option("-p", "--path",
                  dest="path", default='',
                  help="Specify the path for resources")

options, _ = parser.parse_args()

if options.env == 'local':
    options.path = ''

TornadoSkeletonAPI(options.path, options.env).start()
