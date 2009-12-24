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
from zope import component, interface
from zope.component import getUtility, queryAdapter
from zojax.content.space.interfaces import ISpace, IWorkspaceFactory
from zojax.content.permissions.permission import ContentPermission


class SpacePermission(ContentPermission):

    def isAvailable(self):
        wf = queryAdapter(self.context, IWorkspaceFactory, 'documents')
        if wf is None or not self.context.isEnabled(wf):
            return

        return super(SpacePermission, self).isAvailable()


@component.adapter(ISpace, interface.Interface)
def documentsPermissionModified(space, permissions):
    if 'zojax.AddDocuments' in permissions or \
            'zojax.SubmitDocuments' in permissions:
        return 'documents.workspace',
