# to-do
from collections import deque
from snakeAI import SnakeAI

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class DQNAgent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness (explore -> exploit)
        self.gamma = 0 # discount rate (influence of next rewards on the learning process)

        self.memory = deque(maxlen=MAX_MEMORY)

    def get_state(self, game):
        
        head = game.snake

    def remember(self, state, action, reward, next_state, done):
        pass
    
    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = [] # wyniki z prób
    plot_mean_scores = [] # średnia z prób
    total_score = 0
    record = 0
    agent = DQNAgent()
    game = SnakeAI()

    while True:

        # get current state
        state_old = agent.get_state(game)

        # get move
        move = agent.get_action(state_old)

        # perform the move
        reward, done, score = game.play_step(move)

        # get updated state
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, move, reward, state_new, done)

        # remember in memory
        agent.remember(state_old, move, reward, state_new, done)

        if done:
            # train long memory (replay) 
            # prevents the correlation problem

            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                # agent.model.save()
            
            print('Game', agent.n_games, '.Score: ', score, '.Record: ', record)

train()