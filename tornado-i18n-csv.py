#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.locale
import tornado.web

"""
☁  tornado-i18n  tree
.
├── locales    
│   ├── en_US.csv
│   ├── ja_JP.csv
│   └── zh_TW.csv
├── main.py
└── templates
    └── template.html

2 directories, 5 files
"""


class BaseHandler(tornado.web.RequestHandler):
    def get_user_locale(self):

        user_locale = self.get_argument('lang', None)
        if user_locale == 'en':
            return tornado.locale.get('en_US')
        elif user_locale == 'tw':
            return tornado.locale.get('zh_TW')
        elif user_locale == 'jp':
            return tornado.locale.get('ja_JP')


class ApiHandler(BaseHandler):
    def get(self, *args, **kwargs):
        _ = self.locale.translate
        print(tornado.locale.get_supported_locales())

        text = (u"原文: {} <br /><br />  译文: {} <p></p>"
                u"原文: {} <br /><br />  译文: {} <p></p>"
                u"原文: {} <br /><br />  译文: {} <p></p>").format(u"你好 世界", _(u"你好 世界"),
                                                               u"你好，世界", _(u"你好，世界"),
                                                               u"登录", _(u"登录"))
        self.finish(text)


class TemplateHandler(BaseHandler):
    """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Template</title>
    </head>
    <body>
        <p><label>原文</label>:你好 世界</p>
        <p><label>译文</label>:{{ _(u"你好 世界") }}</p>

        <p><label>原文</label>:你好，世界</p>
        <p><label>译文</label>:{{ _(u"你好，世界") }}</p>

        <p><label>原文</label>:登录</p>
        <p><label>译文</label>:{{ _(text) }}</p>
    </body>
    </html>
    """

    def get(self, *args, **kwargs):
        text = "登录"
        self.render('template.html', text=text)


class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers=[
            (r'/api', ApiHandler),
            (r'/template', TemplateHandler),
        ],
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            debug=True)


if __name__ == '__main__':
    app = Application()
    i18n_path = os.path.join(os.path.dirname(__file__), 'locales')
    # tornado.locale.load_gettext_translations(i18n_path, 'en_US')
    tornado.locale.load_translations(i18n_path)
    tornado.locale.set_default_locale('zh_CN')
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
