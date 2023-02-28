from sqlalchemy import String, ForeignKey, Integer, Text, Column, Numeric, Table
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[String] = mapped_column(String(30))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f"User {self.id}: {self.username}"


media_association_table = Table(
    "media_association_table",
    Base.metadata,
    Column("playlist", ForeignKey("playlists.id"), primary_key=True, nullable=True),
    Column("media", ForeignKey("media.id"), primary_key=True, nullable=True)
)


class Playlist(Base):
    __tablename__ = "playlists"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    playlength: Mapped[Integer] = mapped_column(Integer)
    name: Mapped[String] = mapped_column(String(30))
    description: Mapped[Text] = mapped_column(Text)
    media: Mapped["Media"] = relationship("Media", secondary="media_association_table", backref="playlist")
    user_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", backref="playlists", uselist=True)

    def __init__(self, playlength, name, description, user):
        self.playlength = playlength
        self.name = name
        self.description = description
        self.user = user
        self.user_id = user.id

    def __repr__(self):
        return f"Playlist {self.name} [{self.playlength}]"


class Media(Base):
    __tablename__ = "media"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    playlength: Mapped[String] = mapped_column(String(10))
    extension: Mapped[String] = mapped_column(String(10))
    url: Mapped[String] = mapped_column(String(256))
    filepath: Mapped[String] = mapped_column(String(256))
    title: Mapped[String] = mapped_column(String(64))
    subtitle: Mapped[String] = mapped_column(String(64))
    videodata: Mapped["VideoData"] = relationship("VideoData", backref="media")
    user_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", backref="media", uselist=True)

    def __init__(self, playlength, extension, url, filepath, title, subtitle, user):
        self.playlength = playlength
        self.extension = extension
        self.url = url
        self.filepath = filepath
        self.title = title
        self.subtitle = subtitle
        self.user = user
        self.user_id = user.id

    def __repr__(self):
        return f"Media {self.title}"
    

class VideoData(Base):
    __tablename__ = "videodata"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    media_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("media.id"))
    resolution: Mapped[String] = mapped_column(String(10))
    fps: Mapped[Numeric] = mapped_column(Numeric)

    def __init__(self, resolution, fps, media):
        self.resolution = resolution
        self.fps = fps
        self.media = media

class AudioData(Base):
    __tablename__ = "audiodata"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    media_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("media.id"))
    quality: Mapped[String] = mapped_column(String(20))
    sample_rate: Mapped[Integer] = mapped_column(Integer)

    def __init__(self, quality : str, sample_rate : int):
        self.quality = quality
        self.sample_rate = sample_rate

    def __repr__(self):
        return f"AudioData {self.quality} {self.sample_rate}"