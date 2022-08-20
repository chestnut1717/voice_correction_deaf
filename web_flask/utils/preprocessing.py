from scipy.io import wavfile
import noisereduce as nr
import numpy as np
from pydub import AudioSegment


class DimentionOverflow(Exception):
    def __init__(self):
      pass

    def __str__(self):
      return "The dimention is greater than 2"

def convert_dim(data):
  assert type(data) == np.ndarray, "Data ype is wrong"
  
  if data.ndim == 1:
    return data
  
  elif data.ndim == 2:
    return data[:, 0]
  
  else:
    raise DimentionOverflow

# wav 변환 method
def to_wav(file_path, file_name):
    audSeg = AudioSegment.from_file(file_path)
    audSeg.export(f"{file_name}.wav", format="wav")
    print(f'{file_name}.wav convert success!')

def reduce_noise(file_path, file_name):
    rate, data = wavfile.read(file_path)
    data_r = convert_dim(data)

    # noise 제거 작업
    reduced_noise = nr.reduce_noise(y=data_r, sr=rate)
    wavfile.write(f"{file_name}_reducednoise.wav", rate, reduced_noise)