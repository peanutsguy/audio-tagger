# Audiotagger

Using [AudD API](https://audd.io/), this image will try to match an audio file and write the appropiate tags for better identification in Music Players. If it's in some format other than `.flac`, `.m4a`, `.mp3` or `.ogg`, it will transcode it to MP3.

```docker
docker run --rm -v {source_folder}:/app/input -v {destination_folder}:/app/output -e TOKEN={AudD API KEY} ghcr.io/peanutsguy/audio-tagger -f {file_name}
```

The output will have the following scheme:
```
{ArtistName}/{AlbumName}/{TrackNumber} - {SongName}
```