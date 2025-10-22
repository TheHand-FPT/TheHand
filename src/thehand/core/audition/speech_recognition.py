import time
from queue import Queue

import numpy as np
from moonshine_onnx import MoonshineOnnxModel, load_tokenizer
from silero_vad import VADIterator, load_silero_vad
from sounddevice import InputStream

from thehand.core.state import State

DEFAULT_MODEL = "moonshine/tiny"
SAMPLING_RATE = 16000
CHUNK_SIZE = 512
LOOKBACK_CHUNKS = 5
MAX_SPEECH_SECS = 10
MIN_REFRESH_SECS = 0.2
MAX_LINE_LENGTH = 80


class Transcriber:
    def __init__(self, model_name):
        self.model = MoonshineOnnxModel(model_name=model_name)
        self.rate = SAMPLING_RATE
        self.tokenizer = load_tokenizer()
        self.__call__(np.zeros(self.rate, dtype=np.float32))

    def __call__(self, speech):
        tokens = self.model.generate(speech[np.newaxis, :].astype(np.float32))
        text = self.tokenizer.decode_batch(tokens)[0]
        return text


class SpeechRecognition:
    def __init__(self, state: State) -> None:
        self.state = state

        self._model = DEFAULT_MODEL

        print(f"Loading Moonshine model '{self._model}' ...")
        self._transcriber = Transcriber(self._model)
        print("Moonshine model loaded.")

        self._vad_model = load_silero_vad(onnx=True)
        self._vad_iterator = VADIterator(
            model=self._vad_model,
            sampling_rate=SAMPLING_RATE,
            threshold=0.5,
            min_silence_duration_ms=300,
        )

        self._q_data = Queue()
        self._stream = InputStream(
            samplerate=SAMPLING_RATE,
            channels=1,
            blocksize=CHUNK_SIZE,
            dtype=np.float32,
            callback=lambda data, frames, time_, status: self._q_data.put((data.copy().flatten(), status)),
        )

        self.captions = []

        self._recording = False
        self._lookback_size = LOOKBACK_CHUNKS * CHUNK_SIZE
        self._speech = np.empty(0, dtype=np.float32)
        self._start_time: float = 0

    def get_speech_volume(self) -> float:
        if len(self._speech) == 0:
            return 0.0
        return np.sqrt(np.mean(self._speech**2))

    def run(self) -> None:
        print("Speech Recognition ready.")
        self._stream.start()
        self.state.sr_running = True

        while self.state.sr_running:
            chunk, status = self._q_data.get()
            if status:
                print(status)
            self._speech = np.concatenate((self._speech, chunk))
            if not self._recording:
                self._speech = self._speech[-self._lookback_size :]
            speech_dict = self._vad_iterator(chunk)
            if speech_dict:
                if "start" in speech_dict and not self._recording:
                    self._recording = True
                    self._start_time = time.time()
                if "end" in speech_dict and self._recording:
                    self._recording = False
                    self._end_recording()
            elif self._recording:
                if (len(self._speech) / SAMPLING_RATE) > MAX_SPEECH_SECS:
                    self._recording = False
                    self._end_recording()
                    self._soft_reset_vad()
                if (time.time() - self._start_time) > MIN_REFRESH_SECS:
                    translation = self._transcriber(self._speech)
                    if self.state.sr_callback:
                        self.state.sr_callback(translation)
                    self._start_time = time.time()

    def stop(self) -> None:
        self._stream.close()
        if self._recording:
            while not self._q_data.empty():
                chunk, _ = self._q_data.get()
                self._speech = np.concatenate((self._speech, chunk))
            self._end_recording()

    def _soft_reset_vad(self) -> None:
        self._vad_iterator.triggered = False
        self._vad_iterator.temp_end = 0
        self._vad_iterator.current_sample = 0

    def _end_recording(self) -> None:
        text = self._transcriber(self._speech)
        if self.state.sr_callback:
            self.state.sr_callback(text)
        self.captions.append(text)
        self._speech *= 0.0
