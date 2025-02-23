import customtkinter as ctk
from CTkMessagebox import CTkMessagebox as mb
from PIL import Image, ImageSequence
from Magbanua_Manansala_APP import VoiceRecorder

class VoiceRecorderGUI(ctk.CTkFrame):
    ctk.set_appearance_mode("light")
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        self.parent = master
        self.poppins = ctk.CTkFont(
            family="Poppins",
        )
        self.parent.title("Voice Recorder")
        self.parent.geometry("1000x600")
        self.recorder = VoiceRecorder()
        self.is_paused = False
        self.is_darked = False

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frame = ctk.CTkFrame(self, corner_radius=10)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.hero_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=10,
            width=450,
            height=400,
            fg_color="transparent",
        )
        self.hero_frame.place(x=360, y=70)

        self.dark_icon = ctk.CTkImage(
            light_image=Image.open("icons/moon.png"),
            dark_image=Image.open("icons/moon_dark.png"),
            size=(20, 20),
        )
        self.sun_icon = ctk.CTkImage(
            light_image=Image.open("icons/sun.png"),
            dark_image=Image.open("icons/sun_dark.png"),
            size=(20, 20),
        )

        self.mic_icon = ctk.CTkImage(
            size=(20, 20),
            light_image=Image.open("icons/mic_dark.png"),
            dark_image=Image.open("icons/mic.png"),
        )
        self.pause_icon = ctk.CTkImage(
            light_image=Image.open("icons/pause.png"),
            dark_image=Image.open("icons/pause_dark.png"),
            size=(20, 20),
        )
        self.play_icon = ctk.CTkImage(
            light_image=Image.open("icons/play.png"),
            dark_image=Image.open("icons/play_dark.png"),
            size=(20, 20),
        )
        self.stop_icon = ctk.CTkImage(
            light_image=Image.open("icons/stop.png"),
            dark_image=Image.open("icons/stop_dark.png"),
            size=(20, 20),
        )
        self.save_icon = ctk.CTkImage(
            light_image=Image.open("icons/save.png"),
            dark_image=Image.open("icons/save_dark.png"),
            size=(20, 20),
        )
        self.plot_icon = ctk.CTkImage(
            light_image=Image.open("icons/plot.png"),
            dark_image=Image.open("icons/plot_dark.png"),
            size=(20, 20),
        )
        self.logo_image = ctk.CTkImage(
            light_image=Image.open("utils/logo.png"), size=(400, 350)
        )
        self.dark_button = ctk.CTkButton(
            self.frame,
            image=self.dark_icon,
            text="",
            fg_color="#FF6505",
            hover_color="#FF8C42",
            text_color="white",
            font=(self.poppins, 14, "bold"),
            height=40,
            width=40,
            corner_radius=4,
            command=self.lightDarkMode,
        )

        self.start_button = ctk.CTkButton(
            self.frame,
            image=self.mic_icon,
            text="Start",
            compound="right",
            fg_color="#FF6505",
            hover_color="#FF8C42",
            text_color="white",
            font=(self.poppins, 14, "bold"),
            height=40,
            width=140,
            corner_radius=4,
            command=self.startRecording,
        )
        self.pause_button = ctk.CTkButton(
            self.frame,
            image=self.pause_icon,
            text="Pause",
            compound="right",
            fg_color="#FF6505",
            hover_color="#FF8C42",
            text_color="white",
            font=(self.poppins, 14, "bold"),
            height=40,
            width=140,
            corner_radius=4,
            state="disabled",
            command=self.pausePlayRecording,
        )
        self.stop_button = ctk.CTkButton(
            self.frame,
            image=self.stop_icon,
            text="Stop",
            compound="right",
            fg_color="#FF6505",
            hover_color="#FF8C42",
            text_color="white",
            font=(self.poppins, 14, "bold"),
            height=40,
            width=140,
            corner_radius=4,
            state="disabled",
            command=self.stopRecording,
        )
        self.save_button = ctk.CTkButton(
            self.frame,
            image=self.save_icon,
            text="Save",
            compound="right",
            fg_color="#FF6505",
            hover_color="#FF8C42",
            text_color="white",
            font=(self.poppins, 14, "bold"),
            height=40,
            width=140,
            corner_radius=4,
            state="disabled",
            command=self.saveRecording,
        )
        self.plot_button = ctk.CTkButton(
            self.frame,
            image=self.plot_icon,
            text="Plot",
            compound="right",
            fg_color="#FF6505",
            hover_color="#FF8C42",
            text_color="white",
            font=(self.poppins, 14, "bold"),
            height=40,
            width=140,
            corner_radius=4,
            state="disabled",
            command=self.plot_Recording,
        )

        self.current_frame = 0
        self.gif_running = False
        self.wave_gif = "utils/wave.gif"
        self.gif = Image.open(self.wave_gif)
        self.frames = [
            ctk.CTkImage(light_image=frame.convert("RGBA"), size=(400, 350))
            for frame in ImageSequence.Iterator(self.gif)
        ]

        self.plot_current_frame = 0
        self.plot_running = False
        self.plot_wave_gif = "utils/plot.gif"
        self.plot_gif = Image.open(self.plot_wave_gif)
        self.plot_frames = [
            ctk.CTkImage(light_image=frame.convert("RGBA"), size=(400, 350))
            for frame in ImageSequence.Iterator(self.plot_gif)
        ]

        self.hero = ctk.CTkLabel(self.hero_frame, image=self.logo_image, text="")
        self.hero.pack()
        self.dark_button.place(relx=0.96, rely=0.05, anchor="ne")
        self.start_button.place(x=45, y=115, anchor="w")
        self.pause_button.place(x=45, y=185, anchor="w")
        self.stop_button.place(x=45, y=255, anchor="w")
        self.save_button.place(x=45, y=325, anchor="w")
        self.plot_button.place(x=45, y=395, anchor="w")

    def startRecording(self):
        self.recorder.startRecording()
        if not self.gif_running:
            self.plot_running = False
            self.gif_running = True
            self.animateWave()

        self.pause_button.configure(state="normal")
        self.stop_button.configure(state="normal")
        self.save_button.configure(state="normal")
        self.plot_button.configure(state="normal")
        self.start_button.configure(state="disabled")

    def pausePlayRecording(self):
        if self.is_paused:
            self.recorder.resumeRecording()
            mb(title="Resumed", message="Playback resumed.")
            self.pause_button.configure(text="Pause", image=self.pause_icon)
            self.is_paused = False
            self.animateWave()
        else:
            self.recorder.pauseRecording()
            mb(title="Paused", message="Recording paused.")
            self.pause_button.configure(text="Play", image=self.play_icon)
            self.is_paused = True

    def stopRecording(self):
        self.recorder.stopRecording()
        mb(
            title="Recording Stopped",
            message="Recording has been stopped.",
            icon="cancel",
        )
        self.gif_running = False
        self.is_paused = False
        self.current_frame = 0
        self.hero.configure(image=self.frames[0])
        self.pause_button.configure(text="Pause", image=self.pause_icon)
        self.start_button.configure(state="disabled")
        self.pause_button.configure(state="disabled")

    def saveRecording(self):
        self.recorder.saveRecording()
        mb(
            title="Recording Saved",
            message="Recording saved successfully.",
            icon="check",
            option_1="Thanks",
        )
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="normal")
        self.gif_running = False

    def plot_Recording(self):
        mb(title="Plotted", message="Recording waveform plotted successfully.")
        self.gif_running = False
        self.plot_running = True
        self.plot_current_frame = 0
        self.animatePlot()
        self.recorder.plotRecording()

    def lightDarkMode(self):
        if self.is_darked:
            ctk.set_appearance_mode("light")
            self.dark_button.configure(image=self.dark_icon)
        else:
            ctk.set_appearance_mode("dark")
            self.dark_button.configure(image=self.sun_icon)

        self.is_darked = not self.is_darked

    def animateWave(self):
        if not self.is_paused and self.gif_running:
            self.hero.configure(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.after(100, self.animateWave)

    def animatePlot(self):
        if self.plot_running:
            self.hero.configure(image=self.plot_frames[self.plot_current_frame])
            self.plot_current_frame = (self.plot_current_frame + 1) % len(
                self.plot_frames
            )
            self.after(100, self.animatePlot)

root = ctk.CTk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
app = VoiceRecorderGUI(root)
root.mainloop()
