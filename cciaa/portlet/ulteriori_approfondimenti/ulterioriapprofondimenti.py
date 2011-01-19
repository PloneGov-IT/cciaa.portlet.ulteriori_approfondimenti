# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#from cciaa.portlet.ulteriori_approfondimenti import UlterioriApprofondimentiMessageFactory as _


class IUlterioriApprofondimenti(IPortletDataProvider):
    """The "ulteriori approfondimenti" portlet"""

class Assignment(base.Assignment):
    """Portlet assignment."""
    implements(IUlterioriApprofondimenti)

    def __init__(self):
        pass

    @property
    def title(self):
        return "Ulteriori Approfondimenti"


class Renderer(base.Renderer):
    """Portlet renderer."""
    @property
    def available(self):
        if self.getApprofondimenti():
            return True
        else:
            return False
    
    def getTitle(self):
        """ritorna il titolo della cartella ulteriori approfondimenti"""
        path= self.hasApprofondimenti()
        if path:
            return self.context.unrestrictedTraverse(path).Title()
        else:
            return "Ulteriori Approfondimenti"

            
        
    def getApprofondimenti(self):
        """ritorna l'elenco degli oggetti contenuti nella cartella ulteriori approfondimenti, altrimenti torna una stringa vuota"""
        folder_path = self.hasApprofondimenti() 
        if folder_path:
            return self.context.portal_catalog(path={'query': folder_path,'depth':1},
                                         sort_on='getObjPositionInParent',
                                         sort_order='asc')
        else:
            return ''
            
    def hasApprofondimenti(self):
        """controlla se tra i figli o nel padre è presente una cartella ulteriori approfondimenti"""
        plone_view = getMultiAdapter((aq_inner(self.context), self.request), name='plone')
        item_path = self.context.getPhysicalPath()
        if plone_view.isDefaultPageInFolder() or self.context.portal_type != 'Folder':
            result= self.context.portal_catalog(path=dict(query='/'.join(item_path[:-1]), depth=1),
                                                portal_type='Folder',
                                                id='ulteriori-approfondimenti')
            if result:
                return result[0].getPath()
            else:
                result2= self.context.portal_catalog(path=dict(query='/'.join(item_path[:-2]), depth=1),
                                                     portal_type='Folder',
                                                     id='ulteriori-approfondimenti')
                if result2:
                    return result2[0].getPath()
                else:
                    return ''
        else:
            if 'ulteriori-approfondimenti' in self.context.keys():
                if self.context.portal_type=='Folder':
                    return '/'.join(item_path) +'/ulteriori-approfondimenti'
                else:
                    return '/'.join(item_path[:-1]) +'/ulteriori-approfondimenti'
            else:
                result= self.context.portal_catalog(path=dict(query='/'.join(item_path[:-1]), depth=1),
                                                    portal_type='Folder',
                                                    id='ulteriori-approfondimenti')
                if result:
                    return result[0].getPath()
                else:
                    return ''
        
    render = ViewPageTemplateFile('ulterioriapprofondimenti.pt')


class AddForm(base.NullAddForm):
    """Portlet add form."""
    form_fields = form.Fields(IUlterioriApprofondimenti)

    def create(self):
        return Assignment()
