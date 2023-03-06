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
    while len([player for player in players if (not player.stopped and not player.is_out)]) >= 1:
        for player in players:
            if not player.is_out and not player.stopped:
                value = int(player.hand.get_value())
                # croupier_value=players[0].hand.get_value()
                if player.is_croupier:
                    player.play(game)
                    player.check(game)
                else:
                    player.rand_play(game)
                    player.check()

                if player.hand.get_value() > 21:
                    data.append([value, 0]) # " ".join(str(card.value) for card in player.hand.l_cards)

                else:
                    data.append([value, 1]) #" ".join(str(card.value) for card in player.hand.l_cards)])
                                

    return data


croupier = Croupier(Hand(0, []), 0)
hector = Player(Hand(0, []), 1)
gabriel = Player(Hand(0, []), 2)

players = [croupier, hector, gabriel]


def write_data(file, data):
    with open(file, 'a') as f:
        for liste in data:
            f.write(f"{liste[0]},{liste[1]}\n")


write_data('./blackjack.csv', generate_game(players))
