class Protocol:
  def __init__(self,request_info):
    self.requestInfo = request_info
    self.releaseID = ''
    self.checkInList = []

  def ParseReportRequestInfo(self):
    reqInfo =  self.requestInfo.split('&&')
    self.releaseID = reqInfo[0]
    srcCheckInList = reqInfo[1]
    for info in srcCheckInList.split('&'):
      fileinfo = info.split(';')
      checkInDic = dict(
          filepath=fileinfo[0],
          version=fileinfo[1],
          comment=fileinfo[2]
          )
      self.checkInList.append(checkInDic)
