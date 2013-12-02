import urllib
import urllib2
import cookielib
import json
import logging
import os
from time import gmtime, strftime, sleep
from ntlm import HTTPNtlmAuthHandler

class CQRelease(object):
  def __init__(self, release_id):
    self.release_id = release_id
    self._create_log_file(self.release_id)
    self._init_logger()
    self._init_http_info()

  def _create_log_file(self, release_id):
    if not os.path.exists('/opt/AutoBCT'):
        os.makedirs('/opt/AutoBCT')
    sysTime = strftime("%Y-%m-%d-%H%M%S_", gmtime())
    self.logPath = "/opt/AutoBCT/PreBuild_" + sysTime + format(release_id)
    open(self.logPath,'a+').close()

  def _init_logger(self):   
    self.logger = logging.getLogger(self.logPath)
    self.logger.setLevel(logging.DEBUG)
    self.logHandler = logging.FileHandler(self.logPath)
    self.logHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]  %(module)s:%(funcName)s:lineno %(lineno)d:  %(message)s')
    self.logHandler.setFormatter(formatter)
    self.logger.addHandler(self.logHandler)

  def _init_http_info(self):
    self.logger.info("init http info.")
    self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31 AlexaToolbar/alxg-3.1'
    }

  def getReleaseDetailInfo(self):
    cq_url = 'http://10.8.33.110/cqweb/'
    self._init_cookies(cq_url)
    self._login_cq(self.cj)
    self._connect_relDB()
    self._set_preferrnce()
    self._get_resourse_id()

  def _init_cookies(self, cq_url):
    self.logger.info("init cookies.")
    self.cj=cookielib.CookieJar()
    self.cookie_support= urllib2.HTTPCookieProcessor(self.cj)
    self.opener = urllib2.build_opener(self.cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(self.opener)
    result = urllib2.urlopen(cq_url)
    for index, cookie in enumerate(self.cj):
        #print index, cookie;
        self.cookies_jsessionid = cookie.value
        #print self.cookies_jsessionid
    self.logger.info("get cookies_jessionid is %s", format(self.cookies_jsessionid))

  def _login_cq(self, cj):
    self.logger.info("login CQ.")
    postdata=urllib.urlencode({
        'loginId':'fliu',
        'password':'',
        'repository':'VCNTR',
        'tzOffset':'GMT+8:00',
        'loadAllRequiredInfo':'true',
        'cquid':'00008PbQY_R5-CbM_zTT3LnfjWa:-1'
    })
    req = urllib2.Request(
        url = 'http://10.8.33.110/cqweb/cqlogin.cq?action=DoLogin',
        data = postdata,
        headers = self.headers
    )
    result = urllib2.urlopen(req).read()
    #print result
  
  def _connect_relDB(self):
    self.logger.info("connect release DB.")
    postdata=urllib.urlencode({
        'userDb':'RELDB',
        'loadAllRequiredInfo':'true',
        'cquid':self.cookies_jsessionid
    })
    req = urllib2.Request(
        url = 'http://10.8.33.110/cqweb/cqlogin.cq?action=DoConnect',
        data = postdata,
        headers = self.headers
    )
    result= urllib2.urlopen(req).read()
    for index, cookie in enumerate(self.cj):
      #print index, cookie;
      self.cookies_jsessionid = cookie.value
      #print self.cookies_jsessionid
    self.logger.info("get cookies_jessionid is %s", format(self.cookies_jsessionid))
    #print result

  def _set_preferrnce(self):
    self.logger.info("set preferrnce")
    postdata=urllib.urlencode({
        'prefData':'{"HIDDEN_FIELDS": {"FAVORITES": {"value": "%7B%0A%09%22identifier%22%3A%20%22stableLocation%22%2C%20%0A%09%22label%22%3A%20%22title%22%2C%20%0A%09%22items%22%3A%20%5B%0A%09%09%7B%0A%09%09%09%22type%22%3A%20%22LIST%22%2C%20%0A%09%09%09%22title%22%3A%20%22Open%20Releases%22%2C%20%0A%09%09%09%22stableLocation%22%3A%20%22cq.repo.cq-query%3A33567501%40VCNTR%2FRELDB%22%2C%20%0A%09%09%09%22friendlyLocation%22%3A%20%22cq.query%3APublic%20Queries%2FRelease%20Record%20Queries%2FOpen%20Releases%40VCNTR%2FRELDB%22%2C%20%0A%09%09%09%22masterReplica%22%3A%20%22%3Clocal%3E%22%2C%20%0A%09%09%09%22insertIndex%22%3A%20%22sortByAlpha%22%0A%09%09%7D%0A%09%5D%0A%7D"}, "STARTUP_QUERY": {"value": "%7B%22loginDate%22%3A%20%22Wed%2C%2010%20Jul%202013%2012%3A17%3A58%20GMT%22%7D"}}, "generalView": {"SHOW_PROPERTIES_VIEW": {"defaultValue": "false", "uiCTRL": "CHECKBOX", "value": "false", "possibleValues": "true$false"}, "LOAD_STARTUP_QUERY_RESULT": {"defaultValue": "true", "uiCTRL": "CHECKBOX", "value": "true", "possibleValues": "true$false"}}, "resultSetview": {"NUMBER_ROWS_PER_PAGE": {"defaultValue": "20", "uiCTRL": "COMBOBOX", "value": "20", "possibleValues": "20$50$100"}, "SHOW_SPLIT_VIEW": {"defaultValue": "single", "uiCTRL": "COMBOBOX", "value": "single", "possibleValues": "single$split"}, "SHOW_CUSTOM_RECORD_VIEW": {"defaultValue": "false", "uiCTRL": "CHECKBOX", "value": "false", "possibleValues": "true$false"}, "RESULTSET_DATE_FORMAT": {"defaultValue": "longDate", "uiCTRL": "COMBOBOX", "value": "longDate", "possibleValues": "longDate$mediumDate$shortDate"}, "SORT_SERVER_CLIENT": {"defaultValue": "client", "uiCTRL": "COMBOBOX", "value": "client", "possibleValues": "client$server"}}}',
        'cquid':self.cookies_jsessionid
    })
    req = urllib2.Request(
        url = 'http://10.8.33.110/cqweb/cquser.cq?action=setPreference',
        data = postdata,
        headers = self.headers
    )
    result = urllib2.urlopen(req).read()    
    for index, cookie in enumerate(self.cj):
      #print index, cookie;
      self.cookies_jsessionid = cookie.value
      #print self.cookies_jsessionid
    self.logger.info("get cookies_jessionid is %s", format(self.cookies_jsessionid))
    #print result

  def _get_resourse_id(self):
    postdate=urllib.urlencode({
        'action':'DoFindRecord',
        'recordId':self.release_id,
        'searchType':'BY_RECORD_ID',
        'cquid':self.cookies_jsessionid,
        'dojo.preventCache':'1373459717190'
    })
    request_url="http://10.8.33.110/cqweb/cqfind.cq?"+postdate
    result = urllib2.urlopen(request_url).read()
    #print result
    strlen=len(result)
    self.resourceID=result[33:strlen-2]
    #print self.resourceID
    self.logger.info("get resource id is %s .", format(self.resourceID))
