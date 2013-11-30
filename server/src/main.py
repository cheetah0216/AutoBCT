import web
import time

urls = (
    '/path%(.*)', 'path',
    '/report(.*)', 'report'
    )

class path:
  def GET(self, release_id):
    return release_id

class report:
  def GET(self, release_id):
    return release_id

if __name__ == "__main__":
  app = web.application(urls,globals())
  app.run()
