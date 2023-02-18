from blackjack import *

def generate_data(nb:int):
    """Problemes a resoudre :
    -le bot doit avoir tous les jeux dans la partie
    -le bot doit avoir une main avec juste des int
    """
    dataX=[]
    dataY=[]
    for i in range(nb):
        deck = make_deck(1)
        deck.shuffle(100)
        
        bot0= Player(Hand(0, []), 0)
        bot1= Player(Hand(0, []), 1)

        game = Game([bot0,bot1], deck)
        while len([player for player in [bot0,bot1] if (not player.stopped and not player.is_out)]) > 1:
            for player in [bot0,bot1]:
                if not player.stopped and not player.is_out:
                    player.rand_play(game)
                    player.check()
        if len(player for player in [bot0,bot1] if not player.is_out)>0:
            winners = [player for player in [bot0,bot1] if not player.is_out]
            dataX.append(winner.id for winner in winners)
            dataY.append(winner.hand for winner in winners)
        else:
            dataX.append(None)
            dataY.append([])
            
    return dataX, dataY

liste1,liste2 = generate_data(5)
print(liste1)
print(liste2)

