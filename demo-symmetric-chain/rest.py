#!/usr/bin/python
import argparse
import requests,json
from requests.auth import HTTPBasicAuth
from subprocess import call
import time
import sys
import os


DEFAULT_PORT='8181'


USERNAME='admin'
PASSWORD='admin'


OPER_NODES='/restconf/operational/opendaylight-inventory:nodes/'
CONF_TENANT='/restconf/config/policy:tenants'

def get(host, port, uri):
    url='http://'+host+":"+port+uri
    r = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    return r

def put(host, port, uri, data, debug=False):
    '''Perform a PUT rest operation, using the URL and data provided'''

    url='http://'+host+":"+port+uri

    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "PUT %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.put(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if debug == True:
        print r.text
    r.raise_for_status()

def post(host, port, uri, data, debug=False):
    '''Perform a POST rest operation, using the URL and data provided'''

    url='http://'+host+":"+port+uri
    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "POST %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if debug == True:
        print r.text
    r.raise_for_status()

def wait_for_sff_in_datastore(url):
    for i in xrange(30):
        resp=get(controller, DEFAULT_PORT, url)
        if ('192.168.50.71' in resp.text) and ('192.168.50.73' in resp.text):
            break
        time.sleep(3)
    if ('192.168.50.71' not in resp.text):
        print "ERROR: SFF1 has not been initialized!"
        sys.exit(1)
    if ('192.168.50.73' not in resp.text):
        print "ERROR: SFF2 has not been initialized!"
        sys.exit(1)




def get_service_functions_uri():
    return "/restconf/config/service-function:service-functions"

def get_service_functions_data():
    return {
    "service-functions": {
        "service-function": [
            {
                "name": "firewall-72",
                "ip-mgmt-address": "192.168.50.72",
                "type": "service-function-type:firewall",
                "nsh-aware": "true",
                "sf-data-plane-locator": [
                    {
                        "name": "2",
                        "port": 6633,
                        "ip": "192.168.50.72",
                        "transport": "service-locator:vxlan-gpe",
                        "service-function-forwarder": "SFF1"
                    }
                ]
            },
            {
                "name": "dpi-74",
                "ip-mgmt-address": "192.168.50.74",
                "type": "service-function-type:dpi",
                "nsh-aware": "true",
                "sf-data-plane-locator": [
                    {
                        "name": "3",
                        "port": 6633,
                        "ip": "192.168.50.74",
                        "transport": "service-locator:vxlan-gpe",
                        "service-function-forwarder": "SFF2"
                    }
                ]
            }
        ]
    }
}

def get_service_function_forwarders_uri():
    return "/restconf/config/service-function-forwarder:service-function-forwarders"

def get_service_function_forwarders_data():
    return {
    "service-function-forwarders": {
        "service-function-forwarder": [
            {
                "name": "SFF1",
                "service-node": "OVSDB2",
                "service-function-forwarder-ovs:ovs-bridge": {
                    "bridge-name": "sw2"
                },
                "service-function-dictionary": [
                    {
                        "name": "firewall-72",
                        "sff-sf-data-plane-locator": {
                            "sf-dpl-name": "2",
                            "sff-dpl-name": "sfc-tun2"
                        }
                    }
                ],
                "sff-data-plane-locator": [
                    {
                        "name": "sfc-tun2",
                        "data-plane-locator": {
                            "transport": "service-locator:vxlan-gpe",
                            "port": 6633,
                            "ip": "192.168.50.71"
                        },
                        "service-function-forwarder-ovs:ovs-options": {
                            "remote-ip": "flow",
                            "dst-port": "6633",
                            "key": "flow",
                            "nsp": "flow",
                            "nsi": "flow",
                            "nshc1": "flow",
                            "nshc2": "flow",
                            "nshc3": "flow",
                            "nshc4": "flow"
                        }
                    }
                ]
            },
            {
                "name": "SFF2",
                "service-node": "OVSDB2",
                "service-function-forwarder-ovs:ovs-bridge": {
                    "bridge-name": "sw4"
                },
                "service-function-dictionary": [
                    {
                        "name": "dpi-74",
                        "sff-sf-data-plane-locator": {
                            "sf-dpl-name": "3",
                            "sff-dpl-name": "sfc-tun4"
                        }
                    }
                ],
                "sff-data-plane-locator": [
                    {
                        "name": "sfc-tun4",
                        "data-plane-locator": {
                            "transport": "service-locator:vxlan-gpe",
                            "port": 6633,
                            "ip": "192.168.50.73"
                        },
                        "service-function-forwarder-ovs:ovs-options": {
                            "remote-ip": "flow",
                            "dst-port": "6633",
                            "key": "flow",
                            "nsp": "flow",
                            "nsi": "flow",
                            "nshc1": "flow",
                            "nshc2": "flow",
                            "nshc3": "flow",
                            "nshc4": "flow"
                        }
                    }
                ]
            }
        ]
    }
}

