import requests
from bs4 import BeautifulSoup, element
from pprint import pprint


def getBeautifulSoupitems(url: str) -> tuple[element.ResultSet, element.ResultSet]:
    res: requests.models.Response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(res.text, "html.parser")
    links: element.ResultSet = soup.select(".titleline")
    vote_subtext: element.ResultSet = soup.select(".subtext")
    return links, vote_subtext


def sort_stories(hackernewslist: list) -> list:
    return sorted(hackernewslist, key=lambda k: k["votes"], reverse=True)


def create_hackernews(links_list, vote_list):
    hn = []
    for idx, item in enumerate(links_list):
        title = item.getText()
        url = item.find('a', href=True).get("href", None)
        vote = vote_list[idx].select_one(".score")
        if vote is not None:
            score = int(vote.getText().replace(" points", ""))
            if score >= 100:
                hn.append({"title": title, "link": url, "votes": score})
    return sort_stories(hn)


def main():
    linksPage1: element.ResultSet
    linksPage2: element.ResultSet
    vote_subtext_page1: element.ResultSet
    vote_subtext_page2: element.ResultSet
    linksPage1, vote_subtext_page1 = getBeautifulSoupitems("https://news.ycombinator.com/news")
    linksPage2, vote_subtext_page2 = getBeautifulSoupitems("https://news.ycombinator.com/news?p=2")
    superlist: list = linksPage1 + linksPage2
    supervotes: list = vote_subtext_page1 + vote_subtext_page2
    hn: list = create_hackernews(superlist, supervotes)
    pprint(hn)


if __name__ == '__main__':
    main()
