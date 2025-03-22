import random
import time
import threading

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0

    def roll(self, dice):
        return dice.roll()

    def hold(self):
        self.score += self.turn_total
        self.turn_total = 0

# ComputerPlayer class
class ComputerPlayer(Player):
    def should_roll(self):
        hold_threshold = min(25, 100 - self.score)
        return self.turn_total < hold_threshold

    def make_decision(self, dice):
        if self.should_roll():
            print(f"{self.name} decides to roll.")
            roll_result = self.roll(dice)
            print(f"Rolled a {roll_result}")
            if roll_result == 1:
                print(f"{self.name} rolled a 1. Turn over!")
                self.turn_total = 0
                return True  # Switch player
            else:
                self.turn_total += roll_result
                return False  # Continue turn
        else:
            print(f"{self.name} decides to hold.")
            self.hold()
            return True  # Switch player

# PlayerFactory class
class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")

# Dice class
class Dice:
    def __init__(self):
        self.faces = [1, 2, 3, 4, 5, 6]

    def roll(self):
        return random.choice(self.faces)

# Game class
class Game:
    def __init__(self, player1, player2):
        self.dice = Dice()
        self.players = [player1, player2]
        self.current_player = self.players[0]

    def play_turn(self):
        if isinstance(self.current_player, ComputerPlayer):
            # Computer's turn
            print(f"{self.current_player.name}'s turn:")
            print(f"Current score: {self.current_player.score}, Turn score: {self.current_player.turn_total}")
            switch_player = self.current_player.make_decision(self.dice)
            if switch_player:
                self.switch_player()
        else:
            # Human's turn
            while True:
                action = input(f"{self.current_player.name}'s turn:\n"
                               f"Current score: {self.current_player.score}, "
                               f"Turn score: {self.current_player.turn_total}\n"
                               "Enter 'r' to roll or 'h' to hold: ").strip().lower()
                if action == 'r':
                    roll_result = self.current_player.roll(self.dice)
                    print(f"Rolled a {roll_result}")
                    if roll_result == 1:
                        print(f"{self.current_player.name} rolled a 1. Turn over!")
                        self.current_player.turn_total = 0
                        self.switch_player()
                        break
                    else:
                        self.current_player.turn_total += roll_result
                elif action == 'h':
                    self.current_player.hold()
                    self.switch_player()
                    break
                else:
                    print("Invalid input. Please enter 'r' to roll or 'h' to hold.")

    def switch_player(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def is_game_over(self):
        return self.players[0].score >= 100 or self.players[1].score >= 100

    def get_winner(self):
        if self.players[0].score >= 100:
            return self.players[0]
        elif self.players[1].score >= 100:
            return self.players[1]
        else:
            return None

# TimedGameProxy class
class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.time_up = False

    def end_game(self):
        print("Time's up! Game over.")
        self.time_up = True

    def play(self):
        # Start a timer to end the game after 60 seconds
        timer = threading.Timer(60.0, self.end_game)
        timer.start()

        while not self.game.is_game_over() and not self.time_up:
            self.game.play_turn()

        # Determine the winner
        player1, player2 = self.game.players
        if player1.score > player2.score:
            print(f"Time's up! {player1.name} wins with {player1.score} points!")
        elif player2.score > player1.score:
            print(f"Time's up! {player2.name} wins with {player2.score} points!")
        else:
            print("Time's up! It's a tie!")

# Main function
def main():
    # Hardcoded values for testing in Jupyter Notebook
    player1_type = "human"  # Change to "computer" if needed
    player2_type = "computer"  # Change to "human" if needed
    timed = True  # Set to False to disable timed mode

    # Create players using the PlayerFactory
    player1 = PlayerFactory.create_player(player1_type, "Player 1")
    player2 = PlayerFactory.create_player(player2_type, "Player 2")

    # Create the game
    game = Game(player1, player2)

    # Play the game
    if timed:
        timed_game = TimedGameProxy(game)
        timed_game.play()
    else:
        while not game.is_game_over():
            game.play_turn()
        winner = game.get_winner()
        print(f"Game over! {winner.name} wins with {winner.score} points!")

if __name__ == "__main__":
    main()
