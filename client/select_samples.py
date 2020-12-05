import pandas as pd
import pyaudio
import wave
import soundfile as sf
import os

df = pd.read_csv('../data/asvspoof/ASVspoof2019_LA_asv_protocols/ASVspoof2019.LA.asv.eval.male.trl.txt',
                 delimiter=' ', names=["speaker", "file", "method", "type"])

real_filter = df["method"] == "bonafide"
fake_filter = df["method"] != "bonafide"

df.where(real_filter)

real_sample = df[real_filter].sample(n=10)
fake_sample = df[fake_filter].sample(n=10)

# Create an interface to PortAudio
p = pyaudio.PyAudio()


for i, row in real_sample.iterrows():
    fn = "../data/asvspoof/ASVspoof2019_LA_eval/flac/"+row["file"]+".flac"
    if(not os.path.exists(fn)):
        continue
    data, samplerate = sf.read(fn)
    filename = "./temp/"+row["file"]+".wav"
    sf.write(filename, data, samplerate)
    print(filename)

    # Set chunk size of 1024 samples per data frame
    chunk = 1024

    # Open the sound file
    wf = wave.open(filename, 'rb')
    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks
    data = wf.readframes(chunk)

    # Play the sound by writing the audio data to the stream
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)
        # print(data)
    stream.close()
    os.remove(filename)


# Close and terminate the stream

p.terminate()
