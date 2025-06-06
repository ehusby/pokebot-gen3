import re
from enum import Enum
from typing import Generator

from modules.context import context
from modules.map import MapLocation, get_map_data_for_current_position


def _might_be_map_coordinates(value) -> bool:
    return isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], int) and isinstance(value[1], int)


class MapGroupFRLG(Enum):
    Link = 0
    Dungeons = 1
    SpecialArea = 2
    TownsAndRoutes = 3
    IndoorPallet = 4
    IndoorViridian = 5
    IndoorPewter = 6
    IndoorCerulean = 7
    IndoorLavender = 8
    IndoorVermilion = 9
    IndoorCeladon = 10
    IndoorFuchsia = 11
    IndoorCinnabar = 12
    IndoorIndigoPlateau = 13
    IndoorSaffron = 14
    IndoorRoute2 = 15
    IndoorRoute4 = 16
    IndoorRoute5 = 17
    IndoorRoute6 = 18
    IndoorRoute7 = 19
    IndoorRoute8 = 20
    IndoorRoute10 = 21
    IndoorRoute11 = 22
    IndoorRoute12 = 23
    IndoorRoute15 = 24
    IndoorRoute16 = 25
    IndoorRoute18 = 26
    IndoorRoute19 = 27
    IndoorRoute22 = 28
    IndoorRoute23 = 29
    IndoorRoute25 = 30
    IndoorSevenIsland = 31
    IndoorOneIsland = 32
    IndoorTwoIsland = 33
    IndoorThreeIsland = 34
    IndoorFourIsland = 35
    IndoorFiveIsland = 36
    IndoorSixIsland = 37
    IndoorThreeIslandRoute = 38
    IndoorFiveIslandRoute = 39
    IndoorTwoIslandRoute = 40
    IndoorSixIslandRoute = 41
    IndoorSevenIslandRoute = 42

    def __contains__(self, item):
        if _might_be_map_coordinates(item):
            return self.value == item[0]
        elif isinstance(item, MapFRLG):
            return self.value == item.value[0]
        else:
            return NotImplemented

    @property
    def maps(self) -> "list[MapFRLG]":
        result = []
        for item in MapFRLG:
            if item.value[0] == self.value:
                result.append(item)
        return result


