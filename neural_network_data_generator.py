from blackjack import *


# total,croupier_value,should_take


def generate_game(players: list):
    """ doit generer des bouts de partie et dire si il doit piocher ou non
    ATTENTION LE CROUPIER EST LE PREMIER DE LA LISTE

    """

    data = []

    deck = make_deck(1)
    deck.shuffle(100)
    game = Game(players, deck)
    while len([player for player in players if (not player.stopped and not player.is_out)]) > 1:
        for player in players:
            if player.is_croupier:
                data.append([player.hand.get_value(), player.hand.get_value()])
                player.play(game)
                if player.is_out:
                    data[-1].append(0)
                else:
                    data[-1].append(1)
            else:
                data.append([player.hand.get_value(),
                            players[0].hand.get_value()])
                player.rand_play(game)
                if player.is_out:
                    data[-1].append(0)
                else:
                    data[-1].append(1)
    return data


croupier = Croupier(Hand(0, []), 0)
hector = Player(Hand(0, []), 1)
gabriel = Player(Hand(0, []), 2)

players = [croupier, hector, gabriel]


def write_data(file, data):
    with open(file, 'a') as f:
        for liste in data:
            f.write(f"{liste[0]},{liste[1]},{liste[2]}\n")


write_data('./blackjack.csv', generate_game(players))
