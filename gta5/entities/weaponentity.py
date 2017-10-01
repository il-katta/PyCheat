from gtaentity import GTA5Entity

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

