# File: srtfixer.py
# Summary: GUI for SRT Lib.

import os
import Tkinter as tk
import tkFileDialog

import srt


def open_file_browser(filepath):
    """Opens the file browser and sets the filepath to the path of the selected
    file."""
    def _open():
        filename = tkFileDialog.askopenfilename(
            filetypes=[('SRT File', '.srt')])
        filepath.set(filename)

    return _open


def save_srt(
        help, filepath, radio_value, hours, minutes, seconds, milliseconds):
    """Save the modified SRT file."""
    def _save():
        parser = srt.Subtitles()
        parser.load(filepath.get())

        if radio_value.get() == "Add":
            parser.addTime(
                hours.get(), minutes.get(), seconds.get(), milliseconds.get())
        else:
            parser.substractTime(
                hours.get(), minutes.get(), seconds.get(), milliseconds.get())

        parser.save(filepath.get())
        help.set("Your changes have been saved!")

    return _save


def build_gui():
    """Creates the GUI components."""
    root = tk.Tk()
    root.title("SRT Fixer")
    root.resizable(width=False, height=False)

    help_frame = tk.Frame(root)
    help_frame.pack(fill=tk.BOTH)

    help = tk.StringVar()
    help.set("Select the file you want to fix:")
    tk.Label(help_frame, anchor=tk.W, textvariable=help).pack(
        fill=tk.BOTH, side=tk.LEFT)

    browse_frame = tk.Frame(root)
    browse_frame.pack()

    filepath = tk.StringVar()
    filepath_entry = tk.Entry(browse_frame, textvariable=filepath)
    filepath_entry.grid(column="0", row="0")

    tk.Button(
        browse_frame,
        text="Browse",
        command=open_file_browser(filepath)).grid(column="1", row="0")

    radio_btn_frame = tk.Frame(root)
    radio_btn_frame.pack(fill=tk.BOTH)

    radio_value = tk.StringVar()
    radio_value.set("Add")
    tk.Radiobutton(
        radio_btn_frame,
        text="Add",
        value="Add",
        variable=radio_value).grid(column="0", row="0")
    tk.Radiobutton(
        radio_btn_frame,
        text="Substract",
        value="Substract",
        variable=radio_value).grid(column="1", row="0")

    time_frame = tk.Frame(root)
    time_frame.pack(fill=tk.BOTH)

    hours = tk.IntVar()
    minutes = tk.IntVar()
    seconds = tk.IntVar()
    milliseconds = tk.IntVar()

    tk.Label(time_frame, text="H:").grid(column="0", row="0")
    tk.Entry(time_frame, width="3", textvariable=hours).grid(
        column="1", row="0")
    tk.Label(time_frame, text="M:").grid(column="2", row="0")
    tk.Entry(time_frame, width="3", textvariable=minutes).grid(
        column="3", row="0")
    tk.Label(time_frame, text="S:").grid(column="4", row="0")
    tk.Entry(time_frame, width="3", textvariable=seconds).grid(
        column="5", row="0")
    tk.Label(time_frame, text="MS:").grid(column="6", row="0")
    tk.Entry(time_frame, width="3", textvariable=milliseconds).grid(
        column="7", row="0")

    confirm_btns_frame = tk.Frame(root)
    confirm_btns_frame.pack(fill=tk.BOTH)

    tk.Button(
        confirm_btns_frame,
        text="Save",
        command=save_srt(
            help,
            filepath,
            radio_value,
            hours,
            minutes,
            seconds,
            milliseconds)).pack(side=tk.RIGHT)

    return root

if __name__ == '__main__':
    app = build_gui()
    app.mainloop()
