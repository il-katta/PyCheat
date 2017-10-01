from attackersentity import AttackersEntity
from gtaentity import GTA5Entity
from vehicleentity import VehicleEntity
from waypointentity import WayPointEntity


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
            booltype="byte",
            address=self.WorldPTR,
            offsets=[0x8, 0x189],
        )

        self.add(
            name="wanted_level",
            offsets=[0x8, 0x10B8, 0x7f8],
            vtype="uint",
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
            name="_x",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x30, 0x50]
        )
        self.add(
            name="_y",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x30, 0x54]
        )
        self.add(
            name="_z",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x30, 0x58]
        )

        self.add(
            name="x",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x90]
        )
        self.add(
            name="y",
            vtype="float",
            address=self.WorldPTR,
            offsets=[0x8, 0x94]
        )
        self.add(
            name="z",
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

        self.add(
            name="freeze",
            offsets=[0x8, 0x2E],
            vtype="bool",
            booltype="byte",
            address=self.WorldPTR,
            true_value=3,
            false_value=1
        )

    @property
    def vehicle(self):
        try:
            return VehicleEntity()
        except WindowsError:
            return None

    def teleport_to_waypoint(self):

        waypointEntity = WayPointEntity()
        waypointPosition = waypointEntity.get_position()
        if waypointPosition:
            # if self.in_vehicle and self.vehicle:
            if self.vehicle:
                self.vehicle.teleport(waypointPosition[0], waypointPosition[1], -210)
            self.teleport(waypointPosition[0], waypointPosition[1], -210)
            return True
        return False

    # thanks to Zeziroth: your code helps me to fix this
    def kill_some_attackers(self):
        for i in range(3):
            try:
                AttackersEntity(i).healt = 0
            except WindowsError:
                pass

    @property
    def x(self):
        return self.__getattr__("x")

    @x.setter
    def x(self, x):
        self.__setattr__("x", x)
        self.__setattr__("_x", x)

    @property
    def y(self):
        return self.__getattr__("y")

    @y.setter
    def y(self, y):
        self.__setattr__("y", y)
        self.__setattr__("_y", y)

    @property
    def z(self):
        return self.__getattr__("z")

    @z.setter
    def z(self, z):
        self.__setattr__("z", z)
        self.__setattr__("_z", z)
