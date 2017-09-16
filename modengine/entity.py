class Entity(object):
    properties = None
    mm = None

    def __init__(self, memory_manager):
        self.properties = {}
        self.mm = memory_manager

    def add(self, name, offsets=None, address=None, vtype=None, size=None, true_value=1, false_value=0):
        assert vtype == None or vtype in ["float", "string", "int",
                                          "bool"], "type must be 'float', 'string', 'bool' or 'int'"
        assert name not in self.properties.keys(), "property %s already exists" % name

        self.properties[name] = {
            'name': name,
            'offsets': offsets,
            '_address': address,
            'type': vtype,
            'size': size,
            'true_value': true_value,
            'false_value': false_value
        }
        # if type(self.properties[name]['offsets']) is not list:

        if self.properties[name]['offsets'] is not None:
            assert type(self.properties[name]['offsets']) is list
            self.properties[name]['address'] = self.mm.get_pointer_address(
                self.properties[name]['_address'],
                self.properties[name]['offsets']
            )
        else:
            self.properties[name]['address'] = self.properties[name]['_address']

    def write(self, name, value):
        assert self.properties is not None, "object not initialized"
        assert self.has_attribute(name), "Property doesn't exists"

        property = self.properties[name]

        if property['type'] == 'float':
            return self.mm.write_float(property['address'], value)

        elif property['type'] == 'string':
            return self.mm.write_string(property['address'], value, property['size'])

        elif property['type'] == 'int':
            return self.mm.write_int(property['address'], value)

        elif property['type'] == 'bool':
            return self.mm.write_bool(property['address'], value, property['true_value'], property['false_value'])

        else:
            raise NotImplementedError()

    def read(self, name):
        assert self.properties is not None, "object not initialized"
        assert self.has_attribute(name), "Property doesn't exists"
        property = self.properties[name]

        if property['type'] == 'float':
            return self.mm.read_float(property['address'])

        elif property['type'] == 'string':
            return self.mm.read_string(property['address'], property['size'])

        elif property['type'] == 'int':
            return self.mm.read_int(property['address'])

        elif property['type'] == 'bool':
            return self.mm.read_bool(
                property['address'],
                true_value=property['true_value'],
                false_value=property['false_value']
            )

        else:
            raise NotImplementedError()

    def __getattr__(self, name):
        if not self.has_attribute(name):
            raise AttributeError

        return self.read(name)

    def __setattr__(self, name, value):
        if not self.has_attribute(name):
            super(Entity, self).__setattr__(name, value)
        else:
            self.write(name, value)

    def has_attribute(self, name):
        return self.properties is not None and name in self.properties.keys()