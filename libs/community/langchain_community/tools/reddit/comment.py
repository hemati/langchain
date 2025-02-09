"""Tool for commenting on Reddit submissions."""

from typing import Optional, Type

from langchain_community.utilities.reddit_commenter import RedditCommentAPIWrapper
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class RedditCommentSchema(BaseModel):
    """Input schema for posting a comment on Reddit."""
    submission_id: str = Field(
        description="The ID of the Reddit submission to comment on. "
                    "For instance, 'abc123' in the URL /r/test/comments/abc123/..."
    )
    comment_text: str = Field(
        description="The text of the comment to post."
    )


class RedditCommentRun(BaseTool):  # type: ignore[override, override]
    """Tool that comments on a Reddit submission."""

    name: str = "reddit_comment"
    description: str = (
        "A tool that posts a comment to a given Reddit submission by its ID. "
        "Useful when you want to respond to a specific post."
    )
    api_wrapper: RedditCommentAPIWrapper = Field(default_factory=RedditCommentAPIWrapper)  # type: ignore[arg-type]
    args_schema: Type[BaseModel] = RedditCommentSchema

    def _run(
        self,
        submission_id: str,
        comment_text: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool to comment on a Reddit post."""
        return self.api_wrapper.run(
            submission_id=submission_id,
            comment_text=comment_text,
        )
