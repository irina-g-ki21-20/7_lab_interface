import random
import copy
from abc import ABC, abstractmethod
from enum import Enum, auto

class Player(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2

class Game(ABC):
    def __init__(self, n=12):
        self.n = n
        self.pit_1 = [4] * 6 + [0]
        self.pit_2 = [4] * 6 + [0]
        self.state = {Player.PLAYER_1: copy.deepcopy(self.pit_1),
                      Player.PLAYER_2: copy.deepcopy(self.pit_2)}
        self.player_turn = self.whose_move()

    def print_game(game):
        slots = list(range(0, 6))

        print("Slots:   | ", end="")
        print(*slots, sep=" | ", end="")
        print(" |")
        print("=======================================")
        print("Player 2 | ", end="")
        print("---------------------------------------")
        print("Player 1 | ", end="")
        print("=======================================")

    def whose_move(self):
        print(f'Выбор очередности ходов: ')
        print(f'Введите 0, если ходить первым будет игрок 1')
        print(f'Введите 1, если ходить первым будет игрок 2')
        print(f'Введите 2, чтобы выбрать очередность ходов случайным образом')

        while True:
            m = input('> ')
            player = None
            if m.isdigit():
                m = int(m)
                if m > 2 or m < 0:
                    print(f'Введите число 0, 1 или 2')
                elif m == 0:
                    player = Player.PLAYER_1
                    print(f'Первым будет ходить игрок {player.name}!')
                elif m == 1:
                    player = Player.PLAYER_1
                    print(f'Первым будет ходить игрок {player.name}!')
                else:
                    if m == 2:
                        m = random.randint(0, 1)
                    player = Player.PLAYER_1 if m == 0 else Player.PLAYER_2
                    print(f'Первым будет ходить игрок {player.name}!')
                    break
            else:
                print(f'Вы ввели недопустимый символ. Введите число 0, 1 или 2')
        return player

    def move(self, player, pit_number):
        pass

    @abstractmethod
    def game_state(self):
        return 0

class MancalaGame(Game):
    def move(self, player, pit_number):
        current_pit = self.state[player][pit_number]

        if current_pit == 0:
            print(f'Выбранная лунка пуста. Выберите другую лунку.')
            return

        # забираем камни из выбранной лунки
        self.state[player][pit_number] = 0

        # распределяем камни вправо по лункам
        current_index = pit_number + 1
        while current_pit > 0:
            if current_index == self.n:
                current_index = 0
            self.state[player][current_index] += 1
            current_index += 1
            current_pit -= 1

    def game_state(self):
        # игрок 1 победил, когда все его лунки пусты, и игрок 2 имеет еще камни в своих лунках
        if all(pit == 0 for pit in self.state[0][:-1]) and any(pit > 0 for pit in self.state[1][:-1]):
            return 1
        # аналогично со 2
        elif all(pit == 0 for pit in self.state[1][:-1]) and any(pit > 0 for pit in self.state[0][:-1]):
            return 2

        return 0  # игра продолжается


# Вы берете из любой своей лунки все камни и по одному раскладываете их в последующие лунки, свои и чужие, против часовой стрелки,
# исключая «амбары», общие для обоих игроков большие лунки, где можно накапливать камни без опасности их потерять. Если последний
# камень упал в непустую лунку, вы «загребаете» ее содержимое и продолжаете ходить — до тех пор, пока последний камень очередного
# посева не упадет в пустую лунку, дальше — переход хода. Как только в любой лунке после вашего «вброса» оказывается четыре камня,
# вы забираете их себе. Проигрывает тот, кому нечем ходить — то есть ни в одной из лунок на его половине не остается камней.


game = MancalaGame()
game_state = game.game_state()
print(game_state)