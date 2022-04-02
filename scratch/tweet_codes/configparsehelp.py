from configparser import ConfigParser

# ConfigParse Parses the config file
file = 'config.ini'
config = ConfigParser()
config.read(file)

# Accessing the Sections
print(config.sections())
print(config['path'])
print(list(config['path']))

# Accessing the Elements
print(config['path']['scratch_jsonfiles'])


# Updating the config File with new section
'''
config.add_section('note')
config.set('note','n','sgjh')

with open(file,'w') as f:
    config.write(f)
f.close()
'''