https://github.com/atomwalk12/QuestLlama/assets/146588815/cdba11c8-893d-4b46-81f4-dab179fb0ec9


**QuestLlama: An Autonomous Agent in Minecraft**

Welcome to QuestLlama, a project inspired by Voyager that aims to create an alternative to paid subscription-based AI models like ChatGPT. Our goal is to build an autonomous agent in Minecraft using open-source LLaMA 3 models.

**Run Demo**
Check the agent in action [on Youtube](https://www.youtube.com/watch?v=Yi1C9vs1BWM).

**Project Overview**

QuestLlama combines the power of LLaMA 3 models with the popular Minecraft game to create a unique and interactive experience. Our agent is designed to explore, learn, and adapt to its environment without human intervention. By leveraging the capabilities of LLaMA 3 models, we can create an autonomous agent that can perform complex tasks and explore Minecraft.

**Directory Structure**

```md
├── voyager/                            # voyager root directory
├── questllama/                         # questllama root directory
│   ├── core/                           # module internal functions
│   |   |── prompts/                    # system prompts
│   |   └── retriever_factory/          # RAG retrieval
│   ├── extensions/                     # functions used from outside the module
│   |   ├── chat_interactions.py        # main module functions 
│   └── skill_library/                  # functions used for RAG retrieval
└── shared/                             # functions called from both modules
```

**Key Features**

* Autonomous exploration: QuestLlama's agent explores the Minecraft world, acquires new skills, and makes discoveries without human intervention.
* Open-source LLaMA 3 models: We utilize open-source LLaMA 3 models to power our agent, making it a cost-effective alternative to paid subscription-based AI models.
* Interactive experience: QuestLlama provides an immersive and interactive experience in Minecraft, allowing users to engage with the agent and observe its behavior.

**Getting Started**

To get started with QuestLlama, please follow these steps:

1. Install the required dependencies and setup your environment according to our installation guide.
2. Clone our repository and navigate to the project directory.
3. Follow the instructions in our README files to set up and run the agent.

**Installation process**

First of all follow the installation instructions found at [Voyager](https://github.com/MineDojo/Voyager) repository. Note that for convenience the required mods needed to use the agent are available under ```installation/questllama/mods directory```.

**Now to setup the environment for QuestLlama**
Please note that both Voyager and QuestLlama require Python 3.9. The easiest way to get up and running with a local environment is to use Anaconda. Follow the instructions at the [Anaconda homepage](https://docs.anaconda.com/free/anaconda/install/index.html) to install Anaconda.
After the installation follow these steps to setup your local environment:


```console
conda create -n questllama python=3.9.19
conda activate questllama
python install.py
```

**Restart Learning**
To restart with a brand new character the learning process simply rename the ```ckpt``` directory and remove the ```resume=True``` flag in learn.py.
