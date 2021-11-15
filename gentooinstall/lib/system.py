"""
Classes which configure Gentoo through config files
"""


from typing import List


class MakeConf:
    """
    Represents the /etc/portage/make.conf file
    """

    # pylint: disable=fixme, too-few-public-methods

    def __init__(self) -> None:
        self.use: List[str] = []
        self.features = ["candy", "parallel-fetch", "parallel-install"]
        self.accept_keywords = ""
        # TODO: Wait for config.py and profile.py
