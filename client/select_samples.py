import pandas as pd
import pyaudio
import wave
import soundfile as sf
import os
from config import FORMAT, RATE, CHUNK, RECORD_SECONDS, TOTAL_CHUNKS
from mic_client import audo_client
from threading import Thread

# Create an interface to PortAudio
p = pyaudio.PyAudio()
print("Device count:", p.get_device_count())


def main():
    df = pd.read_csv('../data/asvspoof/ASVspoof2019_LA_asv_protocols/ASVspoof2019.LA.asv.eval.gi.trl.txt',
                     delimiter=' ', names=["speaker", "file", "method", "type"])

    # real_filter = (df["method"] == "bonafide") & (df["type"] == "target")
    # fake_filter = df["method"] != "bonafide"

    # real_sample = df[real_filter].sample(n=100)
    # fake_sample = df[fake_filter].sample(n=100)
    # real_sample = df.loc[df['file'].isin(['LA_E_1350882', 'LA_E_2378020', 'LA_E_3623417', 'LA_E_3913416', 'LA_E_4570967',
    #                                       'LA_E_5130467', 'LA_E_6137569', 'LA_E_6842509', 'LA_E_7824929', 'LA_E_8983191'])]

    fake_sample = df.loc[df['file'].isin( ['LA_E_1375436', 'LA_E_1682845', 'LA_E_2944451', 'LA_E_3294833', 'LA_E_6091662',
                                           'LA_E_6916145', 'LA_E_7524749', 'LA_E_7791735', 'LA_E_8620578', 'LA_E_9877938'])]




    sample_n = 0
    for i, row in fake_sample.iterrows():
        filename = file_to_wav(row['file'])
        if(filename == None):
            continue
        print("sample:", sample_n, filename)
        t = Thread(target=audo_client)
        t.start()

        while(t.is_alive()):
            play_file(filename)

        os.remove("./temp/"+row['file']+".wav")

        # Close and terminate the stream
        sample_n += 1
        if sample_n == 10:
            break

    p.terminate()


def file_to_wav(name):
    fn = "../data/asvspoof/ASVspoof2019_LA_eval/flac/"+name+".flac"
    if(not os.path.exists(fn)):
        return None

    data, samplerate = sf.read(fn)
    filename = "./temp/"+name+".wav"
    sf.write(filename, data, samplerate)
    return filename


def play_file(filename):
    global p
    wf = wave.open(filename, 'rb')

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks
    data = wf.readframes(CHUNK)

    # Play the sound by writing the audio data to the stream
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)
        # print(data)
    stream.close()


main()
