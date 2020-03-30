import random
import adts
import argparse


class Pig(object):
    def __init__(self, players=2):
        self.players = adts.Queue()
        for num in xrange(players):
            self.players.enqueue(Player('Player' + ' ' + str(num)))
        self.current_player = self.players.dequeue()
        self.current_player.turn = True
        print 'Current player: {}'.format(self.current_player.name)
        self.die = Die()

    def next_player(self):
        self.current_player.turn = False
        self.players.enqueue(self.current_player)
        self.current_player = self.players.dequeue()
        print 'Next player is {}'.format(self.current_player.name)
        self.current_player.turn = True

    def start_game(self):
        ask = 'Roll (R) Hold (H) or Quit (Q)?'
        ask_player = raw_input(ask)
        while ask_player:

            if ask_player.upper()[0] == 'R' and self.current_player.turn:
                num = self.current_player.play(self.die)
                if num == 1:
                    self.current_player.points = []
                    print '{} loses turn. Score set to {}'\
                        .format(self.current_player.name,
                                self.current_player.get_score())
                    self.next_player()
                else:
                    self.current_player.points.append(num)
                    score = self.current_player.get_score()
                    if score >= 100:
                        print '{} wins. Score: {}'.format(self.current_player.name, score)
                        break

            elif ask_player.upper()[0] == 'H':
                print '{} Holds. Score: {}'\
                    .format(self.current_player.name,
                            self.current_player.get_score())
                self.next_player()

            elif ask_player.upper()[0] == 'Q':
                print 'Quitting game...'
                self.players.enqueue(self.current_player)
                while self.players.size() > 0:
                    player = self.players.dequeue()
                    print 'Player {}: {}'.format(player.name, player.score)
                break

            print 'Player: ', self.current_player.name
            print 'Score: ', self.current_player.get_score()
            ask_player = raw_input(ask)


class Die(object):
    faces = (1, 2, 3, 4, 5, 6)

    def roll(self):
        face = random.choice(self.faces)
        print 'Die face: {}'.format(face)
        return face


class Player(object):
    def __init__(self, name):
        self.name = name
        self.turn = False
        self.points = []
        self.score = 0
        self.plays = 0
        self.die = Die()

    def hold(self):
        self.turn = False

    def play(self, die):
        if self.turn:
            print 'Rolling the die.....'
            return die.roll()

    def get_score(self):
        self.score = sum(self.points)
        return self.score


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--NumOfPlayers', required=False, type=int, default=2)
    parser.add_argument("-f", "--fff", help="an argument to fool anaconda jupyter notebook", default="1")
    num = parser.parse_args()
    if num.NumOfPlayers > 1:
        game = Pig(num.NumOfPlayers)
        game.start_game()
    else:
        print 'You need at least two players for this game.'






