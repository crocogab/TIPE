SCORE_LIMIT = 21
BANK_LIMIT= 16
CARDS_LOWER_BOUND = 10
cards_values = [i for i in range(1,CARDS_LOWER_BOUND+1)]

class Game_graph():
    def __init__(self,value=0,children=None,player=0,croupier=0,player_stopped=False):
        self.val = value
        self.children = children or []
        self.player = player
        self.player_stopped = player_stopped
        self.croupier = croupier
    

def create_game_graph():
    base = Game_graph(0,[],0,0)
    for card in cards_values:
        base.children.append(Game_graph(card,[],card,0))
    for child in base.children:
        for card in cards_values:
            # le croupier tire mais et le joueur s'arrête
            child.children.append(Game_graph(card,[],child.player,card,True))
            create_arb_when_player_stopped(child.children[-1],card)
            # le croupier tire et le joueur tire
            child.children.append(Game_graph(card,[],child.player,card,False))
            create_arb_when_player_not_stopped(child.children[-1],card)
    return base

def create_arb_when_player_stopped(base,crouptotal):
    while crouptotal <=BANK_LIMIT:
        for card in cards_values:
            crouptotal += card
            base.children.append(Game_graph(card,[],base.player,crouptotal,True))
            create_arb_when_player_stopped(base.children[-1],crouptotal)
    return base

def create_arb_when_player_not_stopped(base,player_total):
    while player_total <=SCORE_LIMIT:
        for card in cards_values:
            player_total += card
            base.children.append(Game_graph(card,[],player_total,base.croupier,False))
            create_arb_when_player_not_stopped(base.children[-1],player_total)
            base.children.append(Game_graph(card,[],player_total,base.croupier,True))
            create_arb_when_player_stopped(base.children[-1],base.croupier)
    return base

graph = create_game_graph()
print("done")


# alpha beta