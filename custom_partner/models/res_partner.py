from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random
import string

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # حقل Customer Code
    customer_code = fields.Char(
        string='Customer Code',
        copy=False,
        readonly=True,
        index=True
    )

    # قيود SQL: رقم الموبايل والكود فريد
    _sql_constraints = [
        ('mobile_unique', 'unique(mobile)',
         _('The mobile number must be unique! This number is already registered to another contact.')),
        ('customer_code_unique', 'unique(customer_code)',
         _('The Customer Code must be unique!')),
    ]

    @api.model
    def create(self, vals):
        """توليد الكود القصير والفريد عند الحفظ فقط إذا كان عميل"""
        if vals.get('customer_rank', 0) > 0 and not vals.get('customer_code'):
            vals['customer_code'] = self._generate_unique_code()
        return super(ResPartner, self).create(vals)

    def _generate_unique_code(self, length=4, prefix='C'):
        """
        توليد كود قصير وفريد
        length: عدد الأحرف العشوائية
        prefix: حرف ثابت قبل الكود
        """
        while True:
            # توليد سلسلة عشوائية من أحرف كبيرة وأرقام
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            code = f"{prefix}-{rand_str}"
            # التحقق من أن الكود لم يُستخدم من قبل
            if not self.search([('customer_code', '=', code)], limit=1):
                return code
# ########################################################
    def name_get(self):
        result = []
        for rec in self:
            code = rec.customer_code or ''
            name = rec.name or ''
            if code:
                display = f"{code} | {name}"
            else:
                display = name
            result.append((rec.id, display))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, order=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('customer_code', operator, name)]
        return self.search(domain + args, limit=limit, order=order).ids
