from modengine.entity import Entity
from modengine.memory.memorymanager import MemoryManager

GAME = 'steam'

class GTA5Entity(Entity):
    if GAME == 'steam':
        WorldPTR_label = 'GTA5.EXE+236ADE0' # 'gta5!start+0xc667d8'
        BlipPTR_label = 'GTA5.EXE+1F9A2C0'  # 'gta5!start+0x895cb8'
        AmmoPTR_label = 'GTA5.EXE+E89425'
        ClipPTR_label = 'GTA5.EXE+E893E0'
        GetPointerAddressA_label = 'GTA5.EXE!start+14e7d78'
        ObjectsPTR_label = 'GTA5.EXE+1E92AB8'
        NamePTR_label = 'GTA5.EXE+0274E7A8'
        PlayerListPTR_label = 'GTA5.EXE+1CE49C0'
        GloablPTR_label = 'GTA5.EXE+16EB380'
    else:
        WorldPTR_label = 'GTA5.EXE+2366EC8'
        BlipPTR_label = 'GTA5.EXE+1F9E750'
        AmmoPTR_label = 'GTA5.EXE+E88EB9'
        ClipPTR_label = 'GTA5.EXE+E88E74'
        GetPointerAddressA_label = '??'
        ObjectsPTR_label = 'GTA5.EXE+1E90138'
        NamePTR_label = 'GTA5.EXE+02749450'
        PlayerListPTR_label = 'GTA5.EXE+1CE0AA0'
        GloablPTR_label = 'GTA5.EXE+16F5EF0'

    _WorldPTR = None
    _BlipPTR = None
    _AmmoPTR = None
    _ClipPTR = None
    _ObjectsPTR = None
    _getPTRAddress = None
    _NamePTR = None
    _PlayerListPTR = None
    _GloablPTR = None
    def __init__(self):
        super(GTA5Entity, self).__init__(MemoryManager("GTA5.EXE"))

    @property
    def WorldPTR(self):
        if self._WorldPTR is None:
            self._WorldPTR = self.getPTRAddress(self.WorldPTR_label)
        return self._WorldPTR

    @property
    def BlipPTR(self):
        if self._BlipPTR is None:
            self._BlipPTR = self.getPTRAddress(self.BlipPTR_label)
        return self._BlipPTR

    @property
    def ClipPTR(self):
        if self._ClipPTR is None:
            self._ClipPTR = self.getPTRAddress(self.ClipPTR_label)
        return self._ClipPTR

    @property
    def AmmoPTR(self):
        if self._AmmoPTR is None:
            self._AmmoPTR = self.getPTRAddress(self.AmmoPTR_label)
        return self._AmmoPTR

    @property
    def ObjectsPTR(self):
        if self._ObjectsPTR is None:
            self._ObjectsPTR = self.getPTRAddress(self.ObjectsPTR_label)
        return self._ObjectsPTR

    @property
    def GetPointerAddressA(self):
        if self._getPTRAddress is None:
            self._getPTRAddress = self.getPTRAddress(self.GetPointerAddressA_label) + 0x8
        return self._getPTRAddress

    @property
    def NamePTR(self):
        if self._NamePTR is None:
            self._NamePTR = self.getPTRAddress(self.NamePTR_label)
        return self._NamePTR

    @property
    def PlayerListPTR(self):
        if self._PlayerListPTR is None:
            self._PlayerListPTR = self.getPTRAddress(self.PlayerListPTR_label)
        return self._PlayerListPTR

    @property
    def GloablPTR(self):
        if self._GloablPTR is None:
            self._GloablPTR = self.getPTRAddress(self.GloablPTR_label)
        return self._GloablPTR

    def self_test(self):
        for property_name in self.properties:
            print("testing %s" % property_name)
            try:
                prop_value = self.__getattr__(property_name)
                print("%s : %s" % (property_name, str(prop_value)))
            except Exception as e:
                print("failed to read property %s: %s" % (property_name, e.message))

            try:
                self.__setattr__(property_name, prop_value)
            except Exception as e:
                print("failed to write property %s: %s" % (property_name, e.message))

            try:
                if self.__getattr__(property_name) == prop_value:
                    print("%s: test successfull" % property_name)
                else:
                    # raise Exception("%s: fail to test write" % property_name)
                    print("%s: test failed: %s != %s" % (
                        property_name, str(self.__getattr__(property_name)), prop_value))
            except Exception:
                pass

    def teleport(self, x, y, z, freeze=True):
        assert self.has_attribute('x'), "no x attribute"
        assert self.has_attribute('y'), "no y attribute"
        assert self.has_attribute('z'), "no z attribute"
        if freeze:
            self.freeze = True

        self.x = x
        self.y = y
        self.z = z

        if freeze:
            self.freeze = False
