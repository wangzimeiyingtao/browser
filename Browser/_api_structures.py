from typing import Optional, TypedDict, Literal, List


class Cookie(TypedDict, total=False):
    name: str
    value: str
    url: Optional[str]
    domain: Optional[str]
    path: Optional[str]
    expires: Optional[float]
    httpOnly: Optional[bool]
    secure: Optional[bool]
    sameSite: Optional[Literal["Lax", "None", "Strict"]]


class HttpCredentials(TypedDict):
    username: str
    password: str


class LocalStorageEntry(TypedDict):
    name: str
    value: str


class OriginState(TypedDict):
    origin: str
    localStorage: List[LocalStorageEntry]


class Position(TypedDict):
    x: float
    y: float


class ProxySettings(TypedDict, total=False):
    server: str
    bypass: Optional[str]
    username: Optional[str]
    password: Optional[str]


class ViewportSize(TypedDict):
    width: int
    height: int


class StorageState(TypedDict, total=False):
    cookies: Optional[List[Cookie]]
    origins: Optional[List[OriginState]]
