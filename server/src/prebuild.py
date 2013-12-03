import json
import logging
import urllib2
from ntlm import HTTPNtlmAuthHandler

from release_info import CQRelease

class Report(CQRelease):
  def __init__(self, release_id):
    CQRelease.__init__(self, release_id)
    self.prepBuildReportUrl = ''

  def CheckPreBuildLists(self):
    self.logger.info("Start CheckPreBuildLists")
    self.getReleaseDetailInfo()
    self._get_prebuild_report()
    #self._get_check_in_lists()
    #self._is_prebulid_approved()
  
  def _get_prebuild_report(self):
    self._get_prebuild_report_url(self.releaseInfo)

    user = 'COMVERSE\\fliu'
    password = 'null'
    url =  self.prepBuildReportUrl.strip()
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, user, password)
    # create the NTLM authentication handler
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
    # create and install the opener
    opener = urllib2.build_opener(auth_NTLM)
    #urllib2.install_opener(opener)
    # retrieve the result
    #response = urllib2.urlopen(url)
    #result = response.read()
    result = opener.open(url).read()
    print result


  def _get_prebuild_report_url(self, releaseInfo):
    self.releaseJson = json.loads(releaseInfo)
    for item in self.releaseJson['fields']:
        prebReadyLineNum = 0
        prebReady = '<Prebuild_Ready>'
        url = 'http://'
        if item['FieldName'] == 'Notes_Log':
          for noteLog in item['CurrentValue']:
            prebReadyLineNum = prebReadyLineNum + 1
            if prebReady in noteLog:
              for prebReportUrl in item['CurrentValue'][prebReadyLineNum+1:len(item['CurrentValue'])]:
                if url in prebReportUrl:
                  self.prepBuildReportUrl = prebReportUrl
                  break
              break
          break
    if self.prepBuildReportUrl == '':
      self.logger.error("prebuid report url is null") 
    else:
      self.logger.info("get prebuid report url is %s",self.prepBuildReportUrl)
