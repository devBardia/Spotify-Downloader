import requests
import json
from dotenv import load_dotenv
import streamlit as st
import os
from io import BytesIO

# Load environment variables
load_dotenv()

# Load the API key from the environment variables
api_key = os.getenv('RAPID_API_KEY')

# Set the page title
st.title(" _Free_:green[ Spotify Downloader]")

# Choose between Song, Album, or Playlist using radio buttons
options = st.radio(
    "Choose one of the options below",
    ["Song 🎶", "Album 💿", "Playlist 📜"]
)

# Get the URL input from the user
user_url = st.text_input("Enter a Spotify URL")

# Function to handle song downloads
def song(user_url):
    api = "https://spotify-downloader9.p.rapidapi.com/downloadSong"
    querystring = {"songId": user_url}
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "spotify-downloader9.p.rapidapi.com"
    }
    
    # Send a request to the API to get song data
    response = requests.get(api, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract song details
        title = data['data']['title']
        artist = data['data']['artist']
        cover = data['data']['cover']
        download_link = data['data']['downloadLink']
    
        # Display song details in two columns
        col1, col2 = st.columns(2)
        with col1:
            st.image(cover, caption="Track Cover", width=250)
        with col2:
            st.write(f"**Song Title:** {title}")
            st.write(f"**Artist:** {artist}")
            
            # Prepare and display the download button with a spinner
            with st.spinner('Preparing download...'):
                file_response = requests.get(download_link)
                file_data = BytesIO(file_response.content)
            st.download_button("Download Song", file_data, file_name=f"{title}.mp3")
    else:
        st.error(f"Failed to fetch song details. Status code: {response.status_code}")

# Function to handle album downloads
def album(user_url):
    api = "https://spotify-downloader9.p.rapidapi.com/downloadAlbum"
    querystring = {"albumId": user_url}
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "spotify-downloader9.p.rapidapi.com"
    }
    
    # Send a request to the API to get album data
    response = requests.get(api, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        
        # Check if 'data' key exists
        if 'data' in data:
            # Extract album details
            album_details = data['data'].get('albumDetails') or data['data'].get('playlistDetails')
            if not album_details:
                st.error("Album details not found in the response.")
                return
            
            # Extract album information
            album_title = album_details.get('title', 'N/A')
            album_artist = album_details.get('artist', 'N/A')
            release_date = album_details.get('releaseDate', 'N/A')
            cover = album_details.get('cover', '')
    
            # Display album details in two columns
            col1, col2 = st.columns(2)
            with col1:
                st.image(cover, caption="Album Cover", width=250)
            with col2:
                st.write(f"**Album Title:** {album_title}")
                st.write(f"**Artist:** {album_artist}")
                st.write(f"**Release Date:** {release_date}")
    
            # Display the table headers
            col1, col2, col3 = st.columns([4, 4, 2])
            col1.write("**Song Title**")
            col2.write("**Artist**")
            col3.write("**Download**")
    
            # Display the album tracks
            if 'songs' in data['data']:
                songs = data['data']['songs']
                for index, song in enumerate(songs):
                    title = song['title']
                    artist = song['artist']
                    download_link = song['downloadLink']
    
                    col1, col2, col3 = st.columns([4, 4, 2])
                    col1.write(title)
                    col2.write(artist)
    
                    # Prepare and display the download button with a spinner
                    try:
                        with col3:
                            with st.spinner('Preparing download...'):
                                file_response = requests.get(download_link)
                                file_data = BytesIO(file_response.content)
                            col3.download_button("Download", file_data, file_name=f"{title}.mp3", key=f"download_{index}")
                    except Exception as e:
                        col3.write("Download failed")
            else:
                st.warning("No songs found in album data.")
        else:
            st.error("The 'data' key was not found in the response.")
    else:
        st.error(f"Failed to fetch album details. Status code: {response.status_code}")

# Function to handle playlist downloads
def playlist(user_url):
    # Extract the playlist ID from the URL
    import re
    def extract_playlist_id(url):
        match = re.search(r'playlist/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        else:
            st.error("Invalid Spotify playlist URL.")
            return None
    
    playlist_id = extract_playlist_id(user_url)
    if not playlist_id:
        return  # Exit the function if playlist ID is invalid
    
    # API endpoint for playlist download
    api = "https://spotify-downloader9.p.rapidapi.com/downloadPlaylist"
    querystring = {"playlistId": playlist_id}
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "spotify-downloader9.p.rapidapi.com"
    }
    
    # Send a request to the API to get playlist data
    response = requests.get(api, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'data' in data and 'playlistDetails' in data['data']:
            playlist_details = data['data']['playlistDetails']
            
            # Extract playlist information
            playlist_title = playlist_details.get('title', 'N/A')
            playlist_artist = playlist_details.get('artist', 'N/A')
            cover = playlist_details.get('cover', '')
    
            # Display playlist details in two columns
            col1, col2 = st.columns(2)
            with col1:
                st.image(cover, caption="Playlist Cover", width=250)
            with col2:
                st.write(f"**Playlist Title:** {playlist_title}")
                st.write(f"**Artist:** {playlist_artist}")
    
            # Display the table headers
            col1, col2, col3 = st.columns([4, 4, 2])
            col1.write("**Song Title**")
            col2.write("**Artist**")
            col3.write("**Download**")
    
            # Display the playlist tracks
            if 'songs' in data['data']:
                songs = data['data']['songs']
                for index, song in enumerate(songs):
                    title = song['title']
                    artist = song['artist']
                    download_link = song['downloadLink']
    
                    col1, col2, col3 = st.columns([4, 4, 2])
                    col1.write(title)
                    col2.write(artist)
    
                    # Prepare and display the download button with a spinner
                    try:
                        with col3:
                            with st.spinner('Preparing download...'):
                                file_response = requests.get(download_link)
                                file_data = BytesIO(file_response.content)
                            col3.download_button("Download", file_data, file_name=f"{title}.mp3", key=f"download_{index}")
                    except Exception as e:
                        col3.write("Download failed")
            else:
                st.warning("No songs found in playlist data.")
        else:
            st.error("Playlist details not found in the response.")
    else:
        st.error(f"Failed to fetch playlist details. Status code: {response.status_code}")

# Main logic to determine which function to call based on the URL
if user_url:
    # Check if the user has chosen Song, Album, or Playlist and ensure the URL matches the correct type
    if options == "Song 🎶" and "track" in user_url:
        song(user_url)
    elif options == "Album 💿" and "album" in user_url:
        album(user_url)
    elif options == "Playlist 📜" and "playlist" in user_url:
        playlist(user_url)
    else:
        st.error(f"The URL you entered doesn't match the selected option: {options}")
