# -*- coding: utf-8 -*-

{
    'name': 'formation3 ',
    'version': '1.0',
    'author': 'Harzi Malek',
    'website': 'www.taraji.net',
    'support': 'harzi.malek907@gmail.com',
    'license': "GPL-3",
    'complexity': 'easy',
    'sequence': 1,
    'category': 'category',
    'description': """
        Put your description here for your module:
            - model1
            - model2
            - model3
    """,
    'depends': ['base','mail','hr','website'],
    'summary': 'formation3, summary2, ',
    'data': [
        #'security/formation.xml',
        #'security/ir.model.access.csv',
        #'data/ModuleName_data.xml',
        #'views/formation_views.xml',
        #'views/formation_inherit.xml',
        'views/Configuration/session.xml',
        'views/Configuration/year.xml',
       
        
        'views/Inscription/register.xml',
        'views/Inscription/claim.xml',
        
        'views/University/cycle.xml',
        'views/University/level.xml',
        'views/University/module.xml',
        'views/University/section.xml',
        #'demo/demo.xml',
        'data/sequence.xml',
        'wizard/wiz_views.xml',
        'report/report.xml',
        'report/registrationn.xml',
        'controllers/formation.xml',
        'controllers/claim.xml',
        
        'views/snippet.xml',





        'menu.xml',
    ],
    'demo': [
        'demo/demo.xml'
    ],
    'css': [
        #'static/src/css/ModuleName_style.css'
    ],
    
   
    'currency': 'EUR',
    'installable': True,
    'application': True,
}
