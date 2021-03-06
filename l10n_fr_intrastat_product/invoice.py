# -*- encoding: utf-8 -*-
##############################################################################
#
#    Report intrastat product module for Odoo
#    Copyright (C) 2010-2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    intrastat_transport = fields.Selection([
        (1, 'Transport maritime'),
        (2, 'Transport par chemin de fer'),
        (3, 'Transport par route'),
        (4, 'Transport par air'),
        (5, 'Envois postaux'),
        (7, 'Installations de transport fixes'),
        (8, 'Transport par navigation intérieure'),
        (9, 'Propulsion propre')
        ], string='Type of transport',
        help="Type of transport of the goods. This information is "
        "required for the product intrastat report (DEB).")
    intrastat_department = fields.Char(
        string='Department', size=2,
        help="For a customer invoice, contains France's department "
        "number from which the goods have be shipped. For a supplier "
        "invoice, contains France's department number of reception "
        "of the goods. This information is required for the product "
        "intrastat report (DEB).")
    intrastat_country_id = fields.Many2one(
        'res.country', string='Destination/Origin country of the goods',
        help="For a customer invoice, contains the country to which "
        "the goods have been shipped. For a supplier invoice, contains "
        "the country from which the goods have been shipped.")
    intrastat_type_id = fields.Many2one(
        'report.intrastat.type', string='Intrastat type', ondelete='restrict')

    @api.one
    @api.constrains('intrastat_department')
    def _check_intrastat_department(self):
        self.env['res.company'].real_department_check(
            self.intrastat_department)
