from modengine.entity import Entity
from modengine.memory.memorymanager import MemoryManager
import threading
GAME = 'steam'


class GTA5Entity(Entity):
    if GAME == 'steam':
        WorldPTR_label = 'GTA5.EXE+236ADE0'  # 'gta5!start+0xc667d8'
        BlipPTR_label = 'GTA5.EXE+1F9A2C0'  # 'gta5!start+0x895cb8'
        AmmoPTR_label = 'GTA5.EXE+E89425'
        ClipPTR_label = 'GTA5.EXE+E893E0'
        GetPointerAddressA_label = 'gta5!start+0x14e7d78'
        ObjectsPTR_label = 'GTA5.EXE+1E92AB8'
    else:
        WorldPTR_label = 'GTA5.EXE+2366EC8'
        BlipPTR_label = 'GTA5.EXE+1F9E750'
        AmmoPTR_label = 'GTA5.EXE+E88EB9'
        ClipPTR_label = 'GTA5.EXE+E88E74'
        GetPointerAddressA_label = '??'
        ObjectsPTR_label = 'GTA5.EXE+1E90138'

    WorldPTR = None
    BlipPTR = None
    AmmoPTR = None
    ClipPTR = None
    GetPointerAddressA = None
    ObjectsPTR = None

    def __init__(self):
        super(GTA5Entity, self).__init__(MemoryManager("GTA5.EXE"))
        self.updatePTR()

    def updatePTR(self):
        self.WorldPTR = self.getPTRAddress(self.WorldPTR_label)
        self.BlipPTR = self.getPTRAddress(self.BlipPTR_label)
        self.ClipPTR = self.getPTRAddress(self.ClipPTR_label)
        self.AmmoPTR = self.getPTRAddress(self.AmmoPTR_label)
        self.ObjectsPTR = self.getPTRAddress(self.ObjectsPTR_label)
        self.GetPointerAddressA = self.getPTRAddress(self.GetPointerAddressA_label) + 0x8



    def self_test(self):
        for property_name in self.properties:
            print "testing %s" % property_name
            try:
                prop_value = self.__getattr__(property_name)
                print "%s : %s" % (property_name, str(prop_value))
            except Exception as e:
                print "failed to read property %s: %s" % (property_name, e.message)

            try:
                self.__setattr__(property_name, prop_value)
            except Exception as e:
                print "failed to write property %s: %s" % (property_name, e.message)

            try:
                if self.__getattr__(property_name) == prop_value:
                    print "%s: test successfull" % property_name
                else:
                    # raise Exception("%s: fail to test write" % property_name)
                    print "%s: test failed: %s != %s" % (
                        property_name, str(self.__getattr__(property_name)), prop_value)
            except Exception:
                pass

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




class PedsEntity(GTA5Entity):

    def __init__(self):
        super(PedsEntity, self).__init__()
        self.add(
            name="peds_count",
            vtype="int",
            offsets=[0x18, 0x110],
            address=self.ObjectsPTR,
        )

    def get_all_peds(self, filter=True):
        for i in range(self.peds_count):
            try:
                ped = PedEntity(i)
                if not filter:
                    print "yield ped"
                    yield  ped
                elif ped.type == 77:
                    print "yield ped"
                    yield ped
            except WindowsError:
                pass
        print "get_all_peds finished"

    @staticmethod
    def drop(player, ped):
        try:
            ped.freeze = True
            if ped.cash < 2000:
                ped.cash = 2000
            ped.invisible = True
            ped.teleport_to_player(player.z + 10)
            ped.healt_ = 99
            print "."
        except WindowsError:
            print "umh... error!"

    def ped_drop(self):
        player = PlayerEntity()
        threads = []
        for ped in self.get_all_peds(True):
            p = threading.Thread(target=PedsEntity.drop, args=(player, ped))
            threads.append(p)
            p.start()

        for p in threads:
            p.join()


    def kill_all_peds(self):
        for i in range(self.peds_count):
            print "** %s **" % (str(i))
            try:
                ped = PedEntity(i)
                if ped.type == 77:
                    ped.cash = 2000
                    ped.healt_ = 99
            except Exception as e:
                print "fail"

    def invisible_peds(self):
        for i in range(self.peds_count):
            print "** %s **" % (str(i))
            try:
                ped = PedEntity(i)
                ped.invisible = True
            except Exception as e:
                print "fail"


