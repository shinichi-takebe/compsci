import random
from graphics import *
from button import Button


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit
class Deck:
    ranks = "23456789TJQKA"
    suits = "♣♦♥♠"

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

    def get_cards(self):
        return self.cards

    def _get_ranks(self):
        ranks = [card.get_rank() for card in self.cards]
        return ranks

    def _get_suits(self):
        suits = [card.get_suit() for card in self.cards]
        return suits

    def _count_ranks(self):
        count = {rank: 0 for rank in Deck.ranks}
        for rank in self._get_ranks():
            count[rank] += 1
        return count

    def _count_suits(self):
        count = {suit: 0 for suit in Deck.suits}
        for suit in self._get_suits():
            count[suit] += 1
        return count

    def _has_flush(self):
        return any(count >= 5 for count in self._count_suits().values())

    def _has_straight(self):
        ranks = self._get_ranks()
        ranks.sort(key=lambda x: Deck.ranks.index(x))

        for i in range(len(ranks) - 4):
            if Deck.ranks.index(ranks[i + 4]) - Deck.ranks.index(ranks[i]) == 4:
                return True

        if 'A' in ranks and '2' in ranks and '3' in ranks and '4' in ranks and '5' in ranks:
            return True

        return False

    def _has_straight_flush(self):
        for suit in Deck.suits:
            suited_cards = [card for card in self.cards if card.get_suit() == suit]
            if len(suited_cards) < 5:
                continue

            suited_hand = PokerHand()
            for card in suited_cards:
                suited_hand.add_card(card)

            if suited_hand._has_straight():
                return True

        return False

    def _highest_category(self):
        if self._has_straight_flush():
            return "Straight flush"
        if 4 in self._count_ranks().values():
            return "Four of a kind"
        if sorted(self._count_ranks().values(), reverse=True)[:2] == [3, 2]:
            return "Full house"
        if self._has_flush():
            return "Flush"
        if self._has_straight():
            return "Straight"
        if 3 in self._count_ranks().values():
            return "Three of a kind"
        if list(self._count_ranks().values()).count(2) == 2:
            return "Two pair"
        if 2 in self._count_ranks().values():
            return "One pair"
        return "High card"

    def get_highest_rank(self):
        if self._highest_category() == "One pair":
            return next(rank for rank, count in self._count_ranks().items() if count == 2)
        elif self._highest_category() == "High card":
            return max(self._get_ranks(), key=lambda x: Deck.ranks.index(x))
        else:
            return None

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


