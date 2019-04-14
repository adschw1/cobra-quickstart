Cisco ACI Python Quick Start Guide
==================================

This is a quick start guide to working with Cisco ACI using the Python Cobra SDK.

**NOTE: This works best on Mac or Linux. I would recommend using a Ubuntu/CentOS/Fedora VirtualBox if using Windows**

.. contents::


Getting started with Cisco ACI using Python
===========================================

Requirements
------------
- Python 2.7
- ``git`` command line tool
- ``pip`` and ``virtualenv``

Setting up the Environment
--------------------------

If you need to install ``pip``

.. code-block:: bash

  curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
  sudo python get-pip.py        

Install ``virtualenv`` and developer tools

.. code-block:: bash

  sudo pip install virtualenv

  xcode-select --install

Prepare ACI Environment for Mac/Linux

.. code-block:: bash

    #From your working directory
    git clone https://github.com/CiscoDevNet/aci-learning-labs-code-samples
    cd aci-learning-labs-code-samples
    virtualenv venv --python=python2.7
    source venv/bin/activate
    pip install -r requirements.txt

For Windows

.. code-block:: bash

  #From your working directory
  git clone https://github.com/CiscoDevNet/aci-learning-labs-code-samples
  cd aci-learning-labs-code-samples
  virtualenv venv --python=C:\Python27\python.exe
  venv\Scripts\activate.bat
  pip install -r requirements.txt

Install Cobra SDK
=================

To download Cobra SDK you will need a Cisco account:

https://developer.cisco.com/fileMedia/download/39308f27-4956-4bd8-8127-d0fac29158c4

https://developer.cisco.com/fileMedia/download/928a762b-c2c7-4374-840a-9d3242aa8e27

Install Cobra SDK using ``easy_install``

.. code-block:: bash

  # From your Downloads Dirctory
  easy_install -Z acicobra-[apic_version]-py2.7.egg
  easy_install -Z acimodel-[apic_version]-py2.7.egg
  # Note: If you are NOT using a Virtual Environment, you may need to use "sudo" to install

APIC Sandbox Environment Setup
==============================

Run the baselining script located in the code repo at ``aci-learning-labs-code-samples/apic_fabric_setup/baseline.py``::
  
  # From within the correct virtual environment
  (venv) apic_fabric_setup\ $ python baseline.py

  # Expected Output
  Baselining APIC Simulator for Learning Labs
  Setting up Fabric Nodes
  Configuring Fabric Policies
  Setting up Common Tenant
  Setting up Heroes Tenant
  Setting up SnV Tenant
  


Creating Your First Tenant
==========================

Once you have successfully completed all the previous steps you may now begin this section.

Credentials File
----------------

You should have a ``credentials.py`` in your ``aci-learning-labs-code-samples`` folder, if you don't you can create it

.. code-block:: python
  
  URL = 'https://sandboxapicdc.cisco.com'
  LOGIN = 'admin'
  PASSWORD = 'ciscopsdt'

Understanding the SDK
---------------------

The Cobra SDK can seem a little daunting at first. But really it's just a Python SDK that supports CRUD operations for the ACI fabric.

- Any operations through the API or GUI can be accomplished via Cobra
- The Cobra module is the letters up to the first capital letter.
- The Cobra class is the rest of the ID.
- Examples:

  - fvTenant: Module = fv, Class = Tenant
  - l3extOut: Module = l3ext, Class = Out

- Properties can be accessed by calling ``.property`` on the object.
- Examples:

  - tenant.name
  - endpoint.ip

Be sure to create a ``.py`` file to save your work as we go. This can be done from python interactive prompt if you don't care about saving, just type ``python`` in terminal. 

**Make Sure your Virutalenv is activated** if not, type ``source venv/bin/activate`` from wherever your venv/ directory is located

Importing your modules
----------------------

For **Tenant** operations

.. code-block:: python

  from credentials import *
  import cobra.mit.access
  import cobra.mit.request
  import cobra.mit.session
  import cobra.model.fv
  import cobra.model.pol

