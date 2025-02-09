"""Wrapper for the Reddit API (Commenting)"""

from typing import Any, Dict, Optional

from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, model_validator


class RedditCommentAPIWrapper(BaseModel):
    """Wrapper for Reddit API to comment on Reddit submissions.

    To use, set the following environment variables:
      - REDDIT_CLIENT_ID
      - REDDIT_CLIENT_SECRET
      - REDDIT_USER_AGENT
      - REDDIT_USERNAME
      - REDDIT_PASSWORD

    Alternatively, all six can be supplied as named parameters in the constructor:
      - reddit_client_id
      - reddit_client_secret
      - reddit_user_agent
      - reddit_username
      - reddit_password

    Example:
        .. code-block:: python

            from langchain_community.utilities import RedditCommentAPIWrapper

            comment_tool = RedditCommentAPIWrapper(
                reddit_client_id="my_id",
                reddit_client_secret="my_secret",
                reddit_user_agent="my_user_agent",
                reddit_username="my_username",
                reddit_password="my_password",
            )
            response = comment_tool.run(
                submission_id="abc123",
                comment_text="Hello from my script!"
            )
            print(response)
    """

    reddit_client: Any

    # Values required to access Reddit API via praw
    reddit_client_id: Optional[str]
    reddit_client_secret: Optional[str]
    reddit_user_agent: Optional[str]
    reddit_username: Optional[str]
    reddit_password: Optional[str]

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate that the API credentials exist in environment or are provided,
        and check that the praw module is present.
        """
        reddit_client_id = get_from_dict_or_env(
            values, "reddit_client_id", "REDDIT_CLIENT_ID"
        )
        values["reddit_client_id"] = reddit_client_id

        reddit_client_secret = get_from_dict_or_env(
            values, "reddit_client_secret", "REDDIT_CLIENT_SECRET"
        )
        values["reddit_client_secret"] = reddit_client_secret

        reddit_user_agent = get_from_dict_or_env(
            values, "reddit_user_agent", "REDDIT_USER_AGENT"
        )
        values["reddit_user_agent"] = reddit_user_agent

        # For commenting, we need username/password to authenticate a script-type app
        reddit_username = get_from_dict_or_env(
            values, "reddit_username", "REDDIT_USERNAME"
        )
        values["reddit_username"] = reddit_username

        reddit_password = get_from_dict_or_env(
            values, "reddit_password", "REDDIT_PASSWORD"
        )
        values["reddit_password"] = reddit_password

        try:
            import praw
        except ImportError:
            raise ImportError(
                "praw package not found. Please install with: pip install praw"
            )

        reddit_client = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent,
            username=reddit_username,
            password=reddit_password,
        )
        values["reddit_client"] = reddit_client

        return values

    def run(self, submission_id: str, comment_text: str) -> str:
        """Comment on a Reddit submission by its ID, returning a link to the new comment."""
        # Fetch the submission by ID
        submission = self.reddit_client.submission(id=submission_id)
        # Post the comment
        new_comment = submission.reply(comment_text)
        # Return a permalink to view the new comment
        return f"Comment posted! View at: https://www.reddit.com{new_comment.permalink}"
