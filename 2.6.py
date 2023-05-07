from graphics import *
from button import Button
import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank}{self.suit}'

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

class Deck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['♣', '♦', '♥', '♠']

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class PokerHand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_best_hand(self):
        # Simplified hand evaluation
        hand_ranks = [card.get_rank() for card in self.cards]
        hand_suits = [card.get_suit() for card in self.cards]
        distinct_ranks = set(hand_ranks)
        distinct_suits = set(hand_suits)

        # Check for flush
        flush = len(distinct_suits) == 1

        # Check for straight
        sorted_ranks = sorted(list(distinct_ranks), key=lambda x: Deck.ranks.index(x))
        straight = all(Deck.ranks.index(sorted_ranks[i]) == Deck.ranks.index(sorted_ranks[i-1]) + 1 for i in range(1, len(sorted_ranks)))

        # Count the occurrences of each rank
        rank_counts = {rank: hand_ranks.count(rank) for rank in distinct_ranks}

        # Determine the best hand
        if straight and flush:
            return "Straight Flush", max(sorted_ranks, key=lambda x: Deck.ranks.index(x))
        elif 4 in rank_counts.values():
            return "Four of a Kind", [rank for rank, count in rank_counts.items() if count == 4][0]
        elif sorted(rank_counts.values()) == [2, 3]:
            return "Full House", [rank for rank, count in rank_counts.items() if count == 3][0]
        elif flush:
            return "Flush", max(sorted_ranks, key=lambda x: Deck.ranks.index(x))
        elif straight:
            return "Straight", max(sorted_ranks, key=lambda x: Deck.ranks.index(x))
        elif 3 in rank_counts.values():
            return "Three of a Kind", [rank for rank, count in rank_counts.items() if count == 3][0]
        elif len([count for count in rank_counts.values() if count == 2]) == 2:
            return "Two Pair", max([rank for rank, count in rank_counts.items() if count == 2], key=lambda x: Deck.ranks.index(x))
        elif 2 in rank_counts.values():
            return "One Pair", [rank for rank, count in rank_counts.items() if count == 2][0]
        else:
            return "High Card", max(sorted_ranks, key=lambda x: Deck.ranks.index(x))
