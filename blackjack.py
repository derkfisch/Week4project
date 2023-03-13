import random

#I used https://dev.to/nexttech/build-a-blackjack-command-line-game-3o4b
#and Tech with Tim: OOP for Beginners YT video to help me go through
#each line of code and understand this concept. This is my third attempt at this project :')


#in this class Card, the card belongs to a suit and worth a certain value.
class Card:
    #create an initalization with the args suit and value to pass throught the card
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        #we have to use a repr function to represent the cards by returning 
        #the value of the suit ('Queen' of 'Hearts')
        return f"{self.value} of {self.suit}"


#in this class Deck, the deck contains 52 cards and decreases when cards are drawn
#the deck must also be able to shuffle itself
class Deck:

    #need to pass over each cards suit/value combo through the initialization of class Card to make 52 different cards
    def __init__(self):
        self.cards = [Card(suits, values) for suits in ["Diamonds", "Clubs", "Spades", "Hearts"] 
                      for values in ["Ace", "2", "3", "4", "5", "6", 
                      "7", "8", "9", "10", "Jack", "Queen", "King"]]

    #need a shuffle function to shuffle the deck at the beginning of the game    
    def shuffle_cards(self):
        #this reads, if there are cards in the deck, shuffle them.
        if len(self.cards) > 0:
            #https://www.w3schools.com/python/ref_random_shuffle.asp
            random.shuffle(self.cards)

    #the next step is to deal the cards utilizing the .pop() method
    def deal_cards(self):
        #if there are cards in the deck,
        if len(self.cards) > 0:
            #return the top card and get it out of the deck
            return self.cards.pop(0)

#in this class Hand, each person dealt a hand which decides who wins from comparing the scores
#i have to also keep track if its the dealer's hand or the player's hand
#because the dealers hand has one card hidden to start
class Hand:
    
    #through this initialization, this allows us to tell when it is the players hand or dealers hand
    def __init__(self, dealer=False):
        self.dealer = dealer
        #each hand holds a lists of card instances
        self.cards = []
        self.value = 0

    #I have to add the card to our list of cards instances through an .append() method
    def add_card(self, card):
        self.cards.append(card)

    #I have to calculate the values of the cards to determine the winners/losers
    def calculate_the_value(self):
        #start at 0 for the value of the hand
        self.value = 0
        #in this first instance, Im under the assumption that an ace was NOT drawn
        has_ace = False
        #for every card in my hand of cards
        for card in self.cards:
            #if the value of the card is a number
            if card.value.isnumeric():
                #add that card value to the hand
                self.value += int(card.value)
            #if the card isnt a number card(ace, king, queen, jack)
            else:
                #and the card is an Ace
                if card.value == "Ace":
                    #I change the assumption to there IS an ace drawn
                    has_ace = True
                    #the value of that drawing is 11
                    self.value += 11
                else:
                    #if i got a king queen or jack, the value return is 10
                    self.value += 10
        #if for an instance that an ace is drawn and the 11 value makes our hand bust,
        #I subtract 10 from my hand value which gives the ace value 1 instead
        if has_ace and self.value > 21:
            self.value -= 10

    #after calculating the value i want to return it to hand
    def return_the_value(self):
        self.calculate_the_value()
        return self.value
    
    #I have to make a function to display the hands
    def display_hands(self):
        #if its the dealers hand
        if self.dealer:
            #print the first card as hidden and the second card
            print("HIDDEN")
            print(self.cards[1])
        #if its the players hand
        else:
            #print the cards in the players hand
            for card in self.cards:
                print(card)
                #then print the total
            print('Value:', self.return_the_value())

