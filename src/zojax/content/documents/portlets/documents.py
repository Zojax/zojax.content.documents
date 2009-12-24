##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
from zope.component import getUtilitiesFor
from zope.traversing.browser import absoluteURL
from zojax.content.space.interfaces import ISpace
from zojax.content.documents.interfaces import IDocumentType
from zojax.content.space.portlets.content import RecentContentPortlet


class DocumentsPortlet(RecentContentPortlet):

    rssfeed = 'documents'
    cssclass = 'portlet-documents'

    def extraParameters(self):
        return {'type': {'any_of': [name for name, ct in
                                    getUtilitiesFor(IDocumentType)]}}

    def getMoreLink(self):
        context = self.context
        while not ISpace.providedBy(context):
            context = context.__parent__
            if context is None:
                break

        if context is not None:
            return u'%s/browse-documents.html'%absoluteURL(context, self.request)
