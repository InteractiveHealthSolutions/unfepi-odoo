# -*- coding: utf-8 -*-
from odoo import http

# class Unfepi(http.Controller):
#     @http.route('/unfepi/unfepi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/unfepi/unfepi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('unfepi.listing', {
#             'root': '/unfepi/unfepi',
#             'objects': http.request.env['unfepi.unfepi'].search([]),
#         })

#     @http.route('/unfepi/unfepi/objects/<model("unfepi.unfepi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('unfepi.object', {
#             'object': obj
#         })