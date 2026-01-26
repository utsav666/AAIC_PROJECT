import os
from autogen import AssistantAgent, UserProxyAgent,GroupChat, GroupChatManager, config_list_from_json
import warnings
warnings.filterwarnings("ignore", message="You may be able to resolve this warning")
# --- Load API Key ---
config_list = config_list_from_json("config/model_config.json")

# Disable Docker (for local code execution)
os.environ["AUTOGEN_USE_DOCKER"] = "0"
code_execution_config = {"use_docker": False}

# --- Define Agents ---

# Research agent
researcher = AssistantAgent(
    name="Researcher",
    system_message=(
        "You are a senior data scientist. "
        "When you find a good algorithmic idea, explain it clearly "
        "and end your response with 'TERMINATE'."
    ),
    llm_config={"config_list": config_list}
)

# Coding agent — with local execution
coder = AssistantAgent(
    name="Coder",
    system_message=(
        "You are a Python engineer. Implement the given idea using clean code. "
        "Execute and verify the code. End with 'TERMINATE' after success."
    ),
    llm_config={"config_list": config_list},
    code_execution_config=code_execution_config,  # 👈 move here
)

# User Proxy
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").upper(),
)

# --- GroupChat Setup ---
groupchat = GroupChat(
    agents=[researcher, coder, user_proxy],
    messages=[],
    max_round=15
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)

# --- Kick off Dynamic Chat ---
if __name__ == "__main__":
    user_proxy.initiate_chat(
        manager,
        message="Please work together to build an efficient credit card fraud detection pipeline."
    )
