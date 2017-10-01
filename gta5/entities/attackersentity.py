from gtaentity import GTA5Entity

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
