from typing import Optional
import random


class JibberJabber:
    def __init__(self):
        self.responses_base = {
            'coffee': [
                'Coffee gives you dehydration, you know',
                'Good choice, get more caffeine',
                'Seriously? Coffee?',
                'One cup of coffee demands one extra glass of water!'
            ],
            'takeaway': [
                'Try eating home-made food for a change!',
                'I hope you enjoyed it!',
                'Junk again? Really?',
                'Stop wasting money!',
                'Meat and veggies are better for your health than this!',
                'What about your diet?',
                'Not enough nutrition!',
                'Carbs will make you sleepy.'
            ],
            'meat': [
                'GO CARNIVORE!!!',
                'Mmmmm... Proteins!',
                'Iron levels UP!'
            ],
            'alcohol': [
                'Bad for your brain!',
                'Alcoholism is a new career',
                'Alcohol doesn\'t make you happier!'
            ]
        }

    def have_response(self) -> bool:
        chance = random.randint(0, 100)
        return chance >= 60

    def choose_response(self, purchase: str, category: str) -> str:
        if purchase in self.responses_base and category in self.responses_base:
            key = random.choice(list(self.responses_base.keys()))
            return random.choice(self.responses_base[key])
        elif purchase in self.responses_base:
            return random.choice(self.responses_base[purchase])
        elif category in self.responses_base:
            return random.choice(self.responses_base[category])
        return ''

    def toxic_response(self, purchase: str, category: str) -> str:
        if self.have_response():
            return self.choose_response(purchase, category)

        return ''

