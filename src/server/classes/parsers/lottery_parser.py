from hvpytils import HvSession
from ..errors import NoResultsError, UnparsablePageError
from ..models.lottery import Lottery, LotteryItem, LotteryType
from ..models.user import User
from .user_parser import UserParser

from bs4 import BeautifulSoup
from urlpath import URL

import logging, re

LOG = logging.getLogger('LotteryParser')


class LotteryParser:
    # timestamps for when the first lottos started
    START_DATES = {
        LotteryType.ARMOR: 1396094400,
        LotteryType.WEAPON: 1379116800
    }

    def __init__(self, session: HvSession):
        self.uninitialized_users: dict[str, LotteryItem] = dict()
        self.session = session

    def fetch_one(self, type: LotteryType, id: int):
        """
        Returns a Lottery and the corresponding LotteryItem's
        The LotteryItem's are **not** fully initialized. Please remember to call intialize_winners() after all fetch_one's are completed.
        """

        lotto, items, winners = self._fetch_one(type, id, self.session)
        for item,user in zip(items,winners):
            self.uninitialized_users.setdefault(user, []).append(item)
        
        return lotto

    @classmethod
    def _fetch_one(cls, type: LotteryType, id: int, session: HvSession) -> tuple[Lottery, list[LotteryItem], list[str]]:
        page = cls.fetch_page(type=type, id=id, session=session)

        lotto = cls._parse_lotto(page)
        lotto.id = id
        lotto.type = type

        items, winners = cls._parse_lotto_items(page)
        for it in items:
            it.id = id
            it.type = type
            it.lottery = lotto

        return lotto, items, winners

    def initialize_winners(self):
        """
        Initialize winners on each item. 
        This function is isolated from fetch_one in order to reduce the number of requests by taking advantage of repeated winners.
        """

        user_map: dict[str, User] = dict()
        keys = sorted(list(self.uninitialized_users.keys()))
        LOG.debug(f'Initializing users {user_map}')
        for ign in keys:
            if ign not in user_map:
                try:
                    user = UserParser(session=self.session).from_search(ign)
                    user_map[ign] = user
                except NoResultsError:
                    user_map[ign] = None
        
        for ign, item_lst in self.uninitialized_users.items():
            if user_map[ign] is not None:
                for item in item_lst:
                    item.winner = user_map[ign]
            else:
                strings = [f'{item.quantity}x {item.name}' for item in item_lst]
                LOG.error(f'Could not link user [{ign}] to items [{", ".join(strings)}]')

        for k in keys:
            del self.uninitialized_users[k]
            
        return self

    @classmethod
    def get_latest(cls, type: LotteryType, session: HvSession) -> tuple[BeautifulSoup, int]:
        """Get (html,id) for current lottery"""

        page = session.get(type.value)
        soup = BeautifulSoup(page.text, 'html.parser')

        prev_button = soup.select_one('img[src="/y/shops/lottery_prev_a.png"]')
        prev_url = re.search(r"'(http.*)'", prev_button['onclick'])
        prev_url = URL(prev_url.group(1))

        prev_id = prev_url.form.get_one('lottery')
        prev_id = int(prev_id)
        
        return soup, prev_id+1

    @classmethod
    def fetch_page(cls, type: LotteryType, id: int, session: HvSession) -> BeautifulSoup:
        url = type.value + f'&lottery={id}'
        page = session.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup

    @classmethod
    def _parse_lotto(cls, page: BeautifulSoup) -> Lottery:
        """Return partially initialized Lottery"""

        text = page.select_one('#rightpane > div:nth-child(5)').text
        m = re.search(r'You hold \d+ of (\d+) sold tickets.', text)
        tickets = int(m.group(1))

        return Lottery(tickets=tickets)

    @classmethod
    def _parse_lotto_items(cls, page: BeautifulSoup) -> tuple[list[LotteryItem], list[str]]:
        """Return partially intialized list of LotteryItem's"""

        prizes = []
        raw_winners = []

        # parse page
        equip_name = page.select_one('#lottery_eqname').text

        divs = page.select('#leftpane > div:last-child > div')
        assert len(divs) == 9, f'Expected 9 divs but found {len(divs)}'

        texts = [x.text for x in divs]
        if not all(':' in x for x in texts):
            raise UnparsablePageError(f'Missing "Winner: ..." string in lottery texts. Maybe you\'re trying to parse the latest lottery? Or a lottery with an invalid id? {texts}')
        texts = [x.split(': ') for x in texts]
        texts = [x[1] for x in texts]

        # grand prize
        equip = LotteryItem(name=equip_name, place=0, quantity=1, raw_winner=texts[0])
        prizes.append(equip)
        raw_winners.append(equip.raw_winner)

        # consolation prizes
        items = [texts[2*i + 1] for i in range(4)]
        raw_winners.extend(texts[2*i + 2] for i in range(4))

        for i,it in enumerate(items):
            quantity, name = it.split(' ', maxsplit=1)
            conslation_prize = LotteryItem(name=name, place=i+1, quantity=int(quantity), raw_winner=raw_winners[i+1])
            prizes.append(conslation_prize)
        
        # return
        return prizes, raw_winners

    @classmethod
    def get_start(cls, id: int, type: LotteryType) -> float:
        return cls.START_DATES[type] + 86400*(id-1)