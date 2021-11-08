#!/usr/bin/env python3

import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1

accesslog = '-' # log stdout to stdout
errorlog = '-' # log stderr to stdout 
loglevel = 'info' # one of: debug, info, warning, error, critical

