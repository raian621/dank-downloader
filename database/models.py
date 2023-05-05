from sqlalchemy import String, ForeignKey, Integer, Text, Column, Numeric, Table
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    __allow_unmapped__ = True

class User(Base):
    __tablename__ = "users"

    id =       Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(30))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f"User {self.id}: {self.username}"


class MediaPlaylistRelation(Base):
    __tablename__ = "media_association_table"
    playlist_id = Column(ForeignKey("playlists.id"), primary_key=True)
    media_id =    Column(ForeignKey("media.id"), primary_key=True)


class Playlist(Base):
    __tablename__ = "playlists"

    id =          Column(Integer, primary_key=True, autoincrement=True)
    playlength =  Column(Integer)
    name =        Column(String(30))
    description = Column(Text)
    media =       relationship("Media", secondary="media_association_table")
    user_id =     Column(Integer, ForeignKey("users.id"))
    user =        relationship("User", backref="playlists")

    def __init__(self, **kwargs):
        super(Playlist, self).__init__(**kwargs)

    def __repr__(self):
        return f"Playlist {self.name} [{self.playlength}]"


class Media(Base):
    __tablename__ = "media"

    id =         Column(Integer, primary_key=True, autoincrement=True)
    playlength = Column(Integer)
    extension =  Column(String(10))
    url =        Column(String(256))
    filepath =   Column(String(256))
    title =      Column(String(64))
    subtitle =   Column(String(64))
    videodata =  relationship("VideoData", backref="media", uselist=False)
    user_id =    Column(Integer, ForeignKey("users.id"))
    user =       relationship("User", backref="media")
    media_hash = Column(String(64))
    playlist =   relationship("Playlist", secondary="media_association_table")

    def __init__(self, **kwargs):
        super(Media, self).__init__(**kwargs)

    def __repr__(self):
        return f"Media {self.title}"
    

class VideoData(Base):
    __tablename__ = "videodata"

    id =         Column(Integer, primary_key=True, autoincrement=True)
    media_id =   Column(Integer, ForeignKey("media.id"))
    resolution = Column(String(10))
    fps =        Column(Numeric)

    def __init__(self, **kwargs):
        super(VideoData, self).__init__(**kwargs)


class AudioData(Base):
    __tablename__ = "audiodata"

    id =          Column(Integer, primary_key=True, autoincrement=True)
    media_id =    Column(Integer, ForeignKey("media.id"))
    quality =     Column(String(20))
    sample_rate = Column(Integer)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f"AudioData {self.quality} {self.sample_rate}"