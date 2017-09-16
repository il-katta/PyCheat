import modengine.entity
import modengine.memorymanager


class GTA5Entity(modengine.entity.Entity):
    WorldPTR_label = 'gta5!start+0xc667d8'
    BlipPTR_label = 'GTA5.EXE+1F9A2C0'  # BlipPTR_label = 'gta5!start+0x895cb8'
    AmmoPTR_label = 'GTA5.EXE+E89425'
    ClipPTR_label = 'GTA5.EXE+E893E0'
    GetPointerAddressA_label = 'gta5!start+0x14e7d78'

    GetPointerAddressA = None
    WorldPTR = None
    BlipPTR = None
    ClipPTR = None
    AmmoPTR = None

    def __init__(self):
        super(GTA5Entity, self).__init__(modengine.memorymanager.MemoryManager("GTA5.EXE"))

        self.WorldPTR = self.getPTRAddress(self.WorldPTR_label)
        self.BlipPTR = self.getPTRAddress(self.BlipPTR_label)
        self.ClipPTR = self.getPTRAddress(self.ClipPTR_label)
        self.AmmoPTR = self.getPTRAddress(self.AmmoPTR_label)
        self.GetPointerAddressA = self.getPTRAddress(self.GetPointerAddressA_label) + 0x8

    def getPTRAddress(self, PTR_label):
        return self.mm.resolve_label(PTR_label)
        ## -36935655
        # addr = memory_search_aob(process.get_pid(), "gta5", HexPattern("48 8B 05 ?? ?? ?? ?? 45 ?? ?? ?? ?? 48 8B 48 08 48 85 C9 74 07"))
        # print("aobscan", addr)
        ## addr =  addr + readInteger(addr + 3) + 7
        # return addr + process.read_int(addr + 3) + 7

    def self_test(self):
        for property_name in self.properties:
            print "testing %s" % property_name
            prop_value = self.__getattr__(property_name)
            print "%s : %s" % (property_name, str(prop_value))
            self.__setattr__(property_name, prop_value)
            if self.__getattr__(property_name) == prop_value:
                print "%s: test successfull" % property_name
            else:
                raise Exception("%s: fail to test write" % property_name)

    def teleport(self, x, y, z):
        assert self.has_attribute('x')
        assert self.has_attribute('y')
        assert self.has_attribute('z')
        self.x = x
        self.y = y
        self.z = z
        # teleport fix
        self._x = x
        self._y = y
        self._z = z

class WeaponEntity(GTA5Entity):
    def __init__(self):
        super(WeaponEntity, self).__init__()
        self.add(
            name="unlimited_ammo",
            vtype="bool",
            address=self.AmmoPTR,
            true_value=0xe8909090,  # 3901788304
            false_value=0xe8d12b41  # 3906022209
        )

        self.add(
            name="unlimited_magazine",
            vtype="bool",
            address=self.ClipPTR,
            true_value=0x3b909090,  # 999329936
            false_value=0x3bc92b41  # 1003039553
        )


class VehicleEntity(GTA5Entity):
    def __init__(self):
        super(VehicleEntity, self).__init__()
        self.add(
            name="healt",
            offsets=[0x8, 0xD28, 0x280],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="max_healt",
            offsets=[0x8, 0xD28, 0x2A0],
            vtype="float",
            address=self.WorldPTR,
        )
        '''
        self.add(
            name="velocity",
            offsets=[0x8, 0xD28, 0x4f1c8c4],
            vtype="float",
            address=self.WorldPTR,
        )
        '''

        '''
        GTA5.exe+27C04E4 or GTA5.exe+2430260 # player
        
        GTA5.exe+24929EC #veihcle ( anche negativa )
        GTA5.exe+2363E44 @ probabili miglia orarie
        '''
        self.add(
            name="x",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0xD28, 0x30, 0x50]
        )
        self.add(
            name="y",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0xD28, 0x30, 0x54]
        )
        self.add(
            name="z",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0xD28, 0x30, 0x58]
        )

        self.add(
            name="_x",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0xD28, 0x90]
        )
        self.add(
            name="_y",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0xD28, 0x94]
        )
        self.add(
            name="_z",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0xD28, 0x98]
        )

        self.add(
            name="god",
            vtype="bool",
            address=self.WorldPTR,
            offsets=[0x8, 0xD28, 0x189],
        )

