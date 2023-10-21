import requests
import tidalapi
from typing import List, Tuple
import argparse
import logging

def get_deezer_tracks(deezer_user_id: str) -> List[Tuple[str, str]]:
    """
    This function fetches the favourite tracks of a user from Deezer.

    :param deezer_user_id: The user id of the Deezer user.
    :return: A list of tuples, where each tuple contains the title and artist of a track.
    """
    url = f"https://api.deezer.com/user/{deezer_user_id}/tracks"
    tracks = []

    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tracks.extend(
                [(track["title"], track["artist"]["name"]) for track in data["data"]]
            )
            url = data.get("next")
        else:
            print(f"Failed to fetch tracks. HTTP status code: {response.status_code}")
            break

    print(f"Found {len(tracks)} tracks")
    return tracks

def get_deezer_artists(deezer_user_id: str) -> List[str]:
    """
    This function fetches the favourite artists of a user from Deezer.

    :param deezer_user_id: The user id of the Deezer user.
    :return: A list of artists.
    """
    url = f"https://api.deezer.com/user/{deezer_user_id}/artists"
    artists = []

    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            artists.extend([artist["name"] for artist in data["data"]])
            url = data.get("next")
        else:
            print(f"Failed to fetch artists. HTTP status code: {response.status_code}")
            break

    print(f"Found {len(artists)} artists")
    return artists

def search_track_on_tidal(session: tidalapi.Session, track_title: str, track_artist: str) -> str:
    """
    This function searches a track on Tidal.

    :param session: The Tidal session object.
    :param track_title: The title of the track.
    :param track_artist: The artist of the track.
    :return: The id of the track if found, else None.
    """
    #remove (feat. ...) from track title because it's generics in deezer
    if "(feat." in track_title:
        track_title = track_title.split("(feat.")[0]
    track_title = track_title.lower()
    track_artist = track_artist.lower()
    
    search_results = session.search(query=f"{track_title} {track_artist}")["tracks"]

    if not search_results:
        print(f"No results found for track: {track_title} by {track_artist}")
        user_search = input("Enter the track you want to search for: ")
        search_results = session.search(query=user_search)["tracks"]

        if not search_results :
            logging.info(f"No results found from search for track: {track_title} by {track_artist}")
            return None

        while search_results:
            for i, track in enumerate(search_results):
                print(f"{i + 1}) {track.name} : {track.artist.name} : {track.duration/60}min")
            user_choice = input("Choose the track number or 's' to skip: ")
            if user_choice.lower() == 's':
                return None
            else:
                return search_results[int(user_choice) - 1].id

    try:
        return search_results[0].id
    except:
        print(f"Could not find match for track: {track_title} by {track_artist}")
        return None

def search_artist_on_tidal(session: tidalapi.Session, artist_name: str) -> str:
    """
    This function searches an artist on Tidal.

    :param session: The Tidal session object.
    :param artist_name: The name of the artist.
    :return: The id of the artist if found, else None.
    """
    artist_name = artist_name.lower()
    
    search_results = session.search(query=artist_name)["artists"]

    if not search_results :
        print(f"No results can be identified for artist: {artist_name}")
        user_search = input("Enter the artist you want to search for: ")
        search_results = session.search(query=user_search)["artists"]

        while search_results:
            for i, artist in enumerate(search_results):
                print(f"{i + 1}) {artist.name}")
            user_choice = input("Choose the artist number or 's' to skip: ")
            if user_choice.lower() == 's':
                return None
            else:
                return search_results[int(user_choice) - 1].id

    try:
        return search_results[0].id
    except:
        print(f"Could not find match for artist: {artist_name}")
        return None

def add_track_to_tidal_favorites(session: tidalapi.Session, track_id: str) -> None:
    """
    This function adds a track to the user's favourites on Tidal.

    :param session: The Tidal session object.
    :param track_id: The id of the track.
    """
    session.user.favorites.add_track(track_id)

def add_artist_to_tidal_favorites(session: tidalapi.Session, artist_id: str) -> None:
    """
    This function adds an artist to the user's favourites on Tidal.

    :param session: The Tidal session object.
    :param artist_id: The id of the artist.
    """
    session.user.favorites.add_artist(artist_id)

def remove_favorite_tracks_from_tidal(session: tidalapi.Session) -> None:
    """
    This function removes all tracks from the user's favourites on Tidal.

    :param session: The Tidal session object.
    """
    print("Starting to remove tracks")
    fav_tracks = session.user.favorites.tracks()
    for track in fav_tracks:
        try :
            session.user.favorites.remove_track(track.id)
        except:
            print(f"Could not remove track: {track.full_name}")
    print("Finished removing tracks")

