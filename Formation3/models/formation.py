from odoo import models, fields, api,_
from odoo.exceptions import UserError, AccessError, ValidationError
from _ast import Store
from __builtin__ import True
from django.template.defaultfilters import default







class Registration(models.Model):
    _name = 'registration.registration'
    _description = 'registration.registration'
    _inherit = ['mail.thread']
    @api.one
    def action_new(self):
        self.state = 'new'
        return True 
    @api.one
    def action_done(self):
        self.state = 'done'
        return True 

    @api.one
    def action_cancel(self):
        self.state = 'cancel'
        return True  
    
    @api.multi
    def print_report(self):
        return self.env.ref('Formation3.report_registration').report_action(self)
    

   # @api.model
    #def create(self, vals):
     #   if vals.get('name'):
        #    vals['name'] = ' value by create method'
      #  res = super(Registration, self).create(vals)
       # return res    
   # @api.multi
   # def write(self, vals):
    #    vals['name'] = 'value by write method'
   #     return super(Registration, self).write(vals)
  #  @api.multi
  #  def copy(self, default=None):
   #     default = dict(default or {})
    #    default.update({'name': 'copy(name)','code': 'copy -001'})
    #    return super(Registration, self).copy(default)
 

    @api.model
    @api.depends('code')
    def create(self, vals):
        if ('code' not in vals) or (vals.get('code')=='/'):
            vals['code'] = self.env['ir.sequence'].get('registration.registration')
        return super(Registration, self).create(vals) 
    
     
    @api.multi
    def unlink(self):
        for record in self:
            if record.state == 'done':
                raise UserError(_('You cannot delete records in done state.'))
        res = super(Registration, self).unlink()
        return res 
    
    @api.one
    @api.depends('claim_ids')
    def _malek(self):
        self.nbr = len(self.claim_ids)  
        
    
    
    name=fields.Char(string='Nom', required=False, readonly=False)
    code=fields.Char(string='Code', default='/',readonly=True)
    start_date= fields.Date('Date de debut',help="Date")
    end_date= fields.Date('Date de fin',help="Date")
    description=fields.Text(string='Description', required=False, readonly=False)     
    cycle_id = fields.Many2one('cycle.cycle', string='Cycle',track_visibility='onchange')
    years_id =fields.Many2one('year.year', string='Annee',track_visibility='onchange')
    claim_ids = fields.One2many('claim.claim', 'reg_id',string='reclammation')
    student_id = fields.Many2one('res.partner', string='Etudient',domain="[('age', '=',25)]")
    state = fields.Selection([('new', 'Nouveau'), ('done', 'Valider'), ('cancel', 'Annuler')], string= 'Statut',default='new',track_visibility='onchange')
    priority = fields.Selection([('1', 'low'), ('2', 'normal'), ('3', 'high')], string= 'Priorite')
    nbr = fields.Integer(compute='_malek',string='#reclamation')
class Claim(models.Model):
    _name = 'claim.claim'
    _description = 'Reclammation'
 
   
    @api.one
    @api.depends('amount','hours')
    def _total_compute(self):
        if self.hours:
            self.total = self.amount * self.hours  
        else :  
            self.sum = self.amount + self.amount    
     
 
 

 
    name=fields.Char(string='Nom', required=False, readonly=False)
    code=fields.Char(string='Code', default=lambda x: x.env['ir.sequence'].get('claim.claim'))
    description=fields.Text(string='Description', required=False, readonly=False)
    start_date= fields.Date('Date de debut',help="Date")
    end_date= fields.Date('Date de fin',help="Date")
    reg_id= fields.Many2one('registration.registration',string='Inscription')
    user_id = fields.Many2one('res.users',string='Responsable')
    state=fields.Selection([('new', 'Nouvelle'), ('done', 'Valider'), ('cancel', 'Annuler')], string= 'Statut')
    amount = fields.Integer(string='Montant')
    sum = fields.Integer(string='Somme')
    hours = fields.Integer(string='Nbredheure')

    total = fields.Integer(compute='_total_compute',string='Total',Store=True)    
    
class Year(models.Model):
    _name = 'year.year'
    _description = 'year.year'
 
    name=fields.Char(string='Nom', required=False, readonly=False)
    code=fields.Char(string='Code', required=False, readonly=False)
    description=fields.Text(string='Description', required=False, readonly=False)
    start_date= fields.Date('Date de debut',help="Date")
    end_date= fields.Date('Date de fin',help="Date")
    reg_ids = fields.One2many('registration.registration','years_id', string='Registration') 
    session_ids=fields.One2many('session.session','year_id',string='session')
    
    
class Session(models.Model):
    _name = 'session.session'
    _description = ''
 
    name=fields.Char(string='Nom', required=False, readonly=False)
    code=fields.Char(string='Code', required=False, readonly=False)
    description=fields.Text(string='Description', required=False, readonly=False)
    start_date= fields.Date('Date de debut',help="Date")
    end_date= fields.Date('Date de fin',help="Date")
    year_id= fields.Many2one('year.year',string='Annee')

class Cycle(models.Model):
    _name = 'cycle.cycle'
    _description = 'cycle.cycle'
 
    name=fields.Char(string='Nom', required=False, readonly=False)
    code=fields.Char(string='Code', required=False, readonly=False)
    description=fields.Text(string='Description', required=False, readonly=False)
    level_ids = fields.One2many('level.level','cycle_id', string='Niveau')
    
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name and record.code:
                result.append((record.id, record.name + '--' + record.code))
            if record.name and not record.code:
                result.append((record.id, record.name))
        return result


  
class level(models.Model):
    _name = 'level.level'
    _description = 'level.level'
 
    name=fields.Char(string='Nom', required=False, readonly=False)
    code=fields.Char(string='Code', required=False, readonly=False)
    description=fields.Text(string='Description', required=False, readonly=False)
    section_ids = fields.One2many('section.section','level_id', string='section')
    cycle_id =fields.Many2one('cycle.cycle', string='Cycle')

class Section(models.Model):
    _name = 'section.section'
    _description = 'ModelName'
 
    name=fields.Char(string='Nom', required=False, readonly=False)
    code=fields.Char(string='Code', required=False, readonly=False)
    description=fields.Text(string='Description', required=False, readonly=False)
    module_ids = fields.One2many('module.module','section_id', string='module') 
    level_id = fields.Many2one('level.level',sting='Niveau')



class Module(models.Model):
    _name = 'module.module' 
    _description = 'modules'
    
    name = fields.Char(string="Nom", required=True) 
    code =fields.Char(string="Code", default='001')
    description = fields.Text(string ='Description')
    section_id = fields.Many2one('section.section',string='Section')
  


    
    
    
    
    
    
    