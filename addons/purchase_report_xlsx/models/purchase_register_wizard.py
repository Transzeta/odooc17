import xlwt
from odoo import fields, models, api, _
from datetime import timedelta
from odoo.exceptions import UserError
import base64
import xlwt
from io import BytesIO


class PoReportWizard(models.TransientModel):
    _name = 'po.register.wizard'
    _description = 'Purchase Report Wizard'

    start_date = fields.Date()
    end_date = fields.Date()
    excel_file = fields.Binary('Report Download')
    file_name = fields.Char('Excel File', size=64)

    def po_report_sheet(self):
        # Create Workbook and Sheet
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet("invoice")

        # Styles
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'dd/mm/yyyy'
        header_style = xlwt.easyxf('font: bold on, height 220, color black; align: wrap 1, horiz center;')
        row_style = xlwt.easyxf('align: wrap 1;')

        # Headers
        headers = ['Invoice Number', 'Journal', 'Date', 'Partner/Name', 'Partner/Tax ID', 'Partner/City',
                   'Partner/State', 'Partner/GST Treatment', 'Product', 'Account', 'HSN Code', 'Unit of Measure',
                   'Quantity', 'Unit Price', 'Discount (%)', 'Taxes', 'Taxable', 'CGST', 'SGST', 'IGST', 'TDS', 'TOTAL']

        for index, value in enumerate(headers):
            sheet.write(0, index, value, header_style)

        row_indx = 1

        # Fetching Invoices
        invoice = self.env['account.move'].search([('move_type', '=', 'in_invoice'),
                                                   ('invoice_date', '>=', self.start_date),
                                                   ('invoice_date', '<=', self.end_date),
                                                   ('state', '=', 'posted')])

        for inv in invoice:
            tax_name = None
            sgst = None
            cgst = None
            igst = None
            for line in inv.invoice_line_ids:
                product = line.product_id
                product_qty = line.quantity
                unit_price = line.price_unit
                discount = line.discount
                taxes = line.tax_ids
                tds = line.on_account_amount

                print(inv.amount_tax, "tax amount")

                for gst in taxes:
                    tax_name = gst.name
                    for gst_type in gst.children_tax_ids:
                        if gst_type.description == 'SGST':
                            sgst = gst_type.name
                            print("SGST:", sgst.name)
                        elif gst_type.description == 'CGST':
                            cgst = gst_type.name
                            print("CGST:", cgst.name)
                        elif gst_type.description == 'IGST':
                            igst = gst_type.name
                            print("IGST:", igst.name)

                # Writing Data to Sheet
                sheet.write(row_indx, 0, inv.name or "", row_style)
                sheet.write(row_indx, 1, inv.journal_id.name or "", row_style)
                sheet.write(row_indx, 2, inv.invoice_date or "", date_style)
                sheet.write(row_indx, 3, inv.partner_id.name or "", row_style)
                sheet.write(row_indx, 4, inv.partner_id.vat or "", row_style)
                sheet.write(row_indx, 5, inv.partner_id.city or "", row_style)
                sheet.write(row_indx, 6, inv.partner_id.state_id.name or "", row_style)
                sheet.write(row_indx, 7, inv.l10n_in_gst_treatment or "", row_style)
                sheet.write(row_indx, 8, product.name or "", row_style)
                sheet.write(row_indx, 9, product.name or "", row_style)
                sheet.write(row_indx, 10, product.l10n_in_hsn_code or "", row_style)
                sheet.write(row_indx, 11, product.uom_id.name or "", row_style)
                sheet.write(row_indx, 12, product_qty or "", row_style)
                sheet.write(row_indx, 13, unit_price or "", row_style)
                sheet.write(row_indx, 14, discount or "", row_style)
                sheet.write(row_indx, 15, tax_name or "", row_style)
                # below tax amount
                sheet.write(row_indx, 16, inv.amount_tax or "", row_style)
                sheet.write(row_indx, 17, sgst or "", row_style)
                sheet.write(row_indx, 18, cgst or "", row_style)
                sheet.write(row_indx, 19, igst or "", row_style)
                sheet.write(row_indx, 20, tds or "", row_style)
                sheet.write(row_indx, 21, inv.amount_residual or "", row_style)

                row_indx += 1

        # Saving Workbook
        fp = BytesIO()
        workbook.save(fp)
        xls = base64.encodebytes(fp.getvalue())

        self.write({'excel_file': xls, 'file_name': 'Purchase Report.xls'})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'po.register.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new',
        }
