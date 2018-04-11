#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

import sys


# returns the probability of drawing n cards off a treasure hunt with a deck of l lands and s spells
def t(n, lands, spells):
    ret = spells / (lands + spells - n + 1)
    for i in range(n-1):
        ret *= (lands - i) / (lands + spells - i)
    return ret


# prints a chart of the EV of t() for all possible values of n for all l up to MAX_LANDS and all s up to MAX_SPELLS
def print_chart(min_lands, max_lands, min_spells, max_spells, to_file=False):

    # Open file
    if to_file:
        try:
            f = open('chart.txt', 'w')
        except:
            print('Couldn\'t open output file.')
            sys.exit()

    # Print the top index (lands)
    string = '     '
    if to_file:
        f.write(string)
    else:
        print(string, end='')

    for l in range(min_lands, max_lands + 1):
        string = '|  {:2}  '.format(l)
        if to_file:
            f.write(string)
        else:
            print(string, end='')
    if to_file:
        f.write('\n')
    else:
        print('')

    # Main loops
    for s in range(min_spells, max_spells + 1):

        # Print dashes
        if s != max_spells + 1:
            dashes = '-' * (6 * (max_lands - min_lands + 1)+ (max_lands - min_lands) + 5)
            if to_file:
                f.write(dashes + '\n')
            else:
                print(dashes)

        string = ' {:2} '.format(s)
        if to_file:
            f.write(string)
        else:
            print(string, end='')

        for l in range(min_lands, max_lands + 1):

            # Skip configurations with more than 60 cards
            if l + s > 60:
                continue

            # Print divider
            if l != max_lands + 1:
                string = ' |'
                if to_file:
                    f.write(string)
                else:
                    print(string, end='')

            # Calculate EV and print it
            ev = 0
            for n in range(1, l + s + 1):
                prob = t(n, l, s)
                ev += n * prob
            string = '{0:5.2f}'.format(ev)
            if to_file:
                f.write(string)
            else:
                print(string, end='')

        if to_file:
            f.write('\n')
        else:
            print('')


if __name__ == '__main__':
    min_lands = 1
    max_lands = 59
    min_spells = 1
    max_spells = 59
    print_chart(min_lands, max_lands, min_spells, max_spells, True)