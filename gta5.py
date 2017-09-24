import sys
from time import sleep

from gta5.entities import PlayerEntity, VehicleEntity, PedsEntity

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
            print "god: ", player.god
            print "no_bike_fall: ", player.no_bike_fall
            print("rp_m: %d" % player.rp_m)
            print("x: %d" % player.x)
            print("y: %d" % player.y)
            print("z: %d" % player.z)
            print("_x: %d" % player._x)
            print("_y: %d" % player._y)
            print("_z: %d" % player._z)
            print "in vehicle:", player.in_vehicle
            print "teleport"
            player.teleport_to_waypoint()
            print("")
            sleep(1)
    elif cmd == "test":
        player = PlayerEntity()
        vehicle = VehicleEntity()

        player.self_test()
        if player.in_vehicle:
            vehicle.self_test()