def get_service_function_chains_uri():
    return "/restconf/config/service-function-chain:service-function-chains/"

def get_service_function_chains_data():
    return {
    "service-function-chains": {
        "service-function-chain": [
            {
                "name": "SFCGBP",
                "symmetric": "true",
                "sfc-service-function": [
                    {
                        "name": "firewall-abstract1",
                        "type": "service-function-type:firewall"
                    },
                    {
                        "name": "dpi-abstract1",
                        "type": "service-function-type:dpi"
                    }
                ]
            }
        ]
    }
}

def get_service_function_paths_uri():
    return "/restconf/config/service-function-path:service-function-paths/"

def get_service_function_paths_data():
    return {
    "service-function-paths": {
        "service-function-path": [
            {
                "name": "SFCGBP-Path",
                "service-chain-name": "SFCGBP",
                "starting-index": 255,
                "symmetric": "true"

            }
        ]
    }
}

def get_tenant_data():
    return {
    "tenant": [
      {
        "id": "f5c7d344-d1c7-4208-8531-2c2693657e12",
        "l2-flood-domain": [
          {
            "id": "393b4a3f-431e-476f-9674-832fb9f5fab9",
            "parent": "7b796915-adf4-4356-b5ca-de005ac410c1"
          },
          {
            "id": "4ae1198e-0380-427f-8386-28281672eca3",
            "parent": "7b796915-adf4-4356-b5ca-de005ac410c1"
          }
        ],
        "name": "DockerTenant",
        "l3-context": [
          {
            "id": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
          }
        ],
        "l2-bridge-domain": [
          {
            "id": "7b796915-adf4-4356-b5ca-de005ac410c1",
            "parent": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
          }
        ],
        "subnet": [
          {
            "id": "49850b5a-684d-4cc0-aafe-95d25c9a4b97",
            "virtual-router-ip": "10.0.36.1",
            "parent": "4ae1198e-0380-427f-8386-28281672eca3",
            "ip-prefix": "10.0.36.1/24"
          },
          {
            "id": "7f43a456-2c99-497b-9ecf-7169be0163b9",
            "virtual-router-ip": "10.0.35.1",
            "parent": "393b4a3f-431e-476f-9674-832fb9f5fab9",
            "ip-prefix": "10.0.35.1/24"
          }
        ],
        "endpoint-group": [
          {
            "id": "e593f05d-96be-47ad-acd5-ba81465680d5",
            "network-domain": "49850b5a-684d-4cc0-aafe-95d25c9a4b97",
            "name" : "webservers",
            "provider-named-selector": [
              {
                "name": "e593f05d-96be-47ad-acd5-ba81465680d5-1eaf9a67-a171-42a8-9282-71cf702f61dd-22282cca-9a13-4d0c-a67e-a933ebb0b0ae",
                "contract": [
                  "22282cca-9a13-4d0c-a67e-a933ebb0b0ae"
                ]
              }
            ]
          },
          {
            "id": "1eaf9a67-a171-42a8-9282-71cf702f61dd",
            "name" : "clients",
            "network-domain": "7f43a456-2c99-497b-9ecf-7169be0163b9",
            "consumer-named-selector": [
              {
                "name": "e593f05d-96be-47ad-acd5-ba81465680d5-1eaf9a67-a171-42a8-9282-71cf702f61dd-22282cca-9a13-4d0c-a67e-a933ebb0b0ae",
                "contract": [
                  "22282cca-9a13-4d0c-a67e-a933ebb0b0ae"
                ]
              }
            ]
          }
        ],
        "subject-feature-instances": {
          "classifier-instance": [
            {
              "name": "icmp",
              "classifier-definition-id": "Classifier-IP-Protocol",
              "parameter-value": [
                {
                  "name": "proto",
                  "int-value": 1
                }
              ]
            },
            {
              "name": "http-dest",
              "classifier-definition-id": "Classifier-L4",
              "parameter-value": [
                {
                  "int-value": "6",
                  "name": "proto"
                },
                {
                  "int-value": "80",
                  "name": "destport"
                }
              ]
            },
            {
              "name": "http-src",
              "classifier-definition-id": "Classifier-L4",
              "parameter-value": [
                {
                  "int-value": "6",
                  "name": "proto"
                },
                {
                  "int-value": "80",
                  "name": "sourceport"
                }
              ]
            }
          ],
          "action-instance": [
            {
              "name": "chain1",
              "action-definition-id": "Action-Chain",
              "parameter-value": [
                {
                  "name": "sfc-chain-name",
                  "string-value": "SFCGBP"
                }
              ]
            },
            {
              "name": "allow1",
              "action-definition-id": "Action-Allow"
            }
          ]
        },
        "contract": [
          {
            "id": "22282cca-9a13-4d0c-a67e-a933ebb0b0ae",
            "subject": [
              {
                "name": "icmp-subject",
                "rule": [
                  {
                    "name": "allow-icmp-rule",
                    "order" : 0,
                    "classifier-ref": [
                      {
                        "name": "icmp",
			"instance-name" : "icmp"
                      }
                    ],
                    "action-ref": [
                      {
                        "name": "allow1",
                        "order": 0
                      }
                    ]
                  }

                ]
              },
              {
                "name": "http-subject",
                "rule": [
                  {
                    "name": "http-chain-rule-in",
                    "classifier-ref": [
                      {
                        "name" : "http-dest",
			"instance-name": "http-dest",
                        "direction": "in"
                      }
                    ],
                    "action-ref": [
                      {
                        "name": "chain1",
                        "order": 0
                      }
                    ]
                  },
                  {
                    "name": "http-chain-rule-out",
                    "classifier-ref": [
                      {
                        "name" : "http-src",
  			"instance-name": "http-src",
                        "direction": "out"
                      }
                    ],
                    "action-ref": [
                      {
                        "name": "chain1",
                        "order": 0
                      }
                    ]
                  }
                ]
              }
            ],
            "clause": [
              {
                "name": "icmp-http-clause",
                "subject-refs": [
                  "icmp-subject",
                  "http-subject"
                ]
              }
            ]
          }
        ]
      }
    ]
}

