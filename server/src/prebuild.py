import urllib
import urllib2
import cookielib
import json
import logging
import os
from time import gmtime, strftime, sleep
from ntlm import HTTPNtlmAuthHandler

from release_info import CQRelease

class Report(CQRelease):
  def __init__(self, release_id):
    CQRelease.__init__(self, release_id)

  def getPreBuildLists(self):
    self.logger.info("Start %s getPreBuildLists", self.release_id)
    self.getReleaseDetailInfo()
