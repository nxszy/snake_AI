# to-do
from collections import deque
from gameAI import gameAI
import numpy as np
import random
import torch
from model import Linear_QNet, QTrainer
from ploting import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class DQNAgent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness (explore -> exploit)
        self.gamma = 0.9 # discount rate (influence of next rewards on the learning process)

        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = Linear_QNet(11, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        
        head_x, head_y = game.snake.body[0].pos
        fruit_x, fruit_y = game.fruit.pos
        point_d_x, point_d_y = head_x + 1, head_y
        point_a_x, point_a_y = head_x - 1, head_y
        point_w_x, point_w_y = head_x, head_y - 1
        point_s_x, point_s_y = head_x, head_y + 1

        dir_d = game.snake.direction.name == "D"
        dir_a = game.snake.direction.name == "A"
        dir_w = game.snake.direction.name == "W"
        dir_s = game.snake.direction.name == "S"

        state = [
            # danger straight
            (dir_d and game.snake.check_collision(point_d_x, point_d_y)) or
            (dir_a and game.snake.check_collision(point_a_x, point_a_y)) or
            (dir_w and game.snake.check_collision(point_w_x, point_w_y)) or
            (dir_s and game.snake.check_collision(point_s_x, point_s_y)),

            # danger right
            (dir_d and game.snake.check_collision(point_s_x, point_s_y)) or
            (dir_a and game.snake.check_collision(point_w_x, point_w_y)) or
            (dir_w and game.snake.check_collision(point_d_x, point_d_y)) or
            (dir_s and game.snake.check_collision(point_a_x, point_a_y)),

            # danger left
            (dir_d and game.snake.check_collision(point_w_x, point_w_y)) or
            (dir_a and game.snake.check_collision(point_s_x, point_s_y)) or
            (dir_w and game.snake.check_collision(point_a_x, point_a_y)) or
            (dir_s and game.snake.check_collision(point_d_x, point_d_y)),

            dir_d,
            dir_a,
            dir_w,
            dir_s,

            fruit_x > head_x,
            fruit_x < head_x,
            fruit_y < head_y,
            fruit_y > head_y
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*sample)

        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):

        move = [0,0,0,0]
        
        self.epsilon = 100 - self.n_games

        if random.randint(0,200) < self.epsilon:
            idx = random.randint(0,3)
            move[idx] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move_idx = torch.argmax(prediction).item()
            move[move_idx] = 1
        
        return move

def train():
    plot_scores = [] # wyniki z prób
    plot_mean_scores = [] # średnia z prób
    total_score = 0
    record = 0
    agent = DQNAgent()
    game = gameAI()

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
                agent.model.save()
            
            print('Game', agent.n_games, '.Score: ', score, '.Record: ', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)

            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()