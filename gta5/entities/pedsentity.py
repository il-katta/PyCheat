from gtaentity import GTA5Entity
from pedentity import PedEntity

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
            ped = PedEntity(i, self.ObjectsPTR)
            if filter and ped.type != 77:
                # not a ped
                continue

            if filter and ped.is_player():
                # its the player
                continue

            yield ped









