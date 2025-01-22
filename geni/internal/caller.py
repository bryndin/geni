from typing import Any

import requests

from geni.internal.auth import Auth
from geni.internal.ratelimiter import RateLimiter


def remove_none(d: dict[Any, Any]) -> dict[Any, Any]:
    """Remove None values from a dictionary."""
    return {k: v for k, v in d.items() if v is not None}


def flatten_dict(d: dict[Any, Any], parent_key: str = "") -> dict[Any, Any]:
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}[{k}]" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key))
        else:
            items[new_key] = v
    return items


class Caller:
    __HEADER_AUTH: str = "Authorization"

    def __init__(self, api_key: str | None = None) -> None:
        self._auth: Auth = Auth(api_key)
        self._ratelimiter: RateLimiter = RateLimiter()

    def _call(self,
              url: str,
              headers: dict[str, Any] | None = None,
              params: dict[str, Any] | None = None,
              method: str = "get"
              ) -> requests.Response:
        """
        Preprocess params before executing request.
        """
        processed_params = None
        if params is not None:
            # Flatten dicts passed inside params
            processed_params = {}
            for k, v in params.items():
                if isinstance(v, dict):
                    processed_params.update(flatten_dict(v, parent_key=k))
                else:
                    processed_params[k] = v

            # Remove None values
            processed_params = remove_none(processed_params)

        return self._raw_call(url, headers=headers, params=processed_params, method=method)

    def _raw_call(self,
                  url: str,
                  headers: dict[str, Any] | None = None,
                  params: dict[str, Any] | None = None,
                  method: str = "get"
                  ) -> requests.Response:
        """
        Execute request with auth and ratelimiting.
        """
        hdrs = headers or {}
        if self.__HEADER_AUTH not in hdrs:
            hdrs[self.__HEADER_AUTH] = f"Bearer {self._auth.access_token}"

        self._ratelimiter.wait()
        response: requests.Response = requests.request(method, url, headers=hdrs, params=params)
        self._ratelimiter.update(response.headers)

        return response
