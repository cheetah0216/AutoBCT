import web
import time

from prebuild import Report
from path import Path
from protocol import Protocol

urls = (
    '/path%(.*)', 'path',
    '/report%(.*)', 'report'
    )

class path:
  def GET(self, request_info):
    pro = Protocol(request_info)
    pro.ParsePathRequestInfo()

    path = Path(pro.releaseID)
    path.getPackageName()
    return path.componentName

class report:
  def GET(self, request_info):
    pro = Protocol(request_info)
    pro.ParseReportRequestInfo()

    build = Report(pro.releaseID, pro.checkInList)
    build.CheckPreBuildLists()
    return build.isApproved

if __name__ == "__main__":
  app = web.application(urls,globals())
  app.run()
