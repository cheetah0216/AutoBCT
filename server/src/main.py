import web
import time

urls = (
    '/path', 'path',
    '/report', 'report'
    )

class path:
  def GET(self):
    time.sleep(10)
    return "path"

class report:
  def GET(self):
    return "report"

if __name__ == "__main__":
  app = web.application(urls,globals())
  app.run()