class MapFRLG(Enum):
    # Link
    BATTLE_COLOSSEUM_2P = (0, 0)
    TRADE_CENTER = (0, 1)
    RECORD_CORNER = (0, 2)
    BATTLE_COLOSSEUM_4P = (0, 3)
    UNION_ROOM = (0, 4)

    # Dungeons
    VIRIDIAN_FOREST = (1, 0)
    MT_MOON_1F = (1, 1)
    MT_MOON_B1F = (1, 2)
    MT_MOON_B2F = (1, 3)
    SSANNE_EXTERIOR = (1, 4)
    SSANNE_1F_CORRIDOR = (1, 5)
    SSANNE_2F_CORRIDOR = (1, 6)
    SSANNE_3F_CORRIDOR = (1, 7)
    SSANNE_B1F_CORRIDOR = (1, 8)
    SSANNE_DECK = (1, 9)
    SSANNE_KITCHEN = (1, 10)
    SSANNE_CAPTAINS_OFFICE = (1, 11)
    SSANNE_1F_ROOM1 = (1, 12)
    SSANNE_1F_ROOM2 = (1, 13)
    SSANNE_1F_ROOM3 = (1, 14)
    SSANNE_1F_ROOM4 = (1, 15)
    SSANNE_1F_ROOM5 = (1, 16)
    SSANNE_1F_ROOM7 = (1, 17)
    SSANNE_2F_ROOM1 = (1, 18)
    SSANNE_2F_ROOM2 = (1, 19)
    SSANNE_2F_ROOM3 = (1, 20)
    SSANNE_2F_ROOM4 = (1, 21)
    SSANNE_2F_ROOM5 = (1, 22)
    SSANNE_2F_ROOM6 = (1, 23)
    SSANNE_B1F_ROOM1 = (1, 24)
    SSANNE_B1F_ROOM2 = (1, 25)
    SSANNE_B1F_ROOM3 = (1, 26)
    SSANNE_B1F_ROOM4 = (1, 27)
    SSANNE_B1F_ROOM5 = (1, 28)
    SSANNE_1F_ROOM6 = (1, 29)
    UNDERGROUND_PATH_NORTH_ENTRANCE = (1, 30)
    UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL = (1, 31)
    UNDERGROUND_PATH_SOUTH_ENTRANCE = (1, 32)
    UNDERGROUND_PATH_WEST_ENTRANCE = (1, 33)
    UNDERGROUND_PATH_EAST_WEST_TUNNEL = (1, 34)
    UNDERGROUND_PATH_EAST_ENTRANCE = (1, 35)
    DIGLETTS_CAVE_NORTH_ENTRANCE = (1, 36)
    DIGLETTS_CAVE_B1F = (1, 37)
    DIGLETTS_CAVE_SOUTH_ENTRANCE = (1, 38)
    VICTORY_ROAD_1F = (1, 39)
    VICTORY_ROAD_2F = (1, 40)
    VICTORY_ROAD_3F = (1, 41)
    ROCKET_HIDEOUT_B1F = (1, 42)
    ROCKET_HIDEOUT_B2F = (1, 43)
    ROCKET_HIDEOUT_B3F = (1, 44)
    ROCKET_HIDEOUT_B4F = (1, 45)
    ROCKET_HIDEOUT_ELEVATOR = (1, 46)
    SILPH_CO_1F = (1, 47)
    SILPH_CO_2F = (1, 48)
    SILPH_CO_3F = (1, 49)
    SILPH_CO_4F = (1, 50)
    SILPH_CO_5F = (1, 51)
    SILPH_CO_6F = (1, 52)
    SILPH_CO_7F = (1, 53)
    SILPH_CO_8F = (1, 54)
    SILPH_CO_9F = (1, 55)
    SILPH_CO_10F = (1, 56)
    SILPH_CO_11F = (1, 57)
    SILPH_CO_ELEVATOR = (1, 58)
    POKEMON_MANSION_1F = (1, 59)
    POKEMON_MANSION_2F = (1, 60)
    POKEMON_MANSION_3F = (1, 61)
    POKEMON_MANSION_B1F = (1, 62)
    SAFARI_ZONE_CENTER = (1, 63)
    SAFARI_ZONE_EAST = (1, 64)
    SAFARI_ZONE_NORTH = (1, 65)
    SAFARI_ZONE_WEST = (1, 66)
    SAFARI_ZONE_CENTER_REST_HOUSE = (1, 67)
    SAFARI_ZONE_EAST_REST_HOUSE = (1, 68)
    SAFARI_ZONE_NORTH_REST_HOUSE = (1, 69)
    SAFARI_ZONE_WEST_REST_HOUSE = (1, 70)
    SAFARI_ZONE_SECRET_HOUSE = (1, 71)
    CERULEAN_CAVE_1F = (1, 72)
    CERULEAN_CAVE_2F = (1, 73)
    CERULEAN_CAVE_B1F = (1, 74)
    POKEMON_LEAGUE_LORELEIS_ROOM = (1, 75)
    POKEMON_LEAGUE_BRUNOS_ROOM = (1, 76)
    POKEMON_LEAGUE_AGATHAS_ROOM = (1, 77)
    POKEMON_LEAGUE_LANCES_ROOM = (1, 78)
    POKEMON_LEAGUE_CHAMPIONS_ROOM = (1, 79)
    POKEMON_LEAGUE_HALL_OF_FAME = (1, 80)
    ROCK_TUNNEL_1F = (1, 81)
    ROCK_TUNNEL_B1F = (1, 82)
    SEAFOAM_ISLANDS_1F = (1, 83)
    SEAFOAM_ISLANDS_B1F = (1, 84)
    SEAFOAM_ISLANDS_B2F = (1, 85)
    SEAFOAM_ISLANDS_B3F = (1, 86)
    SEAFOAM_ISLANDS_B4F = (1, 87)
    POKEMON_TOWER_1F = (1, 88)
    POKEMON_TOWER_2F = (1, 89)
    POKEMON_TOWER_3F = (1, 90)
    POKEMON_TOWER_4F = (1, 91)
    POKEMON_TOWER_5F = (1, 92)
    POKEMON_TOWER_6F = (1, 93)
    POKEMON_TOWER_7F = (1, 94)
    POWER_PLANT = (1, 95)
    MT_EMBER_RUBY_PATH_B4F = (1, 96)
    MT_EMBER_EXTERIOR = (1, 97)
    MT_EMBER_SUMMIT_PATH_1F = (1, 98)
    MT_EMBER_SUMMIT_PATH_2F = (1, 99)
    MT_EMBER_SUMMIT_PATH_3F = (1, 100)
    MT_EMBER_SUMMIT = (1, 101)
    MT_EMBER_RUBY_PATH_B5F = (1, 102)
    MT_EMBER_RUBY_PATH_1F = (1, 103)
    MT_EMBER_RUBY_PATH_B1F = (1, 104)
    MT_EMBER_RUBY_PATH_B2F = (1, 105)
    MT_EMBER_RUBY_PATH_B3F = (1, 106)
    MT_EMBER_RUBY_PATH_B1F_STAIRS = (1, 107)
    MT_EMBER_RUBY_PATH_B2F_STAIRS = (1, 108)
    THREE_ISLAND_BERRY_FOREST = (1, 109)
    FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE = (1, 110)
    FOUR_ISLAND_ICEFALL_CAVE_1F = (1, 111)
    FOUR_ISLAND_ICEFALL_CAVE_B1F = (1, 112)
    FOUR_ISLAND_ICEFALL_CAVE_BACK = (1, 113)
    FIVE_ISLAND_ROCKET_WAREHOUSE = (1, 114)
    SIX_ISLAND_DOTTED_HOLE_1F = (1, 115)
    SIX_ISLAND_DOTTED_HOLE_B1F = (1, 116)
    SIX_ISLAND_DOTTED_HOLE_B2F = (1, 117)
    SIX_ISLAND_DOTTED_HOLE_B3F = (1, 118)
    SIX_ISLAND_DOTTED_HOLE_B4F = (1, 119)
    SIX_ISLAND_DOTTED_HOLE_SAPPHIRE_ROOM = (1, 120)
    SIX_ISLAND_PATTERN_BUSH = (1, 121)
    SIX_ISLAND_ALTERING_CAVE = (1, 122)

    # SpecialArea
    NAVEL_ROCK_EXTERIOR = (2, 0)
    TRAINER_TOWER_1F = (2, 1)
    TRAINER_TOWER_2F = (2, 2)
    TRAINER_TOWER_3F = (2, 3)
    TRAINER_TOWER_4F = (2, 4)
    TRAINER_TOWER_5F = (2, 5)
    TRAINER_TOWER_6F = (2, 6)
    TRAINER_TOWER_7F = (2, 7)
    TRAINER_TOWER_8F = (2, 8)
    TRAINER_TOWER_ROOF = (2, 9)
    TRAINER_TOWER_LOBBY = (2, 10)
    TRAINER_TOWER_ELEVATOR = (2, 11)
    FIVE_ISLAND_LOST_CAVE_ENTRANCE = (2, 12)
    FIVE_ISLAND_LOST_CAVE_ROOM1 = (2, 13)
    FIVE_ISLAND_LOST_CAVE_ROOM2 = (2, 14)
    FIVE_ISLAND_LOST_CAVE_ROOM3 = (2, 15)
    FIVE_ISLAND_LOST_CAVE_ROOM4 = (2, 16)
    FIVE_ISLAND_LOST_CAVE_ROOM5 = (2, 17)
    FIVE_ISLAND_LOST_CAVE_ROOM6 = (2, 18)
    FIVE_ISLAND_LOST_CAVE_ROOM7 = (2, 19)
    FIVE_ISLAND_LOST_CAVE_ROOM8 = (2, 20)
    FIVE_ISLAND_LOST_CAVE_ROOM9 = (2, 21)
    FIVE_ISLAND_LOST_CAVE_ROOM10 = (2, 22)
    FIVE_ISLAND_LOST_CAVE_ROOM11 = (2, 23)
    FIVE_ISLAND_LOST_CAVE_ROOM12 = (2, 24)
    FIVE_ISLAND_LOST_CAVE_ROOM13 = (2, 25)
    FIVE_ISLAND_LOST_CAVE_ROOM14 = (2, 26)
    SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER = (2, 27)
    SEVEN_ISLAND_TANOBY_RUINS_LIPTOO_CHAMBER = (2, 28)
    SEVEN_ISLAND_TANOBY_RUINS_WEEPTH_CHAMBER = (2, 29)
    SEVEN_ISLAND_TANOBY_RUINS_DILFORD_CHAMBER = (2, 30)
    SEVEN_ISLAND_TANOBY_RUINS_SCUFIB_CHAMBER = (2, 31)
    SEVEN_ISLAND_TANOBY_RUINS_RIXY_CHAMBER = (2, 32)
    SEVEN_ISLAND_TANOBY_RUINS_VIAPOIS_CHAMBER = (2, 33)
    THREE_ISLAND_DUNSPARCE_TUNNEL = (2, 34)
    SEVEN_ISLAND_SEVAULT_CANYON_TANOBY_KEY = (2, 35)
    NAVEL_ROCK_1F = (2, 36)
    NAVEL_ROCK_SUMMIT = (2, 37)
    NAVEL_ROCK_BASE = (2, 38)
    NAVEL_ROCK_SUMMIT_PATH_2F = (2, 39)
    NAVEL_ROCK_SUMMIT_PATH_3F = (2, 40)
    NAVEL_ROCK_SUMMIT_PATH_4F = (2, 41)
    NAVEL_ROCK_SUMMIT_PATH_5F = (2, 42)
    NAVEL_ROCK_BASE_PATH_B1F = (2, 43)
    NAVEL_ROCK_BASE_PATH_B2F = (2, 44)
    NAVEL_ROCK_BASE_PATH_B3F = (2, 45)
    NAVEL_ROCK_BASE_PATH_B4F = (2, 46)
    NAVEL_ROCK_BASE_PATH_B5F = (2, 47)
    NAVEL_ROCK_BASE_PATH_B6F = (2, 48)
    NAVEL_ROCK_BASE_PATH_B7F = (2, 49)
    NAVEL_ROCK_BASE_PATH_B8F = (2, 50)
    NAVEL_ROCK_BASE_PATH_B9F = (2, 51)
    NAVEL_ROCK_BASE_PATH_B10F = (2, 52)
    NAVEL_ROCK_BASE_PATH_B11F = (2, 53)
    NAVEL_ROCK_B1F = (2, 54)
    NAVEL_ROCK_FORK = (2, 55)
    BIRTH_ISLAND_EXTERIOR = (2, 56)
    ONE_ISLAND_KINDLE_ROAD_EMBER_SPA = (2, 57)
    BIRTH_ISLAND_HARBOR = (2, 58)
    NAVEL_ROCK_HARBOR = (2, 59)

    # TownsAndRoutes
    PALLET_TOWN = (3, 0)
    VIRIDIAN_CITY = (3, 1)
    PEWTER_CITY = (3, 2)
    CERULEAN_CITY = (3, 3)
    LAVENDER_TOWN = (3, 4)
    VERMILION_CITY = (3, 5)
    CELADON_CITY = (3, 6)
    FUCHSIA_CITY = (3, 7)
    CINNABAR_ISLAND = (3, 8)
    INDIGO_PLATEAU_EXTERIOR = (3, 9)
    SAFFRON_CITY = (3, 10)
    SAFFRON_CITY_CONNECTION = (3, 11)
    ONE_ISLAND = (3, 12)
    TWO_ISLAND = (3, 13)
    THREE_ISLAND = (3, 14)
    FOUR_ISLAND = (3, 15)
    FIVE_ISLAND = (3, 16)
    SEVEN_ISLAND = (3, 17)
    SIX_ISLAND = (3, 18)
    ROUTE1 = (3, 19)
    ROUTE2 = (3, 20)
    ROUTE3 = (3, 21)
    ROUTE4 = (3, 22)
    ROUTE5 = (3, 23)
    ROUTE6 = (3, 24)
    ROUTE7 = (3, 25)
    ROUTE8 = (3, 26)
    ROUTE9 = (3, 27)
    ROUTE10 = (3, 28)
    ROUTE11 = (3, 29)
    ROUTE12 = (3, 30)
    ROUTE13 = (3, 31)
    ROUTE14 = (3, 32)
    ROUTE15 = (3, 33)
    ROUTE16 = (3, 34)
    ROUTE17 = (3, 35)
    ROUTE18 = (3, 36)
    ROUTE19 = (3, 37)
    ROUTE20 = (3, 38)
    ROUTE21_NORTH = (3, 39)
    ROUTE21_SOUTH = (3, 40)
    ROUTE22 = (3, 41)
    ROUTE23 = (3, 42)
    ROUTE24 = (3, 43)
    ROUTE25 = (3, 44)
    ONE_ISLAND_KINDLE_ROAD = (3, 45)
    ONE_ISLAND_TREASURE_BEACH = (3, 46)
    TWO_ISLAND_CAPE_BRINK = (3, 47)
    THREE_ISLAND_BOND_BRIDGE = (3, 48)
    THREE_ISLAND_PORT = (3, 49)
    PROTOTYPE_SEVII_ISLE_6 = (3, 50)
    PROTOTYPE_SEVII_ISLE_7 = (3, 51)
    PROTOTYPE_SEVII_ISLE_8 = (3, 52)
    PROTOTYPE_SEVII_ISLE_9 = (3, 53)
    FIVE_ISLAND_RESORT_GORGEOUS = (3, 54)
    FIVE_ISLAND_WATER_LABYRINTH = (3, 55)
    FIVE_ISLAND_MEADOW = (3, 56)
    FIVE_ISLAND_MEMORIAL_PILLAR = (3, 57)
    SIX_ISLAND_OUTCAST_ISLAND = (3, 58)
    SIX_ISLAND_GREEN_PATH = (3, 59)
    SIX_ISLAND_WATER_PATH = (3, 60)
    SIX_ISLAND_RUIN_VALLEY = (3, 61)
    SEVEN_ISLAND_TRAINER_TOWER = (3, 62)
    SEVEN_ISLAND_SEVAULT_CANYON_ENTRANCE = (3, 63)
    SEVEN_ISLAND_SEVAULT_CANYON = (3, 64)
    SEVEN_ISLAND_TANOBY_RUINS = (3, 65)

    # IndoorPallet
    PALLET_TOWN_PLAYERS_HOUSE_1F = (4, 0)
    PALLET_TOWN_PLAYERS_HOUSE_2F = (4, 1)
    PALLET_TOWN_RIVALS_HOUSE = (4, 2)
    PALLET_TOWN_PROFESSOR_OAKS_LAB = (4, 3)

    # IndoorViridian
    VIRIDIAN_CITY_HOUSE = (5, 0)
    VIRIDIAN_CITY_GYM = (5, 1)
    VIRIDIAN_CITY_SCHOOL = (5, 2)
    VIRIDIAN_CITY_MART = (5, 3)
    VIRIDIAN_CITY_POKEMON_CENTER_1F = (5, 4)
    VIRIDIAN_CITY_POKEMON_CENTER_2F = (5, 5)

    # IndoorPewter
    PEWTER_CITY_MUSEUM_1F = (6, 0)
    PEWTER_CITY_MUSEUM_2F = (6, 1)
    PEWTER_CITY_GYM = (6, 2)
    PEWTER_CITY_MART = (6, 3)
    PEWTER_CITY_HOUSE1 = (6, 4)
    PEWTER_CITY_POKEMON_CENTER_1F = (6, 5)
    PEWTER_CITY_POKEMON_CENTER_2F = (6, 6)
    PEWTER_CITY_HOUSE2 = (6, 7)

    # IndoorCerulean
    CERULEAN_CITY_HOUSE1 = (7, 0)
    CERULEAN_CITY_HOUSE2 = (7, 1)
    CERULEAN_CITY_HOUSE3 = (7, 2)
    CERULEAN_CITY_POKEMON_CENTER_1F = (7, 3)
    CERULEAN_CITY_POKEMON_CENTER_2F = (7, 4)
    CERULEAN_CITY_GYM = (7, 5)
    CERULEAN_CITY_BIKE_SHOP = (7, 6)
    CERULEAN_CITY_MART = (7, 7)
    CERULEAN_CITY_HOUSE4 = (7, 8)
    CERULEAN_CITY_HOUSE5 = (7, 9)

    # IndoorLavender
    LAVENDER_TOWN_POKEMON_CENTER_1F = (8, 0)
    LAVENDER_TOWN_POKEMON_CENTER_2F = (8, 1)
    LAVENDER_TOWN_VOLUNTEER_POKEMON_HOUSE = (8, 2)
    LAVENDER_TOWN_HOUSE1 = (8, 3)
    LAVENDER_TOWN_HOUSE2 = (8, 4)
    LAVENDER_TOWN_MART = (8, 5)

    # IndoorVermilion
    VERMILION_CITY_HOUSE1 = (9, 0)
    VERMILION_CITY_POKEMON_CENTER_1F = (9, 1)
    VERMILION_CITY_POKEMON_CENTER_2F = (9, 2)
    VERMILION_CITY_POKEMON_FAN_CLUB = (9, 3)
    VERMILION_CITY_HOUSE2 = (9, 4)
    VERMILION_CITY_MART = (9, 5)
    VERMILION_CITY_GYM = (9, 6)
    VERMILION_CITY_HOUSE3 = (9, 7)

    # IndoorCeladon
    CELADON_CITY_DEPARTMENT_STORE_1F = (10, 0)
    CELADON_CITY_DEPARTMENT_STORE_2F = (10, 1)
    CELADON_CITY_DEPARTMENT_STORE_3F = (10, 2)
    CELADON_CITY_DEPARTMENT_STORE_4F = (10, 3)
    CELADON_CITY_DEPARTMENT_STORE_5F = (10, 4)
    CELADON_CITY_DEPARTMENT_STORE_ROOF = (10, 5)
    CELADON_CITY_DEPARTMENT_STORE_ELEVATOR = (10, 6)
    CELADON_CITY_CONDOMINIUMS_1F = (10, 7)
    CELADON_CITY_CONDOMINIUMS_2F = (10, 8)
    CELADON_CITY_CONDOMINIUMS_3F = (10, 9)
    CELADON_CITY_CONDOMINIUMS_ROOF = (10, 10)
    CELADON_CITY_CONDOMINIUMS_ROOF_ROOM = (10, 11)
    CELADON_CITY_POKEMON_CENTER_1F = (10, 12)
    CELADON_CITY_POKEMON_CENTER_2F = (10, 13)
    CELADON_CITY_GAME_CORNER = (10, 14)
    CELADON_CITY_GAME_CORNER_PRIZE_ROOM = (10, 15)
    CELADON_CITY_GYM = (10, 16)
    CELADON_CITY_RESTAURANT = (10, 17)
    CELADON_CITY_HOUSE1 = (10, 18)
    CELADON_CITY_HOTEL = (10, 19)

    # IndoorFuchsia
    FUCHSIA_CITY_SAFARI_ZONE_ENTRANCE = (11, 0)
    FUCHSIA_CITY_MART = (11, 1)
    FUCHSIA_CITY_SAFARI_ZONE_OFFICE = (11, 2)
    FUCHSIA_CITY_GYM = (11, 3)
    FUCHSIA_CITY_HOUSE1 = (11, 4)
    FUCHSIA_CITY_POKEMON_CENTER_1F = (11, 5)
    FUCHSIA_CITY_POKEMON_CENTER_2F = (11, 6)
    FUCHSIA_CITY_WARDENS_HOUSE = (11, 7)
    FUCHSIA_CITY_HOUSE2 = (11, 8)
    FUCHSIA_CITY_HOUSE3 = (11, 9)

    # IndoorCinnabar
    CINNABAR_ISLAND_GYM = (12, 0)
    CINNABAR_ISLAND_POKEMON_LAB_ENTRANCE = (12, 1)
    CINNABAR_ISLAND_POKEMON_LAB_LOUNGE = (12, 2)
    CINNABAR_ISLAND_POKEMON_LAB_RESEARCH_ROOM = (12, 3)
    CINNABAR_ISLAND_POKEMON_LAB_EXPERIMENT_ROOM = (12, 4)
    CINNABAR_ISLAND_POKEMON_CENTER_1F = (12, 5)
    CINNABAR_ISLAND_POKEMON_CENTER_2F = (12, 6)
    CINNABAR_ISLAND_MART = (12, 7)

    # IndoorIndigoPlateau
    INDIGO_PLATEAU_POKEMON_CENTER_1F = (13, 0)
    INDIGO_PLATEAU_POKEMON_CENTER_2F = (13, 1)

    # IndoorSaffron
    SAFFRON_CITY_COPYCATS_HOUSE_1F = (14, 0)
    SAFFRON_CITY_COPYCATS_HOUSE_2F = (14, 1)
    SAFFRON_CITY_DOJO = (14, 2)
    SAFFRON_CITY_GYM = (14, 3)
    SAFFRON_CITY_HOUSE = (14, 4)
    SAFFRON_CITY_MART = (14, 5)
    SAFFRON_CITY_POKEMON_CENTER_1F = (14, 6)
    SAFFRON_CITY_POKEMON_CENTER_2F = (14, 7)
    SAFFRON_CITY_MR_PSYCHICS_HOUSE = (14, 8)
    SAFFRON_CITY_POKEMON_TRAINER_FAN_CLUB = (14, 9)

    # IndoorRoute2
    ROUTE2_VIRIDIAN_FOREST_SOUTH_ENTRANCE = (15, 0)
    ROUTE2_HOUSE = (15, 1)
    ROUTE2_EAST_BUILDING = (15, 2)
    ROUTE2_VIRIDIAN_FOREST_NORTH_ENTRANCE = (15, 3)

    # IndoorRoute4
    ROUTE4_POKEMON_CENTER_1F = (16, 0)
    ROUTE4_POKEMON_CENTER_2F = (16, 1)

    # IndoorRoute5
    ROUTE5_POKEMON_DAY_CARE = (17, 0)
    ROUTE5_SOUTH_ENTRANCE = (17, 1)

    # IndoorRoute6
    ROUTE6_NORTH_ENTRANCE = (18, 0)
    ROUTE6_UNUSED_HOUSE = (18, 1)

    # IndoorRoute7
    ROUTE7_EAST_ENTRANCE = (19, 0)

    # IndoorRoute8
    ROUTE8_WEST_ENTRANCE = (20, 0)

    # IndoorRoute10
    ROUTE10_POKEMON_CENTER_1F = (21, 0)
    ROUTE10_POKEMON_CENTER_2F = (21, 1)

    # IndoorRoute11
    ROUTE11_EAST_ENTRANCE_1F = (22, 0)
    ROUTE11_EAST_ENTRANCE_2F = (22, 1)

    # IndoorRoute12
    ROUTE12_NORTH_ENTRANCE_1F = (23, 0)
    ROUTE12_NORTH_ENTRANCE_2F = (23, 1)
    ROUTE12_FISHING_HOUSE = (23, 2)

    # IndoorRoute15
    ROUTE15_WEST_ENTRANCE_1F = (24, 0)
    ROUTE15_WEST_ENTRANCE_2F = (24, 1)

    # IndoorRoute16
    ROUTE16_HOUSE = (25, 0)
    ROUTE16_NORTH_ENTRANCE_1F = (25, 1)
    ROUTE16_NORTH_ENTRANCE_2F = (25, 2)

    # IndoorRoute18
    ROUTE18_EAST_ENTRANCE_1F = (26, 0)
    ROUTE18_EAST_ENTRANCE_2F = (26, 1)

    # IndoorRoute19
    ROUTE19_UNUSED_HOUSE = (27, 0)

    # IndoorRoute22
    ROUTE22_NORTH_ENTRANCE = (28, 0)

    # IndoorRoute23
    ROUTE23_UNUSED_HOUSE = (29, 0)

    # IndoorRoute25
    ROUTE25_SEA_COTTAGE = (30, 0)

    # IndoorSevenIsland
    SEVEN_ISLAND_HOUSE_ROOM1 = (31, 0)
    SEVEN_ISLAND_HOUSE_ROOM2 = (31, 1)
    SEVEN_ISLAND_MART = (31, 2)
    SEVEN_ISLAND_POKEMON_CENTER_1F = (31, 3)
    SEVEN_ISLAND_POKEMON_CENTER_2F = (31, 4)
    SEVEN_ISLAND_UNUSED_HOUSE = (31, 5)
    SEVEN_ISLAND_HARBOR = (31, 6)

    # IndoorOneIsland
    ONE_ISLAND_POKEMON_CENTER_1F = (32, 0)
    ONE_ISLAND_POKEMON_CENTER_2F = (32, 1)
    ONE_ISLAND_HOUSE1 = (32, 2)
    ONE_ISLAND_HOUSE2 = (32, 3)
    ONE_ISLAND_HARBOR = (32, 4)

    # IndoorTwoIsland
    TWO_ISLAND_JOYFUL_GAME_CORNER = (33, 0)
    TWO_ISLAND_HOUSE = (33, 1)
    TWO_ISLAND_POKEMON_CENTER_1F = (33, 2)
    TWO_ISLAND_POKEMON_CENTER_2F = (33, 3)
    TWO_ISLAND_HARBOR = (33, 4)

    # IndoorThreeIsland
    THREE_ISLAND_HOUSE1 = (34, 0)
    THREE_ISLAND_POKEMON_CENTER_1F = (34, 1)
    THREE_ISLAND_POKEMON_CENTER_2F = (34, 2)
    THREE_ISLAND_MART = (34, 3)
    THREE_ISLAND_HOUSE2 = (34, 4)
    THREE_ISLAND_HOUSE3 = (34, 5)
    THREE_ISLAND_HOUSE4 = (34, 6)
    THREE_ISLAND_HOUSE5 = (34, 7)

    # IndoorFourIsland
    FOUR_ISLAND_POKEMON_DAY_CARE = (35, 0)
    FOUR_ISLAND_POKEMON_CENTER_1F = (35, 1)
    FOUR_ISLAND_POKEMON_CENTER_2F = (35, 2)
    FOUR_ISLAND_HOUSE1 = (35, 3)
    FOUR_ISLAND_LORELEIS_HOUSE = (35, 4)
    FOUR_ISLAND_HARBOR = (35, 5)
    FOUR_ISLAND_HOUSE2 = (35, 6)
    FOUR_ISLAND_MART = (35, 7)

    # IndoorFiveIsland
    FIVE_ISLAND_POKEMON_CENTER_1F = (36, 0)
    FIVE_ISLAND_POKEMON_CENTER_2F = (36, 1)
    FIVE_ISLAND_HARBOR = (36, 2)
    FIVE_ISLAND_HOUSE1 = (36, 3)
    FIVE_ISLAND_HOUSE2 = (36, 4)

    # IndoorSixIsland
    SIX_ISLAND_POKEMON_CENTER_1F = (37, 0)
    SIX_ISLAND_POKEMON_CENTER_2F = (37, 1)
    SIX_ISLAND_HARBOR = (37, 2)
    SIX_ISLAND_HOUSE = (37, 3)
    SIX_ISLAND_MART = (37, 4)

    # IndoorThreeIslandRoute
    THREE_ISLAND_HARBOR = (38, 0)

    # IndoorFiveIslandRoute
    FIVE_ISLAND_RESORT_GORGEOUS_HOUSE = (39, 0)

    # IndoorTwoIslandRoute
    TWO_ISLAND_CAPE_BRINK_HOUSE = (40, 0)

    # IndoorSixIslandRoute
    SIX_ISLAND_WATER_PATH_HOUSE1 = (41, 0)
    SIX_ISLAND_WATER_PATH_HOUSE2 = (41, 1)

    # IndoorSevenIslandRoute
    SEVEN_ISLAND_SEVAULT_CANYON_HOUSE = (42, 0)

    def __eq__(self, other):
        if _might_be_map_coordinates(other):
            return self.value == other
        elif isinstance(other, MapFRLG):
            return self.value == other.value
        else:
            return NotImplemented

    def __ne__(self, other):
        equals = self.__eq__(other)
        return not equals if isinstance(equals, bool) else NotImplemented

    def __contains__(self, item):
        if item is None:
            return False
        elif isinstance(item, MapLocation):
            return item.map_group == self.value[0] and item.map_number == self.value[1]
        else:
            return NotImplemented

    def __getitem__(self, item) -> int:
        if item == 0:
            return self.value[0]
        elif item == 1:
            return self.value[1]
        elif isinstance(item, int):
            raise KeyError(f"Object does not have an item with key '{item}'.")
        else:
            raise TypeError(f"Object only has items of type int.")

    def __len__(self) -> int:
        return 2

    def __iter__(self) -> Generator:
        yield self.value[0]
        yield self.value[1]

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return self.name

    @property
    def exists_on_rs(self) -> bool:
        return False

    @property
    def pretty_name(self) -> str:
        name = self.name.replace("_", " ").title().split()

        substitutions = {
            "Pokemon": "Pokémon",
            "Ssanne": "S.S. Anne",
            "Digletts": "Diglett’s",
            "Co": "Co.",
            "Mt": "Mt.",
            "Loreleis": "Lorelei’s",
            "Brunos": "Bruno’s",
            "Agathas": "Agatha’s",
            "Lances": "Lance’s",
            "Champions": "Champion’s",
            "Players": "Player’s",
            "Rivals": "Rival’s",
            "Oaks": "Oak’s",
            "Wardens": "Warden’s",
            "Copycats": "Copycat’s",
            "Mr": "Mr.",
            "Psychics": "Psychic’s",
            "Captains": "Captain’s",
        }

        for index in range(len(name)):
            if name[index] in substitutions:
                name[index] = substitutions[name[index]]

            if match := re.match("^([A-Z][a-z]+)(\\d+)$", name[index]):
                name[index] = f"{match.group(1)} {match.group(2)}"
                if len(name) > index + 1:
                    name[index] += ","

            if re.match("^B?\\d+[FP]$", name[index]):
                name[index] = f"({name[index]})"

        name = " ".join(name).replace(", (", " (")

        prefixes = (
            "S.S. Anne",
            "Underground Path",
            "Diglett’s Cave",
            "Rocket Hideout",
            "Safari Zone",
            "Safari Zone, Center",
            "Safari Zone, East",
            "Safari Zone, North",
            "Safari Zone, West",
            "Pokémon League",
            "Mt. Ember",
            "One Island",
            "One Island, Kindle Road",
            "Two Island",
            "Two Island, Cape Brink",
            "Three Island",
            "Four Island",
            "Four Island, Icefall Cave",
            "Five Island",
            "Five Island, Lost Cave",
            "Five Island, Resort Gorgeous",
            "Six Island",
            "Six Island, Dotted Hole",
            "Six Island, Water Path",
            "Seven Island",
            "Seven Island, Tanoby Ruins",
            "Seven Island, Sevault Canyon",
            "Navel Rock",
            "Trainer Tower",
            "Birth Island",
            "Indigo Plateau",
            "Saffron City",
            "Pallet Town",
            "Viridian City",
            "Pewter City",
            "Cerulean City",
            "Lavender Town",
            "Vermilion City",
            "Celadon City",
            "Celadon City, Game Corner",
            "Fuchsia City",
            "Cinnabar Island",
            "Cinnabar Island, Pokémon Lab",
        )

        for prefix in prefixes:
            if name.startswith(prefix):
                first_part = prefix
                next_part = name[len(prefix) :].strip()
                if next_part.startswith("("):
                    first_part += " " + next_part[: next_part.index(")") + 1]
                    next_part = next_part[next_part.index(")") + 1 :].strip()
                if next_part not in ("", "Gym", "School", "Mart", "Museum"):
                    name = f"{first_part}, {next_part}"

        full_substitutions = {
            "North South Tunnel": "North/South Tunnel",
            "East West Tunnel": "East/West Tunnel",
        }
        for substitution in full_substitutions:
            name = name.replace(substitution, full_substitutions[substitution])

        return name


