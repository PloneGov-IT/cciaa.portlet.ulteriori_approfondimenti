# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from cciaa.portlet.ulteriori_approfondimenti import _
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implements


class IUlterioriApprofondimenti(IPortletDataProvider):
    """The "ulteriori approfondimenti" portlet"""

    ua_id = schema.TextLine(
        title=_(u"Id della cartella UA"),
        description=_(
            u"Inserisci l'id dela cartella Ulteriori approfondimenti."
        ),
        required=True,
        default=u'ulteriori-approfondimenti',
    )

    up_levels = schema.Int(
        title=_(u"Livelli su"),
        description=_(
            u"Inserisci il numero di livelli di ricerca verso l'alto.\n "
            u"Usa '1' per la sola cartella corrente."
        ),
        required=True,
        default=2,
    )


class Assignment(base.Assignment):
    """Portlet assignment."""

    implements(IUlterioriApprofondimenti)

    ua_id = u'ulteriori-approfondimenti'
    up_levels = 2

    def __init__(self, ua_id=u"ulteriori-approfondimenti", up_levels=2):
        self.ua_id = ua_id
        self.up_levels = up_levels

    @property
    def title(self):
        return "Ulteriori Approfondimenti"


class Renderer(base.Renderer):
    """Portlet renderer."""

    @property
    def available(self):
        return bool(self.getApprofondimenti())

    def getTitle(self):
        """ritorna il titolo della cartella ulteriori approfondimenti"""
        path = self._getApprofondimentiPath(self.data.up_levels)
        if path:
            return self.context.unrestrictedTraverse(path).Title()
        else:
            return "Ulteriori Approfondimenti"

    def getApprofondimenti(self):
        """
        Ritorna l'elenco degli oggetti contenuti nella cartella ulteriori approfondimenti,
        altrimenti torna una stringa vuota
        """
        folder_path = self._getApprofondimentiPath(self.data.up_levels)
        if folder_path:
            return self.context.portal_catalog(
                path={'query': folder_path, 'depth': 1},
                sort_on='getObjPositionInParent',
            )
        else:
            return None

    @memoize
    def _getApprofondimentiPath(self, level=2):
        """controlla se tra i figli o nei padri è presente una cartella ulteriori approfondimenti"""
        context = self.context
        plone_view = getMultiAdapter(
            (aq_inner(context), self.request), name='plone'
        )
        item_path = context.getPhysicalPath()
        catalog = getToolByName(context, 'portal_catalog')
        if (
            plone_view.isDefaultPageInFolder()
            or context.portal_type != 'Folder'
        ):
            folder_path = item_path[:-1]
        else:
            folder_path = item_path
        return self._lookForUpUA(
            context, folder_path, level=level, ua_id=self.data.ua_id
        )

    def _lookForUpUA(
        self, context, folder_path, level=2, ua_id='ulteriori-appronfondimenti'
    ):
        """Look above for an \"Ulteriori approfondimenti\" folder"""
        catalog = getToolByName(context, 'portal_catalog')
        if level == 0:
            return None
        result = catalog(
            path=dict(query='/'.join(folder_path), depth=1), id=ua_id
        )
        if result:
            return result[0].getPath()
        return self._lookForUpUA(
            context, folder_path[:-1], level=level - 1, ua_id=ua_id
        )

    render = ViewPageTemplateFile('ulterioriapprofondimenti.pt')


class AddForm(base.AddForm):
    """Portlet add form."""

    schema = IUlterioriApprofondimenti

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    schema = IUlterioriApprofondimenti