# Main definition - constants

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu

# =======================
#      MAIN PROGRAM
# =======================

# Main Program

def get_tenant_uri():
    return "/restconf/config/policy:tenants/policy:tenant/f5c7d344-d1c7-4208-8531-2c2693657e12"

def get_tunnel_data_1():
    return {
    "node": [
      {
        "id": "openflow:1",
        "ofoverlay:tunnel": [
          {
            "tunnel-type": "overlay:tunnel-type-vxlan-gpe",
            "node-connector-id": "openflow:1:1",
            "ip": "192.168.50.70",
            "port": 6633
          },
          {
            "tunnel-type": "overlay:tunnel-type-vxlan",
            "node-connector-id": "openflow:1:2",
            "ip": "192.168.50.70",
            "port": 4789
          }
        ]
      }
    ]
  }

def get_tunnel_uri_1():
    return "/restconf/config/opendaylight-inventory:nodes/node/openflow:1"

def get_tunnel_data_6():
    return {
    "node": [
      {
        "id": "openflow:6",
        "ofoverlay:tunnel": [
          {
            "tunnel-type": "overlay:tunnel-type-vxlan-gpe",
            "node-connector-id": "openflow:6:1",
            "ip": "192.168.50.75",
            "port": 6633
          },
          {
            "tunnel-type": "overlay:tunnel-type-vxlan",
            "node-connector-id": "openflow:6:2",
            "ip": "192.168.50.75",
            "port": 4789
          }
        ]
      }
    ]
}

