##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, component
from zope.interface import Interface
from zope.component import getUtility, getUtilitiesFor
from zope.traversing.browser import absoluteURL

from zojax.table.table import Table
from zojax.catalog.interfaces import ICatalog
from zojax.content.space.interfaces import IContentSpace
from zojax.content.table.interfaces import IContentsTable
from zojax.content.actions.contentactions import BrowseContentAction
from zojax.content.documents.interfaces import _, IDocuments, IDocumentType

from interfaces import IBrowseDocumentsAction


class DocumentsTable(Table):
    interface.implements(IContentsTable)
    component.adapts(Interface, Interface, Interface)

    title = _('Documents')

    pageSize = 15
    enabledColumns = ('author', 'title', 'type', 'location', 'modified')
    msgEmptyTable = _('No content has been added yet.')

    def initDataset(self):
        types = [name for name, ct in getUtilitiesFor(IDocumentType)]

        results = getUtility(ICatalog).searchResults(
            traversablePath={'any_of':(self.context,)},
            type={'any_of': types},
            sort_order='reverse', sort_on='modified',
            isDraft={'any_of': (False,)})

        self.dataset = results


class SpaceDocumentsTable(DocumentsTable):
    component.adapts(IContentSpace, Interface, Interface)

    enabledColumns = ('author', 'title', 'type', 'space', 'modified')


class BrowseDocumentsAction(BrowseContentAction):
    interface.implements(IBrowseDocumentsAction)

    title = _('Browse documents')
    weight = 100
    contextInterface = IContentSpace

    @property
    def url(self):
        return '%s/browse-documents.html'%absoluteURL(self.context, self.request)
