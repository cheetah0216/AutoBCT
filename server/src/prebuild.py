import json
import logging
import urllib2
from ntlm import HTTPNtlmAuthHandler
from bs4 import BeautifulSoup

from release_info import CQRelease

class Report(CQRelease):
  def __init__(self, release_id, checkInList):
    CQRelease.__init__(self, release_id)
    self.viewCheckInList = checkInList
    self.prepBuildReportUrl = ''
    self.prepBuildReportInfo = ''
    self.srcCheckInList = []
    self.checkInList = []
    self.isApproved = 'true'

  def CheckPreBuildLists(self):
    self.logger.info("Start CheckPreBuildLists")
    self.getReleaseDetailInfo()
    self._get_prebuild_report()
    self._get_check_in_lists(self.prepBuildReportInfo)
    self._is_prebulid_approved()
     
  def _get_prebuild_report(self):
    self._get_prebuild_report_url(self.releaseInfo)

    user = 'COMVERSE\\fliu'
    password = 'lf'
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
    self.prepBuildReportInfo = opener.open(url).read()

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

  def _get_check_in_lists(self, reportHTML):
    self._prep_prepbuild_report(reportHTML)
    index = 4;
    while index < len(self.srcCheckInList):
      if self.srcCheckInList[index] != self.srcCheckInList[5]:
        checkInDic = dict(
            filepath=self.srcCheckInList[index-1].strip().replace('\\','/'),
            version=self.srcCheckInList[index].strip(),
            comment=self.srcCheckInList[index+1].strip()
            )
        self.checkInList.append(checkInDic)
      index = index + 3

  def _prep_prepbuild_report(self, reportHTML):
    reportHTML = reportHTML.replace("<br>", "")
    soup = BeautifulSoup(reportHTML)
    for tr in soup.table:
      tmp = tr
      break
    for tr in soup.table:
      if tr != tmp:
        for td in tr:
          tmp = td
          break
        for td in tr:
          if td != tmp:
            self.srcCheckInList.append(td.string)
 
  def _is_prebulid_approved(self):
    self.isApproved = 'true'
    for viewFileInfo in self.viewCheckInList:
      flag = self._is_file_in_checkin_list(viewFileInfo)
      if flag == 'false':
        self.isApproved = 'false'
        self.logger.error("%s:%s/%s is not in check in lists.",\
            viewFileInfo['comment'],\
            viewFileInfo['filepath'],\
            viewFileInfo['version'],\
            )
    self.logger.info("isApproved: %s", self.isApproved)
    return self.isApproved

  def _is_file_in_checkin_list(self,viewFileInfo):
    flag = 'false'
    for fileInfo in self.checkInList:
      if viewFileInfo['filepath'] in fileInfo['filepath'] and \
          viewFileInfo['version'] == fileInfo['version'] and \
          viewFileInfo['comment'] in fileInfo['comment']:
        flag = 'true'
        break
    return flag
