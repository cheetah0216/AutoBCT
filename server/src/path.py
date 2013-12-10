import json
from release_info import CQRelease

class Path(CQRelease):
  def __init__(self, release_id):
    CQRelease.__init__(self, release_id)
    self.funcDict = {
        'Rating Billing Backend AIX':self._get_RBB_package_path,
        'KID':self._get_KID_package_path
        }
    self.componentName = ''
    self.packageName = ''
    self.packageFullName = ''

  def getPackagePath(self):
    self.logger.info("Start getPackageName")
    self.getReleaseDetailInfo()
    self._get_component_name(self.releaseInfo)
    self._get_package_path(self.componentName)

  def _get_component_name(self,releaseInfo):
    self.releaseJson = json.loads(releaseInfo)
    for item in self.releaseJson['fields']:
      if item['FieldName'] == 'Component':
        self.componentName = item['CurrentValue']
        self.logger.info('get Component name is %s', self.componentName)
        break
    if self.componentName == '':
      self.logger.error('Can not get component.')

  def _get_package_path(self,componentName):
    if componentName != '':
      self.logger.info('Start get %s package full path.', componentName)
      self.funcDict[componentName]()

  def _get_package_path_base(self,packagePath,packageName):
    for item in self.releaseJson['fields']:
      lineNum = 0
      if item['FieldName'] == 'Notes_Log':
        for noteLog in item['CurrentValue']:
          lineNum = lineNum + 1
          if packagePath in noteLog:
            for name in item['CurrentValue'][lineNum+1:len((item['CurrentValue']))]:
              #print noteLog
              #print name
              if packageName in name:
                self.packageFullName = noteLog.strip() + '/' + name.split(' ')[-1].strip().replace('*','')
                break
            break
        break

  def _get_RBB_package_path(self):
    packagePath = '/proj/CBS/DIT/'
    packageName = 'RATING_BILLING_BACKEND'
    self._get_package_path_base(packagePath, packageName)

    if self.packageFullName == '':
      self.logger.error('Can not get RBB package full path')
    else:
      self.logger.info('get RBB package full path is: %s', self.packageFullName)

  def _get_KID_package_path(self):
    packagePath = '/proj/CBS/DIT/'
    packageName = 'KID'
    self._get_package_path_base(packagePath, packageName)

    if self.packageFullName == '':
      self.logger.error('Can not get KID package full path')
    else:
      self.logger.info('get KID package full path is: %s', self.packageFullName)
