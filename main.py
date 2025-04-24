import argparse
import logging

from filter import FilterFactory

from app_ctk import AppCtk
from app_opencv import AppOpenCV

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
        app = AppCtk(filters)
        app.mainloop()


if __name__ == "__main__":
    main()
