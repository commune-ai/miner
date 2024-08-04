
## Usage

To get the networks
```bash
c agent/networks
```
['bittensor', 'commune']


To clone all of the subnets
```bash
c agent/clone_all
```
{'msg': 'Cloned 48 subnets.'}

To list all of the subnets
```bash
c agent/subnets
```
[
    'comchat-subnet',
    'comtensor',
    'eden-subnet',
    'kaiwa-subnet',
    'marketcompass-subnet',
    'mosaic-subnet',
    'openscope',
    'prediction-subnet',
    'synthia',
    'zangief'
]


To remove a subnet

```bash
c agent/remove_subnet CommuneImplementation
```
{'success': True, 'message': '~/subnets/subnet/commune/CommuneImplementation removed'}





