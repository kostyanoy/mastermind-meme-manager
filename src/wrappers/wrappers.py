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

    def __init__(self, author_id: str, author_name: str, text: str, wall_text: str, photos: list[PhotoWrapper], videos: list[VideoWrapper]):
        self.author_id: str = author_id
        self.author_name: str = author_name
        self.text: str = text
        self.wall_text: str = wall_text
        self.photos: list[PhotoWrapper] = photos
        self.videos: list[VideoWrapper] = videos

    def __repr__(self):
        return (
            f"MessageWrapper(\n"
            f"  author_id={self.author_id!r},\n"
            f"  author_name={self.author_name!r},\n"
            f"  text={self.text!r},\n"
            f"  wall_text={self.wall_text!r},\n"
            f"  photos={self.photos!r},\n"
            f"  videos={self.videos!r}\n"
            f")"
        )
