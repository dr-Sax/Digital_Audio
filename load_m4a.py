from pydub import AudioSegment
from pydub import playback

audio = AudioSegment.from_file('monsoon.m4a')
rev = AudioSegment.reverse(audio)

from pydub import silence
leading_silence = silence.detect_silence(audio)[0][1]
ending_silence = silence.detect_silence(audio)[-1][0]
print(leading_silence, ending_silence)
riff = audio[leading_silence:ending_silence]
rev = riff.reverse()
c = rev.overlay(riff)

print(c.raw_data[0:9])
from pydub.utils import get_array_type
import array

bit_depth = c.sample_width * 8
array_type = get_array_type(bit_depth)

numeric_array = array.array(array_type, c._data)
print(numeric_array[0])

print(int.from_bytes(b'/xdb/', "big"))