from blackjack import *


def generate_game(players: list):
    deck = make_deck(1)
    deck.shuffle(100)
    game = Game(players, deck)
    for _ in range(50) :
        for player in game.players:
            if not player.stopped and not player.is_out:
                if player.is_croupier:
                    player.play(game)
                    #player.check(game) 
                else:
                    player.rand_play(game)
                    # player.check(game)
    

    resultats=[] #dans l'ordre : id,is_croupier,total,is_out,is_winner
    
    croupier_is_out=True
    
    for player in players :
        if not player.is_out:
            if player.is_croupier :
                croupier_is_out=False
                croupier_hand_value=player.hand.get_value()
    
    if croupier_is_out:
        for player in players:
            if not player.is_out:
                resultats.append([player.id,0,player.hand.get_value(),0,2])
                
    else:
        for player in players :
            
            if not player.is_out and player.is_croupier:
                resultats.append([player.id,1,player.hand.get_value(),0,0])
            if not player.is_out and player.hand.get_value() > croupier_hand_value and not player.is_croupier:
                resultats.append([player.id,0,player.hand.get_value(),0,2])
            if not player.is_out and player.hand.get_value() == croupier_hand_value and not player.is_croupier:
                resultats.append([player.id,0,player.hand.get_value(),0,1])
    list_id=[elem[0] for elem in resultats]
    for player in players:
        if player.id not in list_id:
            if player.is_croupier:
                resultats.append([player.id,1,player.hand.get_value(),1,0])
            else:
                resultats.append([player.id,0,player.hand.get_value(),1,0])
    for data in resultats:
        data=data[1:]
        

    return resultats



hector = Player(Hand(0, []), 0)
gabriel = Player(Hand(0, []), 1)
croupier = Croupier(Hand(0, []), 2)
players = [hector, gabriel,croupier]

print(generate_game(players))

all_games=[]

for i in range(100):
    all_games.append(generate_game(players))

print(all_games)
        

            


    

