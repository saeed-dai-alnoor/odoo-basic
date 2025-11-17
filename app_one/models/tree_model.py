from odoo import models, fields

class TreePlant(models.Model):
    _name = 'tree.plant'
    _description = 'Tree Plant'

    name = fields.Char(string='Tree Name', required=True)
    type = fields.Char(string='Type')
    category = fields.Selection([
        ('fruit', 'Fruit'),
        ('shade', 'Shade'),
        ('ornamental', 'Ornamental')
    ], string='Category')
    region = fields.Char(string='Region')
    governorate = fields.Char(string='Governorate')
     # العلاقة One2many مع الموديل الثاني
    notes_ids = fields.One2many(
        'tree.note',        # اسم الموديل الثاني
        'plant_id',         # الحقل العكسي في الموديل الثاني
        string='Notes'
    )
