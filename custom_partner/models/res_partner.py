from odoo import models, fields, api, _
import random
import string

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(
        string='Customer Code',
        copy=False,
        readonly=True,
        index=True
    )

    _sql_constraints = [
        ('mobile_unique', 'unique(mobile)',
         _('The mobile number must be unique! This number is already registered to another contact.')),
        ('customer_code_unique', 'unique(customer_code)',
         _('The Customer Code must be unique!')),
    ]

    @api.model
    def create(self, vals):
        # توليد الكود دائماً عند الإنشاء إن لم يكن محدداً
        if not vals.get('customer_code'):
            vals['customer_code'] = self._generate_unique_code()
        return super().create(vals)

    def _generate_unique_code(self, length=4, prefix='C'):
        while True:
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            code = f"{prefix}-{rand_str}"
            if not self.search([('customer_code', '=', code)], limit=1):
                return code

    def name_get(self):
        """عرض الكود مع الاسم: 'C-XXXX | Name'"""
        result = []
        for rec in self:
            code = rec.customer_code or ''
            name = rec.name or ''
            display = f"{code} | {name}" if code else name
            result.append((rec.id, display))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        البحث باسم أو بكود العميل ثم إرجاع name_get لعرض متناسق.
        لا تعدل _name_search لكي لا تتعرض لاختلافات التوقيع بين الإصدارات.
        """
        args = args or []
        if name:
            domain = ['|', ('name', operator, name), ('customer_code', operator, name)] + args
            partners = self.search(domain, limit=limit)
        else:
            partners = self.search(args, limit=limit)
        return partners.name_get()
