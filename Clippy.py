import os
from tkinter import Tk, Label, Button, filedialog, IntVar, Entry, Toplevel
from moviepy.video.io.VideoFileClip import VideoFileClip

class VideoCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clippy")

        # Set window size
        self.root.geometry("500x400")

        # Set window icon

        # Set background color
        self.root.configure(bg="lightgray")

        self.selected_file = ""
        self.output_directory = ""

        self.label = Label(root, text="Select a video file:")
        self.label.pack()

        self.choose_button = Button(root, text="Choose File", command=self.choose_file)
        self.choose_button.pack()

        self.cut_options_button = Button(root, text="Cut Video with Options", command=self.show_cut_options, state="disabled")
        self.cut_options_button.pack()

        self.cut_auto_button = Button(root, text="Cut Video Automatically", command=self.cut_auto_video, state="disabled")
        self.cut_auto_button.pack()

    def choose_file(self):
        self.selected_file = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if self.selected_file:
            self.cut_options_button.config(state="normal")
            self.cut_auto_button.config(state="normal")

    def show_cut_options(self):
        self.cut_options_window = Toplevel(self.root)
        self.cut_options_window.title("Cut Options")

        self.parts_var = IntVar()
        self.parts_label = Label(self.cut_options_window, text="Number of parts:")
        self.parts_label.pack()
        self.parts_entry = Entry(self.cut_options_window, textvariable=self.parts_var)
        self.parts_entry.pack()

        self.cut_confirm_button = Button(self.cut_options_window, text="Confirm", command=self.cut_video)
        self.cut_confirm_button.pack()

    def cut_auto_video(self):
        if self.selected_file:
            video_clip = VideoFileClip(self.selected_file)
            duration = video_clip.duration
            min_duration = 60  # Minimum duration for each part
            num_parts = int(duration / min_duration)

            self.output_directory = filedialog.askdirectory()
            if self.output_directory:
                print(f"Exporting {num_parts} parts...")
                for i in range(num_parts):
                    start_time = i * min_duration
                    end_time = (i + 1) * min_duration
                    part_clip = video_clip.subclip(start_time, end_time)
                    output_path = os.path.join(self.output_directory, f"part_{i+1}.mp4")
                    part_clip.write_videofile(output_path)
                    print(f"Part {i+1} exported to: {output_path}")

                video_clip.close()
                print("Video parts exported successfully!")

    def cut_video(self):
        if self.selected_file and self.parts_var.get() > 0:
            video_clip = VideoFileClip(self.selected_file)
            duration = video_clip.duration
            num_parts = self.parts_var.get()
            part_duration = duration / num_parts

            self.output_directory = filedialog.askdirectory()
            if self.output_directory:
                print(f"Exporting {num_parts} parts...")
                for i in range(num_parts):
                    start_time = i * part_duration
                    end_time = (i + 1) * part_duration
                    part_clip = video_clip.subclip(start_time, end_time)
                    output_path = os.path.join(self.output_directory, f"part_{i+1}.mp4")
                    part_clip.write_videofile(output_path)
                    print(f"Part {i+1} exported to: {output_path}")

                video_clip.close()
                print("Video parts exported successfully!")
                self.cut_options_window.destroy()


root = Tk()
app = VideoCutterApp(root)
root.mainloop()
