import cv2

from .filter import Filter
from .utils import convert_any_to_bgr


class AppOpenCV:
    def __init__(self, filters: list[Filter]) -> None:
        self.filters = filters

        self.window_name = "Webcam Stream"
        cv2.namedWindow(self.window_name)

        self.tb_filter_name = "Filter"
        cv2.createTrackbar(
            self.tb_filter_name,
            self.window_name,
            0,
            len(self.filters) - 1,
            lambda _: None,
        )

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

            # Convert the frame to BGR format if needed
            frame = convert_any_to_bgr(frame)

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
