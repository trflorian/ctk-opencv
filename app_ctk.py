import threading

import customtkinter
import cv2

from ctk_image_display import CTkImageDisplay
from filter import Filter


class AppCtk(customtkinter.CTk):
    def __init__(self, filters: list[Filter]) -> None:
        self.filters = filters

        self.title("Webcam Stream")
        self.geometry("800x600")

        self.filter_var = customtkinter.IntVar(value=0)

        self.filters_frame = customtkinter.CTkFrame(self)
        self.filters_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        for filter_id, filter in enumerate(self.filters):
            rb_filter = customtkinter.CTkRadioButton(
                self.filters_frame,
                text=filter.name,
                variable=self.filter_var,
                value=filter_id,
            )
            rb_filter.pack(padx=10, pady=10)

            if filter_id == 0:
                rb_filter.select()

        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Create a CTkImageDisplay widget
        self.image_display = CTkImageDisplay(self.image_frame)
        self.image_display.pack(fill="both", expand=True, padx=10, pady=10)

        self.webcam_stream_thread = threading.Thread(target=self.start_webcam_stream, daemon=True)
        self.webcam_stream_thread.start()

    def start_webcam_stream(self) -> None:
        """
        Start the webcam stream and update the image display.
        """
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Apply the selected filter
            filter_id = self.filter_var.get()
            filter = self.filters[filter_id]
            frame = filter.apply(frame)

            # Update the image display
            self.image_display.update_frame(frame)

        cap.release()
