import sys
from time import sleep

from gta5.entities import PlayerEntity, VehicleEntity, PedsEntity


def drop_ped(ped, player):
    try:
        ped.freeze = True
        if ped.cash < 2000:
            ped.cash = 2000
        ped.invisible = True
        ped.teleport_to_player(z_offset=10, player=player)
        ped.healt_ = 99
        print(".")
    except WindowsError:
        print("umh... error!")


if __name__ == '__main__':
    cmd = ""
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

    if cmd == "run" or cmd == "":
        player = PlayerEntity()
        while True:
            print("name: %s" % player.name)
            print("healt: %d" % player.healt)
            print("max_healt_m: %d" % player.max_healt_m)
            print("max_healt: %d" % player.max_healt)
            print("max_healt_regen_m: %d" % player.max_healt_regen_m)
            print("healt_regen_rate_m: %d" % player.healt_regen_rate_m)
            print("min_healt_m: %d" % player.min_healt_m)
            print("armor: %d" % player.armor)
            print("min_armor_m: %d" % player.min_armor_m)
            print("god: ", player.god)
            print("no_bike_fall: ", player.no_bike_fall)
            print("rp_m: %d" % player.rp_m)
            print("x: %d" % player.x)
            print("y: %d" % player.y)
            print("z: %d" % player.z)
            print("_x: %d" % player._x)
            print("_y: %d" % player._y)
            print("_z: %d" % player._z)
            print("in vehicle:", player.in_vehicle)
            print("teleport")
            player.teleport_to_waypoint()
            print("")
            sleep(1)
    elif cmd == "test":
        player = PlayerEntity()
        vehicle = VehicleEntity()

        player.self_test()
        if player.in_vehicle:
            vehicle.self_test()
    elif cmd == "ped":
        # while True:
        peds = PedsEntity()
        player = PlayerEntity()
        for ped in peds.get_all_peds():
            print(".")
            drop_ped(ped, player)
    '''
    else:
        system = System()
        system.request_debug_privileges()

        dwParentProcessId = get_pid("GTA5.EXE")
        python_exe = get_python_path()
        # start
        try:
            args = [python_exe, sys.argv[0], "run"]
            print "executing %s" % ' '.join(args)
            process = system.start_process(
                system.argv_to_cmdline(args),
                bConsole=True,
                bInheritHandles=True,
                dwParentProcessId=dwParentProcessId
            )
            dwProcessId = process.get_pid()
            print "Process created: %d" % dwProcessId
        except AttributeError, e:
            if "InitializeProcThreadAttributeList" in str(e):
                raise Exception("This tool requires Windows Vista or above.")
            else:
                # ...
                raise
        except WindowsError, e:
            # ...
            raise
    '''
