import configparser
import sys

def import_module(relative_name):
    raise NotImplementedError('import_module must be overridden by module client')

def import_plugin(plug_type, plugin):
    module_name = '.plugins.{}.{}'.format(plug_type, plugin)
    return import_module(module_name)

def get_best_wan_ip(plugins, config):
    # The best WAN IP is found by searching in order for WAN IPs provided
    # by each method, until a sensible result is reached
    for plugin_name in plugins:
        plugin = import_plugin('lookup', plugin_name)
        try:
             # get_wan_ip is the plugin's hook
            return plugin.get_wan_ip(config[plugin_name])
        except Exception as e:
            print(e) # Not a problem, we'll try the next one

    # If we couldn't find anything, now that's a real problem
    raise RuntimeError('Unable to determine WAN IP by any method!')

def update_all_target_records(plugins, wan_ip, config):
    # Each loaded plugin defines a place where the WAN IP needs to be sent
    # in turn and all need to be run
    for plugin_name in plugins:
        plugin = import_plugin('target', plugin_name)
        try:
            # update_target_record is the plugin's hook
            plugin.update_target_record(wan_ip, config[plugin_name])
        except Exception as e:
            print(e) # Log and move on

def run(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    lookup_plugins = config['lookup']['plugins'].split()
    wan_ip = get_best_wan_ip(lookup_plugins, config)
    print(wan_ip)

    target_plugins = config['target']['plugins'].split()
    update_all_target_records(target_plugins, wan_ip, config)