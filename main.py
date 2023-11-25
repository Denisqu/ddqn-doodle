import utils.env_tuner as env_tuner
import utils.logging as logging
import core.agent as agent
from pathlib import Path
import torch
import random, datetime, os, copy
import doodle_env.env


if __name__ == '__main__':
    env = env_tuner.get_tuned_env()
    
    use_cuda = torch.cuda.is_available()
    checkpoint_file_rel_path = "C:\git-repos\python-projects\ddqn-doodle\checkpoints\2023-11-24T18-59-18\mario_net_0.chkpt"
    print(f"Using CUDA: {use_cuda}")

    save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)

    doodle_agent = agent.Mario(state_dim=(4, 84, 84), action_dim=env.action_space.n, save_dir=save_dir)

    

    if os.path.exists(f'{checkpoint_file_rel_path}'):
         checkpoint = torch.load(checkpoint_file_rel_path)
         doodle_agent.net.load_state_dict(checkpoint['model'])
         #mario.exploration_rate = checkpoint['exploration_rate'] - 0.39
         #mario.curr_step = checkpoint["curr_step"]
    else:
        print(f"no checkpoint found - ({checkpoint_file_rel_path})")
        
    logger = logging.MetricLogger(save_dir)

    episodes = 40000
    for e in range(episodes):
        state = env.reset()
        print("!!!restarting game from python!!!")
        step_num_in_episode = 0
        previous_reward = 0
        # Play the game!
        while True:

            step_num_in_episode += 1
            # Run agent on the state
            action = doodle_agent.act(state)
            
            
            # Agent performs action
            next_state, reward, done, info = env.step(action)
            # previous_reward_cache = previous_reward
            # temp = current_reward
            # reward = current_reward - previous_reward
            # previous_reward = temp

            # Remember
            doodle_agent.cache(state, next_state, action, reward, done)

            # Learn
            q, loss = doodle_agent.learn()
            #print(f"current_reward={current_reward}, prev_reward={previous_reward_cache}, reward={reward}, done={done}, step_in_episode={step_num_in_episode}")
            print(f"e={e}, q={q}, loss={loss}, r={reward}, done={done}, step={step_num_in_episode}")

            # Logging
            logger.log_step(reward, loss, q)
            
            # Update state
            state = next_state

            # Check if end of game
            if done:
                break
        
        
        logger.log_episode()
        if e % 2 == 0:
            logger.record(episode=e, epsilon=doodle_agent.exploration_rate, step=doodle_agent.curr_step)
        if e % 10 == 0:
            doodle_agent.save()
            
        

    

    

