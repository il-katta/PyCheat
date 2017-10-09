class Entity(object):
    properties = None
    mm = None

    def __init__(self, memory_manager):
        self.properties = {}
        self.mm = memory_manager

    def add(self, name, offsets=None, address=None, vtype=None, size=None, true_value=1, false_value=0, booltype='int'):
        assert vtype is not None and vtype in ["float", "string", "int", "bool", "byte", "uint"], \
            "type must be 'float', 'string', 'bool', 'byte', 'uint' or 'int'"
        assert name not in self.properties.keys(), "property %s already exists" % name

        self.properties[name] = {
            'name': name,
            'offsets': offsets,
            '_address': address,
            'type': vtype,
            'size': size,
            'true_value': true_value,
            'false_value': false_value,
            'booltype': booltype
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

    def getPTRAddress(self, PTR_label):
        return self.mm.resolve_label(PTR_label)

    def write(self, name, value, type=None):
        assert self.properties is not None, "object not initialized"
        assert self.has_attribute(name), "Property doesn't exists"
        # print ("of %s write %s" % (self.__class__.__name__, name))
        property = self.properties[name]
        if type is None:
            type = property['type']

        if type == 'float':
            return self.mm.write_float(property['address'], value)

        elif type == 'string':
            return self.mm.write_string(property['address'], value, property['size'])

        elif type == 'int':
            return self.mm.write_int(property['address'], value)

        elif type == 'bool':
            if value:
                return self.write(name, property['true_value'], property['booltype'])
            else:
                return self.write(name, property['false_value'], property['booltype'])

        elif type == 'byte':
            return self.mm.write_byte(property['address'], value)

        elif type == 'uint':
            return self.mm.write_uint(property['address'], value)

        else:
            raise NotImplementedError()

    def read(self, name, type=None):
        assert self.properties is not None, "object not initialized"
        assert self.has_attribute(name), "Property doesn't exists"
        property = self.properties[name]
        # print ("of %s read %s" % (self.__class__.__name__, name))
        if type is None:
            type = property['type']

        if type == 'float':
            return self.mm.read_float(property['address'])

        elif type == 'string':
            return self.mm.read_string(property['address'], property['size'])

        elif type == 'int':
            return self.mm.read_int(property['address'])

        elif type == 'bool':
            v = self.read(name, property['booltype'])
            if v == property['true_value']:
                return True
            if v == property['false_value']:
                return False
            return None

        elif type == 'byte':
            return self.mm.read_byte(property['address'])

        elif type == 'uint':
            return self.mm.read_uint(property['address'])

        else:
            raise NotImplementedError()

    def __getattr__(self, name):
        if not self.has_attribute(name):
            return super(Entity, self).__getattribute__(name)
        return self.read(name)

    def __setattr__(self, name, value):
        if not self.has_attribute(name):
            super(Entity, self).__setattr__(name, value)
        else:
            self.write(name, value)

    def has_attribute(self, name):
        return self.properties is not None and name in self.properties.keys()
