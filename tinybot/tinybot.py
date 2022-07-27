"""
    
"""
import os
import yaml

from tinybot.config import Config
from tinybot.trainer import Trainer


def train(config_path, root_dir = "./"):
    """
        function to train tiny bot from the config

        Args :
        config_path : path of config yaml file required to train a tiny bot
        root_dir : path of dir where tiny bot will store trained virtual agent 
    """
    
    if not os.path.exists(config_path):
        raise Exception(f"config yaml path {config_path} does not exists")
    
    agent_config = {}
    with open(config_path) as r:
        agent_config = yaml.load(r, yaml.FullLoader)


    agent_dir = os.path.join(root_dir, agent_config["name"])
    model_caching_dir = os.path.join(agent_dir, Config.model_caching_dir)

    os.makedirs(agent_dir, exist_ok=True)
    os.makedirs(model_caching_dir, exist_ok=True)

    trainer = Trainer()

    # training intent classifier
    intent_classifier_path = os.path.join(model_caching_dir, "intent_classifier.pkl")

    trainer.train_intent_classifier(agent_config["intents"], Config.classifier_head, intent_classifier_path)






def load():
    pass