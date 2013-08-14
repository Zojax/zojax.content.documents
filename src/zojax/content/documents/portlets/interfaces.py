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
from zojax.portlet.interfaces import IPortletManagerWithStatus, statusVocabulary, ENABLED
from zope import schema, interface
from zojax.content.documents.interfaces import _


class IContentPortletsManager(interface.Interface):
    """ content column portlets manager """


class IContentPortletsManagerConfiguration(IPortletManagerWithStatus):
    """ configuration schema """

    portletIds = schema.Tuple(
        title=_(u'Portlets'),
        value_type=schema.Choice(vocabulary="zojax portlets"),
        default=('portlet.recentcontent',),
        required=True)

    status = schema.Choice(
        title=_(u'Status'),
        vocabulary=statusVocabulary,
        default=ENABLED,
        required=True)
