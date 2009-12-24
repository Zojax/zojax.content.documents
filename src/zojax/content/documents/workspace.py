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
from zope import interface, component, event
from zojax.content.space.interfaces import IContentSpace
from zojax.content.space.workspace import WorkspaceFactory

from container import DocumentsContainer
from interfaces import _, IDocuments, IDocumentsFactory


class Documents(DocumentsContainer):
    interface.implements(IDocuments)

    @property
    def space(self):
        return self.__parent__


class DocumentsFactory(WorkspaceFactory):
    component.adapts(IContentSpace)
    interface.implements(IDocumentsFactory)

    name = 'documents'
    title = _(u'Documents')
    description = _(u'Documents workspace.')
    weight = 100
    factory = Documents
