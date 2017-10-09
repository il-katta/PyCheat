import threading
from gta5.entities import PlayerEntity, VehicleEntity, PedsEntity, WeaponEntity, GTA5Entity


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

'''
class Player(object):
    # test
    healt = 200
    maxhealt = 200
    god = False
    freeze = False
    x = 0
    y = 0
    z = 0
    radar_hide_mode = False
'''
class Player(PlayerEntity):

    _flymode = False
    flymode_speed = 0.5
    fly_x = 0
    fly_y = 0
    fly_z = 0

    @threaded
    def start_flymode(self):
        if self.flymode:
            return
        self._flymode = True
        self.fly_x = self.x
        self.fly_y = self.y
        self.fly_z = self.z
        while self.flymode:
            self.freeze = True
            self.x = self.fly_x
            self.y = self.fly_y
            self.z = self.fly_z
            #sleep(0.01)

    def stop_flymode(self):
        if self.flymode:
            self._flymode = False
            # todo: wait for thread ?
            # take off
            self.z = -210 
            self.freeze = False

    @property
    def flymode(self):
        return self._flymode

    @flymode.setter
    def flymode(self, value):
        if value:
            self.start_flymode()
        else:
            self.stop_flymode()

    def fly_west(self):
        if self.flymode:
            self.fly_x -= self.flymode_speed
        return self.flymode

    def fly_east(self):
        if self.flymode:
            self.fly_x += self.flymode_speed
        return self.flymode

    def fly_north(self):
        if self.flymode:
            self.fly_y += self.flymode_speed
        return self.flymode

    def fly_south(self):
        if self.flymode:
            self.fly_y -= self.flymode_speed
        return self.flymode

    def fly_up(self):
        if self.flymode:
            self.fly_z += self.flymode_speed
        return self.flymode

    def fly_down(self):
        if self.flymode:
            self.fly_z -= self.flymode_speed
        return self.flymode

    @property
    def radar_hide_mode(self):
        return self.max_healt == 0 and self.god

    @radar_hide_mode.setter
    def radar_hide_mode(self, value):
        if value:
            self.max_healt = 0
            self.god = True
        else:
            if self.healt > 200:
                self.max_healt = self.healt
            else:
                self.max_healt = 200
            self.god = False


#class PedDropper(object):
class PedDropper(PedsEntity):
    _ped_drop = False

    _z_offset = 3
    _x_offset = 0
    _y_offset = 0
    _money = 2000
    _freeze = True
    _invisible = True
    _teleport = True
    _healt = 0

    def __init__(self):
        super(PedDropper, self).__init__()
        self.player = Player()

    @property
    def ped_drop(self):
        return self._ped_drop

    @ped_drop.setter
    def ped_drop(self, value):
        if value:
            self.start_ped_drop()
        else:
            self.stop_ped_drop()

    @threaded
    def start_ped_drop(self):
        self._ped_drop = True
        while self._ped_drop:
            try:
                for ped in self.get_all_peds(filter=True):
                    try:
                        if ped.healt > 0:
                            try:
                                ped.freeze = self._freeze
                                if self._money is not None:
                                    ped.cash = self._money
                                ped.invisible = self._invisible
                                if self._teleport:
                                    ped.teleport_to_player(
                                        x_offset=self._x_offset,
                                        y_offset=self._y_offset,
                                        z_offset=self._z_offset,
                                        player=player
                                    )
                                if self._healt is not None:
                                    ped.healt = self._healt
                            except Exception as e:
                                print(e.message)
                    except WindowsError:
                        print("umh... WindowsError!")
            except Exception as e:
                print("umh... error! %s" % e.message)

    def stop_ped_drop(self):
        self._ped_drop = False
    



class EntitySafeExecDecorator(object):
    _entity = None
    EntityClass = None
    
    def __init__(self, EntityClass):
        self.EntityClass = EntityClass
    
    @property
    def entity(self):
        if not self._entity:
            try:
                self._entity = self.EntityClass()
            except:
                pass
        return self._entity

    def __getattr__(self, name):
        if not self.entity:
            return None
        
        if self.entity.has_attribute(name):
            try:
                return self.entity.read(name)
            except:
                pass
        else:
            if hasattr(self.entity, name):
                return getattr(self.entity, name, None)

        return None

    def __setattr__(self, name, arg):
        if not self.entity:
            return
        
        if self.entity.has_attribute(name):
            try:
                self.entity.write(name, arg)
            except:
                return None
        else:
            if hasattr(self.entity, name):
                setattr(self.entity, name, arg)

        return None

player = Player()
ped_dropper = PedDropper()
weapon = WeaponEntity()
#vehicle = EntitySafeExecDecorator(VehicleEntity)
#vehicle = VehicleEntity()
