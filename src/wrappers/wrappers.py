class PhotoWrapper:
    url: str = None
    file: str = None

    def __init__(self, url: str, file: str):
        self.url = url
        self.file = file

    def __repr__(self):
        return f"PhotoWrapper(url={self.url!r}, file={self.file!r})"


class VideoWrapper:
    url: str = None
    file: str = None

    def __init__(self, url, file):
        self.url = url
        self.file = file

    def __repr__(self):
        return f"VideoWrapper(url={self.url!r}, file={self.file!r})"


class MessageWrapper:
    author_id = None
    author_name = None
    text = None
    wall_text = None
    photos = []
    videos = []
    reactor_id = None
    reactor_name = None

    def __init__(self,
                 author_id: int,
                 author_name: str,
                 text: str,
                 wall_text: str,
                 photos: list[PhotoWrapper],
                 videos: list[VideoWrapper],
                 reactor_id: str,
                 reactor_name: str
                 ):
        self.author_id: int = author_id
        self.author_name: str = author_name
        self.text: str = text
        self.wall_text: str = wall_text
        self.photos: list[PhotoWrapper] = photos
        self.videos: list[VideoWrapper] = videos
        self.reactor_id = reactor_id
        self.reactor_name = reactor_name

    def __repr__(self):
        return (
            f"MessageWrapper(\n"
            f"  author_id={self.author_id!r},\n"
            f"  author_name={self.author_name!r},\n"
            f"  text={self.text!r},\n"
            f"  wall_text={self.wall_text!r},\n"
            f"  photos={self.photos!r},\n"
            f"  videos={self.videos!r}\n"
            f"  reactor_id={self.reactor_id!r}\n"
            f"  reactor_name={self.reactor_name!r}\n"
            f")"
        )
