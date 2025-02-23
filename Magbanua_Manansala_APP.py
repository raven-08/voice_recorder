import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import time
import threading


class VoiceRecorder:
    def __init__(
        self,
        frames_per_buffer=3200,
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
    ):
        self.frames_per_buffer = frames_per_buffer
        self.format = format
        self.channels = channels
        self.rate = rate
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.is_paused = False
        self.record_thread = None
        self.recording_finished_event = threading.Event()

    def startRecording(self, seconds=8):
        self.is_recording = True
        self.is_paused = False
        self.frames = []
        self.recording_finished_event.clear()
        def recordingFunc(seconds):
            self.stream = self.pa.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.frames_per_buffer,
            )
            print("Recording started")
            second_tracking = 0
            second_count = 0
            try:
                while self.is_recording and second_count < seconds:
                    if not self.is_paused:
                        data = self.stream.read(self.frames_per_buffer)
                        self.frames.append(data)
                        second_tracking += 1
                        if second_tracking == int(self.rate / self.frames_per_buffer):
                            second_count += 1
                            second_tracking = 0
                            print(f"Time Left: {seconds - second_count} seconds")
                    else:
                        time.sleep(0.1)
                print("Recording finished, time limit reached")

            except Exception as e:
                print(f"Error during recording: {e}")
            finally:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
                self.recording_finished_event.set()
                self.is_recording = False

        self.record_thread = threading.Thread(target=recordingFunc, args=(seconds,))
        self.record_thread.daemon = True
        self.record_thread.start()

    def pauseRecording(self):
        if self.is_recording and not self.is_paused:
            self.is_paused = True
            print("Recording paused")

    def resumeRecording(self):
        if self.is_recording and self.is_paused:
            self.is_paused = False
            print("Recording resumed")

    def stopRecording(self):
        if self.is_recording:
            self.is_recording = False
            self.recording_finished_event.wait()
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            print("Recording stopped")

    def saveRecording(self, filename="record.wav"):
        self.stopRecording()
        print("Recording saved")
        obj = wave.open(filename, "wb")
        obj.setnchannels(self.channels)
        obj.setsampwidth(self.pa.get_sample_size(self.format))
        obj.setframerate(self.rate)
        obj.writeframes(b"".join(self.frames))
        obj.close()

    def plotRecording(self, filename="record.wav"):
        file = wave.open(filename, "rb")
        sample_freq = file.getframerate()
        frames = file.getnframes()
        signal_wave = file.readframes(-1)
        file.close()
        time = frames / sample_freq
        audio_array = np.frombuffer(signal_wave, dtype=np.int16)
        times = np.linspace(0, time, num=frames)
        plt.figure(figsize=(12, 6))
        plt.plot(times, audio_array, color="royalblue", linewidth=1)
        plt.fill_between(times, audio_array, color="royalblue", alpha=0.4)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.xlabel("Time (s)", fontsize=12, fontweight="bold")
        plt.ylabel("Amplitude", fontsize=12, fontweight="bold")
        plt.xlim(0, time)
        plt.title(
            "Voice Recorder Visual Representation",
            fontsize=14,
            fontweight="bold",
            color="darkred",
        )

        plt.gcf().canvas.manager.set_window_title("Audio Plot | Voice Recorder")
        plt.show()

    def __del__(self):
        self.pa.terminate()
