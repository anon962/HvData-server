from config import paths
from ..errors import NoResultsError
from hvpytils.classes.hv_session import HvSession
from ..models.user import User
from utils.date_utils import utc_date_to_timestamp

from bs4 import BeautifulSoup
from urlpath import URL

import base64, re, requests, time


class UserParser:
    def __init__(self, session: HvSession):
        self.session = session

    def from_profile(self, id: int) -> User:
        page = self.fetch_page(id=id)
        
        user = self._parse_profile_page(page)
        user.id = id
        user.last_fetch_profile = time.time()

        return user

    def from_search(self, ign: str) -> User:
        url = str(paths.FORUM_ROOT.add_query(act='members'))

        form_data = dict(name=ign,max_results=50)
        resp = self.session.post(url, data=form_data)
        page = BeautifulSoup(resp.text, 'html.parser')

        results = page.select('.ipbtable tr:has(> td.row1)')
        if len(results) == 0: raise NoResultsError
        
        for row in results:
            cells = row.select(':scope > td')

            name = cells[0].text
            group = cells[2].text
            joined = self._parse_joined_date(cells[3].text)

            profile_link = URL(cells[0].select_one('a')['href'])
            id = int(profile_link.form.get_one('showuser'))

            return User(current_name=name, group=group, id=id, joined=joined, last_fetch_profile=time.time())

    # @todo
    def from_post(self):
        pass

    def fetch_page(self, id: int) -> BeautifulSoup:
        url = str(paths.FORUM_ROOT.add_query(showuser=id))
        page = self.session.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup
    
    def _parse_profile_page(self, page: BeautifulSoup) -> User:
        """Returns partially initialized User"""

        avatar = page.select_one('#profilename ~ div:has(> img)').select_one('img')
        avatar = self._fetch_image_as_base64(avatar['src'])

        current_name = page.select_one('#profilename').text
        
        postdetails = page.select_one('.postdetails').stripped_strings
        assert len(postdetails) == 2, f'Expected 2 lines but found {len(postdetails)}'
        group, joined = postdetails

        joined = self._parse_joined_date(joined)

        signature = str(page.select_one('.signature'))

        return User(avatar=avatar, current_name=current_name, group=group, joined=joined, signature=signature)

    def _fetch_image_as_base64(self, url: str) -> str:
        resp = self.session.get(url)
        type = resp.headers['Content-Type']
        content = base64.b64encode(resp.content)
        return f'data:{type};base64,{content}'

    def _parse_joined_date(self, text: str) -> int:
        m = re.search(r'(\d+)-(\w+) (\d+)', text)
        year = int(m.group(3)) + 2000
        month = self._month_to_int(m.group(2))
        return utc_date_to_timestamp(year, month, m.group(1))

    def _month_to_int(self, month: str):
        months = [
            'January', 'February', 'March', 
            'April', 'May', 'June',
            'July', 'August', 'September',
            'October', 'November', 'December'
        ]

        return 1 + months.index(month)