class PSGame:
    def __init__(self, win):
        self.win = win
        self.deck = Deck()
        self.player_hand = PokerHand()
        self.dealer_hand = PokerHand()
        self.community_cards = PokerHand()
        self.stage = 0
        self.score = 0
        self.num_games = 0

        self.status_text = Text(Point(100, 20), "Stage: Pre-Flop")
        self.status_text.setSize(12)
        self.status_text.draw(self.win)

        self.score_text = Text(Point(100, 40), f"Score: {self.score}")
        self.score_text.setSize(12)
        self.score_text.draw(self.win)

        self.average_score_text = Text(Point(100, 60), f"Average Score: {self.score / max(self.num_games, 1):.2f}")
        self.average_score_text.setSize(12)
        self.average_score_text.draw(self.win)

        self.player_cards = [None, None]
        self.dealer_cards = [None, None]
        self.flop_cards = [None, None, None]
        self.turn_card = None
        self.river_card = None

        self.stay_button = Button(self.win, Point(200, 30), 60, 20, "Stay")
        self.fold_button = Button(self.win, Point(300, 30), 60, 20, "Fold")
        self.next_game_button = Button(self.win, Point(400, 30), 100, 20, "Next Game")
        self.next_game_button.deactivate()

    def deal_hole_cards(self):
        self.deck.shuffle()
        self.player_hand = PokerHand()
        self.dealer_hand = PokerHand()

        for i in range(2):
            card = self.deck.deal_card()
            self.player_hand.add_card(card)
            self.player_cards[i] = self.create_card_graphic(card, Point(50 + i * 50, 100))
            self.player_cards[i].draw(self.win)

            card = self.deck.deal_card()
            self.dealer_hand.add_card(card)
            self.dealer_cards[i] = self.create_card_graphic(card, Point(50 + i * 50, 200), face_up=False)
            self.dealer_cards[i].draw(self.win)
    def deal_flop(self):
        self.community_cards = PokerHand()
        for i in range(3):
            card = self.deck.deal_card()
            self.community_cards.add_card(card)
            self.flop_cards[i] = self.create_card_graphic(card, Point(150 + i * 50, 150))
            self.flop_cards[i].draw(self.win)

    def deal_turn(self):
        card = self.deck.deal_card()
        self.community_cards.add_card(card)
        self.turn_card = self.create_card_graphic(card, Point(300, 150))
        self.turn_card.draw(self.win)

    def deal_river(self):
        card = self.deck.deal_card()
        self.community_cards.add_card(card)
        self.river_card = self.create_card_graphic(card, Point(350, 150))
        self.river_card.draw(self.win)

    def create_card_graphic(self, card, position, face_up=True):
        return Card(card.get_rank(), card.get_suit(), self.win, position, face_up)

    def play(self):
        self.deal_hole_cards()

        while True:
            if self.stage == 0:
                clicked = self.get_clicked_button()
                if clicked == "Stay":
                    self.stage = 1
                    self.status_text.setText("Stage: Flop")
                    self.deal_flop()
                elif clicked == "Fold":
                    self.fold()
            elif self.stage == 1:
                clicked = self.get_clicked_button()
                if clicked == "Stay":
                    self.stage = 2
                    self.status_text.setText("Stage: Turn")
                    self.deal_turn()
                elif clicked == "Fold":
                    self.fold()
            elif self.stage == 2:
                clicked = self.get_clicked_button()
                if clicked == "Stay":
                    self.stage = 3
                    self.status_text.setText("Stage: River")
                    self.deal_river()
                elif clicked == "Fold":
                    self.fold()
            elif self.stage == 3:
                clicked = self.get_clicked_button()
                if clicked == "Stay":
                    self.showdown()
                elif clicked == "Fold":
                    self.fold()
            else:
                clicked = self.get_clicked_button()
                if clicked == "Next Game":
                    self.reset_game()
    def get_clicked_button(self):
        while True:
            click = self.win.getMouse()
            if self.stay_button.clicked(click):
                return "Stay"
            elif self.fold_button.clicked(click):
                return "Fold"
            elif self.next_game_button.clicked(click):
                return "Next Game"

    def fold(self):
        would_have_won = self.get_winner() == "Player"
        if self.stage == 0:
            points = 100 if not would_have_won else -100
        elif self.stage == 1:
            points = 75 if not would_have_won else -75
        elif self.stage == 2:
            points = 50 if not would_have_won else -50
        elif self.stage == 3:
            points = 25 if not would_have_won else -25

        self.update_score(points)
        self.reveal_dealer_hole_cards()
        self.finish_game()

    def showdown(self):
        winner = self.get_winner()
        points = 100 if winner == "Player" else -100
        self.update_score(points)
        self.reveal_dealer_hole_cards()
        self.finish_game()

    def get_winner(self):
        player_final_hand = self.player_hand.combine(self.community_cards)
        dealer_final_hand = self.dealer_hand.combine(self.community_cards)

        if player_final_hand > dealer_final_hand:
            return "Player"
        elif player_final_hand < dealer_final_hand:
            return "Dealer"
        else:
            return "Tie"

    def reveal_dealer_hole_cards(self):
        for card_graphic in self.dealer_cards:
            card_graphic.set_face_up(True)
            card_graphic.undraw()
            card_graphic.draw(self.win)

    def finish_game(self):
        self.stay_button.deactivate()
        self.fold_button.deactivate()
        self.next_game_button.activate()

    def reset_game(self):
        self.stage = 0
        self.status_text.setText("Stage: Pre-Flop")
        self.stay_button.activate()
        self.fold_button.activate()
        self.next_game_button.deactivate()

        for card_graphic in self.player_cards + self.dealer_cards + self.flop_cards + [self.turn_card, self.river_card]:
            card_graphic.undraw()

        self.deal_hole_cards()

    def update_score(self, points):
        self.score += points
        self.num_games += 1
        self.score_text.setText(f"Score: {self.score}")
        self.average_score_text.setText(f"Average Score: {self.score / self.num_games:.2f}")
def main():
    win = GraphWin("Poker Solitaire", 600, 400)
    win.setCoords(0, 0, 600, 400)
    game = PSGame(win)
    game.play()
    win.getMouse()
    win.close()

if __name__ == '__main__':
    main()
