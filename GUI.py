from PoseModule import PoseDetector, Pushup
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

window = tk.Tk()
window.title("Push-up Counter")
label = tk.Label(window)
label.pack()

def open_camera():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    detector = PoseDetector()
    task = Pushup()

    def update_frame():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = detector.findPose(frame)
        lmlist, bboxInfo, neck = detector.findPosition(frame)
        count = task.detect(lmlist)
        cv2.putText(frame, f"Count: {count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (800, 600))
            img = Image.fromarray(frame_resized)
            img_tk = ImageTk.PhotoImage(image=img)
            label.config(image=img_tk)
            label.image = img_tk

        label.after(10, update_frame)

    update_frame()

def open_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    if file_path:
        cap = cv2.VideoCapture(file_path)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        detector = PoseDetector()
        task = Pushup()

        def update_frame():
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = detector.findPose(frame)
            lmlist, bboxInfo, neck = detector.findPosition(frame)
            count = task.detect(lmlist)
            cv2.putText(frame, f"Count: {count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (800, 600))
                img = Image.fromarray(frame_resized)
                img_tk = ImageTk.PhotoImage(image=img)
                label.config(image=img_tk)
                label.image = img_tk

            label.after(10, update_frame)

        update_frame()
def end():
    exit()

camera_button = tk.Button(window, text="Open Camera", command=open_camera)
camera_button.pack(padx = 10 , pady=10)

video_button = tk.Button(window, text="Open Video", command=open_video )
video_button.pack(padx = 10 , pady=10)

end_button = tk.Button(window, text="End", command=end)
end_button.pack(padx = 10 , pady=10)


window.mainloop()
