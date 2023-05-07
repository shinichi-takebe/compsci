from graphics import *
from button import Button
from random import *

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        ranks = "23456789TJQKA"
        suits = "♣♦♥♠"
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class PokerHand:
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        return " ".join(map(str, self.cards))

    def get_category(self):
        ranks = sorted([card.rank for card in self.cards])
        suits = [card.suit for card in self.cards]

        flush = len(set(suits)) == 1
        straight = (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5

        if flush and straight:
            return "Straight flush"
        elif ranks.count(ranks[0]) == 4 or ranks.count(ranks[1]) == 4:
            return "Four of a kind"
        elif ranks.count(ranks[0]) == 3 and ranks.count(ranks[1]) == 2:
            return "Full house"
        elif flush:
            return "Flush"
        elif straight:
            return "Straight"
        elif ranks.count(ranks[0]) == 3 or ranks.count(ranks[1]) == 3 or ranks.count(ranks[2]) == 3:
            return "Three of a kind"
        elif ranks.count(ranks[0]) == 2 and ranks.count(ranks[1]) == 2:
            return "Two pair"
        elif ranks.count(ranks[0]) == 2 or ranks.count(ranks[1]) == 2 or ranks.count(ranks[2]) == 2:
            return "One pair"
        else:
            return "High card"

    def get_pair_rank(self):
        ranks = sorted([card.rank for card in self.cards], reverse=True)
        for rank in ranks:
            if ranks.count(rank) == 2:
                return rank

    def get_highest_rank(self):
        return max([card.rank for card in self.cards])

class PSGame:
    def __init__(self, win):
        self.win = win
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.betting_round = 1
        self.score = 0
        self.create_widgets()

    def create_widgets(self):
        self.title = Text(Point(200, 20), "Poker Solitaire")
        self.title.setSize(20)
        self.title.draw(self.win)

        self.player_hand_label = Text(Point(100, 100), "Player hand:")
        self.player_hand_label.draw(self.win)

        self.player_hand_cards = []
        for i in range(2):
            card = self.deck.deal()
            self.player_hand.append(card)
            card_label = Text(Point(150 + i*50, 100), str(card))
            card_label.draw(self.win)
            self.player_hand_cards.append(card_label)

        self.dealer_hand_label = Text(Point(100, 200), "Dealer hand:")
        self.dealer_hand_label.draw(self.win)

        self.dealer_hand_cards = []
        for i in range(2):
            card_label = Text(Point(150 + i * 50, 200), "??")
            card_label.draw(self.win)
            self.dealer_hand_cards.append(card_label)

        self.bet_button = Button(self.win, Point(100, 300), 80, 40, "Stay", self.bet)
        self.fold_button = Button(self.win, Point(300, 300), 80, 40, "Fold", self.fold)
        self.bet_button.activate()
        self.fold_button.activate()

    def bet(self):
        self.betting_round += 1

        if self.betting_round == 2:
            for i in range(3):
                card = self.deck.deal()
                self.player_hand.append(card)
                card_label = Text(Point(150 + i * 50, 100), str(card))
                card_label.draw(self.win)
                self.player_hand_cards.append(card_label)

        elif self.betting_round == 3:
            card = self.deck.deal()
            self.player_hand.append(card)
            card_label = Text(Point(150 + 3 * 50, 100), str(card))
            card_label.draw(self.win)
            self.player_hand_cards.append(card_label)

        elif self.betting_round == 4:
            card = self.deck.deal()
            self.player_hand.append(card)
            card_label = Text(Point(150 + 4 * 50, 100), str(card))
            card_label.draw(self.win)
            self.player_hand_cards.append(card_label)

            for i in range(2):
                card = self.deck.deal()
                self.dealer_hand.append(card)
                self.dealer_hand_cards[i].setText(str(card))

            self.bet_button.deactivate()
            self.fold_button.deactivate()
            self.end_game()

    def fold(self):
        self.bet_button.deactivate()
        self.fold_button.deactivate()

        if self.betting_round == 1:
            self.dealer_hand.extend([self.deck.deal() for i in range(5)])
        elif self.betting_round == 2:
            self.dealer_hand.extend([self.deck.deal() for i in range(2)])
        elif self.betting_round == 3:
            self.dealer_hand.extend([self.deck.deal()])

        self.end_game()

    def end_game(self):
        player_poker_hand = PokerHand(self.player_hand + self.dealer_hand)
        dealer_poker_hand = PokerHand(self.dealer_hand)

        player_category = player_poker_hand.get_category()
        dealer_category = dealer_poker_hand.get_category()

        if player_category == dealer_category:
            if player_category == "One pair":
                player_pair_rank = player_poker_hand.get_pair_rank()
                dealer_pair_rank = dealer_poker_hand.get_pair_rank()
                if player_pair_rank > dealer_pair_rank:
                    self.score += 100
                elif player_pair_rank == dealer_pair_rank:
                    pass
                else:
                    self.score -= 100
            elif player_category == "High card":
                player_highest_rank = player_poker_hand.get_highest_rank()
                dealer_highest_rank = dealer_poker_hand.get_highest_rank()
                if player_highest_rank > dealer_highest_rank:
                    self.score += 100
                elif player_highest_rank == dealer_highest_rank:
                    pass
                else:
                    self.score -= 100
            else:
                pass
        elif player_category > dealer_category:
            self.score += 100
        else:
            self.score -= 100

        score_text = Text(Point(200, 350), f"Average score: {self.score}")
        score_text.draw(self.win)
        self.deck = Deck()
        self.player_hand = []
        self.player_hand_cards = []
        self.dealer_hand = []
        self.dealer_hand_cards = []
        self.betting_round = 1
        self.bet_button.activate()
        self.fold_button.activate()

        for card_label in self.player_hand_cards + self.dealer_hand_cards:
            card_label.undraw()

        self.play()

    def play(self):
        self.win.getMouse()
        self.bet()

    def run(self):
        self.play()

if __name__ == "__main__":
    win = GraphWin("Poker Solitaire", 400, 400)
    game = PSGame(win)
    game.run()


