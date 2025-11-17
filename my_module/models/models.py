from odoo import models, fields

class Product(models.Model):
    _name = 'my_module.product'
    _description = 'Product'

    name = fields.Char(string="Product Name", required=True)
    price = fields.Float(string="Price")
    is_available = fields.Boolean(string="Available", default=True)