def get_tunnel_uri_6():
    return "/restconf/config/opendaylight-inventory:nodes/node/openflow:6"

def get_endpoint_data():
    return [
{
"input": {

    "endpoint-group": "e593f05d-96be-47ad-acd5-ba81465680d5",

    "network-containment" : "49850b5a-684d-4cc0-aafe-95d25c9a4b97",

    "l2-context": "7b796915-adf4-4356-b5ca-de005ac410c1",
    "mac-address": "00:00:00:00:36:02",

    "l3-address": [
        {
            "ip-address": "10.0.36.2",
            "l3-context": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
        }
    ],
    "port-name": "vethl-h36_2",
    "tenant": "f5c7d344-d1c7-4208-8531-2c2693657e12"
}
},
{
"input": {
    "endpoint-group": "1eaf9a67-a171-42a8-9282-71cf702f61dd",
"network-containment" : "7f43a456-2c99-497b-9ecf-7169be0163b9",
"l2-context": "7b796915-adf4-4356-b5ca-de005ac410c1",
"mac-address": "00:00:00:00:35:02",
"l3-address": [
    {
        "ip-address": "10.0.35.2",
        "l3-context": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
    }
],
"port-name": "vethl-h35_2",
"tenant": "f5c7d344-d1c7-4208-8531-2c2693657e12"
}
},
{
"input": {

    "endpoint-group": "1eaf9a67-a171-42a8-9282-71cf702f61dd",

    "network-containment" : "7f43a456-2c99-497b-9ecf-7169be0163b9",

    "l2-context": "7b796915-adf4-4356-b5ca-de005ac410c1",
    "mac-address": "00:00:00:00:35:03",

    "l3-address": [
        {
            "ip-address": "10.0.35.3",
            "l3-context": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
        }
    ],
    "port-name": "vethl-h35_3",
    "tenant": "f5c7d344-d1c7-4208-8531-2c2693657e12"
}
},
{
"input": {

    "endpoint-group": "e593f05d-96be-47ad-acd5-ba81465680d5",

    "network-containment" : "49850b5a-684d-4cc0-aafe-95d25c9a4b97",

    "l2-context": "7b796915-adf4-4356-b5ca-de005ac410c1",
    "mac-address": "00:00:00:00:36:03",

    "l3-address": [
        {
            "ip-address": "10.0.36.3",
            "l3-context": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
        }
    ],
    "port-name": "vethl-h36_3",
    "tenant": "f5c7d344-d1c7-4208-8531-2c2693657e12"
}
},
{
"input": {

    "endpoint-group": "e593f05d-96be-47ad-acd5-ba81465680d5",

    "network-containment" : "49850b5a-684d-4cc0-aafe-95d25c9a4b97",

    "l2-context": "7b796915-adf4-4356-b5ca-de005ac410c1",
    "mac-address": "00:00:00:00:36:04",

    "l3-address": [
        {
            "ip-address": "10.0.36.4",
            "l3-context": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
        }
    ],
    "port-name": "vethl-h36_4",
    "tenant": "f5c7d344-d1c7-4208-8531-2c2693657e12"
}
},
{
"input": {

    "endpoint-group": "1eaf9a67-a171-42a8-9282-71cf702f61dd",

    "network-containment" : "7f43a456-2c99-497b-9ecf-7169be0163b9",

    "l2-context": "7b796915-adf4-4356-b5ca-de005ac410c1",
    "mac-address": "00:00:00:00:35:04",

    "l3-address": [
        {
            "ip-address": "10.0.35.4",
            "l3-context": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
        }
    ],
    "port-name": "vethl-h35_4",
    "tenant": "f5c7d344-d1c7-4208-8531-2c2693657e12"
}
},
{
"input": {

    "endpoint-group": "1eaf9a67-a171-42a8-9282-71cf702f61dd",

    "network-containment" : "7f43a456-2c99-497b-9ecf-7169be0163b9",

    "l2-context": "7b796915-adf4-4356-b5ca-de005ac410c1",
    "mac-address": "00:00:00:00:35:05",

    "l3-address": [
        {
            "ip-address": "10.0.35.5",
            "l3-context": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
        }
    ],
    "port-name": "vethl-h35_5",
    "tenant": "f5c7d344-d1c7-4208-8531-2c2693657e12"
}
},
{
"input": {

    "endpoint-group": "e593f05d-96be-47ad-acd5-ba81465680d5",

    "network-containment" : "49850b5a-684d-4cc0-aafe-95d25c9a4b97",

    "l2-context": "7b796915-adf4-4356-b5ca-de005ac410c1",
    "mac-address": "00:00:00:00:36:05",

    "l3-address": [
        {
            "ip-address": "10.0.36.5",
            "l3-context": "cbe0cc07-b8ff-451d-8171-9eef002a8e80"
        }
    ],
    "port-name": "vethl-h36_5",
    "tenant": "f5c7d344-d1c7-4208-8531-2c2693657e12"
}
}]