def remove_favorite_artists_from_tidal(session: tidalapi.Session) -> None:
    """
    This function removes all artists from the user's favourites on Tidal.

    :param session: The Tidal session object.
    """
    print("Starting to remove artists")
    fav_artists = session.user.favorites.artists()
    for artist in fav_artists:
        try:
            session.user.favorites.remove_artist(artist.id)
        except:
            print(f"Could not remove artist: {artist.name}")
    print("Finished removing artists")


def remove_all_favorites_from_tidal(session: tidalapi.Session) -> None:
    """
    This function removes all tracks and artists from the user's favourites on Tidal.

    :param session: The Tidal session object.
    """
    remove_favorite_tracks_from_tidal(session)
    remove_favorite_artists_from_tidal(session)

def transfer_tracks(deezer_user_id: str, tidal_session: tidalapi.Session) -> None:
    """
    This function transfers the favourite tracks of a user from Deezer to Tidal.

    :param deezer_user_id: The user id of the Deezer user.
    """
    # Get tracks from Deezer
    tracks = get_deezer_tracks(deezer_user_id)

    # Transfer tracks to Tidal
    for track_title, track_artist in tracks:
        track_id = search_track_on_tidal(tidal_session, track_title, track_artist)
        if track_id:
            add_track_to_tidal_favorites(tidal_session, track_id)
    print("Finished transferring tracks")

def transfer_artists(deezer_user_id: str, tidal_session: tidalapi.Session) -> None:
    """
    This function transfers the favourite artists of a user from Deezer to Tidal.

    :param deezer_user_id: The user id of the Deezer user.
    """
    # Get artists from Deezer
    artists = get_deezer_artists(deezer_user_id)

    # Transfer artists to Tidal
    for artist_name in artists:
        artist_id = search_artist_on_tidal(tidal_session, artist_name)
        if artist_id:
            add_artist_to_tidal_favorites(tidal_session, artist_id)
    print("Finished transferring artists")

def transfer_all(deezer_user_id: str, tidal_session: tidalapi.Session) -> None:
    """
    This function transfers the favourite tracks and artists of a user from Deezer to Tidal.

    :param deezer_user_id: The user id of the Deezer user.
    """
    transfer_tracks(deezer_user_id, tidal_session)
    transfer_artists(deezer_user_id, tidal_session)
    
if __name__ == "__main__":
    print('''
   ___    _____   _____  
  |   \  |_   _| |_   _| 
  | |) |   | |     | |   
  |___/   _|_|_   _|_|_  
_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-' 
          
    @Author: ugomeguerditchian
    ''')
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Transfer favorites from Deezer to Tidal')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-tAll', action='store_true', help='Transfer both tracks and album from Deezer ID to Tidal account and keep the chronological order')
    group.add_argument('-tT', action='store_true', help='Transfer just tracks')
    group.add_argument('-tA', action='store_true', help='Transfer just artists')
    group.add_argument('-rAll', action='store_true', help='Remove all favorites from a Tidal account')
    group.add_argument('-rT', action='store_true', help='Remove just favorite tracks from Tidal account')
    group.add_argument('-rA', action='store_true', help='Remove just favorite artists from Tidal account')

    args = parser.parse_args()
    if args.tAll:
        # Code to transfer both tracks and artists
        deezer_user_id = input("Enter your Deezer user id: ")
        session = tidalapi.Session()
        session.login_oauth_simple()
        transfer_all(deezer_user_id, session)
    elif args.tT:
        # Code to transfer just tracks
        deezer_user_id = input("Enter your Deezer user id: ")
        session = tidalapi.Session()
        session.login_oauth_simple()
        transfer_tracks(deezer_user_id, session)
    elif args.tA:
        # Code to transfer just artists
        deezer_user_id = input("Enter your Deezer user id: ")
        session = tidalapi.Session()
        session.login_oauth_simple()
        transfer_artists(deezer_user_id, session)
    elif args.rAll:
        # Code to remove all favorites
        session = tidalapi.Session()
        session.login_oauth_simple()
        remove_all_favorites_from_tidal(session)
    elif args.rT:
        # Code to remove just favorite tracks
        session = tidalapi.Session()
        session.login_oauth_simple()
        remove_favorite_tracks_from_tidal(session)
    elif args.rA:
        # Code to remove just favorite artists
        session = tidalapi.Session()
        session.login_oauth_simple()
        remove_favorite_artists_from_tidal(session)