class WayPointEntity(GTA5Entity):
    def get_position(self):
        pointer = self.BlipPTR

        for i in range(0, 0x800):
            address = self.mm.read_pointer(pointer + i * 8)
            if address > 0:
                try:
                    a = self.mm.read_int(address + 0x40)
                    b = self.mm.read_int(address + 0x48)
                    if a == 8 and b == 84:
                        x = self.mm.read_float(address + 0x10)
                        y = self.mm.read_float(address + 0x14)
                        return (x, y)
                except WindowsError:
                    pass


class PlayerEntity(GTA5Entity):
    waypointEnity = None

    def __init__(self):
        super(PlayerEntity, self).__init__()

        self.add(
            name="name",
            offsets=[0x8, 0x10B8, 0x7C],
            vtype="string",
            size=20,
            address=self.WorldPTR,
        )

        self.add(
            name="healt",
            offsets=[0x8, 0x280],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="max_healt_m",
            vtype="float",
            address=self.GetPointerAddressA,
            offsets=[350],
        )

        self.add(
            name="max_healt",
            offsets=[0x8, 0x2A0],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="max_healt_regen_m",
            offsets=[0x368],
            vtype="float",
            address=self.GetPointerAddressA,
        )

        self.add(
            name="healt_regen_rate_m",
            vtype="float",
            address=self.GetPointerAddressA,
            offsets=[0x360],
        )

        self.add(
            name="min_healt_m",
            vtype="float",
            address=self.GetPointerAddressA,
            offsets=[0x358],
        )

        self.add(
            name="armor",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x14B0],
        )

        self.add(
            name="min_armor_m",
            vtype="float",
            address=self.GetPointerAddressA,
            offsets=[0x378],
        )

        self.add(
            name="god",
            vtype="bool",
            address=self.WorldPTR,
            offsets=[0x8, 0x189],
        )

        self.add(
            name="wanted_level",
            offsets=[0x8, 0x10B8, 0x7f8],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="no_bike_fall",
            vtype="bool",
            address=self.WorldPTR,
            offsets=[0x8, 0x13EC],
            true_value=0xC9,
            false_value=0xC8
        )

        self.add(
            name="rp_m",
            vtype="float",
            address=self.GetPointerAddressA,
            offsets=[0x10],
        )

        self.add(
            name="sprint_speed",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x10B8, 0x14C],
        )

        self.add(
            name="swim_speed",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x10B8, 0x148],
        )

        self.add(
            name="x",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0x30, 0x50]
        )
        self.add(
            name="y",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0x30, 0x54]
        )
        self.add(
            name="z",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0x30, 0x58]
        )

        self.add(
            name="_x",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0x90]
        )
        self.add(
            name="_y",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0x94]
        )
        self.add(
            name="_z",
            vtype="float",
            address=self.WorldPTR,
            offsets=[8, 0x98]
        )

        self.add(
            name="in_vehicle",
            vtype="bool",
            address=self.WorldPTR,
            offsets=[0x8, 0x146B],
            true_value=0x0,
            false_value=0x10
        )



    @property
    def veihcle(self):
        try:
            return VehicleEntity()
        except WindowsError:
            return None

    def teleport_to_waypoint(self):
        waypointEntity = WayPointEntity()
        waypointPosition = waypointEntity.get_position()
        if waypointPosition:
            #if self.in_vehicle and self.veihcle:
            if self.veihcle:
                self.veihcle.teleport(waypointPosition[0], waypointPosition[1], -210)

            self.teleport(waypointPosition[0], waypointPosition[1], -210)
        else:
            print "no waypoint position"
