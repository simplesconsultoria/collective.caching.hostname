# -*- coding:utf-8 -*-

from zope.interface import implements
from zope.interface import classProvides
from zope.interface import Interface
from zope.component import adapts

from zope.publisher.interfaces.http import IHTTPRequest

from plone.caching.interfaces import ICachingOperation
from plone.caching.interfaces import ICachingOperationType
from plone.caching.utils import lookupOptions

from plone.app.caching.operations.utils import doNotCache
from plone.app.caching.operations.utils import getContext
from plone.app.caching.operations.default import BaseCaching

from collective.caching.hostname.operations.utils import getHostname

from plone.app.caching.interfaces import _

try:
    from Products.ResourceRegistries.interfaces import ICookedFile
    from Products.ResourceRegistries.interfaces import IResourceRegistry
    HAVE_RESOURCE_REGISTRIES = True
except ImportError:
    HAVE_RESOURCE_REGISTRIES = False


class BaseHostnameCaching(BaseCaching):
    """A generic caching operation class based on BaseCaching from
    plone.app.caching which adds a **hostnames_nocache** option
    """
    implements(ICachingOperation)
    adapts(Interface, IHTTPRequest)

    # Type metadata
    classProvides(ICachingOperationType)

    title = _(u"Generic caching w/ hostname support")
    description = _(u"Through this operation, all standard caching functions "
                    u"can be performed via various combinations of the optional "
                    u"parameter settings. For most cases, it's probably easier "
                    u"to use one of the other simpler operations (Strong caching, "
                    u"Moderate caching, Weak caching, or No caching).")
    prefix = 'collective.caching.hostname.baseCaching'
    options = ('maxage', 'smaxage', 'etags', 'lastModified', 'ramCache',
               'vary', 'anonOnly', 'hostnames_nocache')

    hostnames_nocache = []

    def interceptResponse(self, rulename, response, class_=None):
        options = lookupOptions(class_ or self.__class__, rulename)
        hostname = getHostname(self.request)
        if hostname in options.get('hostnames_nocache',
                                   self.hostnames_nocache):
            return None
        return super(BaseHostnameCaching, self).interceptResponse(rulename,
                                                                  response,
                                                                  class_=None)

    def modifyResponse(self, rulename, response, class_=None):
        options = lookupOptions(class_ or self.__class__, rulename)
        hostname = getHostname(self.request)
        if hostname in options.get('hostnames_nocache',
                                   self.hostnames_nocache):
            doNotCache(self.published, self.request, response)
        else:
            return super(BaseHostnameCaching, self).modifyResponse(rulename,
                                                                   response,
                                                                   class_=None)


class WeakCaching(BaseHostnameCaching):
    """Weak caching operation. A subclass of the generic BaseCaching
    operation to help make the UI approachable by mortals
    """

    # Type metadata
    classProvides(ICachingOperationType)

    title = _(u"Weak caching w/ hostname support")
    description = _(u"Cache in browser but expire immediately and enable 304 "
                    u"responses on subsequent requests. 304's require configuration "
                    u"of the 'Last-modified' and/or 'ETags' settings. If Last-Modified "
                    u"header is insufficient to ensure freshness, turn on ETag "
                    u"checking by listing each ETag components that should be used to "
                    u"to construct the ETag header. "
                    u"To also cache public responses in Zope memory, set 'RAM cache' to True. ")
    prefix = 'collective.caching.hostname.weakCaching'
    sort = 3

    # Configurable options
    options = ('etags', 'lastModified', 'ramCache', 'vary',
               'anonOnly', 'hostnames_nocache')

    # Default option values
    maxage = 0
    smaxage = etags = vary = None
    lastModified = ramCache = anonOnly = False
    hostnames_nocache = []


class ModerateCaching(BaseHostnameCaching):
    """Moderate caching operation. A subclass of the generic BaseCaching
    operation to help make the UI approachable by mortals
    """

    # Type metadata
    classProvides(ICachingOperationType)

    title = _(u"Moderate caching w/ hostname support")
    description = _(u"Cache in browser but expire immediately (same as 'weak caching'), "
                    u"and cache in proxy (default: 24 hrs). "
                    u"Use a purgable caching reverse proxy for best results. "
                    u"Caution: If proxy cannot be purged, or cannot be configured "
                    u"to remove the 's-maxage' token from the response, then stale "
                    u"responses might be seen until the cached entry expires. ")
    prefix = 'collective.caching.hostname.moderateCaching'
    sort = 2

    # Configurable options
    options = ('smaxage', 'etags', 'lastModified', 'ramCache', 'vary',
               'anonOnly', 'hostnames_nocache')

    # Default option values
    maxage = 0
    smaxage = 86400
    etags = vary = None
    lastModified = ramCache = anonOnly = False
    hostnames_nocache = []


class StrongCaching(BaseHostnameCaching):
    """Strong caching operation. A subclass of the generic BaseCaching
    operation to help make the UI approachable by mortals
    """

    # Type metadata
    classProvides(ICachingOperationType)

    title = _(u"Strong caching w/ hostname support")
    description = _(u"Cache in browser and proxy (default: 24 hrs). "
                    u"Caution: Only use for stable resources "
                    u"that never change without changing their URL, or resources "
                    u"for which temporary staleness is not critical.")
    prefix = 'collective.caching.hostname.strongCaching'
    sort = 1

    # Configurable options
    options = ('maxage', 'smaxage', 'etags', 'lastModified', 'ramCache',
               'vary', 'anonOnly', 'hostnames_nocache')

    # Default option values
    maxage = 86400
    smaxage = etags = vary = None
    lastModified = ramCache = anonOnly = False
    hostnames_nocache = []

if HAVE_RESOURCE_REGISTRIES:

    class ResourceRegistriesCaching(StrongCaching):
        """Override for StrongCaching which checks ResourceRegistries
        cacheability
        """

        adapts(ICookedFile, IHTTPRequest)

        def interceptResponse(self, rulename, response):
            return super(ResourceRegistriesCaching, self).interceptResponse(rulename, response, class_=StrongCaching)

        def modifyResponse(self, rulename, response):
            registry = getContext(self.published, IResourceRegistry)

            if registry is not None:
                if registry.getDebugMode() or not registry.isCacheable(self.published.__name__):
                    doNotCache(self.published, self.request, response)
                    return

            super(ResourceRegistriesCaching, self).modifyResponse(rulename, response, class_=StrongCaching)
