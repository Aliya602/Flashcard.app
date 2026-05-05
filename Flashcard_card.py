import json
import os
import random
from colorama import Style, Fore, init
init()


class Card:
    def __init__(self, question, answer, wrong_answers):
        self.question = question
        self.answer = answer 
        self.wrong_answers = wrong_answers if wrong_answers  is not None else []
        self.correct_count = 0
        self.wrong_count = 0

    def check_answer(self, user_answer): 
        return user_answer.lower().strip() == self.answer.lower().strip()

    def __str__(self):
        return f"Q: {self.question} | A: {self.answer}"
    
    def to_dict(self):
        """Convert Card to dictionary for JSON saving"""
        return {
            'question': self.question,
            'answer': self.answer,
            'correct_count': self.correct_count,
            'wrong_count': self.wrong_count,
            'wrong_answers': self.wrong_answers
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Card from dictionary data"""
        card = cls(
            data['question'],
            data['answer'],
            data.get('wrong_answers', [])
        )
        card.correct_count = data.get('correct_count', 0)
        card.wrong_count = data.get('wrong_count', 0)
        return card

class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []
    def add_card(self, question, answer, wrong_answers=None):
        self.cards.append (Card(question, answer, wrong_answers))
        print(Fore.GREEN + f"Card added: {question}" + Style.RESET_ALL)
       
        
    def wrong_answers(self):
        print(Fore.YELLOW + "Lets add some wrong answers onto your multiple choice card!" + Style.RESET_ALL)
        wrong_answers = []
        for i in range(3):
            wrong = input(f"Enter wrong answer {i+1}: ")
            wrong_answers.append(wrong)
            print(Fore.GREEN + f"Added: {wrong}" + Style.RESET_ALL)
        return wrong_answers
    

    def show_cards(self):
        if not self.cards:
            print(Fore.YELLOW + "No cards in this deck" + Style.RESET_ALL)
            return
        
        print(Fore.CYAN + f"\n🗂️ Deck: {self.name}" + Style.RESET_ALL)
        for i, card in enumerate(self.cards, 1):
            print(f"{i}. {card}")

    def save_to_file(self, filename=None):
        if filename is None:
            # Replace spaces with underscores for filename
            filename = f"{self.name.replace(' ', '_')}.json"
        
        # Convert all cards to dictionaries
        cards_data = []
        for card in self.cards:
            cards_data.append(card.to_dict())
        
        deck_data = {
            'name': self.name,
            'cards': cards_data
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(deck_data, f, indent=2)
            print(Fore.GREEN + f"Deck saved to {filename}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error saving deck: {e}" + Style.RESET_ALL)
    
    # Load deck from JSON file
    @classmethod
    def load_from_file(cls, filename):
        
        try:
            with open(filename, 'r') as f:
                deck_data = json.load(f)
            
            deck = cls(deck_data['name'])
            
            for card_data in deck_data['cards']:
                card = Card.from_dict(card_data)
                deck.cards.append(card)
            
            print(Fore.GREEN + f"Deck loaded from {filename}" + Style.RESET_ALL)
            return deck
        
        except FileNotFoundError:
            print(Fore.RED + f"File {filename} not found." + Style.RESET_ALL)
            return None
        except Exception as e:
            print(Fore.RED + f"Error loading deck: {e}" + Style.RESET_ALL)
            return None
        

    def display_multiple_choice_options(self, card):
        options = [card.answer] + card.wrong_answers.copy()
        random.shuffle(options)
        letters = ['A', 'B', 'C', 'D']
        letter_to_answer = {}

        print(Fore.CYAN + "Options:" + Style.RESET_ALL)
        for i, option in enumerate(options):
            letter = letters[i]
            letter_to_answer [letter] = option
            print(f"{letter}. {option}")

        while True:
            choice = input("Enter A, B, C or D: ").upper()
            if choice in letter_to_answer:
                return letter_to_answer[choice]
            else:
                print(Fore.RED + "Invalid choice. Please enter A, B, C, or D." + Style.RESET_ALL)


    def quiz(self):
        """Quiz the user on all cards"""
        if not self.cards:
            print(Fore.YELLOW + "No cards to quiz!" + Style.RESET_ALL)
            return
        
        print(Fore.CYAN + f"\n📝 Starting quiz on '{self.name}' deck!" + Style.RESET_ALL)
        print("=" * 30)

        correct = 0
        total = len(self.cards)

        for i, card in enumerate(self.cards, 1):
            print(f"\nQuestion {i}/{total}: {card.question}")

            if card.wrong_answers:
                user_answer = self.display_multiple_choice_options(card)
                is_correct = (user_answer.lower().strip() == card.answer.lower().strip())
            else:
                user_answer = input("Your answer: ")
                is_correct = card.check_answer(user_answer)


            if is_correct:
                print(Fore.GREEN + "✓ Correct!" + Style.RESET_ALL)
                card.correct_count += 1
                correct += 1
            else:
                print(Fore.RED + f"✗ Wrong! The answer is: {card.answer}" + Style.RESET_ALL)
                card.wrong_count += 1
        
        # Random encouragement message based on score
        percentage = (correct / total) * 100
        print(Fore.CYAN + "\n" + "=" * 30)
        print(f"Quiz complete! Score: {correct}/{total} ({percentage:.1f}%)")
        
        if percentage >= 80:
            print(Fore.GREEN + "Excellent work! You're mastering this deck!" + Style.RESET_ALL)
        elif percentage >= 50:
            print(Fore.YELLOW + "Good effort! A little more practice will help!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Keep practicing! You'll improve with repetition!" + Style.RESET_ALL)
        print("=" * 30 + Style.RESET_ALL)



# Main application
print("==" * 20)
print(Fore.GREEN + "Welcome to Flashcard App 🎴" + Style.RESET_ALL)
print("==" * 20)

# Ask if they want to load an existing deck
load_choice = input("Load existing deck? (y/n): ")

if load_choice.lower() == 'y':
    filename = input("Enter filename to load (e.g., mydeck.json): ")
    my_deck = Deck.load_from_file(filename)
    if my_deck is None:
        print(Fore.YELLOW + "Creating a new sample deck instead." + Style.RESET_ALL)
        my_deck = Deck("Sample Deck")
        my_deck.add_card("What is the capital of France?", "Paris", ["London", "Rome", "Berlin"])
        my_deck.add_card("What is 2 + 2?", "4", ["3", "5", "6"])
        my_deck.add_card("What color is the sky?", "Blue", ["Green", "Red", "Yellow"])
        my_deck.add_card("What is the largest mammal?", "Blue Whale", ["Elephant", "Giraffe", "Lion"])
        my_deck.add_card("What is the boiling point of water?", "100 degrees Celsius", ["0 degrees Celsius", "50 degrees Celsius", "212 degrees Fahrenheit"])
else:
    # Create a new deck
    deck_name = input("Enter a name for your new deck: ")
    my_deck = Deck(deck_name)
    
    # Add new cards
    while True:
        question = input("\nEnter question (or 'done' to finish): ")
        if question.lower() == 'done':
            break
        answer = input("Enter answer: ")
        
        mc_choice = input("Is this a multiple choice card? (y/n): ")
        if mc_choice.lower() == 'y':
            wrong_answers = []
            for i in range(3):
                wrong = input(f"Enter wrong answer {i+1}: ")
                wrong_answers.append(wrong)
                print(Fore.GREEN + f"Added: {wrong}" + Style.RESET_ALL)
            my_deck.add_card(question, answer, wrong_answers)
        else:
            my_deck.add_card(question, answer)

# Show all cards
my_deck.show_cards()


save_choice = input("\nSave this deck? (y/n): ")
if save_choice.lower() == 'y' or save_choice.lower() == 'yes':
    my_deck.save_to_file()


print("\n" + "=" * 30)
quiz_now = input("Do you want to take a quiz? (y/n): ")

if quiz_now.lower() == 'y':
    my_deck.quiz()
else:
    print(Fore.YELLOW + "Maybe next time! Goodbye!" + Style.RESET_ALL)
