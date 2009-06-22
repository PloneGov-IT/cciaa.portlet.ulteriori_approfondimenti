from zope.interface import implements
from Products.CMFCore.utils import getToolByName

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
        if 'ulteriori-approfondimenti' in self.context.keys() or 'ulteriori-approfondimenti' in self.context.aq_inner.aq_parent.keys():
            return True
        else:
            return False
    
    def getApprofondimenti(self):
        if 'ulteriori-approfondimenti' in self.context.keys():
            folder = getattr(self.context,'ulteriori-approfondimenti',False)
            return folder.portal_catalog(path=dict(query='/'.join(folder.getPhysicalPath()), depth=1))
        
        if 'ulteriori-approfondimenti' in self.context.aq_inner.aq_parent.keys():
            folder = getattr(self.context.aq_inner.aq_parent,'ulteriori-approfondimenti',False)
            return folder.portal_catalog(path=dict(query='/'.join(folder.getPhysicalPath()), depth=1))
        
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
