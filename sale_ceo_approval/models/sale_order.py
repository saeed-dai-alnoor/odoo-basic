from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ceo_approval_state = fields.Selection([
        ('no', 'No Request'),
        ('waiting', 'Waiting CEO Approval'),
        ('approved', 'Approved by CEO'),
        ('rejected', 'Rejected by CEO')
    ], string="CEO Approval", default='no', copy=False)

    ceo_request_uid = fields.Many2one('res.users', string="Requested By", readonly=True, copy=False)
    ceo_approval_date = fields.Datetime(string="CEO Approval Date", readonly=True, copy=False)

    CEO_LIMIT = 50000.0

    def action_confirm(self):
        """Override confirm to handle CEO approval for high-value quotations."""
        to_confirm = self.env['sale.order']

        for order in self:
            # إذا كانت قيمة الطلب أكبر من الحد المسموح
            if order.amount_total > self.CEO_LIMIT:
                if order.ceo_approval_state != 'approved':
                    order.write({
                        'ceo_approval_state': 'waiting',
                        'ceo_request_uid': self.env.uid,
                        'state': 'draft',  # إبقاءه في draft
                    })
                    # إشعار للمستخدم العادي
                    if order.create_uid:
                        order.message_post(
                            body=_('This quotation exceeds $50,000 and requires CEO approval before confirmation.'),
                            partner_ids=[order.create_uid.partner_id.id]
                        )
            else:
                # الطلب أقل من الحد → تأكيد مباشر
                to_confirm |= order

        if to_confirm:
            return super(SaleOrder, to_confirm).action_confirm()

        # عرض إشعار للمستخدم العادي بأن موافقة CEO مطلوبة
        if any(order.ceo_approval_state == 'waiting' for order in self):
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('CEO Approval Required'),
                    'message': _('Some quotations exceed $50,000 and require CEO approval before confirmation.'),
                    'type': 'warning',
                    'sticky': True,
                }
            }

        return True

    def action_ceo_approve(self):
        """CEO approves the quotation."""
        for order in self:
            if not self.env.user.has_group('sale_ceo_approval.group_ceo'):
                raise UserError(_('Only users in the CEO group can approve.'))
            order.ceo_approval_state = 'approved'
            order.ceo_approval_date = fields.Datetime.now()
            super(SaleOrder, order).action_confirm()
            # إشعار للمستخدم العادي بأن العرض تم الموافقة عليه
            if order.create_uid:
                order.message_post(
                    body=_('CEO has approved this quotation. You can now proceed.'),
                    partner_ids=[order.create_uid.partner_id.id]
                )

    def action_ceo_reject(self):
        """CEO rejects the quotation."""
        for order in self:
            if not self.env.user.has_group('sale_ceo_approval.group_ceo'):
                raise UserError(_('Only users in the CEO group can reject.'))
            order.ceo_approval_state = 'rejected'
            order.state = 'draft'
            # إشعار للمستخدم العادي بأن العرض تم رفضه
            if order.create_uid:
                order.message_post(
                    body=_('CEO has rejected this quotation. Please review and modify if necessary.'),
                    partner_ids=[order.create_uid.partner_id.id]
                )
