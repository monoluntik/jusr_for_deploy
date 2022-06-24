from selenium.webdriver.common.by import By
import time
from my_api import data_convert
from abc import ABC, abstractmethod
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
 
class MarathonBotDriver(ABC):

    def __init__(self, sport_id):
        self.sport_id = sport_id

    def get_match_data(self, match):
        history_button = match.find_elements(
            by=By.CLASS_NAME, value='member-area-buttons-label')
        if history_button == []:
            return match.text
        history_button[0].click()
        time.sleep(2)
        text = match.text.split('\n')
        return self.analysis(data_convert(text))

    def get_league_data(self, league):
        league = league.find_elements(by=By.CLASS_NAME, value='coupon-row')
        return "\n".join([k for match in league if (k:=self.get_match_data(match))])

    def get_live_matches(self):
        options = Options()
        options.headless = True
        options.add_argument('--window-size=1920, 1080')
        options.add_argument('user-agent=Chrome/103.0 (Windows NT 10.0; Win64; x64)')
        self.driver_ = uc.Chrome(options=options, use_subprocess=True)
        url = f'https://www.marathonbet.ru/su/live/{self.sport_id}'
        self.driver_.get(url)
        time.sleep(10)
        self.current_url = self.driver_.current_url
        if self.current_url != url:
            return f'no live mathces   {url}'
        leagues = self.driver_.find_elements(
            by=By.CLASS_NAME, value='foot-market')[:7]
        return "\n".join([self.get_league_data(league) for league in leagues])

    @abstractmethod
    def analysis(self, data_dict):
        pass