class MapGroupRSE(Enum):
    TownsAndRoutes = 0
    IndoorLittleroot = 1
    IndoorOldale = 2
    IndoorDewford = 3
    IndoorLavaridge = 4
    IndoorFallarbor = 5
    IndoorVerdanturf = 6
    IndoorPacifidlog = 7
    IndoorPetalburg = 8
    IndoorSlateport = 9
    IndoorMauville = 10
    IndoorRustboro = 11
    IndoorFortree = 12
    IndoorLilycove = 13
    IndoorMossdeep = 14
    IndoorSootopolis = 15
    IndoorEverGrande = 16
    IndoorRoute104 = 17
    IndoorRoute111 = 18
    IndoorRoute112 = 19
    IndoorRoute114 = 20
    IndoorRoute116 = 21
    IndoorRoute117 = 22
    IndoorRoute121 = 23
    Dungeons = 24
    IndoorDynamic = 25
    SpecialArea = 26
    IndoorRoute104Prototype = 27
    IndoorRoute109 = 28
    IndoorRoute110 = 29
    IndoorRoute113 = 30
    IndoorRoute123 = 31
    IndoorRoute119 = 32
    IndoorRoute124 = 33

    def __contains__(self, item):
        if _might_be_map_coordinates(item):
            return self.value == item[0]
        elif isinstance(item, MapRSE):
            return self.value == item.value[0]
        else:
            return NotImplemented

    @property
    def maps(self) -> "list[MapRSE]":
        result = []
        for item in MapRSE:
            if item.value[0] == self.value:
                result.append(item)
        return result


