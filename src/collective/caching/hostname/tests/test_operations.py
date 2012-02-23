# -*- coding:utf-8 -*-
import unittest2 as unittest

from plone.testing.z2 import Browser

from plone.app.testing import TEST_USER_ID, TEST_USER_PASSWORD
from plone.app.testing import setRoles

from zope.component import getUtility

from zope.globalrequest import setRequest

from plone.registry.interfaces import IRegistry
from plone.caching.interfaces import ICacheSettings

from collective.caching.hostname.testing import FUNCTIONAL_TESTING


class TestOperationDefault(unittest.TestCase):
    """
    Test various edge cases.
    """

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.wt = self.portal['portal_workflow']
        setRequest(self.portal.REQUEST)

        self.registry = getUtility(IRegistry)
        self.cacheSettings = self.registry.forInterface(ICacheSettings)
        self.cacheSettings.enabled = True

    def tearDown(self):
        setRequest(None)

    def test_last_modified_no_etags(self):
        """
        When a new content type is added, the resulting page should not be 
        cached since it has messages. However, it should only trigger an etag 
        if its been configured to use etags
        """
        # Add a document content
        setRoles(self.portal, TEST_USER_ID, ('Manager',))
        self.portal.invokeFactory('Document', 'd1')
        self.portal['d1'].setTitle(u"Document one")
        self.portal['d1'].setDescription(u"Document")
        self.wt.doActionFor(self.portal['d1'], 'publish')

        self.cacheSettings.operationMapping = {'plone.content.itemView':
                                               'collective.caching.hostname.strongCaching'}
        self.registry['collective.caching.hostname.strongCaching.lastModified'] = True
        self.registry['collective.caching.hostname.strongCaching.etags'] = None
        self.registry['collective.caching.hostname.strongCaching.hostnames_nocache'] = []

        import transaction; transaction.commit()

        # log in and access document one
        browser = Browser(self.app)
        browser.addHeader('Authorization', 'Basic %s:%s' % 
                          (TEST_USER_ID, TEST_USER_PASSWORD,)
                         )
        url = "%s" % self.portal['d1'].absolute_url()
        browser.open(url)
        self.failUnless('max-age=86400' in browser.headers['cache-control'])

        # now set up hostname and make sure that a header is added 
        self.registry['collective.caching.hostname.strongCaching.hostnames_nocache'] = ['http://nohost']
        import transaction; transaction.commit()
        url = "%s" % self.portal['d1'].absolute_url()
        browser.open(url)
        self.failIf('max-age=86400' in browser.headers['cache-control'])
