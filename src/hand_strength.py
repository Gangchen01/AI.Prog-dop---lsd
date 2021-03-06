import cards
import itertools
import pre_flop_tester

# Regner ut hand strength for et gitt par med hullkort,
# et gitt antall motstandere, og en gitt bunke med delte kort
def calculateHandStrength(hand, numberOfOpponents, tableCards):
    table = tableCards[:]
    numberOfWins = 0
    numberOfTies = 0
    numberOfLosses = 0
    remainingCards = cards.gen_52_cards()
    for c in hand:
        remainingCards.remove(c)
    for c in tableCards:
        remainingCards.remove(c)
    remainingHoleCombinations = list(itertools.combinations(remainingCards, 2)) # Her lages alle mulige par med hullkort motstanderne kan ha
    for comb in remainingHoleCombinations:
        playerHand = hand[:]
        combination = list(comb)
        for card in tableCards:
            playerHand.append(card)
            combination.append(card)
        outcome = calculateOutcome(playerHand, combination)
        if outcome == 1:
            numberOfWins += 1
        elif outcome == 0:
            numberOfTies += 1
        else:
            numberOfLosses += 1
    # Base strength = (#Wins + 0.5#Ties) / (#Wins + #Ties #Losses)
    base_strength = float(float(float(numberOfWins) + float(float(numberOfTies)/float(2))) / float(float(numberOfWins + float(numberOfTies) + float(numberOfLosses))))
    # Hand strength = base_strength opphoyd i antall spillere
    hand_strength = float(1)
    for i in range(numberOfOpponents):
        hand_strength = hand_strength * base_strength
    return hand_strength


# Her regnes det ut hvem som har best hand av player og opponent
def calculateOutcome(player, opponent):
    playerPower = cards.calc_cards_power(player)
    opponentPower = cards.calc_cards_power(opponent)
    for i in range(len(playerPower)):
        if playerPower[i] > opponentPower[i]:
            return 1
        elif playerPower[i] < opponentPower[i]:
            return -1
        elif i == len(playerPower):
            return 0

def getPreFlopTable():
    #format: H?yeste kort -2, Laveste kort -2, 0:unsuited 1:suited, spillere -2
    pre_flop_table = pre_flop_tester.makePreFlopTable()
    f = open('pre_flop_table_final.txt', 'r')
    for i in range(18):
        players = int(f.readline())
        suited = str(f.readline().strip())
        probabilities = []
        for foo in range(13):
            probabilities.append([float(x) for x in f.readline().split()])
        for j in range(13):
            for k in range(len(probabilities[j])):
                if suited == "unsuited":
                    pre_flop_table[j][k][0][players] = probabilities[j][k]
                else:
                    pre_flop_table[j][k][1][players] = probabilities[j][k]
    return pre_flop_table


