from datetime import datetime

class SeriesSearchResult():
    def __init__(self, id, name, overview, banner, first_aired, imdb):
        self.id = id
        self.name = name
        self.overview = overview
        self.banner = banner
        self.first_aired = first_aired
        self.imdb = imdb

    def __str__(self):
        return "%s: %s" % (self.id, self.name)

    @staticmethod
    def from_xml(xml):
        # Required fields (i.e. throw exception if missing)
        id = xml.find("seriesid").text
        name = xml.find("SeriesName").text

        # Optional fields
        overview = xml.findtext("Overview", default="")
        banner = xml.findtext("banner", default="")
        try:
            first_aired = datetime.strptime(xml.findtext("FirstAired", default=""), "%Y-%m-%d")
        except ValueError:
            first_aired = None
        imdb = xml.findtext("IMDB_ID", default="")

        return SeriesSearchResult(id, name, overview, banner, first_aired, imdb)

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
            first_aired = datetime.strptime(series.findtext("FirstAired", default=""), "%Y-%m-%d")
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
            season = e.findtext("SeasonNumber", default="")
            if season == "0":
                # Ignore specials for now
                continue

            number = e.findtext("EpisodeNumber", default="")
            first_aired = e.findtext("FirstAired", default="")

            try:
                first_aired = datetime.strptime(first_aired, "%Y-%m-%d")
            except (ValueError, TypeError):
                first_aired = None

            series.episodes.append(Episode(
                season=season,
                number=number,
                first_aired=first_aired,
            ))

        return series

class Episode():
    def __init__(self, season, number, first_aired):
        self.season = season
        self.number = number
        self.first_aired = first_aired

    def __str__(self):
        return "%sx%s" % (self.season, self.number)
