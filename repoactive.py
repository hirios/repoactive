from datetime import datetime
from threading import Thread
import lxml.html
import requests


MEMBERS_PATH = '/network/members'
GIT_DOMAIN = 'https://github.com'


def string_to_datetime(date_string: str) -> datetime:
    date_string = date_string.split('T')[0]
    date_string =  datetime.strptime(date_string, '%Y-%m-%d')
    return date_string


def datetetime_to_string(lista: list[datetime, str]) -> list[str, str]:
    lista[0] = lista[0].strftime('%d-%m-%Y')
    return lista


def add_domain(PATH: str) -> str:
    return GIT_DOMAIN + PATH + '/commit/'


class RepoActive:
    def __init__(self):
        self.forks = None # type -> Map
        self.last_commits = [] # type -> [datetime]


    def get_forks(self, url: str) -> None:
        member_url = url + MEMBERS_PATH
        response = requests.get(member_url)
        parser = lxml.html.fromstring(response.text)
        self.forks = map(add_domain, parser.xpath('//div[@class="repo"]/a[3]/@href'))


    def get_last_commit(self, fork: str) -> None: 
        response = requests.get(fork)
        parser = lxml.html.fromstring(response.text)
        date_string = parser.xpath('//relative-time[@datetime]/@datetime')[0]
        date_string = string_to_datetime(date_string)
        self.last_commits.append([date_string, fork])


    def search(self, url: str) -> list:
        self.get_forks(url)
        threads = [Thread(target=self.get_last_commit, args=(x,)) for x in self.forks]
        for method in (Thread.start, Thread.join):
            for thread in threads:
                method(thread)

        self.last_commits = sorted(self.last_commits, key = lambda x: x[0])
        self.last_commits = list(map(datetetime_to_string, self.last_commits))
        return self.last_commits


if __name__ == '__main__':
    url = 'https://github.com/Anorov/cloudflare-scrape'
    repo = RepoActive()
    lista = repo.search(url)
    print(lista)
