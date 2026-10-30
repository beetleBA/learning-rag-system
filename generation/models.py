from pydantic import BaseModel, Field, ConfigDict


class AnswerDraft(BaseModel):
    """Внутренний формат ответа, генерируемого LLM."""

    model_config = ConfigDict(extra="forbid")

    answer_markdown: str = Field(
        description="Ответ пользователю в формате Markdown."
    )

    used_source_ids: list[str] = Field(
        description="Идентификаторы источников, использованных при ответе."
    )

    insufficient_information: bool = Field(
        description=(
            "True, если найденной информации недостаточно "
            "для полноценного ответа."
        )
    )
