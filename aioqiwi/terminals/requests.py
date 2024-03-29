import typing

from ..urls import Urls
from ..requests import Requests

from .models.polygon import Polygon
from .models.terminal import Terminal
from .models.partner import Partner

from ..utils.requests import new_http_session, params_filter


class QiwiMaps(Requests):
    def __init__(self):
        self._session = new_http_session("", atype="application/json;charser=UTF-8")

        self._get = self._session.get

    async def terminals(
        self,
        polygon: Polygon,
        zoom: int = None,
        pop_if_inactive_x_mins: int = 30,
        include_partners: bool = None,
        partners_ids: list = None,
        cache_terminals: bool = None,
        card_terminals: bool = None,
        identification_types: int = None,
        terminal_groups: list = None,
    ) -> typing.List[Terminal]:
        """
        Get map of terminals sent for passed polygon with additional params
        :param polygon: aioqiwi.models.polygon.Polygon model or dict with NW SE <l->l>s dict
        :param zoom: https://tech.yandex.ru/maps/doc/staticapi/1.x/dg/concepts/map_scale-docpage/
        :param pop_if_inactive_x_mins: do not show if terminal was inactive for X minutes default 0.5 hours
        :param include_partners: result will include/exclude partner terminals
        :param partners_ids: Not fixed IDS array look at docs
        :param cache_terminals: result will include/exclude cache-acceptable terminals
        :param card_terminals: result will include/exclude card-acceptable terminals
        :param identification_types: `0` - not identified, `1` - partly identified, `2` - fully identified
        :param terminal_groups: look at QiwiMaps.partners
        :return: list of Terminal instances
        """
        url = Urls.Maps.base

        params = params_filter(
            {
                **polygon.dict,
                "zoom": zoom,
                "activeWithinMinutes": pop_if_inactive_x_mins,
                "withRefillWallet": include_partners,
                "ttpIds": partners_ids,
                "cacheAllowed": cache_terminals,
                "cardAllowed": card_terminals,
                "identificationTypes": identification_types,
                "ttpGroups": terminal_groups,
            }
        )

        async with self._get(url, params=params) as resp:
            return await self._make_return(resp, Terminal, spec_ignore=True)

    async def partners(self) -> typing.List[Partner]:
        """
        Get terminal partners for ttpGroups
        :return: list of TTPGroups
        """

        url = Urls.Maps.ttp_groups

        async with self._get(url) as response:
            return await self._make_return(response, spec_ignore=True)

    # session-related
    async def close(self):
        await self._session.close()

    # `async with` block
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
