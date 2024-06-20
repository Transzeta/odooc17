from odoo import fields, api, models


class ProductCategoryInherit(models.Model):
    _inherit = 'product.category'

    product_indian_sales = fields.Html(string="Indian Sales")
    product_export_sale = fields.Html(string="Export Sales")
