import web
import time
from prebuild import Report

urls = (
    '/path%(.*)', 'path',
    '/report%(.*)', 'report'
    )

class path:
  def GET(self, release_id):
    return release_id

class report:
  def GET(self, release_id):
    bulid = Report(release_id)
    preBuildLists = bulid.CheckPreBuildLists()
    return preBuildLists

if __name__ == "__main__":
  app = web.application(urls,globals())
  app.run()
