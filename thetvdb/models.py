class SeriesSearchResult():
    def __init__(self, id, name, overview, banner, first_aired, imdb):
        self.id = id
        self.name = name
        self.overview = overview
        self.banner = banner
        self.first_aired = first_aired
        self.imdb = imdb

class Series():
    def __init__(self, tvdbid, name, overview, status, banner, first_aired, imdb):
        self.tvdbid = tvdbid
        self.name = name
        self.overview = overview
        self.status = status
        self.banner = banner
        self.first_aired = first_aired
        self.imdb = imdb
        self.episodes = []

    def add_episode(self, season):
        self.episodes.append(season)

class Episode():
    def __init__(self, season, number, first_aired):
        self.season = season
        self.number = number
        self.first_aired = first_aired
