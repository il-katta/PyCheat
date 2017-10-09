from gtaentity import GTA5Entity
from playerentity import PlayerEntity


class PedEntity(GTA5Entity):
    index = None

    def __init__(self, index=0, ObjectsPTR=None):
        super(PedEntity, self).__init__()
        self.index = index
        self._ObjectsPTR = ObjectsPTR
        self.add(
            name="_",
            vtype="byte",
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
            name="max_healt",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x2A0],
            address=self.ObjectsPTR,
        )


        self.add(
            name="x",
            vtype="float",
            offsets=[0x18, 0x100, index * 0x10, 0x90], # 0x30 0x50 0x90
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
            false_value=7 # TODO: fix
        )

        self.add(
            name="c",
            vtype="uint",
            offsets=[0x18, 0x100, index * 0x10, 4264],
            address=self.ObjectsPTR,
        )

        self.add(
            name="god",
            vtype="bool",
            booltype="byte",
            offsets=[0x18, 0x100, index * 0x10, 0x189],
            address=self.ObjectsPTR,
        )

        self.add(
            name="player_healt",
            offsets=[0x8, 0x280],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="player_info_ptr",
            vtype="bool",
            booltype="byte",
            offsets=[0x18, 0x100, index * 0x10, 0x10B8],
            address=self.ObjectsPTR,
        )

        self.add(
            name="player_name",
            vtype="string",
            size=20,
            offsets=[0x18, 0x100, index * 0x10, 0x10B8, 0x7C],
            address=self.ObjectsPTR,
        )


    def is_player(self):
        #return  self.player_healt == self.healt and ++self.player_healt == self.healt
        # return (ped.c >> 24) == 96:
        # return (ped.c << 11 >> 25) in [8320, 106754, 8750]:
        return self.player_info_ptr != 0

    def teleport(self, x, y, z, freeze=False):
        # freeze default False
        return super(PedEntity, self).teleport(x, y, z, freeze)

    def teleport_to_player(self, x_offset=0, y_offset=0, z_offset=0, player=None):
        if not player:
            player = PlayerEntity()
        x = player.x + x_offset
        y = player.y + y_offset
        z = player.z + z_offset

        self.teleport(x, y, z)

    def teleport_near_player(self, distance=1, player=None):
        if not player:
            player = PlayerEntity()
        x = player.x + distance
        y = player.y + distance
        z = player.z

        self.teleport(x, y, z)

    def teleport_near_over_the_player(self, distance=1, player=None):
        if not player:
            player = PlayerEntity()
        x = player.x + distance
        y = player.y + distance
        z = player.z + 15

        self.teleport(x, y, z)

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

    def __str__(self):
        return (
            "*********************\n" +
            "\thealt: {} \n" +
            "\tcash: {} \n" +
            "\tpos: ( {}, {}, {} ) \n" +
            "\ttype: {} \n" +
            "\t_: {}\n" +
            "\tc: {} >> {}"
        ).format(
            str(self.healt),
            str(self.cash),
            str(self.x), str(self.y), str(self.z),
            str(self.type),
            str(self._),
            str(self.c), str(self.c << 11 >> 25)
        )
