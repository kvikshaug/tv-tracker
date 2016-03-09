from datetime import datetime

class SeriesSearchResult():
    def __init__(self, tvdbid, name, overview, banner, first_aired, imdb):
        self.tvdbid = tvdbid
        self.name = name
        self.overview = overview
        self.banner = banner
        self.first_aired = first_aired
        self.imdb = imdb

    def __str__(self):
        return "%s: %s" % (self.tvdbid, self.name)

    @staticmethod
    def from_xml(xml):
        # Required fields (i.e. throw exception if missing)
        tvdbid = xml.find("seriesid").text
        name = xml.find("SeriesName").text

        # Optional fields
        overview = xml.findtext("Overview", default="")
        banner = xml.findtext("banner", default="")
        try:
            first_aired = datetime.strptime(xml.findtext("FirstAired", default=""), "%Y-%m-%d").date()
        except ValueError:
            first_aired = None
        imdb = xml.findtext("IMDB_ID", default="")

        return SeriesSearchResult(tvdbid, name, overview, banner, first_aired, imdb)

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

    def __str__(self):
        return "%s (tvdb id: %s)" % (self.name, self.tvdbid)

    @staticmethod
    def from_xml(xml):
        series = xml.find("Series")
        tvdbid = series.findtext("id", default="")
        name = series.findtext("SeriesName", default="")
        overview = series.findtext("Overview", default="")
        status = series.findtext("Status", default="")
        banner = series.findtext("banner", default="")
        try:
            first_aired = datetime.strptime(series.findtext("FirstAired", default=""), "%Y-%m-%d").date()
        except ValueError:
            first_aired = None
        imdb = series.findtext("IMDB_ID", default="")

        series = Series(
            tvdbid=tvdbid,
            name=name,
            overview=overview,
            status=status,
            banner=banner,
            first_aired=first_aired,
            imdb=imdb,
        )

        for e in xml.findall("Episode"):
            season = int(e.findtext("SeasonNumber", default=""))
            if season == 0:
                # Ignore specials for now
                continue

            episode = int(e.findtext("EpisodeNumber", default=""))
            try:
                air_date = datetime.strptime(e.findtext("FirstAired", default=""), "%Y-%m-%d").date()
            except ValueError:
                air_date = None

            series.episodes.append(Episode(
                season=season,
                episode=episode,
                air_date=air_date,
            ))

        return series

class Episode():
    def __init__(self, season, episode, air_date):
        self.season = season
        self.episode = episode
        self.air_date = air_date

    def __str__(self):
        return "%sx%s" % (self.season, self.episode)
