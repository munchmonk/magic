#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

# TODO: merge test_kept and test_lands in a single function; merge third and fourth turn simulation

import sys
import random
import time
from specific import get_deck
from specific import is_hand_keepable
from specific import count_lands
from specific import count_red_sources
from specific import count_blue_sources
from specific import MULLIGAN, KEEP, COMBO


def draw_hand(deck, n):
    hand = [deck.pop() for i in range(n)]

    # Reset deck
    deck += hand
    random.shuffle(deck)

    return hand


def draw_more_cards(deck, hand, n):
    # Remove drawn cards from deck
    for card in hand:
        deck.remove(card)
    random.shuffle(deck)

    # Draw more cards
    for i in range(n):
        hand.append(deck.pop())

    # Reset deck before returning
    deck += hand
    random.shuffle(deck)


# def test_lands(n):
#     deck = get_deck()
#     tot_lands = 0
#     tot_reds = 0
#     tot_blue = 0
#
#     for i in range(n):
#         curr_cards = 7
#         hand = draw_hand(deck, curr_cards)
#
#         # Keep mulliganing until we have a keepable hand
#         while not is_hand_keepable(hand):
#             curr_cards -= 1
#             hand = draw_hand(deck, curr_cards)
#
#         # Draw 2 more cards to simulate turn 3 or 3 more cards to simulate turn 4
#         draw_more_cards(deck, hand, 3)
#         tot_lands += count_lands(hand)
#         reds = count_reds(hand)
#         blue = count_blue(hand)
#         if reds >= 3:
#             tot_reds += 1
#         if blue >= 2:
#             tot_blue += 1
#
#     avg_lands = tot_lands / n
#     avg_reds_hit = tot_reds / n
#     avg_blue_hit = tot_blue / n
#     print('Average lands: {:.2f}'.format(avg_lands))
#     # print('% of 3+ R: {:.2f}'.format(avg_reds_hit))
#     print('% of 2+ U: {:.2f}'.format(avg_blue_hit))


def test_kept(n):
    deck = get_deck()

    kept_7 = 0
    kept_6 = 0
    kept_5 = 0
    combo_7 = 0
    combo_6 = 0
    combo_5 = 0

    turn_3_lands = 0
    turn_4_lands = 0
    turn_3_red_sources = 0
    turn_4_blue_sources = 0
    hit_turn_3 = 0
    hit_turn_4 = 0
    start = time.time()

    for i in range(n):
        # 7 cards
        hand = draw_hand(deck, 7)
        keep = is_hand_keepable(hand)
        if keep != MULLIGAN:
            kept_7 += 1
            if keep == COMBO:
                combo_7 += 1

        # 6 cards
        if keep == MULLIGAN:
            hand = draw_hand(deck, 6)
            keep = is_hand_keepable(hand)
            if keep != MULLIGAN:
                kept_6 += 1
                if keep == COMBO:
                    combo_6 += 1

        # 5 cards
        if keep == MULLIGAN:
            hand = draw_hand(deck, 5)
            keep = is_hand_keepable(hand)
            if keep != MULLIGAN:
                kept_5 += 1
                if keep == COMBO:
                    combo_5 += 1

        # 4 cards
        if keep == MULLIGAN:
            hand = draw_hand(deck, 4)

        # Simulate turn 3
        draw_more_cards(deck, hand, 2)
        turn_3_lands += count_lands(hand)
        red_sources = count_red_sources(hand)
        turn_3_red_sources += red_sources
        if red_sources >= 3:
            hit_turn_3 += 1

        # Simulate turn 4
        draw_more_cards(deck, hand, 1)
        turn_4_lands += count_lands(hand)
        blue_sources = count_blue_sources(hand)
        turn_4_blue_sources += blue_sources
        if blue_sources >= 2:
            hit_turn_4 += 1

    tot_kept = kept_7 + kept_6 + kept_5
    tot_kept_6 = kept_7 + kept_6
    mull_to_4 = n - tot_kept

    tot_combo = combo_7 + combo_6 + combo_5
    no_combo = n - tot_combo

    avg_lands_turn_3 = turn_3_lands / n
    avg_lands_turn_4 = turn_4_lands / n
    avg_red_sources_turn_3 = turn_3_red_sources / n
    avg_blue_sources_turn_4 = turn_4_blue_sources / n

    end = time.time()
    seconds = end - start
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    digits = get_n_of_digits(n)

    print('Simulation complete, time elapsed: {}\'{}\'\'\n'.format(minutes, seconds))
    print('Kept 7:     {1:{0}} / {2} = {3:.2f}%'.format(digits, kept_7, n, kept_7 / n * 100))
    print('Kept 6:     {1:{0}} / {2} = {3:.2f}%'.format(digits, kept_6, n, kept_6 / n * 100))
    print('Kept 5:     {1:{0}} / {2} = {3:.2f}%'.format(digits, kept_5, n, kept_5 / n * 100))
    print('Mull to 4:  {1:{0}} / {2} = {3:.2f}%'.format(digits, mull_to_4, n, mull_to_4 / n * 100))
    print('')
    print('Combo in 7: {1:{0}} / {2} = {3:.2f}%'.format(digits, combo_7, n, combo_7 / n * 100))
    print('Combo in 6: {1:{0}} / {2} = {3:.2f}%'.format(digits, combo_6, n, combo_6 / n * 100))
    print('Combo in 5: {1:{0}} / {2} = {3:.2f}%'.format(digits, combo_5, n, combo_5 / n * 100))
    print('No combo:   {1:{0}} / {2} = {3:.2f}%'.format(digits, no_combo, n, no_combo / n * 100))
    print('')
    print('Average lands by turn 3:        {:.2f}'.format(avg_lands_turn_3))
    print('Average lands by turn 4:        {:.2f}'.format(avg_lands_turn_4))
    print('Average red sources by turn 3:  {:.2f}'.format(avg_red_sources_turn_3))
    print('Average blue sources by turn 4: {:.2f}'.format(avg_blue_sources_turn_4))
    print('')
    print('Total strong hands (6 or 7):     {1:{0}} / {2} = {3:.2f}%'.format(digits, tot_kept_6, n, tot_kept_6 / n * 100))
    print('Total kept hands (5 or more):    {1:{0}} / {2} = {3:.2f}%'.format(digits, tot_kept, n, tot_kept / n * 100))
    print('Total starting combos:           {1:{0}} / {2} = {3:.2f}%'.format(digits, tot_combo, n, tot_combo / n * 100))
    print('Total hands with RRR+ by turn 3: {1:{0}} / {2} = {3:.2f}%'.format(digits, hit_turn_3, n, hit_turn_3 / n * 100))
    print('Total hands with UU+ by turn 4:  {1:{0}} / {2} = {3:.2f}%'.format(digits, hit_turn_4, n, hit_turn_4 / n * 100))


def get_n_of_digits(n):
    digits = 1
    while n / 10 > 1:
        n /= 10
        digits += 1
    return digits


if __name__ == '__main__':
    try:
        n = sys.argv[1]
    except IndexError:
        print('Usage: ./main.py N')
        sys.exit()

    try:
        n = int(n)
    except ValueError:
        print('Usage: ./main.py N')

    test_kept(n)
    # test_lands(n)