class MapRSE(Enum):
    # TownsAndRoutes
    PETALBURG_CITY = (0, 0)
    SLATEPORT_CITY = (0, 1)
    MAUVILLE_CITY = (0, 2)
    RUSTBORO_CITY = (0, 3)
    FORTREE_CITY = (0, 4)
    LILYCOVE_CITY = (0, 5)
    MOSSDEEP_CITY = (0, 6)
    SOOTOPOLIS_CITY = (0, 7)
    EVER_GRANDE_CITY = (0, 8)
    LITTLEROOT_TOWN = (0, 9)
    OLDALE_TOWN = (0, 10)
    DEWFORD_TOWN = (0, 11)
    LAVARIDGE_TOWN = (0, 12)
    FALLARBOR_TOWN = (0, 13)
    VERDANTURF_TOWN = (0, 14)
    PACIFIDLOG_TOWN = (0, 15)
    ROUTE101 = (0, 16)
    ROUTE102 = (0, 17)
    ROUTE103 = (0, 18)
    ROUTE104 = (0, 19)
    ROUTE105 = (0, 20)
    ROUTE106 = (0, 21)
    ROUTE107 = (0, 22)
    ROUTE108 = (0, 23)
    ROUTE109 = (0, 24)
    ROUTE110 = (0, 25)
    ROUTE111 = (0, 26)
    ROUTE112 = (0, 27)
    ROUTE113 = (0, 28)
    ROUTE114 = (0, 29)
    ROUTE115 = (0, 30)
    ROUTE116 = (0, 31)
    ROUTE117 = (0, 32)
    ROUTE118 = (0, 33)
    ROUTE119 = (0, 34)
    ROUTE120 = (0, 35)
    ROUTE121 = (0, 36)
    ROUTE122 = (0, 37)
    ROUTE123 = (0, 38)
    ROUTE124 = (0, 39)
    ROUTE125 = (0, 40)
    ROUTE126 = (0, 41)
    ROUTE127 = (0, 42)
    ROUTE128 = (0, 43)
    ROUTE129 = (0, 44)
    ROUTE130 = (0, 45)
    ROUTE131 = (0, 46)
    ROUTE132 = (0, 47)
    ROUTE133 = (0, 48)
    ROUTE134 = (0, 49)
    UNDERWATER_ROUTE124 = (0, 50)
    UNDERWATER_ROUTE126 = (0, 51)
    UNDERWATER_ROUTE127 = (0, 52)
    UNDERWATER_ROUTE128 = (0, 53)
    UNDERWATER_ROUTE129 = (0, 54)
    UNDERWATER_ROUTE105 = (0, 55)
    UNDERWATER_ROUTE125 = (0, 56)

    # IndoorLittleroot
    LITTLEROOT_TOWN_BRENDANS_HOUSE_1F = (1, 0)
    LITTLEROOT_TOWN_BRENDANS_HOUSE_2F = (1, 1)
    LITTLEROOT_TOWN_MAYS_HOUSE_1F = (1, 2)
    LITTLEROOT_TOWN_MAYS_HOUSE_2F = (1, 3)
    LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB = (1, 4)

    # IndoorOldale
    OLDALE_TOWN_HOUSE1 = (2, 0)
    OLDALE_TOWN_HOUSE2 = (2, 1)
    OLDALE_TOWN_POKEMON_CENTER_1F = (2, 2)
    OLDALE_TOWN_POKEMON_CENTER_2F = (2, 3)
    OLDALE_TOWN_MART = (2, 4)

    # IndoorDewford
    DEWFORD_TOWN_HOUSE1 = (3, 0)
    DEWFORD_TOWN_POKEMON_CENTER_1F = (3, 1)
    DEWFORD_TOWN_POKEMON_CENTER_2F = (3, 2)
    DEWFORD_TOWN_GYM = (3, 3)
    DEWFORD_TOWN_HALL = (3, 4)
    DEWFORD_TOWN_HOUSE2 = (3, 5)

    # IndoorLavaridge
    LAVARIDGE_TOWN_HERB_SHOP = (4, 0)
    LAVARIDGE_TOWN_GYM_1F = (4, 1)
    LAVARIDGE_TOWN_GYM_B1F = (4, 2)
    LAVARIDGE_TOWN_HOUSE = (4, 3)
    LAVARIDGE_TOWN_MART = (4, 4)
    LAVARIDGE_TOWN_POKEMON_CENTER_1F = (4, 5)
    LAVARIDGE_TOWN_POKEMON_CENTER_2F = (4, 6)

    # IndoorFallarbor
    FALLARBOR_TOWN_MART = (5, 0)
    FALLARBOR_TOWN_BATTLE_TENT_LOBBY = (5, 1)
    FALLARBOR_TOWN_BATTLE_TENT_CORRIDOR = (5, 2)
    FALLARBOR_TOWN_BATTLE_TENT_BATTLE_ROOM = (5, 3)
    FALLARBOR_TOWN_POKEMON_CENTER_1F = (5, 4)
    FALLARBOR_TOWN_POKEMON_CENTER_2F = (5, 5)
    FALLARBOR_TOWN_COZMOS_HOUSE = (5, 6)
    FALLARBOR_TOWN_MOVE_RELEARNERS_HOUSE = (5, 7)

    # IndoorVerdanturf
    VERDANTURF_TOWN_BATTLE_TENT_LOBBY = (6, 0)
    VERDANTURF_TOWN_BATTLE_TENT_CORRIDOR = (6, 1)
    VERDANTURF_TOWN_BATTLE_TENT_BATTLE_ROOM = (6, 2)
    VERDANTURF_TOWN_MART = (6, 3)
    VERDANTURF_TOWN_POKEMON_CENTER_1F = (6, 4)
    VERDANTURF_TOWN_POKEMON_CENTER_2F = (6, 5)
    VERDANTURF_TOWN_WANDAS_HOUSE = (6, 6)
    VERDANTURF_TOWN_FRIENDSHIP_RATERS_HOUSE = (6, 7)
    VERDANTURF_TOWN_HOUSE = (6, 8)

    # IndoorPacifidlog
    PACIFIDLOG_TOWN_POKEMON_CENTER_1F = (7, 0)
    PACIFIDLOG_TOWN_POKEMON_CENTER_2F = (7, 1)
    PACIFIDLOG_TOWN_HOUSE1 = (7, 2)
    PACIFIDLOG_TOWN_HOUSE2 = (7, 3)
    PACIFIDLOG_TOWN_HOUSE3 = (7, 4)
    PACIFIDLOG_TOWN_HOUSE4 = (7, 5)
    PACIFIDLOG_TOWN_HOUSE5 = (7, 6)

    # IndoorPetalburg
    PETALBURG_CITY_WALLYS_HOUSE = (8, 0)
    PETALBURG_CITY_GYM = (8, 1)
    PETALBURG_CITY_HOUSE1 = (8, 2)
    PETALBURG_CITY_HOUSE2 = (8, 3)
    PETALBURG_CITY_POKEMON_CENTER_1F = (8, 4)
    PETALBURG_CITY_POKEMON_CENTER_2F = (8, 5)
    PETALBURG_CITY_MART = (8, 6)

    # IndoorSlateport
    SLATEPORT_CITY_STERNS_SHIPYARD_1F = (9, 0)
    SLATEPORT_CITY_STERNS_SHIPYARD_2F = (9, 1)
    SLATEPORT_CITY_BATTLE_TENT_LOBBY = (9, 2)
    SLATEPORT_CITY_BATTLE_TENT_CORRIDOR = (9, 3)
    SLATEPORT_CITY_BATTLE_TENT_BATTLE_ROOM = (9, 4)
    SLATEPORT_CITY_NAME_RATERS_HOUSE = (9, 5)
    SLATEPORT_CITY_POKEMON_FAN_CLUB = (9, 6)
    SLATEPORT_CITY_OCEANIC_MUSEUM_1F = (9, 7)
    SLATEPORT_CITY_OCEANIC_MUSEUM_2F = (9, 8)
    SLATEPORT_CITY_HARBOR = (9, 9)
    SLATEPORT_CITY_HOUSE = (9, 10)
    SLATEPORT_CITY_POKEMON_CENTER_1F = (9, 11)
    SLATEPORT_CITY_POKEMON_CENTER_2F = (9, 12)
    SLATEPORT_CITY_MART = (9, 13)

    # IndoorMauville
    MAUVILLE_CITY_GYM = (10, 0)
    MAUVILLE_CITY_BIKE_SHOP = (10, 1)
    MAUVILLE_CITY_HOUSE1 = (10, 2)
    MAUVILLE_CITY_GAME_CORNER = (10, 3)
    MAUVILLE_CITY_HOUSE2 = (10, 4)
    MAUVILLE_CITY_POKEMON_CENTER_1F = (10, 5)
    MAUVILLE_CITY_POKEMON_CENTER_2F = (10, 6)
    MAUVILLE_CITY_MART = (10, 7)

    # IndoorRustboro
    RUSTBORO_CITY_DEVON_CORP_1F = (11, 0)
    RUSTBORO_CITY_DEVON_CORP_2F = (11, 1)
    RUSTBORO_CITY_DEVON_CORP_3F = (11, 2)
    RUSTBORO_CITY_GYM = (11, 3)
    RUSTBORO_CITY_POKEMON_SCHOOL = (11, 4)
    RUSTBORO_CITY_POKEMON_CENTER_1F = (11, 5)
    RUSTBORO_CITY_POKEMON_CENTER_2F = (11, 6)
    RUSTBORO_CITY_MART = (11, 7)
    RUSTBORO_CITY_FLAT1_1F = (11, 8)
    RUSTBORO_CITY_FLAT1_2F = (11, 9)
    RUSTBORO_CITY_HOUSE1 = (11, 10)
    RUSTBORO_CITY_CUTTERS_HOUSE = (11, 11)
    RUSTBORO_CITY_HOUSE2 = (11, 12)
    RUSTBORO_CITY_FLAT2_1F = (11, 13)
    RUSTBORO_CITY_FLAT2_2F = (11, 14)
    RUSTBORO_CITY_FLAT2_3F = (11, 15)
    RUSTBORO_CITY_HOUSE3 = (11, 16)

    # IndoorFortree
    FORTREE_CITY_HOUSE1 = (12, 0)
    FORTREE_CITY_GYM = (12, 1)
    FORTREE_CITY_POKEMON_CENTER_1F = (12, 2)
    FORTREE_CITY_POKEMON_CENTER_2F = (12, 3)
    FORTREE_CITY_MART = (12, 4)
    FORTREE_CITY_HOUSE2 = (12, 5)
    FORTREE_CITY_HOUSE3 = (12, 6)
    FORTREE_CITY_HOUSE4 = (12, 7)
    FORTREE_CITY_HOUSE5 = (12, 8)
    FORTREE_CITY_DECORATION_SHOP = (12, 9)

    # IndoorLilycove
    LILYCOVE_CITY_COVE_LILY_MOTEL_1F = (13, 0)
    LILYCOVE_CITY_COVE_LILY_MOTEL_2F = (13, 1)
    LILYCOVE_CITY_LILYCOVE_MUSEUM_1F = (13, 2)
    LILYCOVE_CITY_LILYCOVE_MUSEUM_2F = (13, 3)
    LILYCOVE_CITY_CONTEST_LOBBY = (13, 4)
    LILYCOVE_CITY_CONTEST_HALL = (13, 5)
    LILYCOVE_CITY_POKEMON_CENTER_1F = (13, 6)
    LILYCOVE_CITY_POKEMON_CENTER_2F = (13, 7)
    LILYCOVE_CITY_UNUSED_MART = (13, 8)
    LILYCOVE_CITY_POKEMON_TRAINER_FAN_CLUB = (13, 9)
    LILYCOVE_CITY_HARBOR = (13, 10)
    LILYCOVE_CITY_MOVE_DELETERS_HOUSE = (13, 11)
    LILYCOVE_CITY_HOUSE1 = (13, 12)
    LILYCOVE_CITY_HOUSE2 = (13, 13)
    LILYCOVE_CITY_HOUSE3 = (13, 14)
    LILYCOVE_CITY_HOUSE4 = (13, 15)
    LILYCOVE_CITY_DEPARTMENT_STORE_1F = (13, 16)
    LILYCOVE_CITY_DEPARTMENT_STORE_2F = (13, 17)
    LILYCOVE_CITY_DEPARTMENT_STORE_3F = (13, 18)
    LILYCOVE_CITY_DEPARTMENT_STORE_4F = (13, 19)
    LILYCOVE_CITY_DEPARTMENT_STORE_5F = (13, 20)
    LILYCOVE_CITY_DEPARTMENT_STORE_ROOFTOP = (13, 21)
    LILYCOVE_CITY_DEPARTMENT_STORE_ELEVATOR = (13, 22)

    # IndoorMossdeep
    MOSSDEEP_CITY_GYM = (14, 0)
    MOSSDEEP_CITY_HOUSE1 = (14, 1)
    MOSSDEEP_CITY_HOUSE2 = (14, 2)
    MOSSDEEP_CITY_POKEMON_CENTER_1F = (14, 3)
    MOSSDEEP_CITY_POKEMON_CENTER_2F = (14, 4)
    MOSSDEEP_CITY_MART = (14, 5)
    MOSSDEEP_CITY_HOUSE3 = (14, 6)
    MOSSDEEP_CITY_STEVENS_HOUSE = (14, 7)
    MOSSDEEP_CITY_HOUSE4 = (14, 8)
    MOSSDEEP_CITY_SPACE_CENTER_1F = (14, 9)
    MOSSDEEP_CITY_SPACE_CENTER_2F = (14, 10)
    MOSSDEEP_CITY_GAME_CORNER_1F = (14, 11)
    MOSSDEEP_CITY_GAME_CORNER_B1F = (14, 12)

    # IndoorSootopolis
    SOOTOPOLIS_CITY_GYM_1F = (15, 0)
    SOOTOPOLIS_CITY_GYM_B1F = (15, 1)
    SOOTOPOLIS_CITY_POKEMON_CENTER_1F = (15, 2)
    SOOTOPOLIS_CITY_POKEMON_CENTER_2F = (15, 3)
    SOOTOPOLIS_CITY_MART = (15, 4)
    SOOTOPOLIS_CITY_HOUSE1 = (15, 5)
    SOOTOPOLIS_CITY_HOUSE2 = (15, 6)
    SOOTOPOLIS_CITY_HOUSE3 = (15, 7)
    SOOTOPOLIS_CITY_HOUSE4 = (15, 8)
    SOOTOPOLIS_CITY_HOUSE5 = (15, 9)
    SOOTOPOLIS_CITY_HOUSE6 = (15, 10)
    SOOTOPOLIS_CITY_HOUSE7 = (15, 11)
    SOOTOPOLIS_CITY_LOTAD_AND_SEEDOT_HOUSE = (15, 12)
    SOOTOPOLIS_CITY_MYSTERY_EVENTS_HOUSE_1F = (15, 13)
    SOOTOPOLIS_CITY_MYSTERY_EVENTS_HOUSE_B1F = (15, 14)

    # IndoorEverGrande
    EVER_GRANDE_CITY_SIDNEYS_ROOM = (16, 0)
    EVER_GRANDE_CITY_PHOEBES_ROOM = (16, 1)
    EVER_GRANDE_CITY_GLACIAS_ROOM = (16, 2)
    EVER_GRANDE_CITY_DRAKES_ROOM = (16, 3)
    EVER_GRANDE_CITY_CHAMPIONS_ROOM = (16, 4)
    EVER_GRANDE_CITY_HALL1 = (16, 5)
    EVER_GRANDE_CITY_HALL2 = (16, 6)
    EVER_GRANDE_CITY_HALL3 = (16, 7)
    EVER_GRANDE_CITY_HALL4 = (16, 8)
    EVER_GRANDE_CITY_HALL5 = (16, 9)
    EVER_GRANDE_CITY_POKEMON_LEAGUE_1F = (16, 10)
    EVER_GRANDE_CITY_HALL_OF_FAME = (16, 11)
    EVER_GRANDE_CITY_POKEMON_CENTER_1F = (16, 12)
    EVER_GRANDE_CITY_POKEMON_CENTER_2F = (16, 13)
    EVER_GRANDE_CITY_POKEMON_LEAGUE_2F = (16, 14)

    # IndoorRoute104
    ROUTE104_MR_BRINEYS_HOUSE = (17, 0)
    ROUTE104_PRETTY_PETAL_FLOWER_SHOP = (17, 1)

    # IndoorRoute111
    ROUTE111_WINSTRATE_FAMILYS_HOUSE = (18, 0)
    ROUTE111_OLD_LADYS_REST_STOP = (18, 1)

    # IndoorRoute112
    ROUTE112_CABLE_CAR_STATION = (19, 0)
    MT_CHIMNEY_CABLE_CAR_STATION = (19, 1)

    # IndoorRoute114
    ROUTE114_FOSSIL_MANIACS_HOUSE = (20, 0)
    ROUTE114_FOSSIL_MANIACS_TUNNEL = (20, 1)
    ROUTE114_LANETTES_HOUSE = (20, 2)

    # IndoorRoute116
    ROUTE116_TUNNELERS_REST_HOUSE = (21, 0)

    # IndoorRoute117
    ROUTE117_POKEMON_DAY_CARE = (22, 0)

    # IndoorRoute121
    ROUTE121_SAFARI_ZONE_ENTRANCE = (23, 0)

    # Dungeons
    METEOR_FALLS_1F_1R = (24, 0)
    METEOR_FALLS_1F_2R = (24, 1)
    METEOR_FALLS_B1F_1R = (24, 2)
    METEOR_FALLS_B1F_2R = (24, 3)
    RUSTURF_TUNNEL = (24, 4)
    UNDERWATER_SOOTOPOLIS_CITY = (24, 5)
    DESERT_RUINS = (24, 6)
    GRANITE_CAVE_1F = (24, 7)
    GRANITE_CAVE_B1F = (24, 8)
    GRANITE_CAVE_B2F = (24, 9)
    GRANITE_CAVE_STEVENS_ROOM = (24, 10)
    PETALBURG_WOODS = (24, 11)
    MT_CHIMNEY = (24, 12)
    JAGGED_PASS = (24, 13)
    FIERY_PATH = (24, 14)
    MT_PYRE_1F = (24, 15)
    MT_PYRE_2F = (24, 16)
    MT_PYRE_3F = (24, 17)
    MT_PYRE_4F = (24, 18)
    MT_PYRE_5F = (24, 19)
    MT_PYRE_6F = (24, 20)
    MT_PYRE_EXTERIOR = (24, 21)
    MT_PYRE_SUMMIT = (24, 22)
    AQUA_HIDEOUT_1F = (24, 23)
    AQUA_HIDEOUT_B1F = (24, 24)
    AQUA_HIDEOUT_B2F = (24, 25)
    UNDERWATER_SEAFLOOR_CAVERN = (24, 26)
    SEAFLOOR_CAVERN_ENTRANCE = (24, 27)
    SEAFLOOR_CAVERN_ROOM1 = (24, 28)
    SEAFLOOR_CAVERN_ROOM2 = (24, 29)
    SEAFLOOR_CAVERN_ROOM3 = (24, 30)
    SEAFLOOR_CAVERN_ROOM4 = (24, 31)
    SEAFLOOR_CAVERN_ROOM5 = (24, 32)
    SEAFLOOR_CAVERN_ROOM6 = (24, 33)
    SEAFLOOR_CAVERN_ROOM7 = (24, 34)
    SEAFLOOR_CAVERN_ROOM8 = (24, 35)
    SEAFLOOR_CAVERN_ROOM9 = (24, 36)
    CAVE_OF_ORIGIN_ENTRANCE = (24, 37)
    CAVE_OF_ORIGIN_1F = (24, 38)
    CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP1 = (24, 39)
    CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP2 = (24, 40)
    CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP3 = (24, 41)
    CAVE_OF_ORIGIN_B1F = (24, 42)
    VICTORY_ROAD_1F = (24, 43)
    VICTORY_ROAD_B1F = (24, 44)
    VICTORY_ROAD_B2F = (24, 45)
    SHOAL_CAVE_LOW_TIDE_ENTRANCE_ROOM = (24, 46)
    SHOAL_CAVE_LOW_TIDE_INNER_ROOM = (24, 47)
    SHOAL_CAVE_LOW_TIDE_STAIRS_ROOM = (24, 48)
    SHOAL_CAVE_LOW_TIDE_LOWER_ROOM = (24, 49)
    SHOAL_CAVE_HIGH_TIDE_ENTRANCE_ROOM = (24, 50)
    SHOAL_CAVE_HIGH_TIDE_INNER_ROOM = (24, 51)
    NEW_MAUVILLE_ENTRANCE = (24, 52)
    NEW_MAUVILLE_INSIDE = (24, 53)
    ABANDONED_SHIP_DECK = (24, 54)
    ABANDONED_SHIP_CORRIDORS_1F = (24, 55)
    ABANDONED_SHIP_ROOMS_1F = (24, 56)
    ABANDONED_SHIP_CORRIDORS_B1F = (24, 57)
    ABANDONED_SHIP_ROOMS_B1F = (24, 58)
    ABANDONED_SHIP_ROOMS2_B1F = (24, 59)
    ABANDONED_SHIP_UNDERWATER1 = (24, 60)
    ABANDONED_SHIP_ROOM_B1F = (24, 61)
    ABANDONED_SHIP_ROOMS2_1F = (24, 62)
    ABANDONED_SHIP_CAPTAINS_OFFICE = (24, 63)
    ABANDONED_SHIP_UNDERWATER2 = (24, 64)
    ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS = (24, 65)
    ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS = (24, 66)
    ISLAND_CAVE = (24, 67)
    ANCIENT_TOMB = (24, 68)
    UNDERWATER_ROUTE134 = (24, 69)
    UNDERWATER_SEALED_CHAMBER = (24, 70)
    SEALED_CHAMBER_OUTER_ROOM = (24, 71)
    SEALED_CHAMBER_INNER_ROOM = (24, 72)
    SCORCHED_SLAB = (24, 73)
    AQUA_HIDEOUT_UNUSED_RUBY_MAP1 = (24, 74)
    AQUA_HIDEOUT_UNUSED_RUBY_MAP2 = (24, 75)
    AQUA_HIDEOUT_UNUSED_RUBY_MAP3 = (24, 76)
    SKY_PILLAR_ENTRANCE = (24, 77)
    SKY_PILLAR_OUTSIDE = (24, 78)
    SKY_PILLAR_1F = (24, 79)
    SKY_PILLAR_2F = (24, 80)
    SKY_PILLAR_3F = (24, 81)
    SKY_PILLAR_4F = (24, 82)
    SHOAL_CAVE_LOW_TIDE_ICE_ROOM = (24, 83)
    SKY_PILLAR_5F = (24, 84)
    SKY_PILLAR_TOP = (24, 85)
    MAGMA_HIDEOUT_1F = (24, 86)
    MAGMA_HIDEOUT_2F_1R = (24, 87)
    MAGMA_HIDEOUT_2F_2R = (24, 88)
    MAGMA_HIDEOUT_3F_1R = (24, 89)
    MAGMA_HIDEOUT_3F_2R = (24, 90)
    MAGMA_HIDEOUT_4F = (24, 91)
    MAGMA_HIDEOUT_3F_3R = (24, 92)
    MAGMA_HIDEOUT_2F_3R = (24, 93)
    MIRAGE_TOWER_1F = (24, 94)
    MIRAGE_TOWER_2F = (24, 95)
    MIRAGE_TOWER_3F = (24, 96)
    MIRAGE_TOWER_4F = (24, 97)
    DESERT_UNDERPASS = (24, 98)
    ARTISAN_CAVE_B1F = (24, 99)
    ARTISAN_CAVE_1F = (24, 100)
    UNDERWATER_MARINE_CAVE = (24, 101)
    MARINE_CAVE_ENTRANCE = (24, 102)
    MARINE_CAVE_END = (24, 103)
    TERRA_CAVE_ENTRANCE = (24, 104)
    TERRA_CAVE_END = (24, 105)
    ALTERING_CAVE = (24, 106)
    METEOR_FALLS_STEVENS_CAVE = (24, 107)

    # IndoorDynamic
    SECRET_BASE_RED_CAVE1 = (25, 0)
    SECRET_BASE_BROWN_CAVE1 = (25, 1)
    SECRET_BASE_BLUE_CAVE1 = (25, 2)
    SECRET_BASE_YELLOW_CAVE1 = (25, 3)
    SECRET_BASE_TREE1 = (25, 4)
    SECRET_BASE_SHRUB1 = (25, 5)
    SECRET_BASE_RED_CAVE2 = (25, 6)
    SECRET_BASE_BROWN_CAVE2 = (25, 7)
    SECRET_BASE_BLUE_CAVE2 = (25, 8)
    SECRET_BASE_YELLOW_CAVE2 = (25, 9)
    SECRET_BASE_TREE2 = (25, 10)
    SECRET_BASE_SHRUB2 = (25, 11)
    SECRET_BASE_RED_CAVE3 = (25, 12)
    SECRET_BASE_BROWN_CAVE3 = (25, 13)
    SECRET_BASE_BLUE_CAVE3 = (25, 14)
    SECRET_BASE_YELLOW_CAVE3 = (25, 15)
    SECRET_BASE_TREE3 = (25, 16)
    SECRET_BASE_SHRUB3 = (25, 17)
    SECRET_BASE_RED_CAVE4 = (25, 18)
    SECRET_BASE_BROWN_CAVE4 = (25, 19)
    SECRET_BASE_BLUE_CAVE4 = (25, 20)
    SECRET_BASE_YELLOW_CAVE4 = (25, 21)
    SECRET_BASE_TREE4 = (25, 22)
    SECRET_BASE_SHRUB4 = (25, 23)
    BATTLE_COLOSSEUM_2P = (25, 24)
    TRADE_CENTER = (25, 25)
    RECORD_CORNER = (25, 26)
    BATTLE_COLOSSEUM_4P = (25, 27)
    CONTEST_HALL = (25, 28)
    UNUSED_CONTEST_HALL1 = (25, 29)
    UNUSED_CONTEST_HALL2 = (25, 30)
    UNUSED_CONTEST_HALL3 = (25, 31)
    UNUSED_CONTEST_HALL4 = (25, 32)
    UNUSED_CONTEST_HALL5 = (25, 33)
    UNUSED_CONTEST_HALL6 = (25, 34)
    CONTEST_HALL_BEAUTY = (25, 35)
    CONTEST_HALL_TOUGH = (25, 36)
    CONTEST_HALL_COOL = (25, 37)
    CONTEST_HALL_SMART = (25, 38)
    CONTEST_HALL_CUTE = (25, 39)
    INSIDE_OF_TRUCK = (25, 40)
    SS_TIDAL_CORRIDOR = (25, 41)
    SS_TIDAL_LOWER_DECK = (25, 42)
    SS_TIDAL_ROOMS = (25, 43)
    BATTLE_PYRAMID_SQUARE01 = (25, 44)
    BATTLE_PYRAMID_SQUARE02 = (25, 45)
    BATTLE_PYRAMID_SQUARE03 = (25, 46)
    BATTLE_PYRAMID_SQUARE04 = (25, 47)
    BATTLE_PYRAMID_SQUARE05 = (25, 48)
    BATTLE_PYRAMID_SQUARE06 = (25, 49)
    BATTLE_PYRAMID_SQUARE07 = (25, 50)
    BATTLE_PYRAMID_SQUARE08 = (25, 51)
    BATTLE_PYRAMID_SQUARE09 = (25, 52)
    BATTLE_PYRAMID_SQUARE10 = (25, 53)
    BATTLE_PYRAMID_SQUARE11 = (25, 54)
    BATTLE_PYRAMID_SQUARE12 = (25, 55)
    BATTLE_PYRAMID_SQUARE13 = (25, 56)
    BATTLE_PYRAMID_SQUARE14 = (25, 57)
    BATTLE_PYRAMID_SQUARE15 = (25, 58)
    BATTLE_PYRAMID_SQUARE16 = (25, 59)
    UNION_ROOM = (25, 60)

    # SpecialArea
    SAFARI_ZONE_NORTHWEST = (26, 0)
    SAFARI_ZONE_NORTH = (26, 1)
    SAFARI_ZONE_SOUTHWEST = (26, 2)
    SAFARI_ZONE_SOUTH = (26, 3)
    BATTLE_FRONTIER_OUTSIDE_WEST = (26, 4)
    BATTLE_FRONTIER_BATTLE_TOWER_LOBBY = (26, 5)
    BATTLE_FRONTIER_BATTLE_TOWER_ELEVATOR = (26, 6)
    BATTLE_FRONTIER_BATTLE_TOWER_CORRIDOR = (26, 7)
    BATTLE_FRONTIER_BATTLE_TOWER_BATTLE_ROOM = (26, 8)
    SOUTHERN_ISLAND_EXTERIOR = (26, 9)
    SOUTHERN_ISLAND_INTERIOR = (26, 10)
    SAFARI_ZONE_REST_HOUSE = (26, 11)
    SAFARI_ZONE_NORTHEAST = (26, 12)
    SAFARI_ZONE_SOUTHEAST = (26, 13)
    BATTLE_FRONTIER_OUTSIDE_EAST = (26, 14)
    BATTLE_FRONTIER_BATTLE_TOWER_MULTI_PARTNER_ROOM = (26, 15)
    BATTLE_FRONTIER_BATTLE_TOWER_MULTI_CORRIDOR = (26, 16)
    BATTLE_FRONTIER_BATTLE_TOWER_MULTI_BATTLE_ROOM = (26, 17)
    BATTLE_FRONTIER_BATTLE_DOME_LOBBY = (26, 18)
    BATTLE_FRONTIER_BATTLE_DOME_CORRIDOR = (26, 19)
    BATTLE_FRONTIER_BATTLE_DOME_PRE_BATTLE_ROOM = (26, 20)
    BATTLE_FRONTIER_BATTLE_DOME_BATTLE_ROOM = (26, 21)
    BATTLE_FRONTIER_BATTLE_PALACE_LOBBY = (26, 22)
    BATTLE_FRONTIER_BATTLE_PALACE_CORRIDOR = (26, 23)
    BATTLE_FRONTIER_BATTLE_PALACE_BATTLE_ROOM = (26, 24)
    BATTLE_FRONTIER_BATTLE_PYRAMID_LOBBY = (26, 25)
    BATTLE_FRONTIER_BATTLE_PYRAMID_FLOOR = (26, 26)
    BATTLE_FRONTIER_BATTLE_PYRAMID_TOP = (26, 27)
    BATTLE_FRONTIER_BATTLE_ARENA_LOBBY = (26, 28)
    BATTLE_FRONTIER_BATTLE_ARENA_CORRIDOR = (26, 29)
    BATTLE_FRONTIER_BATTLE_ARENA_BATTLE_ROOM = (26, 30)
    BATTLE_FRONTIER_BATTLE_FACTORY_LOBBY = (26, 31)
    BATTLE_FRONTIER_BATTLE_FACTORY_PRE_BATTLE_ROOM = (26, 32)
    BATTLE_FRONTIER_BATTLE_FACTORY_BATTLE_ROOM = (26, 33)
    BATTLE_FRONTIER_BATTLE_PIKE_LOBBY = (26, 34)
    BATTLE_FRONTIER_BATTLE_PIKE_CORRIDOR = (26, 35)
    BATTLE_FRONTIER_BATTLE_PIKE_THREE_PATH_ROOM = (26, 36)
    BATTLE_FRONTIER_BATTLE_PIKE_ROOM_NORMAL = (26, 37)
    BATTLE_FRONTIER_BATTLE_PIKE_ROOM_FINAL = (26, 38)
    BATTLE_FRONTIER_BATTLE_PIKE_ROOM_WILD_MONS = (26, 39)
    BATTLE_FRONTIER_RANKING_HALL = (26, 40)
    BATTLE_FRONTIER_LOUNGE1 = (26, 41)
    BATTLE_FRONTIER_EXCHANGE_SERVICE_CORNER = (26, 42)
    BATTLE_FRONTIER_LOUNGE2 = (26, 43)
    BATTLE_FRONTIER_LOUNGE3 = (26, 44)
    BATTLE_FRONTIER_LOUNGE4 = (26, 45)
    BATTLE_FRONTIER_SCOTTS_HOUSE = (26, 46)
    BATTLE_FRONTIER_LOUNGE5 = (26, 47)
    BATTLE_FRONTIER_LOUNGE6 = (26, 48)
    BATTLE_FRONTIER_LOUNGE7 = (26, 49)
    BATTLE_FRONTIER_RECEPTION_GATE = (26, 50)
    BATTLE_FRONTIER_LOUNGE8 = (26, 51)
    BATTLE_FRONTIER_LOUNGE9 = (26, 52)
    BATTLE_FRONTIER_POKEMON_CENTER_1F = (26, 53)
    BATTLE_FRONTIER_POKEMON_CENTER_2F = (26, 54)
    BATTLE_FRONTIER_MART = (26, 55)
    FARAWAY_ISLAND_ENTRANCE = (26, 56)
    FARAWAY_ISLAND_INTERIOR = (26, 57)
    BIRTH_ISLAND_EXTERIOR = (26, 58)
    BIRTH_ISLAND_HARBOR = (26, 59)
    TRAINER_HILL_ENTRANCE = (26, 60)
    TRAINER_HILL_1F = (26, 61)
    TRAINER_HILL_2F = (26, 62)
    TRAINER_HILL_3F = (26, 63)
    TRAINER_HILL_4F = (26, 64)
    TRAINER_HILL_ROOF = (26, 65)
    NAVEL_ROCK_EXTERIOR = (26, 66)
    NAVEL_ROCK_HARBOR = (26, 67)
    NAVEL_ROCK_ENTRANCE = (26, 68)
    NAVEL_ROCK_B1F = (26, 69)
    NAVEL_ROCK_FORK = (26, 70)
    NAVEL_ROCK_UP1 = (26, 71)
    NAVEL_ROCK_UP2 = (26, 72)
    NAVEL_ROCK_UP3 = (26, 73)
    NAVEL_ROCK_UP4 = (26, 74)
    NAVEL_ROCK_TOP = (26, 75)
    NAVEL_ROCK_DOWN01 = (26, 76)
    NAVEL_ROCK_DOWN02 = (26, 77)
    NAVEL_ROCK_DOWN03 = (26, 78)
    NAVEL_ROCK_DOWN04 = (26, 79)
    NAVEL_ROCK_DOWN05 = (26, 80)
    NAVEL_ROCK_DOWN06 = (26, 81)
    NAVEL_ROCK_DOWN07 = (26, 82)
    NAVEL_ROCK_DOWN08 = (26, 83)
    NAVEL_ROCK_DOWN09 = (26, 84)
    NAVEL_ROCK_DOWN10 = (26, 85)
    NAVEL_ROCK_DOWN11 = (26, 86)
    NAVEL_ROCK_BOTTOM = (26, 87)
    TRAINER_HILL_ELEVATOR = (26, 88)

    # IndoorRoute104Prototype
    ROUTE104_PROTOTYPE = (27, 0)
    ROUTE104_PROTOTYPE_PRETTY_PETAL_FLOWER_SHOP = (27, 1)

    # IndoorRoute109
    ROUTE109_SEASHORE_HOUSE = (28, 0)

    # IndoorRoute110
    ROUTE110_TRICK_HOUSE_ENTRANCE = (29, 0)
    ROUTE110_TRICK_HOUSE_END = (29, 1)
    ROUTE110_TRICK_HOUSE_CORRIDOR = (29, 2)
    ROUTE110_TRICK_HOUSE_PUZZLE1 = (29, 3)
    ROUTE110_TRICK_HOUSE_PUZZLE2 = (29, 4)
    ROUTE110_TRICK_HOUSE_PUZZLE3 = (29, 5)
    ROUTE110_TRICK_HOUSE_PUZZLE4 = (29, 6)
    ROUTE110_TRICK_HOUSE_PUZZLE5 = (29, 7)
    ROUTE110_TRICK_HOUSE_PUZZLE6 = (29, 8)
    ROUTE110_TRICK_HOUSE_PUZZLE7 = (29, 9)
    ROUTE110_TRICK_HOUSE_PUZZLE8 = (29, 10)
    ROUTE110_SEASIDE_CYCLING_ROAD_NORTH_ENTRANCE = (29, 11)
    ROUTE110_SEASIDE_CYCLING_ROAD_SOUTH_ENTRANCE = (29, 12)

    # IndoorRoute113
    ROUTE113_GLASS_WORKSHOP = (30, 0)

    # IndoorRoute123
    ROUTE123_BERRY_MASTERS_HOUSE = (31, 0)

    # IndoorRoute119
    ROUTE119_WEATHER_INSTITUTE_1F = (32, 0)
    ROUTE119_WEATHER_INSTITUTE_2F = (32, 1)
    ROUTE119_HOUSE = (32, 2)

    # IndoorRoute124
    ROUTE124_DIVING_TREASURE_HUNTERS_HOUSE = (33, 0)

    def __eq__(self, other):
        if _might_be_map_coordinates(other):
            return self.value == other
        elif isinstance(other, MapRSE):
            return self.value == other.value
        else:
            return NotImplemented

    def __ne__(self, other):
        equals = self.__eq__(other)
        return not equals if isinstance(equals, bool) else NotImplemented

    def __contains__(self, item):
        if item is None:
            return False
        elif isinstance(item, MapLocation):
            return item.map_group == self.value[0] and item.map_number == self.value[1]
        else:
            return NotImplemented

    def __getitem__(self, item) -> int:
        if item == 0:
            return self.value[0]
        elif item == 1:
            return self.value[1]
        elif isinstance(item, int):
            raise KeyError(f"Object does not have an item with key '{item}'.")
        else:
            raise TypeError(f"Object only has items of type int.")

    def __len__(self) -> int:
        return 2

    def __iter__(self) -> Generator:
        yield self.value[0]
        yield self.value[1]

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return self.name

    @property
    def exists_on_rs(self) -> bool:
        emerald_only_maps = [(0, 54), (0, 55), (0, 56), (5, 7), (6, 8), (9, 13), (15, 13), (15, 14), (16, 14)]
        return self.value not in emerald_only_maps and (self.value[0] != 26 or self.value[1] <= 11)

    @property
    def pretty_name(self) -> str:
        name = self.name.replace("_", " ").title().split()

        substitutions = {
            "Pokemon": "Pokémon",
            "Brendans": "Brendan’s",
            "Mays": "May’s",
            "Birchs": "Birch’s",
            "Cozmos": "Cozmo’s",
            "Wandas": "Wanda’s",
            "Relearners": "Relearner’s",
            "Raters": "Rater’s",
            "Wallys": "Wally’s",
            "Sterns": "Stern’s",
            "Cutters": "Cutter’s",
            "Deleters": "Deleter’s",
            "Stevens": "Steven’s",
            "Sidneys": "Sidney’s",
            "Phoebes": "Phoebe’s",
            "Glacias": "Glacia’s",
            "Drakes": "Drake’s",
            "Champions": "Champion’s",
            "Brineys": "Briney’s",
            "Familys": "Family’s",
            "Ladys": "Lady’s",
            "Tunnelers": "Tunneler’s",
            "Maniacs": "Maniac’s",
            "Captains": "Captain’s",
            "Mt": "Mt.",
            "Ss": "S.S.",
            "Corp": "Corp.",
            "Northwest": "North/West",
            "Southwest": "South/West",
            "Northeast": "North/East",
            "Southeast": "South/East",
        }

        for index in range(len(name)):
            if name[index] in substitutions:
                name[index] = substitutions[name[index]]

            if match := re.match("^([A-Z][a-z]+)(\\d+)$", name[index]):
                name[index] = f"{match.group(1)} {match.group(2)}"
                if len(name) > index + 1:
                    name[index] += ","

            if re.match("^B?\\d+[FP]$", name[index]):
                name[index] = f"({name[index]})"

        if self.name.startswith("CONTEST_HALL_"):
            name[2] = f"({name[2]})"

        if "_BATTLE_TENT_" in self.name:
            name[3] += ","

        if (
            self.name.startswith("BATTLE_FRONTIER_")
            or self.name.startswith("SAFARI_ZONE_")
            or self.name.startswith("BATTLE_PYRAMID_")
            or self.name.startswith("SS_TIDAL_")
            or self.name.startswith("NEW_MAUVILLE_")
            or self.name.startswith("ABANDONED_SHIP_")
            or self.name.startswith("SEALED_CHAMBER_")
            or self.name.startswith("SECRET_BASE_")
            or re.match("^SKY_PILLAR_[A-Z]", self.name)
            or (len(name) > 2 and (name[1] == "Town" or name[1] == "City"))
        ):
            if len(name) > 2 and name[2] != "Gym" and name[2] != "Mart":
                name[1] += ","

        if self.name.startswith("EVER_GRANDE_CITY_"):
            if len(name) > 3 and name[3] != "Gym" and name[3] != "Mart":
                name[2] += ","

        if self.name.startswith("SHOAL_CAVE_"):
            name[2] = f"({name[2]}"
            name[3] = f"{name[3]})"

        if (
            self.name.startswith("BATTLE_FRONTIER_BATTLE_TOWER_")
            or self.name.startswith("BATTLE_FRONTIER_BATTLE_DOME_")
            or self.name.startswith("BATTLE_FRONTIER_BATTLE_PALACE_")
            or self.name.startswith("BATTLE_FRONTIER_BATTLE_PYRAMID_")
            or self.name.startswith("BATTLE_FRONTIER_BATTLE_ARENA_")
            or self.name.startswith("BATTLE_FRONTIER_BATTLE_FACTORY_")
            or self.name.startswith("BATTLE_FRONTIER_BATTLE_PIKE_")
            or self.name.startswith("ROUTE110_SEASIDE_CYCLING_ROAD_")
            or self.name.startswith("SHOAL_CAVE_LOW_TIDE")
            or self.name.startswith("SHOAL_CAVE_HIGH_TIDE")
        ):
            name[3] += ","

        name = " ".join(name).replace(", (", " (")
        return name


