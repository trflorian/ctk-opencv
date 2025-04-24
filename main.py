import logging
import threading
import cv2
import customtkinter

from ctk_image_display import CTkImageDisplay


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.title("Webcam Stream")
        self.geometry("800x600")

        radio_var = customtkinter.StringVar(value="1")

        # LAYOUT: left side radio button group, right side image display
        self.radio_frame = customtkinter.CTkFrame(self)
        self.radio_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.radio_button_1 = customtkinter.CTkRadioButton(
            self.radio_frame, text="Option 1", variable=radio_var, value=1
        )
        self.radio_button_1.pack(padx=10, pady=10)
        self.radio_button_2 = customtkinter.CTkRadioButton(
            self.radio_frame, text="Option 2", variable=radio_var, value=2
        )
        self.radio_button_2.pack(padx=10, pady=10)
        self.radio_button_3 = customtkinter.CTkRadioButton(
            self.radio_frame, text="Option 3", variable=radio_var, value=3
        )
        self.radio_button_3.pack(padx=10, pady=10)

        # LAYOUT: right side image display
        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Create a CTkImageDisplay widget
        self.image_display = CTkImageDisplay(self.image_frame, corner_radius=10)
        self.image_display.pack(fill="both", expand=True, padx=10, pady=10)

        self.webcam_stream_thread = threading.Thread(
            target=self.start_webcam_stream, daemon=True
        )
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

            # Update the image display
            self.image_display.update_frame(frame)

        cap.release()


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
