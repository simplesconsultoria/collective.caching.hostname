**************************************************************
collective.caching.hostname
**************************************************************

.. contents:: Table of Contents
   :depth: 2

Overview
--------

An addon for Plone and plone.app.caching enabling a hostname blacklist for caching
rules.

This package provides three caching operations based on the ones available at plone.app.caching:

  * Weak caching w/ hostname support
  
  * Moderate caching w/ hostname support

  * Strong caching w/ hostname support

You should use this package -- and the operations provided here -- to supress
caching (or some caching rules) when the request is for a specific hostname.

Requirements
------------

    * Plone >=4.1.x (http://plone.org/products/plone)

    * plone.app.caching (http://plone.org/products/plone.app.cahing)    

Installation
------------
    
To enable this product,on a buildout based installation:

    1. Edit your buildout.cfg and add ``collective.caching.hostname``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            collective.caching.hostname


After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product (check its checkbox) and click the 'Install' button.

Uninstall -- This can be done from the same management screen, but only
if you installed it from the quick installer.

Note: You may have to empty your browser cache and save your resource registries
in order to see the effects of the product installation.

Sponsoring
----------

Development of this product was sponsored by :
    
    * `Universidade Metodista de Sao Paulo <http://metodista.br/>`_.


Credits
-------

    * Rodrigo Cesar Perlin (rodrigo punto perlin at metodista punto br) - 
      Conception

    * Simples Consultoria (products at simplesconsultoria dot com dot br) - 
      Implementation
    