For *almost* **all** other operations

.. code-block:: python

  import urllib3
  import argparse
  import requests
  import cobra.mit.access
  import cobra.mit.request
  import cobra.mit.session
  import cobra.model.fv
  import cobra.model.ip
  import cobra.model.vz
  import cobra.model.pol
  import cobra.model.vpc
  import cobra.model.fvns
  import cobra.model.lacp
  import cobra.model.phys
  import cobra.model.infra
  import cobra.model.l3ext
  import cobra.model.fabric
  from cobra.internal.codec.xmlcodec import toXMLStr
  from credentials import *

Connect to the APIC
-------------------

Using your credentials

.. code-block:: python

  auth = cobra.mit.session.LoginSession(URL, LOGIN, PASSWORD)
  session = cobra.mit.access.MoDirectory(auth)
  session.login()

Expected output:

- ``SSL Warning``

Create Tenant
-------------

Create a Variable for your *Tenant Name* using your *initials*
For example, John Deere would be ``JD_Cobra_Tenant``

.. code-block:: python

  tenant_name = "INITIALS_Cobra_Tenant"

Create a new tenant

.. code-block:: python

  root = cobra.model.pol.Uni('')
  new_tenant = cobra.model.fv.Tenant(root, tenant_name)

Committing Your Changes
-----------------------

To commit your changes add

.. code-block:: python

  config_request = cobra.mit.request.ConfigRequest()
  config_request.addMo(new_tenant)
  session.commit(config_request)

Expected output:

- ``SSL Warning``
- ``<Response [200]>``

Congratulations
---------------

You have now set up a tenant using the Cobra SDK. You can add policies to your tenant by adding just a few more lines of Python to your file.

Add VRF, Bridge Domain, Gateway, Scope, and Subnet

.. code-block:: python

  TENANT = #INITIALS_Cobra_TENANT
  VRF = #INTIIALS_Cobra_VRF
  BRIDGEDOMAIN = #INTIIALS_Cobra_BRDM
  GATEWAY = #INTIIALS_Cobra_GATE
  SCOPE = #INTIIALS_Cobra_SCOPE
  SUBNETNAME = #INTIIALS_Cobra_SUBNET

Configure Tenant example script

.. code-block:: python

  #!/usr/bin/env python
  import argparse
  import requests
  import cobra.mit.access
  import cobra.mit.session
  import cobra.mit.request
  import cobra.model.pol
  import cobra.model.fv
  from credentials import *

  # create a session and define the root
  requests.packages.urllib3.disable_warnings()
  auth = cobra.mit.session.LoginSession(URL, LOGIN, PASSWORD)
  session = cobra.mit.access.MoDirectory(auth)
  session.login()

  root = cobra.model.pol.Uni('')

  # test if tenant name is already in use
  # build query for existing tenants
  tenant_query = cobra.mit.request.ClassQuery('fvTenant')
  tenant_query.propFilter = 'eq(fvTenant.name, "{}")'.format(tenant_name)

  # test for truthiness
  if apic_session.query(tenant_query):
      print("\nTenant {} has already been created on the APIC\n".format(tenant_name))
      exit(1)

  # model new tenant configuration
  tenant = cobra.model.fv.Tenant(root, name=TENANT)
  vrf = cobra.model.fv.Ctx(tenant, name=VRF)
  bridge_domain = cobra.model.fv.BD(tenant, name=BRIDGEDOMAIN)
  attached_vrf = cobra.model.fv.RsCtx(bridge_domain, tnFvCtxName=VRF)
  subnet = cobra.model.fv.Subnet(bridge_domain, ip=GATEWAY, scope=SCOPE, name=SUBNETNAME)

  #submit the configuration to the apic and print a success message
  config_request = cobra.mit.request.ConfigRequest()
  config_request.addMo(tenant)
  session.commit(config_request)

  print("\nNew Tenant, {}, has been created:\n\n{}\n".format(TENANT, config_request.data))
