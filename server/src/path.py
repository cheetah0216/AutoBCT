import json
from release_info import CQRelease

class Path(CQRelease):
  def __init__(self, release_id):
    CQRelease.__init__(self, release_id)
    self.componentName = ''
    self.packageName = ''

  def getPackageName(self):
    self.logger.info("Start getPackageName")
    self.getReleaseDetailInfo()
    self._get_component_name(self.releaseInfo)

  def _get_component_name(self,releaseInfo):
    self.releaseJson = json.loads(releaseInfo)
    for item in self.releaseJson['fields']:
      if item['FieldName'] == 'Component':
        self.componentName = item['CurrentValue']
        break
