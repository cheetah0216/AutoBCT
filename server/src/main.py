import web
import time
import prebuild

urls = (
    '/path%(.*)', 'path',
    '/report%(.*)', 'report'
    )

class path:
  def GET(self, release_id):
    return release_id

class report:
  def GET(self, release_id):
    bulid = prebuild.report(release_id)
    return release_id

if __name__ == "__main__":
  app = web.application(urls,globals())
  app.run()
