import os
from pose import PoseEstimation
import tkinter as tk
from tkinter import filedialog
import time

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pose Estimation")
        self.root.geometry("427x241")
        self.a = '#106EBE'
        self.create_widgets()
        self.pose_estimator = None

    def create_widgets(self):
        self.frame = tk.Frame(self.root, width=1000, height=600, bg=self.a)
        self.frame.place(x=0, y=0)

        self.label1 = tk.Label(self.root, text='PerfectPose', fg='black', bg=self.a)
        self.label1.config(font=('Calibri (Body)', 18, 'bold'))
        self.label1.place(x=130, y=80)

        self.label3 = tk.Label(self.root, text='Detection', fg='white', bg=self.a)
        self.label3.config(font=('Calibri (Body)', 13))
        self.label3.place(x=130, y=110)

        self.button = tk.Button(self.root, width=10, height=1, text='Get Started', command=self.start_progress,
                                border=0, fg=self.a, bg='white')
        self.button.place(x=170, y=200)

    def start_progress(self):
        self.label4 = tk.Label(self.root, text='Loading...', fg='white', bg=self.a)
        self.label4.config(font=('Calibri (Body)', 10))
        self.label4.place(x=18, y=210)

        r = 0
        for i in range(100):
            self.root.update_idletasks()
            # time.sleep(0.03)
            r = r + 1

        self.root.after(1000, self.create_file_upload_view)
        
    def create_file_upload_view(self):
        self.frame.destroy()

        self.frame2 = tk.Frame(self.root, width=527, height=341, bg=self.a)
        self.frame2.place(x=0, y=0)

        self.label5 = tk.Label(self.root, text='File Upload', fg='white', bg=self.a)
        self.label5.config(font=('Calibri (Body)', 18))
        self.label5.place(x=50, y=20)

        self.label6 = tk.Label(self.root, text='Upload your video file:', fg='white', bg=self.a)
        self.label6.config(font=('Calibri (Body)', 12))
        self.label6.place(x=50, y=60)

        self.button2 = tk.Button(self.root, width=15, height=1, text='Upload Video', command=self.select_file,
                                 border=0, fg=self.a, bg='white')
        self.button2.place(x=180, y=100)

        self.button3 = tk.Button(self.root, width=15, height=1, text='Upload Image', command=self.select_imageURL,
                                 border=0, fg=self.a, bg='white')
        self.button3.place(x=180, y=140)
        
        self.label7 = tk.Label(self.root, text='', fg='white', bg=self.a)
        self.label7.config(font=('Calibri (Body)', 10))
        self.label7.place(x=50, y=165)

        
        self.button4 = tk.Button(self.root, width=15, height=1, text='Live Preview', command=self.live_preview,
                                 border=0, fg=self.a, bg='white')
        self.button4.place(x=180, y=190)

    def live_preview(self):
        self.label7.config(text="Webcam Live Preview (Press q for close)")
        self.start_webcam_pose_estimation()
        
    def live_preview(self):
        self.label7.config(text="Webcam Live Preview (Press q for close)")
        self.start_webcam_pose_estimation()

    def file_upload_view(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.label4.config(text='Video Uploaded: ' + file_path)
            self.start_pose_estimation(file_path)
        else:
            self.label4.config(text='No file selected.')

    def select_imageURL(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select File",
                                               filetypes=(("Jpg files", "*.jpg"),("Png files", "*.png"),("JPEG files", "*.jpeg"),("All files", "*.*")))
        if file_path:
            print("File selected:", file_path)
            self.start_img_pose_estimation(file_path)

    def select_file(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select File",
                                               filetypes=(("MP4 files", "*.mp4"),("All files", "*.*")))
        if file_path:
            print("File selected:", file_path)
            self.start_pose_estimation(file_path)

    def start_pose_estimation(self, file_path):
        self.pose_estimator = PoseEstimation(file_path)
        self.pose_estimator.process_video()
    
    def start_img_pose_estimation(self, file_path):
        self.pose_estimator = PoseEstimation(file_path)
        self.pose_estimator.process_image(file_path)
        
    def start_webcam_pose_estimation(self):
        self.webcam_pose_estimator = PoseEstimation(0)  # Pass 0 for webcam
        self.webcam_pose_estimator.process_webcam()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
