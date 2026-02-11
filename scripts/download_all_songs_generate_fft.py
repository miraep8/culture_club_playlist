import pandas as pd
import os
import music_management_functions as mmf # lol, this was actually unintentional but I am rolling with it
from pathlib import Path

def get_all_wav(row, music_dir, download):
    return mmf.extract_yt_url_to_wav(music_dir, row['song_id'], row["youtube_link"], download)

script_location = Path(__file__).resolve()
script_directory = script_location.parent
music_dir = f"{script_directory.parent}\\data\\music"

song_db = pd.read_csv(f"{script_directory.parent}/data/playlist_song_list_recommender_ids.tsv", sep = "\t")
song_db['wav_file'] = song_db.apply(get_all_wav, axis=1, args=(music_dir, False)) # skips download because I already did it :)  Set to true if needed.
song_db.to_csv(f"{script_directory.parent}\\data\\song_info_wit_wav_file.csv", index=False)

fft_rows = []
song_ids = []
base_freq = None
for index, row in song_db.iterrows():
    if os.path.exists(row["wav_file"]):
        print(row['song_id'])
        magnitides, freq = mmf.generate_fft_from_wav(row['wav_file']) # note because of how we do sampling freq should be the same for all songs, we will check
        if base_freq is not None:
            for i, j in zip(base_freq, freq):
                if i != j: print("Issue in freqs")
        else:
            base_freq = freq
        fft_rows.append(magnitides)
        song_ids.append(row['song_id'])
fft_df = pd.DataFrame(fft_rows, columns = freq, index = song_ids)
fft_df.to_csv(f"{script_directory.parent}\\data\\fft_for_each_song_id.csv", index=True)
