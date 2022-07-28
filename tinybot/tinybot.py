"""
    
"""
from http.client import responses
import os
from tinybot.dataset import query
from urllib import response
from libcst import While
import yaml
import shutil

from tinybot.config import Config
from tinybot.trainer import Trainer
from tinybot.state_manager import StateManager



def read_agent_config(config_path):

    if not os.path.exists(config_path):
        raise Exception(f"config yaml path {config_path} does not exists")
    
    agent_config = {}
    with open(config_path) as r:
        agent_config = yaml.load(r, yaml.FullLoader)
    
    return agent_config



def train(config_path, root_dir = "./"):
    """
        function to train tiny bot from the config

        Args :
        config_path : path of config yaml file required to train a tiny bot
        root_dir : path of dir where tiny bot will store trained virtual agent 
    """
    agent_config = read_agent_config(config_path)

    agent_dir = os.path.join(root_dir, agent_config["name"])
    model_caching_dir = os.path.join(agent_dir, Config.model_caching_dir)

    os.makedirs(agent_dir, exist_ok=True)
    os.makedirs(model_caching_dir, exist_ok=True)

    # moving config file to agent dir
    shutil.copy2(config_path, os.path.join(agent_dir, "config.yaml"))

    trainer = Trainer()

    # training intent classifier
    intent_classifier_path = os.path.join(model_caching_dir, "intent_classifier.pkl")
    trainer.train_intent_classifier(agent_config["intents"], Config.classifier_head, intent_classifier_path)

    # training a semantic similarity model
    similarity_model_path = os.path.join(model_caching_dir, "similarity_model.pkl")
    trainer.train_semantic_similarity_model(agent_config["knowledge_base"], similarity_model_path)

    # training contextual token classifier
    # TODO:

    



def load(agent_dir):
    
    config_path = os.path.join(agent_dir, "config.yaml")
    agent_config = read_agent_config(config_path)

    model_caching_dir = os.path.join(agent_dir, Config.model_caching_dir)
    intent_classifier_path = os.path.join(model_caching_dir, "intent_classifier.pkl")
    similarity_model_path = os.path.join(model_caching_dir, "similarity_model.pkl")

    # initializing new state
    state_manager = StateManager(agent_config["name"], agent_config["flows"], agent_config["nlu_settings"], intent_classifier_path, similarity_model_path)
    
    print("\nStarting TinyBot... \n")
    print("-"*100)

    responses = state_manager.process_query('', "event.welcome")
    print_repsonse(responses)

    while True:
        query = input(f"user \t >> ")
        responses = state_manager.process_query(query)
        print_repsonse(responses)

    



def print_repsonse(responses):
    for res in responses:
        print(res)
    print("-"*100)
    