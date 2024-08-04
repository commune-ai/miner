import commune as c

class Subnets(c.Module):


    def __init__(self, network='commune'):
        self.set_network(network)


    def set_subnets_path(self, path):
        self.subnets_path = path
        return {
        'msg': f"Set subnets_path to {path}", 
        'subnets_path': path
        }

    def set_network(self, network):
        self.network = network
        self.set_subnets_path('/'.join(__file__.split('/')[:-1]))
        self.state_path = f"{self.subnets_path}/state.json"
        self.state =  c.get_json(self.state_path)
        return {
        'msg': f"Set network to {network}", 
        'network': network, 
        'state_path': self.state_path
        }

    def shortcut2network(self):
        shortcut_map =  {k:v.get('shortcuts') for k,v in self.state.items()}
        shortcut2network = {}
        for network, shortcuts in shortcut_map.items():
            for shortcut in shortcuts:
                shortcut2network[shortcut] = network
            
        return shortcut2network

    def resolve_network(self, network):
        if network == None:
            network = self.network
        shortcut2network = self.shortcut2network()
        network = shortcut2network.get(network, network)
        return network


    @property
    def networks(self):
        return list(self.state.keys())
    
    def clone_subnet(self, subnet, network):

        try:
            network = self.resolve_network(network)
            if self.exists(subnet):
                return f"{subnet} already exists."
            name2link = self.name2link()
            link2name = {v: k for k, v in name2link.items()}

            if subnet in name2link:
                url = name2link[subnet]
            else:
                url = subnet
            repo_name = link2name[url]

            return c.cmd(f"git clone {url} {self.subnets_path}/{network}/{repo_name}")
        except Exception as e:
            return str(e)



    def clone_all(self, network='all'):
        return self.clone_network(network)

    def clone_network(self, network=None, timeout=60):
        futures = []
        network = self.resolve_network(network)
        state = self.state
        if network == 'all':
            for network in self.networks:
                links = state[network]['links']
                for link in links:
                    print(f"Cloning {link}")
                    params =  {'subnet':link, 'network': network}
                    futures.append(c.submit(self.clone_subnet,params))
        else:
            links = state[network]['links']
            for link in links:
                print(f"Cloning {link}")
                params =  {'subnet':link, 'network': network}
                futures.append(c.submit(self.clone_subnet,params))
            
        results = []
        for future in c.as_completed(futures, timeout=timeout):
            print(future.result())
            results.append(future.result())
        
        n = len(results)

        return {'msg': f"Cloned {n} subnets."}


    def subnets(self, network=None):
        path2name = lambda p: p.split('/')[-1]
        if network == 'all':
            subnets = []
            for network in self.networks:
                subnets.extend(self.subnets(network))
            return subnets
        network = self.resolve_network(network)
        return [path2name(p) for p in self.ls(f"{self.subnets_path}/{network}")]

    def network2subnets(self):
        newtork2subnets = {}
        for network in self.networks:
            newtork2subnets[network] = self.subnets(network)
        return newtork2subnets
    
    def subnet2network(self):
        network2subnets = self.network2subnets()
        subnet2network = {}
        for network, subnets in network2subnets.items():
            for subnet in subnets:
                subnet2network[subnet] = network
        return subnet2network

    def link2network(self):
        network2subnets = self.network2subnets()
        link2network = {}
        for network, subnets in network2subnets.items():
            for subnet in subnets:
                link = self.name2link().get(subnet)
                link2network[link] = network
        return link2network


    def all_subnets(self):
        return self.subnets(network='all')
    def exists(self, name):
        return name in self.subnets()
    
    def get_link_name(self, link):  
        if link.endswith('/'):
            return link.split('/')[-2]
        return link.split('/')[-1]
    
    def find(self, search):
        name2link = self.name2link()
        found_links = [name2link[n] for n in name2link if search in n]
        return found_links
    
    def name2link(self):
        links = self.links(network='all')
        name2link = {}
        for link in links:
            name = self.get_link_name(link)
            name2link[name] = link
        return name2link



    def network2links(self):
        network2links = {}
        for network in self.networks:
            network2links[network] = self.links(network)
        return network2links

    
    def links(self, network=None):
        network = self.resolve_network(network)
        state = self.state
        links = []
        if network == 'all':
            for s in state.values():
                links.extend(s['links'])
        else:
            assert network in state, f"{network} not in state."
            links = state[network]['links']
        return links
    
    def is_path_subnet(self, path):
        return self.isdir(path) and not path.startswith('__')

    def subnet2files(self):
        subnet2path = {}
        for p in self.ls(self.subnets_path):
            if self.is_path_subnet(p):
                name = p.split('/')[-1]
                subnet2path[name] = c.glob(p)
        
        return subnet2path
                
    def subnet2readme(self):
        subnet2readme = {}
        for name, files in self.subnet2files().items():
            for file in files:
                if 'readme' in file.lower():
                    readme = c.get_text(file)
                    subnet2readme[name] = readme
                    break
        return subnet2readme
    
    def subnet2info(self):
        subnet2readme = self.subnet2readme()
        subnet2files = self.subnet2files()

        subnet2info = {}
        for name, files in subnet2files.items():
            
            subnet2info[name] = {
                'cwd': f"{self.subnets_path}/{name}",
                'files': files,
                'readme': subnet2readme.get(name, None)
            }
        
        return subnet2info

    def subnet_info(self, name):
        return self.subnet2info().get(name, None)
    
    def files(self, path='./subnets', search=None):
        files =  c.glob(path)
        if search:
            files = [f for f in files if search in f]
        return files