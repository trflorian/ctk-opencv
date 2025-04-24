import argparse
import logging
import threading
import cv2
import customtkinter
import numpy as np

from ctk_image_display import CTkImageDisplay
from filter import Filter, FilterFactory

class App(customtkinter.CTk):
    def __init__(self, filters: list[Filter], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.filters = filters

        self.title("Webcam Stream")
        self.geometry("800x600")

        self.filter_var = customtkinter.IntVar(value=0)

        self.filters_frame = customtkinter.CTkFrame(self)
        self.filters_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        for filter_id, filter in enumerate(self.filters):
            rb_filter = customtkinter.CTkRadioButton(
                self.filters_frame, text=filter.name, variable=self.filter_var, value=filter_id,
            )
            rb_filter.pack(padx=10, pady=10)

            if filter_id == 0:
                rb_filter.select()

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
            filter_id = self.filter_var.get()
            filter = self.filters[filter_id]
            frame = filter.apply(frame)

            # Update the image display
            self.image_display.update_frame(frame)

        cap.release()

class AppOpenCV:
    def __init__(self, filters: list[Filter]) -> None:
        self.filters = filters

        self.window_name = "Webcam Stream"
        cv2.namedWindow(self.window_name)
        
        self.tb_filter_name = "Filter"
        cv2.createTrackbar(self.tb_filter_name, self.window_name, 0, len(self.filters), lambda x: None)
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
            filter_id = cv2.getTrackbarPos(self.tb_filter_name, self.window_name)
            filter = self.filters[filter_id]

            # Get the filter name and apply the filter
            filter_name = filter.name
            frame = filter.apply(frame)

            # convert the frame to BGR format
            if frame.dtype != np.uint8:
                # scale the frame to uint8 if necessary
                cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
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

    filters = FilterFactory.create_all_filters()

    if args.gui == "opencv":
        app = AppOpenCV(filters)
        app.start_webcam_stream()
    elif args.gui == "ctk":
        app = App(filters)
        app.mainloop()


if __name__ == "__main__":
    main()
