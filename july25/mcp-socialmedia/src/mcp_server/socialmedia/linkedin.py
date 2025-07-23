"""This module will have necessary functions to post to your linked in
"""
from functools import lru_cache
from linkedin_api.clients.restli.client import RestliClient
from mcp_server.socialmedia.models import ResponseState


PROFILE_RESOURCE = "/userinfo"
UGC_POSTS_RESOURCE = "/ugcPosts"
POSTS_RESOURCE = "/posts"


@lru_cache(maxsize=128)
def get_user_urn(token: str) -> str:
    """This method gets the user urn

    Args:
        token (str): access token
    """
    linkedin_client = RestliClient()
    profile_response = linkedin_client.get(
        resource_path=PROFILE_RESOURCE,
        access_token=token
    )
    return f"urn:li:person:{profile_response.entity['sub']}"


def create_text_post(token, text="Sample text post created with /ugcPosts API"):
    """_summary_

    Args:
        token (_type_): token
        text (str, optional): text. Defaults to "Sample text post created with /ugcPosts API".
    """
    restli_client = RestliClient()
    ugc_posts_create_response = restli_client.create(
        resource_path=UGC_POSTS_RESOURCE,
        entity={
            "author": get_user_urn(token),
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        },
        access_token=token,
    )
    if 100 <= ugc_posts_create_response.status_code <= 399:
        return ResponseState.SUCCESS
    else:
        return ResponseState.FAILURE
