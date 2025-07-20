from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Union

from dotenv import load_dotenv

load_dotenv()


class ModelHfSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MODEL_HF", case_sensitive=False)

    model_name: str
    max_new_tokens: int = 30
    temperature: float = 0.2
    top_k: int = 50
    top_p: float = 0.92
    repetition_penalty: float = 1.2
    do_sample: bool = True
    device: Union[str, int] = "cpu"


class ModelOpenAiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MODEL_OPENAI_", case_sensitive=False)

    openai_api_key: str
    model_name: str
    temperature: float = 0
    max_tokens: Optional[int] = None
    timeout: int = 10.0
    max_retries: Optional[int] = 2


class ModelSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MODEL_SETTINGS_", case_sensitive=False
    )

    use_hf: bool = False
    def get_model_config(self) -> Union[ModelHfSettings, ModelOpenAiSettings]:
        if self.use_hf:
            return ModelHfSettings()
        else:
            return ModelOpenAiSettings()


class AgentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AGENT_", case_sensitive=False)

    log_level: str = "info"
