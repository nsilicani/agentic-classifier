from logging import Logger

import uuid

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

# See https://python.langchain.com/docs/integrations/llms/huggingface_pipelines/
from langchain_huggingface.llms import HuggingFacePipeline

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from prompts import (
    FIND_RELEVANT_TOPIC_PROMPT,
    GET_NEW_TOPIC_SUMMARY_PROMPT,
    GET_NEW_TOPIC_LABEL_PROMPT,
    UPDATE_TOPIC_SUMMARY_PROMPT,
    UPDATE_TOPIC_LABEL_PROMPT,
)
from schema import TopicId
from settings import ModelHfSettings, ModelOpenAiSettings, ModelSettings


# Inspired by: https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/agentic_chunker.py
class AgenticTextCls:
    def __init__(
        self,
        model_settings: ModelSettings,
        logger: Logger,
        topic_id_len: int = 4,
        generate_new_metadata_idx: bool = True,
    ):
        self.logger = logger
        self.topics = {}
        self.topic_id_len = topic_id_len

        # Whether or not to update/refine summaries and titles as you get new information
        self.generate_new_metadata_idx = generate_new_metadata_idx

        # Initialize topic outline injected to the prompt
        self.topic_outline = ""

        # LLM set up
        self.model_settings = model_settings
        if model_settings.use_hf:
            model_hf_settings = model_settings.get_model_config()
            self.llm = self.create_pipeline(model_hf_settings)
            raise NotImplementedError("Structured output not yet implemented for HF")
        else:
            model_openai_settings = model_settings.get_model_config()
            self.logger.info(f"Istantiate model: {model_openai_settings.model_name}")
            self.llm = self.initialize_model_openai(model_openai_settings)
            self.structured_llm = self.llm.with_structured_output(schema=TopicId)

    def initialize_model_openai(
        self, model_openai_settings: ModelOpenAiSettings
    ) -> ChatOpenAI:
        return ChatOpenAI(
            model=model_openai_settings.model_name,
            api_key=model_openai_settings.openai_api_key,
            temperature=model_openai_settings.temperature,
            max_tokens=model_openai_settings.max_tokens,
            timeout=model_openai_settings.timeout,
            max_retries=model_openai_settings.max_retries,
        )

    def create_pipeline(
        self, model_hf_settings: ModelHfSettings
    ) -> HuggingFacePipeline:
        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_hf_settings.model_name)
        model = AutoModelForCausalLM.from_pretrained(model_hf_settings.model_name)

        # Configure tokenizer
        tokenizer.pad_token = tokenizer.eos_token

        # Create generation pipeline with carefully tuned parameters
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=model_hf_settings.max_new_tokens,  # Shorter response for more focus
            temperature=model_hf_settings.temperature,  # Very low temperature for more deterministic output
            top_k=model_hf_settings.top_k,  # Limit vocabulary choices
            top_p=model_hf_settings.top_p,  # Nucleus sampling
            repetition_penalty=model_hf_settings.repetition_penalty,  # Prevent repetition
            do_sample=model_hf_settings.do_sample,
            pad_token_id=tokenizer.eos_token_id,
            device=model_hf_settings.device,
        )

        return HuggingFacePipeline(pipeline=pipe)

    def classify_text(self, text: str) -> None:
        self.logger.info(f"Processing: `{text}`")
        if not self.topics:
            self.logger.info("No topics, creating a new one")
            self._create_new_topic(text)

        topic_id = self._find_relevant_topic(text)
        if topic_id:
            self._add_text_to_topic(topic_id, text)
            return None
        else:
            self._create_new_topic(text)

    def _find_relevant_topic(self, text: str):
        current_topic_outline = self.topic_outline
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", FIND_RELEVANT_TOPIC_PROMPT),
                (
                    "user",
                    "Current Topics:\n--Start of current topics--\n{current_topic_outline}\n--End of current topics--",
                ),
                (
                    "user",
                    "Determine if the following text should belong to one of the topics outlined:\n{text}",
                ),
            ]
        )

        prompt = prompt_template.invoke(
            {"text": text, "current_topic_outline": current_topic_outline}
        )
        topic_found = self.structured_llm.invoke(prompt)
        # self.logger.info(f"Found topic: `{topic_found}`")
        # TODO Add a Validation step here
        if topic_found and topic_found.topic_id != "No topics":
            self.logger.info(f"Found topic: `{topic_found}`")
            # parsed_out = topic_found.additional_kwargs["parsed"]
            topic_id_found = topic_found.topic_id
            return topic_id_found
        return None

    def _update_topic_summary(self, text: str) -> str:
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", UPDATE_TOPIC_SUMMARY_PROMPT),
                (
                    "user",
                    "Determine the summary of the new topic that this text will go into:\n{text}",
                ),
            ]
        )
        chain = prompt_template | self.llm
        new_topic_summary = chain.invoke({"text": text}).content
        return new_topic_summary

    def _update_topic_label(self, summary: str) -> str:
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", UPDATE_TOPIC_LABEL_PROMPT),
                (
                    "user",
                    "Determine the label of the topic that this summary belongs to:\n{summary}",
                ),
            ]
        )
        chain = prompt_template | self.llm
        new_topic_label = chain.invoke({"summary": summary}).content
        return new_topic_label

    def _add_text_to_topic(self, topic_id: str, text: str) -> None:
        self.topics[topic_id]["texts"].append(text)
        # TODO Implement the following methods to update topic summaries and labels
        if self.generate_new_metadata_idx:
            self.topics[topic_id]["summary"] = self._update_topic_summary(text)
            self.topics[topic_id]["label"] = self._update_topic_label(
                self.topics[topic_id]["summary"]
            )

    def _update_topic_outline(self, single_topic_outline: str) -> None:
        self.topic_outline += single_topic_outline

    def _get_new_topic_summary(self, text: str) -> str:
        PROMPT = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    GET_NEW_TOPIC_SUMMARY_PROMPT,
                ),
                (
                    "user",
                    "Determine the summary of the new topic that this proposition will go into:\n{text}",
                ),
            ]
        )

        runnable = PROMPT | self.llm
        new_topic_summary = runnable.invoke({"text": text}).content

        return new_topic_summary

    def _get_new_topic_label(self, new_topic_summary) -> str:
        PROMPT = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    GET_NEW_TOPIC_LABEL_PROMPT,
                ),
                (
                    "user",
                    "Determine the title of the topic that this summary belongs to:\n{new_topic_summary}",
                ),
            ]
        )

        runnable = PROMPT | self.llm

        new_topic_label = runnable.invoke(
            {"new_topic_summary": new_topic_summary}
        ).content

        return new_topic_label

    def _create_new_topic(self, text: str) -> None:
        new_topic_id = str(uuid.uuid4())[: self.topic_id_len]
        new_topic_summary = self._get_new_topic_summary(text)
        new_topic_label = self._get_new_topic_label(new_topic_summary)

        self.topics[new_topic_id] = {
            "topic_id": new_topic_id,
            "summary": new_topic_summary,
            "label": new_topic_label,
            "texts": [text],
        }
        self.logger.info(f"Created new topic ({new_topic_id}): `{new_topic_label}`")

        single_topic_outline = f"""Topic ID: {new_topic_id}\nTopic Label: {new_topic_summary}\nTopic Summary: {new_topic_label}\n\n"""
        self._update_topic_outline(single_topic_outline)
