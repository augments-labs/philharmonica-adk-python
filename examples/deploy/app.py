"""A deployable agent for the ``philharmonica deploy`` walkthrough (see README.md).

Exposes ``agent`` so a container can serve it with
``philharmonica serve --agent app:agent``. There is no ``__main__`` guard on
purpose: the deployment workflow runs this module through the CLI / the
generated image, not by executing the file directly.
"""

from philharmonica.adk.agents.agent import Agent

agent = Agent(
    name="support",
    system_prompt="You are a concise, helpful support assistant.",
)
