import json 
from collections import OrderedDict

def jsonDefault(OrderedDict):
    return OrderedDict.__dict__

class PreAttckObject(object):
    '''
        Parent class of all other MITRE PRE-ATT&CK based classes

        This is a private class and should not be accessed directly
    '''

    _RELATIONSHIPS = None
    
    def __init__(self, **kwargs):
        """
        Sets standard properties that are found in all child classes as well as provides standard methods used by inherited classes
        
        Arguments:
            kwargs (dict) -- Takes the MITRE PRE-ATT&CK Json object as a kwargs values
        """
        self.id = self._set_id(kwargs)
        self.name = self._set_attribute(kwargs, 'name')
        self.description = self._set_attribute(kwargs, 'description')
        self.reference = self._set_reference(kwargs)
        self.created = self._set_attribute(kwargs, 'created')
        self.modified = self._set_attribute(kwargs, 'modified')
        self.type = self._set_attribute(kwargs, 'type')
        

    def __str__(self):
        return json.dumps(self, default=jsonDefault, indent=4)

    def set_relationships(self, attck_obj):
        if not PreAttckObject._RELATIONSHIPS:
            relationship_obj = {}
            for item in attck_obj['objects']:
                if 'type' in item:
                    if item['type'] == 'relationship':
                        source_id = item['source_ref']
                        target_id = item['target_ref']
                        if source_id not in relationship_obj:
                            relationship_obj[source_id] = []
                        relationship_obj[source_id].append(target_id)

                        if target_id not in relationship_obj:
                            relationship_obj[target_id] = []
                        relationship_obj[target_id].append(source_id)
            PreAttckObject._RELATIONSHIPS = relationship_obj

    def set_relationship(self, obj, id, name):
        """Sets relationships on two objects based on a defined relationship from MITRE PRE-ATT&CK
        
        Args:
            obj (dict): MITRE PRE-ATT&CK Json object
            id (str): A MITRE PRE-ATT&CK source reference ID
            name (str): A MITRE PRE-ATT&CK object type
        
        Returns:
            list: A list of related MITRE PRE-ATT&CK related objects based on provided inputs
        """        
        return_list = []
        for item in obj['objects']:
            if 'source_ref' in item:
                if id in item['source_ref']:
                    for o in obj['objects']:
                        if o['type'] == name:
                            if item['target_ref'] in o['id']:
                                return_list.append(o)
        return return_list

    def _set_attribute(self, obj, name):
        """Parent class method to set attribute based on passed in object
           and the name of the property
        
        Arguments:
            obj (dict) -- Provided json objects are passed to this method
            name (str) -- The json property name to set attribute in child classes
        
        Returns:
            (str) -- Returns either the value of the attribute requested or returns 'null'
        """
        try:
            value = obj.get(name)
            return None if not value else value
        except:
            return None


    def _set_list_items(self, obj, list_name):
        """Private method used by child classes and normalizes list items
        
        Args:
            obj (dict) -- Provided json objects are passed to this method
            list_name (str) -- The json property name to set list items attribute in child classes
        
        Returns:
            list: returns a list of values from the provided list_name property
        """        
        item_value = []
        if list_name in obj:
            for item in obj[list_name]:
                item_value.append(item)
                
            return item_value

    def _set_id(self, obj):
        """Returns the MITRE PRE-ATT&CK Framework external ID 
        
        Arguments:
            obj (dict) -- A MITRE PRE-ATT&CK Framework json object
        
        Returns:
            (str) -- Returns the MITRE PRE-ATT&CK Framework external ID
        """
        if "external_references" in obj:
            for p in obj['external_references']:
                for s in p:
                    if p[s] == 'mitre-pre-attack':
                        return p['external_id']
        return 'S0000'
        
    def _set_wiki(self, obj):
        """Returns the MITRE ATT&CK Framework Wiki URL
        
        Arguments:
            obj (dict) -- A MITRE PRE-ATT&CK Framework json object
        
        Returns:
            (str) -- Returns the MITRE PRE-ATT&CK Framework Wiki URL
        """
        if "external_references" in obj:
            for p in obj['external_references']:
                for s in p:
                    if p[s] == 'mitre-attack':
                        return p['url']


    def _set_reference(self, obj):
        """Returns a list of external references from the provided MITRE PRE-ATT&CK Framework json object
        
        Arguments:
            obj (dict) -- A MITRE PRE-ATT&CK Framework json object
        
        Returns:
            (dict) -- Returns a dict containing the following key/value pairs
                external_id (str) -- The MITRE PRE-ATT&CK Framework external ID
                url (str)         -- The MITRE PRE-ATT&CK Framework URL
                source_name (str) -- The MITRE PRE-ATT&CK Framework source name
                description (str) -- The MITRE PRE-ATT&CK Framework description or None if it does not exist
        """
        return_list = []
        if "external_references" in obj:
            for p in obj['external_references']:
                return_list.append(p)
        return return_list
               