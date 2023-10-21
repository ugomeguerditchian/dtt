# Project Description

The purpose of this project is to create a script that can transfer favorite tracks and artists from Deezer to Tidal while maintaining the same chronological order.

I was tired of payfull services that transfered my favorites but without keeping the chronological order. I wanted to keep the same order as I had in Deezer. So I decided to create my own script to do the job.

[**Thanks to tidalapi for the Tidal API wrapper**](https://github.com/tamland/python-tidal)

## Features

* Transfer both tracks and album from Deezer ID to Tidal account
* Transfer just tracks
* Transfer just artists
* Remove all favorites from a Tidal account
* Remove just favorite tracks from Tidal account
* Remove just favorite artists from Tidal account
* **The script will ask you for tracks that are not available to search for alternatives**

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

- requests
- tidalapi

You can install these dependencies using pip :

```bash
pip install -r requirements.txt
```
Or : 

```bash
pip install requests tidalapi
```

## Usage

To use the script, follow these steps:

* Obtain your Deezer user ID, which can be found in the URL of your Deezer profile page.
* Run the script using the followings commands:
python dtt.py -h

```bash
python ddt.py -h
usage: dtt.py [-h] (-tAll | -tT | -tA | -rAll | -rT | -rA)

Transfer favorites from Deezer to Tidal

options:
  -h, --help  show this help message and exit
  -tAll       Transfer both tracks and album from Deezer ID to Tidal account
  -tT         Transfer just tracks
  -tA         Transfer just artists
  -rAll       Remove all favorites from a Tidal account
  -rT         Remove just favorite tracks from Tidal account
  -rA         Remove just favorite artists from Tidal account

```

The script will then ask you to enter your Deezer user ID and Tidal credentials.

**Be aware that Tidal will pop up a browser window to ask for your credentials !**

**You may have some trakcs or artists that are not the same** , tidal sometimes just return things that have nothing to do with the search (usually means that the music is not available on Tidal).

## Conclusion

This script allows you to transfer your favorite tracks and artists from Deezer to Tidal while preserving the chronological order. Feel free to customize and enhance the script according to your needs.

Please note that this README.md file provides a brief overview of the project. For more detailed information, refer to the code comments and documentation within the script itself.

If you have any questions or need further assistance, feel free to reach out. 

Happy transferring and listening ! 🎧🎶
