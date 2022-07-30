# TinyBot
Minimal Framework to build Conversational Virtual Agent

To install tinybot
```
  pip install git+https://github.com/heeyjunaid/TinyBot
```

How train your first bot?
1. Download anyone of the configuration YAML file from the examples folder
    e.g. example/travel_agent.yaml
2. Install tinybot
3. Import train and load function from tinybot
```
  >> from tinybot import train, load
```
4. Train first bot from config YAML file
```
  >> # provide yaml file path and root dir path where you want to store ML models
  >> train("examples/travel_agent.yaml", "test_agents")
```
5. Load trained bot
```
  >> # To load bot trained bot you just have to provide folder path
  >> # which train function has created e.g. test_agents/Anna
  >> load("test_agents/Anna")
```
6. Your trained bot will greet you with welcome flow
```
  Anna     >> Hello, I'm Anna. Your travel companion. I can help you with following things
           [Book Ticket] [Book Hotel] [Check Travel Schedule]
```

# Features
- Intent and small talk support
- Knowledge Base/FAQ support
- Multi flow and multi-turn conversations
- Non-Linear Conversation support
- Fallback Handling


# ToDo Features
- Support for regex and contextual slots
- Support for short term context
- Support for required slots and list slots
- Support for selecting custom classifier head for BERT (currently only logistic regression is supported)
- Support for finetuning custom language models


# TinyAPI
  Api exposing TinyBot
  
# TinyDeploy
  Automate deployment of TinyBot to Kubernetes
