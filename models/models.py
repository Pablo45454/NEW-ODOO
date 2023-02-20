# -*- coding: utf-8 -*-
import math
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class player(models.Model):
    _name = 'warrior.player'
    _description = 'Players'

    name = fields.Char()
    password = fields.Char()
    nivel = fields.Integer(default = 1, readonly="True")
    hp = fields.Integer(compute="_get_hp")
    fuerza = fields.Integer(compute="_get_fuerza")
    destreza = fields.Integer(compute="_get_destreza")
    avatar = fields.Image(max_width=200,max_height=360)

    def _first_weapon(self):
        return self.env['warrior.arma'].search([])[6]

    arma = fields.Many2one("warrior.arma", default=_first_weapon, readonly="True")
    clase = fields.Many2one("warrior.clase")
    xp = fields.Integer(default=0)
    armadura = fields.Integer(related="clase.armadura")
    xp_required = fields.Integer(default=200, compute="_get_xp_required")
    avatar_clase = fields.Image(max_width=200, max_height=200, related="clase.avatar")

    arma_avatar = fields.Image(max_width=80, max_height=80, related="arma.avatar")
    arma_name = fields.Char(related="arma.name")
    arma_precio = fields.Integer(related="arma.precio")
    arma_damage = fields.Integer(related="arma.damage")
    arma_afinidad = fields.Selection(related="arma.afinidad")

    tienda = fields.Many2one("warrior.arma")

    def aumentar_nivel(self):
        for s in self:
            lvl = (s.nivel + 1)

            s.write({'nivel': lvl})

    def disminuir_nivel(self):
        for s in self:
            lvl = (s.nivel - 1)

            s.write({'nivel': lvl})

    @api.constrains('nivel')
    def _min_lvl_exceeded(self):
        for s in self:
            if s.nivel < 1:
                raise ValidationError("Has excedido el nivel minimo: %s " % s.nivel + 1)

    @api.constrains('nivel')
    def _max_lvl_exceeded(self):
        for s in self:
            if s.nivel > 99:
                raise ValidationError("Has excedido el nivel maximo: %s " % s.nivel - 1)

    @api.depends('nivel')
    def _get_xp_required(self):
        for s in self:
            self.xp_required = 200 * math.pow(1 + (0.075), self.nivel - 1)

    @api.depends('nivel')
    def _get_hp(self):
        for player in self:
            self.hp = self.clase.hp + (10 * (player.nivel - 1))

    @api.depends('nivel')
    def _get_fuerza(self):
        for player in self:
            self.fuerza = self.clase.fuerza + (1 * (player.nivel - 1))

    @api.depends('nivel')
    def _get_destreza(self):
        for player in self:
            self.destreza = self.clase.destreza + (1 * (player.nivel - 1))


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
    afinidad = fields.Selection([('1', 'Fuerza'), ('2', 'Destreza'), ('3', 'Ambos'), ('4', 'Ninguna')])
    precio = fields.Integer()