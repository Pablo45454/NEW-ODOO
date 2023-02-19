# -*- coding: utf-8 -*-
# from odoo import http


# class Warrior(http.Controller):
#     @http.route('/warrior/warrior', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/warrior/warrior/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('warrior.listing', {
#             'root': '/warrior/warrior',
#             'objects': http.request.env['warrior.warrior'].search([]),
#         })

#     @http.route('/warrior/warrior/objects/<model("warrior.warrior"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('warrior.object', {
#             'object': obj
#         })
