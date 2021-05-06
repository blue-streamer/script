import threading
import time
from Queue import Queue
import os
import sys
import subprocess
import hashlib
import re
import datetime

import httplib
import xml.parsers.expat
import xml.etree.ElementTree
import urllib

import SimpleHTTPServer
import SocketServer

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
