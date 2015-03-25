#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import web

urls = ('/', 'index')


class index:

    def GET(self):
        return "Hello, world!"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
