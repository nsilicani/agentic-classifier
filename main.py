import os

from agentic_text_cls import AgenticTextCls
from settings import ModelSettings, AgentSettings
from logging_config import setup_logging, logger

from huggingface_hub import login

login(os.getenv("HF_ACCESS_TOKEN"))


def main():
    agentic_config = AgentSettings()
    setup_logging(agentic_config)
    configs = ModelSettings()
    ac = AgenticTextCls(model_settings=configs, logger=logger, generate_new_metadata_idx=False)

    ## Comment and uncomment the propositions to your hearts content
    texts = [
        "The month is October.",
        "The year is 2023.",
        "One of the most important things that I didn't understand about the world as a child was the degree to which the returns for performance are superlinear.",
        # "Teachers and coaches implicitly told us that the returns were linear.",
        # "I heard a thousand times that 'You get out what you put in.'",
    ]
    for text in texts:
        ac.classify_text(text=text)
    
    logger.info(f"Dict with topics:\n{ac.topics}")


if __name__ == "__main__":
    main()
