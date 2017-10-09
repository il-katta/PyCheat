from gtaentity import GTA5Entity


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
            offsets=[0x8, 0xD28, 0x8A8, 0x90],
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
            offsets=[0x8, 0xD28, 0xBAC],
            vtype="float",
            address=self.WorldPTR,
        )

        self.add(
            name="freeze",
            offsets=[0x8, 0xD28, 0x2E],
            vtype="bool",
            booltype="byte",
            address=self.WorldPTR,
            true_value=3,
            false_value=1
        )

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

        # bombs 1208
        # flare 1204