def get_endpoint_uri():
    return "/restconf/operations/endpoint:register-endpoint"

def get_tunnel_oper_uri():
    return "/restconf/operational/opendaylight-inventory:nodes/"

def get_topology_oper_uri():
    return "/restconf/operational/network-topology:network-topology/topology/ovsdb:1/"

if __name__ == "__main__":
    # Launch main menu


    # Some sensible defaults
    controller=os.environ.get('ODL')
    if controller == None:
        sys.exit("No controller set.")

    print "Contacting controller at %s" % controller
    print "waiting for manager on SFFs..."
    wait_for_sff_in_datastore(get_topology_oper_uri())
    print "sending service functions"
    put(controller, DEFAULT_PORT, get_service_functions_uri(), get_service_functions_data(), True)
    print "sending service function forwarders"
    put(controller, DEFAULT_PORT, get_service_function_forwarders_uri(), get_service_function_forwarders_data(), True)
    print "waiting for switches on SFFs..."
    wait_for_sff_in_datastore(get_tunnel_oper_uri())
    print "sending service function chains"
    put(controller, DEFAULT_PORT, get_service_function_chains_uri(), get_service_function_chains_data(), True)
    print "sending service function paths"
    put(controller, DEFAULT_PORT, get_service_function_paths_uri(), get_service_function_paths_data(), True)
    print "sending tunnel"
    put(controller, DEFAULT_PORT, get_tunnel_uri_1(), get_tunnel_data_1(), True)
    print "sending tenant"
    put(controller, DEFAULT_PORT, get_tunnel_uri_6(), get_tunnel_data_6(), True)
    print "sending tenant"
    put(controller, DEFAULT_PORT, get_tenant_uri(), get_tenant_data(),True)
    print "registering endpoints"
    for endpoint in get_endpoint_data():
        post(controller, DEFAULT_PORT, get_endpoint_uri(),endpoint,True)
