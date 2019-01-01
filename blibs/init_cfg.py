
import os
import yaml
import inspect
import pprint
import ntpath
import argparse

pp = pprint.PrettyPrinter(indent=4)
def get_command_line_options():
	print("get command line options")
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--fullreg')
	parser.add_argument('-l', '--local')
	parser.parse_args()

def get_primary_cfg_fn():
	cwd = os.getcwd()  # get the current working directory
	frm = inspect.stack()[1]  # need to inspect hte stack to get the calling script
	pp.pprint(inspect.stack())
	root_fp = frm[1]  # filepath, filename, and filedirectory, so this is the root filepath
	root_dir = ntpath.dirname(root_fp)
	cfg_dir = "cfg"
	script_name = ntpath.basename(root_fp) #returns the script name
	script_name = os.path.splitext(script_name)[0] # now returns the script name without the extension
	cfg_fn = script_name + "_config.yml"
	cfg_fp = os.path.join(cwd, cfg_dir)
	cfg_fp = os.path.join(cfg_fp, cfg_fn)
	return (cfg_fp, cfg_fn)

def get_cfg_object():
	get_command_line_options()
	cwd = os.getcwd()  # get the current working directory
	frm = inspect.stack()[1]  # need to inspect hte stack to get the calling script
	root_fp = frm[1]  # filepath, filename, and filedirectory, so this is the root filepath
	root_dir = ntpath.dirname(root_fp)
	cfg_dir = "cfg"
	script_name = ntpath.basename(root_fp) #returns the script name
	script_name = os.path.splitext(script_name)[0] # now returns the script name without the extension
	cfg_fn = script_name + "_config.yml"
	cfg_fp = os.path.join(cwd, cfg_dir)
	cfg_fp = os.path.join(cfg_fp, cfg_fn)
	print("cfg_fp: ", cfg_fp)
	with open(cfg_fp, 'r') as ymlfile:
		try:
			cfg_obj = yaml.load(ymlfile)
			print(type(cfg_obj))
			cfg_obj["general"]["script_name"] = script_name
			cfg_obj["path"]["root"] = root_dir  #  add the root directory to the config object
		except Exception as e:
			print("Error %s" % (e))
			print("There is an issue reading config file: %s" % (cfg_fp))
			exit()
	return cfg_obj

def read_yaml(yaml_fp):
	with open(yaml_fp, 'r') as ymlfile:
		cfg_obj = yaml.load(ymlfile)
	return cfg_obj
	
def merge_two_dicts(x, y):
	"""Given two dicts, merge them into a new dict as a shallow copy."""
	z = x.copy()
	z.update(y)
	return z

def single_level_config_merge(global_cfg_obj, local_cfg_obj):
	for outer_key in list(global_cfg_obj.keys()):
		print("outer_key: ", outer_key)
		if (outer_key in local_cfg_obj):
			try:
				for inner_layer_key in list(local_cfg_obj[outer_key].keys()): # .keys fails if it's not a dict of dicts, so just copy our local configuration then
					if inner_layer_key not in global_cfg_obj[outer_key]:
						print("inner layer key %s not found in main config, but i'm going to add it" % (inner_layer_key))
					global_cfg_obj[outer_key][inner_layer_key] = local_cfg_obj[outer_key][inner_layer_key]
			except AttributeError: # attibute error should come up because its not a dict of dicts, it's a list, so just copy it
				if local_cfg_obj[outer_key] is not None:
					global_cfg_obj[outer_key] = local_cfg_obj[outer_key][:]
	return global_cfg_obj

def get_all_config_files(cfg_dp = None, file_exts = ('.yml','.yaml'), global_cfg_fp = None, global_cfg_fn = None):  # get all configuration files and append the config object
	get_command_line_options()
	print("Global Configuration File %s at %s" % (global_cfg_fn, global_cfg_fp))
	with open(global_cfg_fp, 'r') as ymlfile:
		try:
			global_cfg_obj = yaml.load(ymlfile)
		except:
			print("Error attempting to load the global configuration object from the global configuration file")
	cwd = os.getcwd()  # get the current working directory
	global_cfg_obj["path"]["root"] = cwd  # add the root directory to the config object
	if (cfg_dp == None):
		cfg_dir = "cfg"
		cfg_dp = os.path.join(cwd, cfg_dir)
	local_cfg_fns = [fn for fn in os.listdir(cfg_dp) if (fn.endswith(file_exts) and fn != global_cfg_fn)] # get all the yml files in the configuration directory
	if len(local_cfg_fns) == 0: # no local configuration files were found, return our global object
		return global_cfg_obj
	else:
		print("Local Configuration File(s): %s " % (local_cfg_fns))
	for fn in local_cfg_fns: # use multiple, but probably only a single local config
		local_cfg_fp = os.path.join(cfg_dp, fn)
		# print "cfg_fp: ", cfg_fp
		with open(local_cfg_fp, 'r') as ymlfile:
			local_cfg_obj = yaml.load(ymlfile)
			final_cfg_obj = single_level_config_merge(global_cfg_obj, local_cfg_obj)
	pp.pprint(final_cfg_obj)
	print("after dict merge")

	return final_cfg_obj

def info(msg):
	frm = inspect.stack()[1]
	print("frm: ", frm)
	mod = inspect.getmodule(frm[0])
	print("mod: ", pp.pprint(mod))
	print('[%s] %s' % (mod.__name__, msg))