class PokemonCenter(Enum):
    OldaleTown = (MapRSE.OLDALE_TOWN, (6, 16))
    PetalburgCity = (MapRSE.PETALBURG_CITY, (20, 16))
    RustboroCity = (MapRSE.RUSTBORO_CITY, (16, 38))
    DewfordTown = (MapRSE.DEWFORD_TOWN, (2, 10))
    SlateportCity = (MapRSE.SLATEPORT_CITY, (19, 19))
    MauvilleCity = (MapRSE.MAUVILLE_CITY, (22, 5))
    VerdanturfTown = (MapRSE.VERDANTURF_TOWN, (16, 3))
    LavaridgeTown = (MapRSE.LAVARIDGE_TOWN, (9, 6))
    FallarborTown = (MapRSE.FALLARBOR_TOWN, (14, 7))
    FortreeCity = (MapRSE.FORTREE_CITY, (5, 6))
    LilycoveCity = (MapRSE.LILYCOVE_CITY, (24, 14))
    MossdeepCity = (MapRSE.MOSSDEEP_CITY, (28, 16))
    EvergrandeCity = (MapRSE.EVER_GRANDE_CITY, (27, 48))
    PacifidlogTown = (MapRSE.PACIFIDLOG_TOWN, (8, 15))

    PalletTown = (MapFRLG.PALLET_TOWN, (6, 7))
    ViridianCity = (MapFRLG.VIRIDIAN_CITY, (26, 26))
    PewterCity = (MapFRLG.PEWTER_CITY, (17, 25))
    Route4 = (MapFRLG.ROUTE4, (12, 5))
    CeruleanCity = (MapFRLG.CERULEAN_CITY, (22, 19))
    VermilionCity = (MapFRLG.VERMILION_CITY, (15, 6))
    Route10 = (MapFRLG.ROUTE10, (13, 20))
    LavenderTown = (MapFRLG.LAVENDER_TOWN, (6, 5))
    CeladonCity = (MapFRLG.CELADON_CITY, (48, 11))
    SaffronCity = (MapFRLG.SAFFRON_CITY, (24, 39))
    FuchsiaCity = (MapFRLG.FUCHSIA_CITY, (25, 31))
    CinnabarIsland = (MapFRLG.CINNABAR_ISLAND, (14, 11))

    def __repr__(self) -> str:
        return f"PokemonCenter.{self.name}"


