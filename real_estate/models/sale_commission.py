from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleCommission(models.Model):
    _name = "sale.commission"
    _description = "Commission in sales"

    def calculate_section(self, base):
        self.ensure_one()
        for section in self.commission_section_ids:
            if section.amount_from <= base <= section.amount_to:
                return base * section.percent / 100.0
        return 0.0

    name = fields.Char("Name", required=True)
    salesmen_ids = fields.Many2many("res.users")
    sales_team_ids = fields.Many2many("crm.team")

    commission_type = fields.Selection(
        selection=[("fixed", "Fixed percentage"), ("section", "By sections")],
        string="Type",
        required=True,
        default="fixed",
    )
    apply_to = fields.Selection(
        selection=[("salesman", "Salesman"), ("team", "Sales Team")],
        string="Apply to",
        required=True,
        default="salesman",
    )

    fix_qty = fields.Float(string="Fixed percentage")
    leader_fix_qty = fields.Float(string="Leader Fixed percentage")
    commission_section_ids = fields.One2many("sale.commission.section", "commission_id")
    active = fields.Boolean(default=True)
    contract_state = fields.Selection(
        [("open", "Contract Based"), ("paid", "Payment Based")],
        string="Contract Status",
        required=True,
        default="open",
    )
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )


class SaleCommissionSection(models.Model):
    _name = "sale.commission.section"
    _description = "Sale Commission section"

    commission_id = fields.Many2one("sale.commission", string="Commission")
    amount_from = fields.Float(string="From")
    amount_to = fields.Float(string="To")
    percent = fields.Float(string="Percent", required=True)
    leader_percent = fields.Float(string="Leader Percent", required=True)

    @api.constrains("amount_from", "amount_to")
    def _check_amounts(self):
        if self.amount_to < self.amount_from:
            raise ValidationError(
                _("The lower limit cannot be greater than upper one.")
            )


class CommissionLine(models.Model):
    _name = "sale.commission.line"
    _description = "Sale Commission line"

    commission_id = fields.Many2one("realestate.contract", string="Contract")
    user_id = fields.Many2one("res.users", required=True, ondelete="restrict")
    amount = fields.Float(string="Amount", digits="Product Price")
    date = fields.Date(string="Date")
    company_id = fields.Many2one("res.company", string="Company")

    @api.onchange("commission_id")
    def _onchange_commission_id(self):
        if self.commission_id and self.commission_id.company_id:
            self.company_id = self.commission_id.company_id.id


class OwnershipContract(models.Model):
    """Invoice inherit to add salesman"""

    _inherit = "realestate.contract"

    def action_confirm(self):
        super(OwnershipContract, self).action_confirm()
        self.get_commission()

    @api.depends("commission_line_ids")
    def _compute_commission_total(self):
        for record in self:
            for line in record.commission_line_ids:
                record.commission_total += line.amount

    @api.model
    def _get_default_team(self):
        return self.env["crm.team"]._get_default_team_id()

    team_id = fields.Many2one(
        "crm.team", "Sales Channel", change_default=True, default=_get_default_team
    )

    commission_total = fields.Float(
        string="Commissions", compute="_compute_commission_total", store=True
    )
    commission_line_ids = fields.One2many("sale.commission.line", "commission_id")

    def get_commission(self):  # noqa: C901
        comm_line_obj = self.env["sale.commission.line"]
        commissions = self.env["sale.commission"].search([])
        user_ids = []

        for record in self:
            for commission in record.commission_line_ids:
                commission.unlink()
        for record in self:
            if record.user_id:
                user_ids.append(record.user_id.id)
            for member in record.team_id.member_ids:
                user_ids.append(member.id)
            for rec in record.team_id:
                if rec.user_id:
                    user_ids.append(rec.user_id.id)
            user_ids = list(set(user_ids))
            for user in user_ids:
                total_commission = 0
                for commission in commissions:
                    user_exist = 0
                    if commission.apply_to == "salesman":
                        for comm_user in commission.salesmen_ids:
                            if comm_user.id == user:
                                user_exist = 1
                        if user_exist:
                            if commission.commission_type == "fixed":
                                if commission.contract_state == "open":
                                    total_commission += (
                                        record.total_amount * commission.fix_qty / 100.0
                                    )
                            else:  # by section
                                if commission.contract_state == "open":
                                    total_commission += commission.calculate_section(
                                        record.total_amount
                                    )
                    elif commission.apply_to == "team":
                        leader = 0
                        for team in commission.sales_team_ids:
                            for team_user in team.member_ids:
                                if user == team_user.id:
                                    user_exist = 1
                                if user == team.user_id.id:
                                    leader = 1
                                    user_exist = 1
                        if user_exist:
                            if leader:
                                if commission.commission_type == "fixed":
                                    if commission.contract_state == "open":
                                        total_commission += (
                                            record.total_amount
                                            * commission.leader_fix_qty
                                            / 100.0
                                        )
                                else:  # by section
                                    if commission.contract_state == "open":
                                        total_commission += (
                                            record.total_amount
                                            * commission.leader_fix_qty
                                            / 100.0
                                        )
                            else:
                                if commission.commission_type == "fixed":
                                    if commission.contract_state == "open":
                                        total_commission += (
                                            record.total_amount
                                            * commission.fix_qty
                                            / 100.0
                                        )
                                else:  # by section
                                    if commission.contract_state == "open":
                                        total_commission += (
                                            record.total_amount
                                            * commission.fix_qty
                                            / 100.0
                                        )
                    if total_commission > 0:
                        comm_line_obj.create(
                            {
                                "date": record.date,
                                "user_id": user,
                                "amount": total_commission,
                                "commission_id": record.id,
                            }
                        )
