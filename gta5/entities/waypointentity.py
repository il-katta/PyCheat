from gtaentity import GTA5Entity

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

