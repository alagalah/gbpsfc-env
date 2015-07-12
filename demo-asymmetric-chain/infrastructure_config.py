# Config for switches, tunnelIP is the local IP address.
switches = [
            {'name': 'sw1',
             'type': 'gbp',
             'dpid': '1'},
            {'name': 'sw2',
             'type': 'sff',
             'dpid': '2'},
            {'name': 'sw3',
             'type': 'sf',
             'dpid': '3'},
            {'name': 'sw4',
             'type': 'sff',
             'dpid': '4'},
            {'name': 'sw5',
             'type': 'sf',
             'dpid': '5'},
            {'name': 'sw6',
             'type': 'gbp',
             'dpid': '6'},
            {'name': 'sw7',
             'type': 'none',
             'dpid': '7'},
            {'name': 'sw8',
             'type': 'none',
             'dpid': '8'}
      ]

defaultContainerImage='alagalah/odlpoc_ovs230'

#Note that tenant name and endpointGroup name come from policy_config.py

hosts = [{'name': 'h35_2',
          'mac': '00:00:00:00:35:02',
          'ip': '10.0.35.2/24',
          'switch': 'sw1'},
         {'name': 'h36_4',
          'ip': '10.0.36.4/24',
          'mac': '00:00:00:00:36:04',
          'switch': 'sw6'}
          ]