def get_map_enum(map_group_and_number: tuple[int, int] | MapLocation) -> MapFRLG | MapRSE:
    if isinstance(map_group_and_number, MapLocation):
        map_group_and_number = map_group_and_number.map_group_and_number

    if context.rom.is_rse:
        return MapRSE(map_group_and_number)
    else:
        return MapFRLG(map_group_and_number)


def is_safari_map() -> bool:
    """
    Checks if the current map is a Safari Zone map.
    Raises an error if the ROM is not FRLG or RSE.
    """
    map = get_map_data_for_current_position()

    if context.rom.is_frlg:
        return (map.map_group, map.map_number) in {
            MapFRLG.SAFARI_ZONE_CENTER,
            MapFRLG.SAFARI_ZONE_EAST,
            MapFRLG.SAFARI_ZONE_NORTH,
            MapFRLG.SAFARI_ZONE_WEST,
        }
    elif context.rom.is_rse:
        return (map.map_group, map.map_number) in {
            MapRSE.SAFARI_ZONE_NORTHWEST,
            MapRSE.SAFARI_ZONE_NORTH,
            MapRSE.SAFARI_ZONE_SOUTHWEST,
            MapRSE.SAFARI_ZONE_SOUTH,
            MapRSE.SAFARI_ZONE_NORTHEAST,
            MapRSE.SAFARI_ZONE_SOUTHEAST,
        }

    raise ValueError("Unsupported ROM type: Safari Zone map check only supports FRLG and RSE.")