#the main loop in class game, I kept trying to set it up like the address book or the roi project
#but everytime id run into the issue that my main function and class Game were being repetitive
#so this way help me understand using the loop inside a class a little better
class Game:

    #I had to create an intialization function to pass the other functions through the class
    def __init__(self):
        pass

    #this playing function is to play the game
    def playing(self):
        #this boolean lets us know whether or not we are still playing
        continue_playing = True

        while continue_playing:
            #if we are playing we need a shuffled deck that passes through the class Deck
            self.deck = Deck()
            self.deck.shuffle_cards()

            #we also need two hands, passed through the class Hand.
            self.player_hand = Hand()
            #this dealer needs to be True for the their hand to pass through
            self.dealer_hand = Hand(dealer=True)

            #using the range function two cards are dealt to both hands
            for i in range(2):
                #the deal_cards function deals the cards,
                #then the add_card function will add the dealt cards to each of the players/dealers hands
                self.player_hand.add_card(self.deck.deal_cards())
                self.dealer_hand.add_card(self.deck.deal_cards())

            #I then print the hands of the player/dealer using the display_hands function
            print("Player's hand:")
            self.player_hand.display_hands()
            print("Dealer's hand:")
            self.dealer_hand.display_hands()

            #we run the loop until a winner is found
            winner = False

            #while the winner hasn't been found, we have to check the ongoing results of the game
            while not winner:
                #to start the game, the first turn only may produce a blackjack
                #so we have to check to see if the player/dealer hit a blackjack
                player_blackjack, dealer_blackjack = self.check_blackjack()

                #if either player/dealer has a backjack
                if player_blackjack or dealer_blackjack:
                    #the winner was found
                    winner = True
                    #we must show the results of the game and if neither has a blackjack the game continues
                    self.blackjack_results(player_blackjack, dealer_blackjack)
                    continue

                #once we continue past the first turn, the game must ask the user to hit or stand
                hit_stand = input("Would you like to hit or stand? ").lower()
                #if the user types in the wrong input
                while hit_stand not in ["h", "s", "hit", "stand"]:
                    #respond to the user with this input to help them type the correct input
                    hit_stand = input("Please type 'hit' or 'stand' or h/s ").lower()

                #if the player hits
                if hit_stand in ['hit', 'h']:
                    #I add another card to the hand by dealing a card from the deck then adding it to the player hand
                    self.player_hand.add_card(self.deck.deal_cards())
                    #I then display the players hand
                    self.player_hand.display_hands()

                    #if the player goes over
                    if self.check_player_over():
                    #the user loses and winner is found
                        print("You lose.")
                        winner = True
                #if the player stands
                else:
                    #we get the hand value of the dealer/player through the return the value function
                    player_hand_value = self.player_hand.return_the_value()
                    dealer_hand_value = self.dealer_hand.return_the_value()

                    #print the results
                    print("Player:", player_hand_value)
                    print("Dealer:", dealer_hand_value)

                    #to determine the winner we must compare the two hands
                    #if the players hand is > the dealers hand
                    if player_hand_value > dealer_hand_value:
                        #the player wins
                        print("You Win!")
                    #if the hands are equal its a draw
                    elif player_hand_value == dealer_hand_value:
                        print("Draw!")
                    #otherwise, we can assume the dealers hand is larger and they win
                    else:
                        print("You lose")
                    #a winner is found so we can close the loop
                    winner = True

            #we ask the user if they want to play again
            play_again = input("Would you like to play again? y/n ")
            #if the user doesnt answer correctly, ask them again
            while play_again.lower() not in ["y", "n"]:
                play_again = input("Please enter Y or N ")
            #if the answer is no, end the loop
            if play_again.lower() == "n":
                print("Thanks for playing!")
                continue_playing = False
            #if yes, we need to find a winner, so restart the loop until we find one
            else:
                winner = False

    #we need this function to check for blackjack to continue playing the game
    def check_blackjack(self):
        #if no blackjack for player/dealer, they both False for having a blackjack
        player = False
        dealer = False
        #but if the players hand pass the the return_the_value function adds up to 21,
        if self.player_hand.return_the_value() == 21:
            #then the player has a blackjack
            player= True
        #same process for checking the dealers hand
        if self.dealer_hand.return_the_value() == 21:
            dealer = True

        #I have to return the whether or not a blackjack was found
        return player, dealer
    
    #we need a function to show the results if a player gets a blackjack
    def blackjack_results(self, player_blackjack, dealer_blackjack):

        #if the player and the dealer get a blackjack, we have a draw
        if player_blackjack and dealer_blackjack:
            print("Draw!")

        #but if only the player has a blackjack, the player wins
        elif player_blackjack:
            print("Blackjack! You win!")

        #and if only the dealer gets a blackjack, the dealer wins
        elif dealer_blackjack:
            print("Dealer has blackjack! You lose.")

    #I need a function to check if the players hand busted
    def check_player_over(self):
        return self.player_hand.return_the_value() > 21

#to run the function I call out the class name, if its class name is __main__ 
if __name__ == "__main__":
    #I create an instance of class game and pass it through the playing function
    game = Game()
    game.playing()
            