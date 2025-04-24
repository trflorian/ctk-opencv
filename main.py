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

        self.radio_var = customtkinter.StringVar(value="1")

        # LAYOUT: left side radio button group, right side image display
        self.radio_frame = customtkinter.CTkFrame(self)
        self.radio_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        for option in ["Normal", "Grayscale", "Blur", "Threshold", "Canny", "Sobel", "Laplacian"]:
            radio_button = customtkinter.CTkRadioButton(
                self.radio_frame, text=option, variable=self.radio_var, value=option
            )
            radio_button.pack(padx=10, pady=10)

            if option == "Normal":
                radio_button.select()

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

            # Apply the selected filter
            filter_option = self.radio_var.get()

            if filter_option == "Grayscale":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif filter_option == "Blur":
                frame = cv2.GaussianBlur(frame, (15, 15), 0)
            elif filter_option == "Threshold":
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            elif filter_option == "Canny":
                frame = cv2.Canny(frame, 100, 200)
            elif filter_option == "Sobel":
                frame = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
            elif filter_option == "Laplacian":
                frame = cv2.Laplacian(frame, cv2.CV_64F)
            elif filter_option == "Normal":
                pass

            # Update the image display
            self.image_display.update_frame(frame)

        cap.release()


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