class PSGame:
    def __init__(self, win):
        self.win = win
        self.deck = Deck()
        self.player_hand = PokerHand()
        self.dealer_hand = PokerHand()
        self.create_game_board()

    def create_game_board(self):
        self.card_images = []
        for i in range(9):
            self.card_images.append(Image(Point(100 + i * 50, 100), "back.gif"))
            self.card_images[-1].draw(self.win)

        self.results = Text(Point(300, 200), "")
        self.results.setSize(14)
        self.results.draw(self.win)

        self.controls = {}
        self.controls['deal'] = Button(self.win, Point(100, 50), 80, 40, "Deal")
        self.controls['quit'] = Button(self.win, Point(200, 50), 80, 40, "Quit")
        self.controls['stay'] = Button(self.win, Point(400, 50), 80, 40, "Stay")
        self.controls['fold'] = Button(self.win, Point(500, 50), 80, 40, "Fold")

        for btn in self.controls.values():
            btn.activate()

    def play(self):
        while True:
            click = self.win.getMouse()
            for btn_name, btn in self.controls.items():
                if btn.clicked(click):
                    if btn_name == 'deal':
                        self.deal()
                    elif btn_name == 'quit':
                        self.win.close()
                        return
                    elif btn_name == 'stay':
                        self.stay()
                    elif btn_name == 'fold':
                        self.fold()

    def deal(self):
        self.deck = Deck()
        self.player_hand = PokerHand()
        self.dealer_hand = PokerHand()

        for i in range(2):
            self.player_hand.add_card(self.deck.deal_card())
            self.dealer_hand.add_card(self.deck.deal_card())

        for i in range(5):
            self.community_cards = [self.deck.deal_card() for _ in range(5)]

        for i in range(2):
            self.card_images[i].undraw()
            self.card_images[i].setImage(self.player_hand.cards[i].get_rank() + self.player_hand.cards[i].get_suit() + ".gif")
            self.card_images[i].draw(self.win)

        self.controls['deal'].deactivate()
        self.controls['quit'].deactivate()
        self.controls['stay'].activate()
        self.controls['fold'].activate()

    def stay(self):
        revealed_cards = sum([card.getImage() != "back.gif" for card in self.card_images[2:7]])
        if revealed_cards == 0:
            for i in range(2, 5):
                self.card_images[i].undraw()
                self.card_images[i].setImage(
                    self.community_cards[i - 2].get_rank() + self.community_cards[i - 2].get_suit() + ".gif")
                self.card_images[i].draw(self.win)
        elif revealed_cards == 3:
            self.card_images[5].undraw()
            self.card_images[5].setImage(
                self.community_cards[3].get_rank() + self.community_cards[3].get_suit() + ".gif")
            self.card_images[5].draw(self.win)
        elif revealed_cards == 4:
            self.card_images[6].undraw()
            self.card_images[6].setImage(
                self.community_cards[4].get_rank() + self.community_cards[4].get_suit() + ".gif")
            self.card_images[6].draw(self.win)
            self.reveal_dealer_cards()
            self.determine_winner()
            self.update_results("stay")
            self.reset_game()

    def fold(self):
        self.reveal_dealer_cards()
        self.reveal_remaining_community_cards()
        self.determine_winner()
        self.update_results("fold")
        self.reset_game()

    def reveal_dealer_cards(self):
        for i in range(2):
            self.card_images[i + 7].undraw()
            self.card_images[i + 7].setImage(
                self.dealer_hand.cards[i].get_rank() + self.dealer_hand.cards[i].get_suit() + ".gif")
            self.card_images[i + 7].draw(self.win)

    def reveal_remaining_community_cards(self):
        for i, card in enumerate(self.card_images[2:7]):
            if card.getImage() == "back.gif":
                card.undraw()
                card.setImage(self.community_cards[i].get_rank() + self.community_cards[i].get_suit() + ".gif")
                card.draw(self.win)

    def determine_winner(self):
        player_best_hand = self.player_hand.get_best_hand(self.community_cards)
        dealer_best_hand = self.dealer_hand.get_best_hand(self.community_cards)
        if player_best_hand[0] == dealer_best_hand[0]:
            if player_best_hand[0] == "One Pair":
                if Deck.ranks.index(player_best_hand[1]) > Deck.ranks.index(dealer_best_hand[1]):
                    self.winner = "Player"
                else:
                    self.winner = "Dealer"
            elif player_best_hand[0] == "High Card":
                if Deck.ranks.index(player_best_hand[1]) > Deck.ranks.index(dealer_best_hand[1]):
                    self.winner = "Player"
                else:
                    self.winner = "Dealer"
            else:
                self.winner = "Draw"
        else:
            if PokerHand.categories.index(player_best_hand[0]) < PokerHand.categories.index(dealer_best_hand[0]):
                self.winner = "Player"
            else:
                self.winner = "Dealer"

    def update_results(self, action):
        if action == "stay":
            if self.winner == "Player":
                self.points = 100
            else:
                self.points = -100
        elif action == "fold":
            if self.winner == "Player":
                self.points = -25 * (5 - sum([card.getImage() != "back.gif" for card in self.card_images[2:7]]))
        else:
            self.points = 25 * (5 - sum([card.getImage() != "back.gif" for card in self.card_images[2:7]]))
        self.total_points += self.points
        self.games_played += 1
        self.average_points = self.total_points / self.games_played
        self.results.setText("Average points: {:.1f}\nGames played: {}\n\n".format(self.average_points, self.games_played))

    def reset_game(self):
        self.dealer_hand = PokerHand()
        self.player_hand = PokerHand()
        self.community_cards = []

        for card in self.card_images:
            card.undraw()

        self.deck.shuffle()
        self.deal_hole_cards()
        self.deal_community_cards()
        self.display_cards()
        self.set_controls("start")


def main():
    win = GraphWin("Poker Solitaire", 800, 600)
    win.setCoords(0, 0, 8, 6)

    game = PSGame(win)
    game.deal_hole_cards()
    game.deal_community_cards()
    game.display_cards()

    # Main game loop
    while True:
        click_point = win.getMouse()
        if game.quit_button.clicked(click_point):
            break
        elif game.stay_button.clicked(click_point) and game.stay_button.isActive():
            game.stay()
        elif game.fold_button.clicked(click_point) and game.fold_button.isActive():
            game.fold()
        elif game.deal_button.clicked(click_point) and game.deal_button.isActive():
            game.reset_game()

    win.close()


if __name__ == "__main__":
    main()
