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
from zope import interface
from zope.i18nmessageid import MessageFactory
from zojax.security.interfaces import IPermissionCategory
from zojax.content.type.interfaces import IItem
from zojax.content.feeds.interfaces import IRSS2Feed
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory

_ = MessageFactory('zojax.content.documents')


class IDocumentType(interface.Interface):
    """ Document content type """


class IDocumentsContainer(IItem):
    """ Documents container """


class IDocuments(IItem, IWorkspace):
    """ Documents workspace """


class IDocumentsFactory(IWorkspaceFactory):
    """ Documents workspace factory """


class IDocumentsRSSFeed(IRSS2Feed):
    """ documents rss feed """


class IDocumentsPermissions(IPermissionCategory):
    """ documents permissions """
