import random

#  0       1       2      3      4        5         6       7      8      9
VORTEX, ASSAULT, SWANS, HUNT, INSIGHT, UNDOING, MOUNTAIN, ISLAND, DUAL, TEMPLE = range(10)
MULLIGAN, KEEP, COMBO = range(3)


def get_deck():
    deck = []

    # Mana base
    deck += [MOUNTAIN for i in range(18)]
    deck += [ISLAND for i in range(8)]
    deck += [DUAL for i in range(12)]
    deck += [TEMPLE for i in range(4)]

    # Spells
    deck += [VORTEX for i in range(2)]
    deck += [ASSAULT for i in range(4)]
    deck += [SWANS for i in range(4)]
    deck += [HUNT for i in range(4)]
    deck += [INSIGHT for i in range(3)]
    deck += [UNDOING for i in range(1)]

    if len(deck) != 60:
        print('******************************************')
        print('')
        print('IMPORTANT - DECK DOES NOT CONTAIN 60 CARDS')
        print('')
        print('******************************************')

    random.shuffle(deck)
    return deck


def count_lands(hand):
    lands = 0
    for card in hand:
        if card in (MOUNTAIN, ISLAND, DUAL, TEMPLE):
            lands += 1
    return lands


def count_red_sources(hand):
    reds = 0
    for card in hand:
        if card in (MOUNTAIN, DUAL, TEMPLE):
            reds += 1
    return reds


def count_blue_sources(hand):
    blue = 0
    for card in hand:
        if card in (ISLAND, DUAL, TEMPLE):
            blue += 1
    return blue


def is_hand_keepable(hand):
    n = len(hand)

    vortex = [VORTEX for card in hand if card == VORTEX]
    assault = [ASSAULT for card in hand if card == ASSAULT]
    swans = [SWANS for card in hand if card == SWANS]
    hunt = [HUNT for card in hand if card == HUNT]
    insight = [INSIGHT for card in hand if card == INSIGHT]
    undoing = [UNDOING for card in hand if card == UNDOING]
    mountain = [MOUNTAIN for card in hand if card == MOUNTAIN]
    island = [ISLAND for card in hand if card == ISLAND]
    dual = [DUAL for card in hand if card == DUAL]
    temple = [TEMPLE for card in hand if card == TEMPLE]

    lands = mountain + island + dual + temple
    spells = vortex + assault + swans + hunt + insight + undoing
    deck_manipulation = insight + hunt + temple
    fire = vortex + assault

    keep = MULLIGAN

    # 7 cards
    if n == 7:
        if len(lands) == 7:
            keep = MULLIGAN
        elif len(lands) <= 1:
            keep = MULLIGAN
        elif (fire != []) and (swans != [] or hunt != []):
            keep = KEEP
        elif assault != [] and undoing != []:
            keep = KEEP
        elif len(deck_manipulation) >= 3:
            keep = KEEP
        elif len(deck_manipulation) >= 2 and (fire != [] or swans != []):
            keep = KEEP

    # 6 cards
    if n == 6:
        if len(lands) == 6:
            keep = MULLIGAN
        elif len(lands) <= 1:
            keep = MULLIGAN
        elif (fire != []) and (swans != [] or hunt != []):
            keep = KEEP
        elif assault != [] and undoing != []:
            keep = KEEP
        elif len(deck_manipulation) >= 2:
            keep = KEEP
        elif len(deck_manipulation) >= 1 and (fire != [] or swans != []):
            keep = KEEP

    # 5 cards
    if n == 5:
        if not lands:
            keep = MULLIGAN
        elif not spells:
            keep = MULLIGAN
        elif fire != [] or deck_manipulation != []:
            keep = KEEP
        elif len(spells) >= 2:
            keep = KEEP

    # 4 cards
    if n == 4:
        keep = KEEP

    if keep == KEEP and assault != [] and swans != []:
        keep = COMBO
    return keep


# Keeping criteria:
# fire = assault or vortrex
# deck manipulation = temple, hunt or insight

# 7 cards:
#   Never keep:
#       0-1 lands
#       0 spells
#   Always keep:
#       fire + swans or hunt
#       assault + undoing
#       any 3 deck manipulation
#       any 2 deck manipulation + fire or swans
#   Mull the rest

# 6 cards:
#   Never keep:
#       0-1 lands
#       0 spells
#   Always keep:
#       fire + swans or hunt
#       assault + undoing
#       any 2 deck manipulation
#       any 1 deck manipulation + fire or swans
#   Mull the rest

# 5 cards:
#   Never keep:
#       0 lands
#       0 spells
#   Always keep:
#       any 1 fire or deck manipulation
#       any 2 spells
#   Mull the rest

# 4 cards:
#   Keep any hand