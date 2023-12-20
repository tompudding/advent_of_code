import sys
import enum
from collections import Counter


class HandType(enum.Enum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


class Hand:
    size = 5
    order = "AKQJT98765432"

    def __init__(self, hand, bid):
        assert len(hand) == self.size

        self.hand_type = self.get_hand_type(hand)
        self.hand = hand
        self.hand_rank = [self.order.index(card) for card in hand]
        self.bid = int(bid)

    def get_hand_type(self, hand):
        counts = sorted(Counter(hand).values(), reverse=True)

        if counts[0] >= 4:
            return {5: HandType.FIVE_OF_A_KIND, 4: HandType.FOUR_OF_A_KIND}[counts[0]]
        elif counts[0] == 3:
            return {2: HandType.FULL_HOUSE, 1: HandType.THREE_OF_A_KIND}[counts[1]]
        elif counts[0] == 2:
            return {2: HandType.TWO_PAIR, 1: HandType.ONE_PAIR}[counts[1]]
        else:
            return HandType.HIGH_CARD

    def __lt__(self, other):
        if self.hand_type.value < other.hand_type.value:
            return True

        if self.hand_type.value > other.hand_type.value:
            return False

        for i in range(Hand.size):
            if self.hand_rank[i] < other.hand_rank[i]:
                return True
            if self.hand_rank[i] > other.hand_rank[i]:
                return False
        return False


class HandNewRules(Hand):
    order = "AKQT98765432J"

    def get_hand_type(self, hand):
        non_jokers = [card for card in hand if card != "J"]
        if not non_jokers:
            return HandType.FIVE_OF_A_KIND

        counter = Counter(non_jokers)
        counts = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        new_hand = hand.replace("J", counts[0][0])
        return super().get_hand_type(new_hand)


def get_winnings(hands):
    # Apparently rank 1 means weakest wtf
    hands.sort(reverse=True)

    return sum(((rank + 1) * hand.bid for (rank, hand) in enumerate(hands)))


with open(sys.argv[1], "r") as file:
    hands = [Hand(*line.strip().split()) for line in file]

print(get_winnings(hands))


# For part 2 we parse again

hands = [HandNewRules(hand.hand, hand.bid) for hand in hands]

print(get_winnings(hands))
