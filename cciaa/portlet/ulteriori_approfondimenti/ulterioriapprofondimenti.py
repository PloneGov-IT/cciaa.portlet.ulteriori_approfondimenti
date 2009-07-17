from Acquisition import aq_inner
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cciaa.portlet.ulteriori_approfondimenti import UlterioriApprofondimentiMessageFactory as _


class IUlterioriApprofondimenti(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IUlterioriApprofondimenti)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Ulteriori Approfondimenti"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
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
        if plone_view.isDefaultPageInFolder():
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
                return '/'.join(item_path) +'/ulteriori-approfondimenti'
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
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IUlterioriApprofondimenti)

    def create(self):
        return Assignment()
