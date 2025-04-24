import argparse
import logging
import threading
import cv2
import customtkinter
import numpy as np

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

class AppOpenCV:
    def __init__(self) -> None:
        self.window_name = "Webcam Stream"
        cv2.namedWindow(self.window_name)
        
        self.tb_filter_name = "Filter"
        cv2.createTrackbar(self.tb_filter_name, self.window_name, 0, 6, lambda x: None)
        cv2.setTrackbarPos(self.tb_filter_name, self.window_name, 0)

    def start_webcam_stream(self) -> None:
        """
        Start the webcam stream and display it using OpenCV.
        """
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Apply the selected filter
            filter_option = cv2.getTrackbarPos(self.tb_filter_name, self.window_name)

            if filter_option == 1:
                filter_name = "Grayscale"
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif filter_option == 2:
                filter_name = "Blur"
                frame = cv2.GaussianBlur(frame, (15, 15), 0)
            elif filter_option == 3:
                filter_name = "Threshold"
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            elif filter_option == 4:
                filter_name = "Canny"
                frame = cv2.Canny(frame, 100, 200)
            elif filter_option == 5:
                filter_name = "Sobel"
                frame = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
            elif filter_option == 6:
                filter_name = "Laplacian"
                frame = cv2.Laplacian(frame, cv2.CV_64F)
            elif filter_option == 0:
                filter_name = "Normal"

            # convert the frame to BGR format
            if frame.dtype != np.uint8:
                # scale the frame to uint8 if necessary
                frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            if len(frame.shape) == 2:
                # If the frame is grayscale, convert it to BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            
            # add a black border at the bottom of the frame
            border_height = 50
            border_color = (0, 0, 0)
            frame = cv2.copyMakeBorder(frame, 0, border_height, 0, 0, cv2.BORDER_CONSTANT, value=border_color)
            
            # center the filter name
            cv2.putText(
                frame,
                filter_name,
                (frame.shape[1] // 2 - 50, frame.shape[0] - border_height // 2 + 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            cv2.imshow(self.window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Webcam Stream with Filters")
    parser.add_argument(
        "--gui",
        type=str,
        choices=["ctk", "opencv"],
        default="ctk",
        help="Choose the GUI framework to use (ctk or opencv).",
    )
    return parser.parse_args()

def main() -> None:
    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    if args.gui == "opencv":
        app = AppOpenCV()
        app.start_webcam_stream()
    elif args.gui == "ctk":
        app = App()
        app.mainloop()


if __name__ == "__main__":
    main()
