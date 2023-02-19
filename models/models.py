# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
    _name = 'warrior.player'
    _description = 'Players'

    name = fields.Char()

class clase(models.Model):
    _name = 'warrior.clase'
    _description = 'Clases'

    name = fields.Char()
    hp = fields.Integer()
    fuerza = fields.Integer()
    destreza = fields.Integer()
    armadura = fields.Integer()
    avatar = fields.Image(max_width=200, max_height=200)

class arma(models.Model):
    _name = 'warrior.arma'
    _description = 'Arma'

    damage = fields.Integer()
    name = fields.Char(required=True)
    avatar = fields.Image(max_width=100, max_height=100)
    afinidad = fields.Selection([('1', 'Fuerza'), ('2', 'Destreza'), ('3', 'Ambos')])
    precio = fields.Integer()