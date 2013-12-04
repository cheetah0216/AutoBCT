import web
import time

from prebuild import Report
from protocol import Protocol

urls = (
    '/path%(.*)', 'path',
    '/report%(.*)', 'report'
    )

class path:
  def GET(self, request_info):
    return request_info

class report:
  def GET(self, request_info):
    pro = Protocol(request_info)
    pro.ParseReportRequestInfo()

    build = Report(pro.releaseID, pro.checkInList)
    preBuildLists = build.CheckPreBuildLists()
    print build.viewCheckInList
    print build.checkInList
    return request_info

if __name__ == "__main__":
  app = web.application(urls,globals())
  app.run()
