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

print('=====Interactive ACI Builder=====')
print('#################################')
print("Welcome to Build an ACI Workshop")
print("=================================")


def login():
    '''Login into ACI'''
    ls = cobra.mit.session.LoginSession(URL, LOGIN, PASSWORD)
    md = cobra.mit.access.MoDirectory(ls)
    md.login()


def buildSpineLeaf(name):
    '''Build the Spine and Leaf Topology'''
    top = md.lookupByDn("uni/controller/nodeidentpol")
    leaf1 = cobra.model.fabric.NodeIdentP(top, serial=u'IT381-1-101', nodeId=u'101', name=u'leaf-1')
    leaf2 = cobra.model.fabric.NodeIdentP(top, serial=u'IT381-1-102', nodeId=u'102', name=u'leaf-2')
    spine1 = cobra.model.fabric.NodeIdentP(top, serial=u'IT381-1-103', nodeId=u'201', name=u'spine-1')


def commitChanges():
    '''Commit Changes'''
    print("Changes to be committed")
    ## TODO: add changes logic
    _ = raw_input('Save changes? (y/n): ')
    if _[0].upper() == 'n':
        print("No changes saved.")
        pass
    else:
        c = cobra.mit.request.ConfigRequest()
        c.addMo(top) #Spine/Leaf commits

        md.commit(c)


if __name__=='__main__':
    login()
    # print("Main Menu")
    buildSpineLeaf()
    commitChanges()
