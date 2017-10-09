from gtaentity import GTA5Entity

class WeaponEntity(GTA5Entity):
    def __init__(self):
        super(WeaponEntity, self).__init__()
        self.add(
            name="unlimited_ammo",
            vtype="bool",
            booltype='uint',
            address=self.AmmoPTR,
            true_value=0xe8909090,  # 3901788304
            false_value=0xe8d12b41  # 3906022209
        )

        self.add(
            name="unlimited_magazine",
            vtype="bool",
            booltype='uint',
            address=self.ClipPTR,
            true_value=0x3b909090,  # 999329936
            false_value=0x3bc92b41  # 1003039553
        )

        self.add(
            name="bullet_damage",
            vtype="float",
            offsets=[0x8, 0x10C8, 0x20, 0xB0],
            address=self.WorldPTR
        )

        self.add(
            name="reload_m",
            vtype="float",
            offsets=[0x8, 0x10C8, 0x20, 0x12C],
            address=self.WorldPTR
        )

        # speed kmh: GTA5.exe+24929EC
        # speed mph: GTA5.exe+2363E44