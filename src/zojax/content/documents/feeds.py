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
import time, rfc822
from zope import interface, component
from zope.component import getUtility, getUtilitiesFor
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import IDCTimes

from zojax.content.feeds.rss2 import RSS2Feed
from zojax.catalog.interfaces import ICatalog
from zojax.ownership.interfaces import IOwnership
from zojax.content.space.interfaces import ISpace
from zojax.principal.profile.interfaces import IPersonalProfile

from interfaces import _, IDocuments, IDocumentType, IDocumentsRSSFeed


class DocumentsRSSFeed(RSS2Feed):
    component.adapts(ISpace)
    interface.implementsOnly(IDocumentsRSSFeed)

    name = u'documents'
    title = _(u'Documents')
    description = _(u'List of recently changed documents in current space '
                    u'and all sub spaces.')

    def items(self):
        request = self.request
        types = [name for name, ct in getUtilitiesFor(IDocumentType)]

        results = getUtility(ICatalog).searchResults(
            traversablePath={'any_of':(self.context,)},
            type={'any_of': types},
            sort_order='reverse', sort_on='modified',
            isDraft={'any_of': (False,)})[:20]

        for item in results:
            url = absoluteURL(item, request)

            info = {
                'title': item.title,
                'description': item.description,
                'guid': '%s/'%url,
                'pubDate': rfc822.formatdate(time.mktime(
                        IDCTimes(item).modified.timetuple())),
                'isPermaLink': True}

            principal = IOwnership(item).owner
            if principal is not None:
                profile = IPersonalProfile(principal)
                info['author'] = u'%s (%s)'%(profile.email, profile.title)

            yield info


class DocumentsWorkspaceRSSFeed(DocumentsRSSFeed):
    component.adapts(IDocuments)

    description = _(u'List of recently changed documents in documents worspace.')
