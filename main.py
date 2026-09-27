from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class ConnectorSettings(BaseModel):
    connector_type: str = Field(..., description="Type of the connector")
    connector_config: dict = Field(..., description="Configuration for the connector")   # todo: expand

class ToolSettings(BaseModel):
    tool_name: str = Field(..., description="Name of the tool")     # convention driven
    tool_config: dict = Field(..., description="Configuration for the tool")  # todo: expand

class AgentSettings(BaseModel):
    connectors: List[ConnectorSettings] = Field(..., description="List of connector settings", default_factory=list)
    tools: List[ToolSettings] = Field(..., description="List of tools available to the agent", default_factory=list)
    # etc.

class AgentConfigBase(BaseSettings):
    # todo add all kwargs DataApps sends us.
    agent_id: str = Field(..., description="Unique identifier for the agent")
    model_id: str = Field(..., description="Identifier for the model to be used by the agent")
    settings: AgentSettings = Field(..., description="Settings for the agent", default_factory=AgentSettings)


class AgentBase(ABC):
    def __init__(self, config: AgentConfigBase):
        self.config = config

        self._instantiate_connectors()
        self._instantiate_tools()

    def _instantiate_connectors(self):
        # todo: logic to instantiate connectors based on self.config.settings.connectors
        self.connectors = []

    def _instantiate_tools(self):
        # todo: logic to instantiate tools based on self.config.settings.tools
        self.tools = []

    @classmethod
    def from_config(cls, config: AgentConfigBase):
        # add any additional initialization logic here if needed
        # e.g. lazy import of connector classes based on config.connector_settings.connector_type
        return cls(config)

    @abstractmethod
    def run(self):
        pass
