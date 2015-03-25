#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import web
urls = (
    '/', 'Index',
)

class Index:
    def GET(self):
        return "test"

if __name__ == '__main__':

    app = web.application(urls, globals())
    app.run()
