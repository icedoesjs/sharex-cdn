import yaml 

def load_config(fp: str):
    '''
    Load the yaml config
    
    Params:
        fp (str): The config's file path (use os.path.abspath)
    
    Returns:
        config_dict (dict): The parsed config in dictionary form.
    '''
    with open(fp) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config