class PedEntity(GTA5Entity):
    def __init__(self, index=0):
        super(PedEntity, self).__init__()
        self.add(
            name="_",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10],
            address=self.ObjectsPTR,
        )

        self.add(
            name="healt",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x280],
            address=self.ObjectsPTR,
        )

        self.add(
            name="x",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x90],
            address=self.ObjectsPTR,
        )

        self.add(
            name="y",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x94],
            address=self.ObjectsPTR,
        )

        self.add(
            name="z",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x98],
            address=self.ObjectsPTR,
        )

        self.add(
            name="_x",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x110],
            address=self.ObjectsPTR,
        )

        self.add(
            name="_y",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x114],
            address=self.ObjectsPTR,
        )

        self.add(
            name="_z",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x118],
            address=self.ObjectsPTR,
        )

        self.add(
            name="_x_",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x120],
            address=self.ObjectsPTR,
        )

        self.add(
            name="_y_",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x124],
            address=self.ObjectsPTR,
        )

        self.add(
            name="_z_",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x128],
            address=self.ObjectsPTR,
        )

        self.add(
            name="__x",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x160],
            address=self.ObjectsPTR,
        )

        self.add(
            name="__y",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x164],
            address=self.ObjectsPTR,
        )

        self.add(
            name="__z",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x168],
            address=self.ObjectsPTR,
        )
        self.add(
            name="__z__",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x280],
            address=self.ObjectsPTR,
        )

        self.add(
            name="cash",
            vtype="int",
            offsets=[0x18, 0x100, index * 0x10, 0x15D4],
            address=self.ObjectsPTR,
        )

        self.add(
            name="peds_count",
            vtype="int",
            offsets=[0x18, 0x110],
            address=self.ObjectsPTR,
        )

        self.add(
            name="type",
            vtype="byte",
            offsets=[0x18, 0x100, index * 0x10, 0x20, 0x270],
            address=self.ObjectsPTR,
        )

        self.add(
            name="freeze",
            vtype="bool",
            booltype="byte",
            offsets=[0x18, 0x100, index * 0x10, 0x2E],
            address=self.ObjectsPTR,
            true_value=3,
            false_value=1
        )

        self.add(
            name="invisible",
            vtype="bool",
            booltype="byte",
            offsets=[0x18, 0x100, index * 0x10, 0x2C],
            address=self.ObjectsPTR,
            true_value=0,
            false_value=7
        )

        self.add(
            name="healt_",
            vtype="int",
            offsets=[0x18, 0x100, index * 0x10, 0x280],
            address=self.ObjectsPTR,
        )

    def teleport(self, x, y, z):
        try:
            self.x = x
            self._x = x
            self._x_ = x
            self.__x = x
        except WindowsError:
            pass

        try:
            self.y = y
            self._y = y
            self._y_ = y
            self.__y = y
        except WindowsError:
            pass

        try:
            self.__z__ = z
            self.z = z
            self._z = z
            self._z_ = z
            self.__z = z
        except WindowsError:
            pass

    def teleport_to_player(self, z=None):
        player = PlayerEntity()
        x = player.x
        y = player.y
        if z == None:
            z = player.z

        self.teleport(x, y, z)




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

        self.add(
            name="accelleration",
            offsets=[0x8, 0xD28, 0x8A8, 0x4C],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="breakforce",
            offsets=[0x8, 0xD28, 0x8A8, 0x6C],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="traction",
            offsets=[0x8, 0xD28, 0x8A8, 0x72],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="demolition",
            offsets=[0x8, 0xD28, 0x8A8, 0xF8],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="suspension",
            offsets=[0x8, 0xD28, 0x8A8, 0xBC],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="gravity",
            offsets=[0x8, 0xD28, 0x8A8, 0xB7C],
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


class AttackersEntity(GTA5Entity):
    def __init__(self, index=0):
        super(AttackersEntity, self).__init__()

        self.add(
            name="healt",
            offsets=[0x8, 0x2A8, (index * 0x18), 0x280],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="max_healt",
            offsets=[0x8, 0x2A8, (index * 0x18), 0x2A0],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="x",
            offsets=[0x8, 0x2A8, (index * 0x18), 0x110],
            vtype="float",
            address=self.WorldPTR,
        )
        self.add(
            name="y",
            offsets=[0x8, 0x2A8, (index * 0x18), 0x114],
            vtype="float",
            address=self.WorldPTR,
        )
        self.add(
            name="z",
            offsets=[0x8, 0x2A8, (index * 0x18), 0x118],
            vtype="float",
            address=self.WorldPTR,
        )


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
            offsets=[0x350],
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
            offsets=[0x8, 0x30, 0x50]
        )
        self.add(
            name="y",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x30, 0x54]
        )
        self.add(
            name="z",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x30, 0x58]
        )

        self.add(
            name="_x",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x90]
        )
        self.add(
            name="_y",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x94]
        )
        self.add(
            name="_z",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x98]
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
            # if self.in_vehicle and self.veihcle:
            if self.veihcle:
                self.veihcle.teleport(waypointPosition[0], waypointPosition[1], -210)

            self.teleport(waypointPosition[0], waypointPosition[1], -210)
        else:
            print "no waypoint position"

    # thanks to Zeziroth: your code helps me to fix this
    def kill_some_attackers(self):
        for i in range(3):
            try:
                AttackersEntity(i).healt = 0
            except WindowsError:
                pass
