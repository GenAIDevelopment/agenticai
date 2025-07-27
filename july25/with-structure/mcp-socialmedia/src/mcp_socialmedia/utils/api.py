"""This module will have reusable utility functions
"""
from typing import Any, Union, Optional, Dict, Tuple
import httpx


async def fetch(
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 10.0
) -> Union[Dict[str, Any], Dict[str, str]]:
    """This method is used to fetch/get the rest api

    Args:
        url (api url): _description_
        headers (Optional[Dict[str, str]], optional): headers. Defaults to None.
        timeout (float, optional): time. Defaults to 10.0.

    Returns:
        Union[Dict[str, Any], Dict[str, str]]: response
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(
            url,
            headers=headers)
        return response.json()


async def post(
        url: str,
        payload: Optional[Dict[str, Any]],
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 10.0,
        expected_status: Tuple[int, int] = (200, 299)) -> Union[Dict[str, Any], Dict[str, str]]:
    """This method posts the api

    Args:
        url (str): url
        payload (Optional[Dict[str, Any]]): data
        headers (Optional[Dict[str, str]]): headers
        timeout (float, optional): Timeout Defaults to 10.0.
        expected_status (Tuple[int, int], optional): Expected Status. Defaults to (200, 299).

    Raises:
        httpx.HTTPStatusError: if status code not in range

    Returns:
        Union[Dict[str, Any], Dict[str, str]]: response 
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            url, json=payload,
            headers=headers)
        if not expected_status[0] <= response.status_code <= expected_status[1]:
            raise httpx.HTTPStatusError(
                f"Status {response.status_code} not in expected range of " +
                "{expected_status[0]} - {expected_status[1]}",
                request=response.request,
                response=response
            )
        return response.json()
