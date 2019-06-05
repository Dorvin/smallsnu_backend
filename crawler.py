def cseSeminar():
    import requests
    from bs4 import BeautifulSoup
    import re
    from snumap.models import Map, Spot, Edge, Shuttle, Route, Building, Restaurant, Seminar, Lecture, Post
    req = requests.get('https://cse.snu.ac.kr/seminars')
    if not req.ok:
        print("Error: request to cseSeminar has failed")
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    thisYearSeminars = soup.select(
        '#block-system-main > div > div > div > div:nth-child(1)'
    )[0]
    year = thisYearSeminars.find('h2').text
    seminarList = thisYearSeminars.select('ul > li')
    for seminar in seminarList:
        divs = seminar.select('li > div')
        title = divs[2].text.strip()
        link = "https://cse.snu.ac.kr"+divs[2].find('a')['href']
        try:
            existing_seminar = Seminar.objects.get(link=link)
        except Seminar.DoesNotExist:
            pass
        else:
            continue
        detailReq = requests.get(link)
        detailHtml = detailReq.text
        detailSoup = BeautifulSoup(detailHtml, 'html.parser')
        detailContents = detailSoup.select('div.content div.content')[0].select('div.field-items > div.even')
        talkerData = detailContents[0].select('div.content')[0]
        talker = talkerData.find(text=True)
        talkerFrom = talkerData.find('div')
        for br in talkerFrom.find_all("br"):
            br.replace_with("-")
        if talkerFrom.text is not None:
            talker = talker+"-"+talkerFrom.text
        time = detailContents[1].text
        where = detailContents[2].text
        description = detailContents[4].text
        codePattern = re.compile('\d+')
        codeMatch = codePattern.search(where)
        code = ""
        if codeMatch:
            code = codeMatch.group()
        else:
            print("no code is found in where information")
        try:
            building = Building.objects.get(code__startswith=code)
        except Building.DoesNotExist:
            print("error: no such a Building code:"+code+"/")
        except Building.MultipleObjectsReturned:
            print("error: ther is duplicated Building that has the code:"+code)
        Seminar(
            title=title,
            talker=talker,
            description=description,
            building=building,
            where=where,
            time=time,
            link=link
        ).save()

cseSeminar()

def econSeminar():
    import requests
    from bs4 import BeautifulSoup
    import re
    from snumap.models import Map, Spot, Edge, Shuttle, Route, Building, Restaurant, Seminar, Lecture, Post
    req = requests.get('http://econ.snu.ac.kr/research/seminars/list-view')
    if not req.ok:
        print("Error: request to econSeminar has failed")
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    Seminars = soup.select(
        '#zcmsprogram'
    )[0]
    seminarList = Seminars.select('div.seminarlist.clearfix')
    for seminar in seminarList:
        link = "http://econ.snu.ac.kr"+seminar.select('a')[0]['href']
        try:
            existing_seminar = Seminar.objects.get(link=link)
        except Seminar.DoesNotExist:
            pass
        else:
            continue
        detailReq = requests.get(link)
        detailReq.encoding = 'UTF-8'
        detailHtml = detailReq.text
        detailSoup = BeautifulSoup(detailHtml, 'html.parser')
        detailContents = detailSoup.select('div.seminarview')[0]
        title = detailContents.find('h3').text
        talker = detailContents.select('div')[2].text[9:]
        time = detailContents.select('div')[1].text[6:]
        where = detailContents.select('div')[3].text[10:]
        description = "No description."
        codePattern = re.compile('\d+')
        codeMatch = codePattern.search(where)
        code = ""
        if codeMatch:
            code = codeMatch.group()
        else:
            print("no code is found in where information")
        try:
            building = Building.objects.get(code=code)
        except Building.DoesNotExist:
            print("error: no such a Building code:"+code+"/")
        except Building.MultipleObjectsReturned:
            print("error: ther is duplicated Building that has the code:"+code)
        Seminar(
            title=title,
            talker=talker,
            description=description,
            building=building,
            where=where,
            time=time,
            link=link
        ).save()

econSeminar()