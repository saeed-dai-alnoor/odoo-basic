# models/tree_note.py
from odoo import models, fields

class TreeNote(models.Model):
    _name = 'tree.note'
    _description = 'Tree Notes'

    title = fields.Char(string='Note Title')
    description = fields.Text(string='Description')

    # العلاقة العكسية Many2one
    plant_id = fields.Many2one(
        'tree.plant',
        string='Tree',
        ondelete='cascade'
    )
