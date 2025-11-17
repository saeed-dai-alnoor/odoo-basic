from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    # ترك الملف مفتوح لتوسعات مستقبلية بدون تعديل كود الشريك
    # dsحالياً جميع القيود الخاصة بعدم الإنشاء تتم عبر XML
    pass


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    # كذلك نفس الفكرة هنا للمنتج
    pass
