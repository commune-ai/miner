import commune as c
state = {
        "bittensor": [

                "impel-intelligence/dippy-bittensor-subnet",
                "backend-developers-ltd/ComputeHorde",
                "macrocosm-os/data-universe",
                "namoray/vision",
                "macrocosm-os/folding/",
                "It-s-AI/llm-detection/",
                "afterpartyai/bittensor-conversation-genome-project/",
                "macrocosm-os/finetuning/",
            ], 
        "commune": [ 
                "nakamoto-ai/zangief", 
                "agicommies/synthia", 
                "Open0xScope/openscope", 
                "kaiwa-dev/kaiwa-subnet", 
                "Agent-Artificial/eden-subnet", 
                "mosaicx-org/mosaic-subnet/", 
                "MarketCompassDev/marketcompass-subnet/", 
                "panthervis/prediction-subnet/", 
                "Comtensor/comtensor/", 
                "smart-window/comchat-subnet/", 
                "bigideainc/CommuneImplementation/"
            ]
    }




class Subnets(c.Module):
    state = state
    repo_path = '/'.join(__file__.split('/')[:-1])
    subnets_path = f"{repo_path}/subnets"
    state_path = f"{repo_path}/state.json"
    def __init__(self, network='all'):
        self.set_network(network)

    def set_network(self, network):
        self.network = network
        return {
        'msg': f"Set network to {network}", 
        'network': network, 
        }

    def resolve_network(self, network):
        if network == None:
            network = self.network
        else:
            networks = self.networks()
            if network == 'all':
                return network
            if network not in networks:
                for n in networks:
                    if network in n:
                        network = n
                        break
        return network

    def networks(self, forget_preffixes=['archive', '__']):
        return [k for k in  self.state.keys() if not any([k.startswith(p) for p in forget_preffixes])]
    
    def resolve_url(self, url):
        prefix = "https://github.com/"
        if not url.startswith(prefix):
            url = f"{prefix}{url}"
        if url.endswith('/'):
            url = url[:-1]
        if not url.endswith('.git'):
            url = f"{url}.git"
        return url
    
    def get_subnet_path(self, subnet:str, network:str):
        network = self.resolve_network(network)
        return f"{self.subnets_path}/{network}/{subnet}"
    
    def paths(self, network=None):
        network = self.resolve_network(network)
        from glob import glob

        if network == 'all':
            return glob(f"{self.subnets_path}/*/*")
        else:
            return glob(f"{self.subnets_path}/{network}/*")
        

    def name2path(self, network=None):
        network = self.resolve_network(network)
        name2path = {}
        for path in self.paths(network):
            name = path.split('/')[-1]
            name2path[name] = path
        return name2path
        
    
    def clone_subnet(self, subnet, network):
        url = self.name2url(network=network)[subnet]
        path = self.get_subnet_path(subnet, network=network)
        print(f"Cloning {subnet} from {url} -> {path}")
        return c.cmd(f"git clone {url} {path}")

    def rm_subnet(self, subnet, network=None):
        network = self.resolve_network(network)
        path = self.get_subnet_path(subnet=subnet, network=network)
        return c.rm(path)


    def clone_all(self, network='all'):
        return self.clone_network(network)
    clone = clone_all
    def clone_network(self, network=None, timeout=60):
        futures = []
        network = self.resolve_network(network)
        subnets = self.subnets(network=network)
        if network == 'all':
            future2network = {}
            for network in self.networks():
                future = c.submit(self.clone_network, dict(network=network))
                future2network[future] = network
            results = {}
            for future in c.as_completed(future2network, timeout=timeout):
                network = future2network[future]
                results[network] = future.result()

            return results
                               
        else:
            for subnet in subnets:
                print(f"Cloning {subnet}")
                futures.append(c.submit(self.clone_subnet, {'subnet':subnet, 'network':network}))
            results = []
            for future in c.as_completed(futures, timeout=timeout):
                print(future.result())
                results.append(future.result())
        
        n = len(results)

        new_subnets = [r for r in results if 'Cloning' in r and 'not found' not in r]
        return {'network': network, 'n': n, 'new_subnets': new_subnets}

    def search(self, search, network=None):
        subnets = self.subnets(network=network)
        found = [s for s in subnets if search in s]
        return found
    
    def subnets(self, network=None, search=None,):
        subnets = list(self.name2url(network).keys())
        if search:
            subnets = [s for s in subnets if search in s]
        return sorted(list(set(subnets)))

    def network2subnets(self):
        newtork2subnets = {}
        for network in self.networks():
            newtork2subnets[network] = self.subnets(network)
        return newtork2subnets
    

    def all_subnets(self):
        return self.subnets(network='all')
    def exists(self, name):
        return name in self.subnets()
    
    def get_url_name(self, link):  
        if link.endswith('/'):
            link = link[:-1]
        return link.split('/')[-1].split('.git')[0]
    
    
    def find(self, search):
        name2url = self.name2url()
        found_links = [name2url[n] for n in name2url if search in n]
        return found_links
    
    def urls(self, network=None):
        network = self.resolve_network(network)
        urls = []
        if network == 'all':
            for network in self.networks():
                urls += self.urls(network)
        else:
            urls = list(map(self.resolve_url, self.state[network]))
        return urls
        
    
    def name2url(self, network=None, search=None):
        urls = self.urls(network=network)
        name2url = {}
        for url in urls:
            if search and search not in url:
                continue
            name = self.get_url_name(url)
            name2url[name] = url
        return name2url



    def network2links(self):
        network2links = {}
        for network in self.networks():
            network2links[network] = self.links(network)
        return network2links

    
    def links(self, network=None):
        network = self.resolve_network(network)
        state = self.state
        links = []
        if network == 'all':
            for s in state.values():
                links.extend(s)
        else:
            assert network in state, f"{network} not in state."
            links = state[network]
        return links
    
    def is_path_subnet(self, path):
        return self.isdir(path) and not path.startswith('__')

    def name2files(self):
        name2files = {}
        name2path = self.name2path()
        for name, path in name2path.items():
            for p in self.ls(path):
                name2files[name] = self.ls(path)
        return name2files
    
    def name2readme(self):
        name2readme = {}
        name2files = self.name2files()
        for name, files in name2files.items():
            for file in files:
                if 'readme' in file.lower():
                    readme = c.get_text(file)
                    name2readme[name] = readme
                    break
        return name2readme
                    
                
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
    
    def git_repos(self, path='./'):
        import os
        repos = []
        for root, dirs, files in os.walk(path):
            for d in dirs:
                if d.endswith('.git'):
                    repos +=  [f"{root}"]

        repos = [r for r in repos if not r == path]

        return repos


    def rm_repos(self, path='./'):
        repos = self.git_repos(path)
        for repo in repos:
            c.rm(repo)
            print(f"Removed {repo}")
        return repos
