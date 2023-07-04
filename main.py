import json
import os
import subprocess
import bencode
import requests

magnet_url = "magnet:?xt=urn:btih:CD19BFCF6F08E58E0ED4A452B7A0265DC76D25DF&dn=Hijack.2023.S01E01.WEB.x264-PHOENiX&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce&tr=udp%3A%2F%2Fipv4.tracker.harry.lu%3A80%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.birkenwald.de%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce&tr=udp%3A%2F%2Fopentor.org%3A2710%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fuploads.gamecoast.net%3A6969%2Fannounce&tr=https%3A%2F%2Ftracker.foreverpirates.co%3A443%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce"

def set_url(slug, link_id, tunnel_url):
    apikey = ""
    path = slug
    url = f"https://api.short.io/links/{link_id}"
    domain = "a8r1.short.gy"

    payload = json.dumps({"allowDuplicates": False, "domain": domain, "path": path, "originalURL": tunnel_url})
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': apikey
    }

    requests.request("POST", url, data=payload, headers=headers)


def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)

def getTorrentName(filename):
    """List name of a torrent from the corresponding .torrent file."""
    with open(filename, "rb") as fin:
        torrent = bencode.bdecode(fin.read())
        files = {}
        for i,file in enumerate(torrent["info"]["files"]):
            extension = file['path'][0].split('.')[-1]
            if extension == 'mkv' or extension == 'mp4' or extension =='avi':
                files[file['length']] = [file['path'][0],i]

        myKeys = list(files.keys())
        myKeys.sort()
        max_size = max(myKeys)
    return files[max_size]

command = ["webtorrent","--out","temp","downloadmeta", magnet_url]
run_command(command)
files = os.listdir("temp")

torrent = f"temp/{files[0]}"
torrentName = getTorrentName(torrent)
print(torrentName)
os.remove(torrent)

stream_url = f"https://yogendrasinghx.jprq.live/{torrentName[1]}/{torrentName[0]}"
print(f"Streaming URL : {stream_url}")
#set_url("ystream", "lnk_3hg7_9dCPkpTPcHo", stream_url)
print(f"Short Streaming URL : https://a8r1.short.gy/ystream")

command = ["webtorrent","--quiet", magnet_url,"--vlc"]
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print("Error executing command:", e)
run_command(command)