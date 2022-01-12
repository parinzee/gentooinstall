"""
Module which contain classes and functions to control Gentoo
"""

import random
import re
from typing import List, Literal

import requests
from bs4 import BeautifulSoup  # type: ignore
from rich.progress import Progress

from .exceptions import NetworkError
from .general import run_command


class MakeConf:
    """
    Represents the /etc/portage/make.conf file
    """

    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        self.use: List[str] = []
        self.features = ["candy", "parallel-fetch", "parallel-install"]
        self.accept_keywords = ""


# Weirdly, pylint thinks str has been redfined.
# pylint: disable=redefined-builtin
def install_stage3(
    type: Literal["openrc", "systemd", "desktop-openrc", "desktop-systemd"],
    path: str = "/mnt/gentoo/stage3.tar.xz",
    optimal_mirror: bool = True,
) -> None:
    """
    Downloads an amd64 stage3 tarball into the path parameter.
    Then unpacks it using a tar command.
    And finally, deletes the tarball.

    - type: Kind of stage3 tarball to download
    - path: optional absolute path,
    - optimal_mirror: optional use of 3rd party api to find geolocation
    """
    # pylint: disable=too-many-locals,invalid-name,too-many-branches,too-many-statements
    with Progress(expand=True) as progress:
        downloads_page = requests.get("https://www.gentoo.org/downloads/")
        downloads_soup = BeautifulSoup(downloads_page.text, "html.parser")
        download_url = downloads_soup.find(
            "a", {"href": re.compile(fr".*stage3-amd64-{type}-.*\.tar\.xz")}
        )
        final_url = download_url.get("href")

        if optimal_mirror:
            # Get IP Geolocation
            finding_mirror = progress.add_task("[yellow]Finding optimal mirror...")
            ip = requests.get("https://api.ipify.org").text
            progress.advance(finding_mirror, 10)

            continent_code = requests.get(
                f"http://ip-api.com/json/{ip}?fields=status,message,continentCode"
            ).json()["continentCode"]
            progress.advance(finding_mirror, 10)

            if continent_code == "AF":
                continent = "Africa"
            elif continent_code == "AS":
                continent = "Asia"
            elif continent_code == "EU":
                continent = "Europe"
            elif continent_code == "NA":
                continent = "North America"
            elif continent_code == "SA":
                continent = "South America"
            elif continent_code == "OC":
                continent = "Australia and Oceania"
            else:
                raise NetworkError("API Error")
            # Use the continent to get a random download link
            mirrors_page = requests.get("https://www.gentoo.org/downloads/mirrors/")
            mirrors_soup = BeautifulSoup(mirrors_page.text, "html.parser")
            progress.advance(finding_mirror, 30)
            mirrors_url = (
                mirrors_soup.find("h2", string=continent)
                .find_next("table")
                .find_all("a", attrs={"href": re.compile(r"http.*://.*")})
            )
            progress.advance(finding_mirror, 30)

            # Do some link black magic
            chosen_mirror_url: str = random.choice(mirrors_url).get("href")
            if chosen_mirror_url.endswith("/"):
                final_url = (
                    chosen_mirror_url + "releases/" + download_url.get("data-relurl")
                )
            else:
                final_url = (
                    chosen_mirror_url + "/releases/" + download_url.get("data-relurl")
                )
            progress.advance(finding_mirror, 20)

        # Download the file from the link (writing bytes basically)
        with open(path, "wb") as f:
            resp = requests.get(final_url, stream=True)
            content_length_header = resp.headers.get("content-length")
            if isinstance(content_length_header, str):
                content_length = int(content_length_header)
            else:
                raise NetworkError(f"No content-length from: {final_url}")
            download_stage3 = progress.add_task(
                "[yellow]Downloading stage3 tarball...", total_length=100
            )
            download_length = 0
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    download_length += len(chunk)
                    f.write(chunk)
                    progress.update(
                        download_stage3,
                        completed=int(100 * download_length / content_length),
                    )

        # Extract the tar file to the specified path
        extracting_stage3 = progress.add_task(
            "[yellow]Extracting stage3...", start=False
        )
        extract_to = "/".join(path.split("/")[:-1])
        run_command(
            f"tar xpvf {path} --xattrs-include='*.*' --numeric-owner -C {extract_to}"
        )
        # Delete the stage3 tar file to save space
        run_command(f"rm -rf {path}")
        progress.start_task(extracting_stage3)
        progress.advance(extracting_stage3, 100)
