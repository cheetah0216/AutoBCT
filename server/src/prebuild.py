import urllib
import urllib2
import cookielib
import json
import logging
from time import gmtime, strftime
from ntlm import HTTPNtlmAuthHandler

class report:
  def __init__(self, release_id):
    '''
    init logger
    '''
    sysTime = strftime("%Y-%m-%d-%H:%M:%S_", gmtime())
    logPath = "/opt/AutoBCT/PreBuild_" + sysTime + format(release_id)
    open(logPath,'a+').close()

    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.DEBUG)
    self.logHandler = logging.FileHandler(logPath)
    self.logHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]   %(module)s %(name)s:%(funcName)s:%(lineno)d:  %(message)s')
    self.logHandler.setFormatter(formatter)
    self.logger.addHandler(self.logHandler)

    self.logger.info('hello!')
 
