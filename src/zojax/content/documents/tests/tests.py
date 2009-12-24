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
""" zojax.content.documents tests

$Id$
"""
import os, unittest, doctest
from zope import interface, component, event, schema
from zope.app.testing import functional
from zope.app.component.hooks import setSite
from zope.app.rotterdam import Rotterdam
from zope.app.security.interfaces import IAuthentication
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectCreatedEvent
from zope.security.management import endInteraction, newInteraction
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.catalog.catalog import Catalog, ICatalog
from zojax.ownership.interfaces import IOwnership
from zojax.content.space.content import ContentSpace
from zojax.personal.space.manager import PersonalSpaceManager
from zojax.personal.space.interfaces import IPersonalSpaceManager
from zojax.content.type.testing import setUpContents
from zojax.content.type.item import IItem, PersistentItem
from zojax.authentication.interfaces import IAuthenticationConfiglet
from zojax.authentication.interfaces import IAuthenticatorPluginFactory
from zojax.authentication.browser.interfaces import ILoginLayer
from zojax.principal.users.principal import Principal
from zojax.principal.users.interfaces import IUsersPlugin
from zojax.principal.password.interfaces import IPasswordTool


zojaxContentDocumentsLayer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxContentDocumentsLayer', allow_teardown=True)


class IDefaultSkin(ILayoutFormLayer, ILoginLayer, Rotterdam):
    """ skin """


class IDocument(IItem):

    text = schema.Text(
        title = u'Text',
        required = False)


class Document(PersistentItem):
    interface.implements(IDocument)


def FunctionalDocFileSuite(*paths, **kw):
    layer = zojaxContentDocumentsLayer

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        newInteraction()

        root = functional.getRootFolder()
        setSite(root)
        sm = root.getSiteManager()

        # IIntIds
        root['ids'] = IntIds()
        sm.registerUtility(root['ids'], IIntIds)
        root['ids'].register(root)

        # catalog
        root['catalog'] = Catalog()
        sm.registerUtility(root['catalog'], ICatalog)

        # space
        space = ContentSpace(title=u'Space')
        event.notify(ObjectCreatedEvent(space))
        root['space'] = space

        # people
        people = PersonalSpaceManager(title=u'People')
        event.notify(ObjectCreatedEvent(people))
        root['people'] = people
        sm.registerUtility(root['people'], IPersonalSpaceManager)

        # users
        authconfiglet = sm.getUtility(IAuthenticationConfiglet)
        authconfiglet.installUtility()

        authfactory = sm.getUtility(IAuthenticatorPluginFactory, name='principal.users')
        authfactory.install()
        authfactory.activate()

        users = sm.getUtility(IUsersPlugin)
        users['01'] = Principal('user@zojax.net' '', 'User', '')
        users['01'].password = sm.getUtility(IPasswordTool).encodePassword('12345')

        endInteraction()

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite("testbrowser.txt"),
            ))
