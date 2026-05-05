import json
import os
from  colorama import Style,Fore, init
init()
import random

feedback = random(0,9)



class Card:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.correct_count = 0
        self.wrong_count = 0

    def check_answer(self, user_answer):
        return user_answer.lower().strip () == self.answer.lower().strip()

    def __str__(self):
        return f"Q: {self.question} | A: {self.answer}"
    
    # JSON can't save Pythom objects directly. It can only save: Dictionaries, Lists, Strings and etc.
    def to_dict(self):
        return{
            'question': self.question,
            'answer' : self.answer,
            'correct_count' : self.correct_count,
            'wrong_count' : self.wrong_count
        }
    @classmethod
    # @classmethod means this method creates a new card instance
    def from_dict(cls, data):
        card = cls(data['question'], data['answer']) #Create a new card
        card.correct_count = data['correct_count'] 
        card.wrong_count = data['wrong_count']
        return card
    

    def save_to_file(self, filename=None):
        if filename is None:
            #Creates a filename from deck name and also replaces spaces with underscores
            filename = f"{self.name.replace('', '_')}.json"

        #Converting all cards to dictionares
        cards_data = []
        for card in self.cards:
            cards_data.append(card.to_dict())
        
        deck_data = {
            'name' : self.name,
            'cards' : cards_data
        }

        try:
            with open(filename, 'w') as f:
                json.dump(deck_data, f, indent=2)
            print(Fore.GREEN + f"Deck Loaded from {filename}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error saving: {e}" + Style.RESET_ALL)
    
    @classmethod
    def load_from_files(cls, filename):
        try:
            with open(filename, 'r') as f:
                deck_data = json.load(f)
                deck = cls(deck_data['name']) # Creates a new deck wth the saved name
            
            # Recreate each card from from ts dictionary data
            for card_data in deck_data['cards']: 
                card = Card.from_dict(card_data) 
                deck.cards.append(card)
            
            print(Fore.GREEN + f"Deck Loaded from {filename}" + Style.RESET_ALL)
            return deck
        
        except FileExistsError:
            print(Fore.RED + f"File {filename} not found." + Style.RESET_ALL)
            return None
        except Exception as e:
            print(Fore.RED + f"Error loading deck {e}" + Style.RESET_ALL)
            return None


class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []
    
    def add_card(self, question, answer):
        self.cards.append(Card(question, answer))

    def show_cards(self):

        if not self.cards:
            print(Fore.YELLOW + "No cards in this deck" + Style.RESET_ALL)
            return
        
        print(Fore.CYAN  + f" 🗂️ Deck: {self.name}" + Style.RESET_ALL)
        for i , card in  enumerate(self.cards, 1):
            print(f"{i}. {card}")


    def quiz(self):

        if not self.cards:
            print(Fore.YELLOW + "No cards to quiz!" + Style.RESET_ALL )
            return
        

        print(Fore.CYAN + f"\n📝 Starting quiz on '{self.name}' deck!" + Style.RESET_ALL)
        print("=="  * 20)
        print("==" * 20)
        print(Fore.GREEN + "Welcome to Flashcard App 🎴" + Style.RESET_ALL)
        print("==" * 20)

        correct = 0
        total = len(self.cards)

        load_choice = input(Fore.BLUE + "Load existing deck? (y/n)" + Style.RESET_ALL)
        if load_choice.lower() == "y":
            filename = input("Enterfilename to load (e.g., mydeck.json): ")
            my_deck = Deck.load_from_file(filename)
            if my_deck is None:
                print(Fore.YELLOW + "Creating/Generating a new sample deck instead" + Style.RESET_ALL)
                my_deck = Deck("Sample Deck")
                my_deck.add_card("What is the capital of France", "Paris")
                my_deck.add_card("What is 2 + 2", "4")

            else:
                deck_name = input("Enter the name of your deck: ")
                my_deck = Deck(deck_name)

                while True:
                    question = input("Enter question (or 'done' or 'end' to finish): ")
                    if question.lower() == 'done' or 'end':
                        break
                    answer = input("Enter answer: ")
                    my_deck.add_card(question,answer)

            my_deck.show_cards

            save_choice = input("\nSave this deck? (y/n)")
            if save_choice.lower() == 'y' or 'yes':
                my_deck.save_to_file()

            # Offer to save 


        for i, card in enumerate(self.cards, 1):
            print(f"\nQuestion {i}/{total}: {card.question}")
            user_answer = input("Your answer: ")

            if card.check_answer(user_answer):
                print(Fore.GREEN +  "✓ Correct!" + Style.RESET_ALL )
                card.correct_count += 1 # Increment this card's correct count
                correct += 1 # Increment total correct count
            else:
                print(Fore.RED + f"✗ Wrong! The answer is: {card.answer}" + Style.RESET_ALL)
                card.wrong_count += 1
            
        
        print(Fore.CYAN + "\n" + "=" * 30)
        percentage = (correct / total * 100)
        print(f"Quiz complete! Score: {correct}/{total} ({percentage:.1f}%)")
        print("=" * 30 + Style.RESET_ALL)

        
my_deck = Deck("Sample Deck")
my_deck.add_card("What is the capital of France?","Paris")
my_deck.add_card("What is 2 + 2?","4")

my_deck.show_cards()
print("=" * 30)
quiz_now = input("Do you want to take a quiz? (y/n) ")

if quiz_now.lower() == 'y':
    my_deck.quiz()    
else:
     print(Fore.YELLOW + "Maybe next time! Goodbye!" + Style.RESET_ALL)
       