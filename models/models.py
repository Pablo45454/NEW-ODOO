# -*- coding: utf-8 -*-
import math
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from random import *
import random

class player(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Players'

    #name = fields.Char()
    password = fields.Char()
    nivel = fields.Integer(default = 1, readonly="True")
    hp = fields.Integer(compute="_get_hp")
    fuerza = fields.Integer(compute="_get_fuerza")
    destreza = fields.Integer(compute="_get_destreza")
    avatar = fields.Image(max_width=200,max_height=360)
    damage = fields.Integer(compute="_get_damage", default=0)
    is_player = fields.Boolean(default="false")
    fecha = fields.Date(default=datetime.now(), readonly="True")
    comentario = fields.Char()
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
    comentario = fields.Char(default="",readonly="true")

    tienda = fields.Many2many("warrior.arma", compute="_get_armas")

    zona_name = fields.Char(related="zona.name")
    zona_avatar = fields.Image(max_width=120, max_height=80,related="zona.avatar")
    zona_dificultad = fields.Selection(related="zona.dificultad")

    def generate_fight(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'warrior.battle_wizard',
            'context': {'player_id': self.id},
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }
    @api.onchange('clase')
    def onchange_arma(self):
        for s in self:
            if s.clase.name == "Bandido":
                s.write({'comentario': "Clase con buen manejo de armas"})
            if s.clase.name == "Samurai":
                s.write({'comentario': "Clase con buena destreza"})
            if s.clase.name == "Guerrero":
                s.write({'comentario': "Clase con buenas estadísticas"})
            if s.clase.name == "Cazador":
                s.write({'comentario': "Clase con buena destreza pero poca vida"})
            if s.clase.name == "Vikingo":
                s.write({'comentario': "Clase con buena fuerza y mucha vida"})



    def dame_xp(self):
        for s in self:
            s.xp += 10000;

    def _first_zone(self):
        return self.env['warrior.zona'].search([])[0]

    zona = fields.Many2one("warrior.zona", default=_first_zone)

    @api.constrains('nivel')
    def _get_damage(self):
        for s in self:
            if s.arma.afinidad == "1":
                s.damage = s.arma.damage + s.fuerza
            if s.arma.afinidad == "2":
                s.damage = s.arma.damage + s.destreza
            if s.arma.afinidad == "3":
                s.damage = s.arma.damage + s.fuerza + s.destreza
            if s.arma.afinidad == "4":
                s.damage = s.arma.damage

    def _get_armas(self):
        for s in self:
            s.tienda = s.env['warrior.arma'].search([])


    def aumentar_nivel(self):
        for s in self:
            if s.xp > s.xp_required:
                lvl = (s.nivel + 1)
                s.write({'nivel': lvl})
                s.xp -= s.xp_required
            else:
                raise ValidationError("No tienes suficiente xp")



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


    @api.model
    def give_xp(self):
        players = self.env['res.partner'].search([])
        for player in players:
            player.xp += 5


class player_wizard(models.TransientModel):
    _name = 'warrior.player_wizard'
    _description = 'Wizard per crear players'


    name = fields.Char()
    password = fields.Char()
    avatar = fields.Image(max_width=200, max_height=200)
    is_player = fields.Boolean(default=False)
    clase = fields.Many2one("warrior.clase")
    def create_player(self):
        self.ensure_one()
        self.env['res.partner'].create({
                            'name':self.name,
                            'password': self.password,
                            'avatar': self.avatar,
                            'is_player': True,
                            'clase': self.clase.id,
                         })



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

    def comprar_arma(self):
            for s in self:
                player_id = self.env['res.partner'].browse(self._context.get('active_id'))
                if player_id.xp > s.precio:
                    player_id.xp -= s.precio
                    player_id.arma = s.id
                else:
                    raise ValidationError("No tienes suficiente xp")
class zona(models.Model):
    _name = 'warrior.zona'
    _description = 'Zona'

    name = fields.Char(required=True)
    avatar = fields.Image(max_width=300, max_height=200)
    dificultad = fields.Selection([('1', 'Principiante'), ('2', 'Intermedio'), ('3', 'Avanzado'), ('4', 'Experimentado'), ('5', 'Leyenda')])

class mob(models.Model):
    _name = 'warrior.mob'
    _description = 'Mob'

    name = fields.Char(required=True)
    avatar = fields.Image(max_width=300, max_height=200)
    hp = fields.Integer()
    damage = fields.Integer()
    armadura = fields.Integer()
    zona = fields.Many2one("warrior.zona")

class battle(models.Model):
    _name = 'warrior.battle'
    _description = 'Battle'

    player1 = fields.Many2one('res.partner')
    player2 = fields.Many2one('res.partner')
    winner = fields.Char()
    xp_earned = fields.Integer()

class battle_mob(models.Model):
    _name = 'warrior.battle_mob'
    _description = "Batalla Mob"

    zona = fields.Many2one('warrior.zona')
    player = fields.Many2one('res.partner')
    mob = fields.Many2one('warrior.mob')
    winner = fields.Char()
    xp_earned = fields.Integer()

class battle_mob_wizard(models.TransientModel):
    _name = 'warrior.battle_mob_wizard'
    _description = "Wizard batalla Mob"

    zona = fields.Many2one('warrior.zona')
    player = fields.Many2one('res.partner')
    mob = fields.Many2one('warrior.mob')


class battle_wizard(models.TransientModel):
    _name = 'warrior.battle_wizard'
    _description = 'Wizard batalla'

    def _get_player(self):
        return self.env['res.partner'].search([('id', "=", self.env.context.get('player_id'))])

    player1 = fields.Many2one('res.partner', readonly=True, domain="[('is_player','=',True)]", ondelete='cascade',
                             default=_get_player)
    player2 = fields.Many2one('res.partner', domain="[('is_player','=',True), ('id', '!=', player1)]")


    def _get_damage(self, atacante, defensor):
        dano = random.randint(0,atacante.damage) - defensor.armadura
        if dano < 0:
            dano = 0
        return dano
    def battle_player(self):
        for s in self:
            player1 = self.player1
            player2 = self.player2
            player1_hp = player1.hp
            player2_hp = player2.hp
            xp_earned = 0
            winner = ""
            while player1_hp > 0 and player2_hp > 0:
                # Turno de player1
                dano = self._get_damage(player1, player2)
                player2_hp -= dano
                print("Vida Player 2: " + str(player2_hp))
                if player2_hp <= 0:
                    break
                # Turno de player2
                dano = self._get_damage(player2, player1)
                player1_hp -= dano
                print("Vida Player 1: " + str(player1_hp))
            if player1_hp <= 0:
                player1.comentario = '¡Perdiste!'
                player2.xp += player1.xp/2
                player2.comentario = '¡Ganaste!'
                player1.xp -= player1.xp / 2
                xp_earned = player1.xp / 2
                winner = player2.name
            elif player2_hp <= 0:
                player2.comentario = '¡Perdiste!'
                player1.comentario = '¡Ganaste!'
                player1.xp += player2.xp / 2
                player2.xp -= player2.xp / 2
                xp_earned = player2.xp / 2
                winner = player1.name

            print(winner)
            print(xp_earned)

            self.env['warrior.battle'].create({
                'player1': self.player1.id,
                'player2': self.player2.id,
                'xp_earned': xp_earned,
                'winner': winner,
            })


