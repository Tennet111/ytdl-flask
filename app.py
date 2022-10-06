from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask("__name__")

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/mp4", methods=["GET"])
def mp4():
    if request.method == "GET":
        if request.args.get("highres") == "on":
            v = request.args.get("v")
            yt = YouTube(v)
            yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution().download("downloads/mp4")
            return send_file(f"downloads/mp4/{yt.title}.mp4", as_attachment=True)
        else:
            v = request.args.get("v")
            yt = YouTube(v)
            yt.streams.filter(progressive=True, file_extension="mp4").get_lowest_resolution().download("downloads/mp4")
            return send_file(f"downloads/mp4/{yt.title}.mp4", as_attachment=True)

@app.route("/mp3", methods=["GET"])
def mp3():  
    if request.method == "GET":
        v = request.args.get("v")
        yt = YouTube(v)
        yt.streams.filter(only_audio=True).first().download("downloads/mp3")
        before = f"downloads/mp3/{yt.title}.mp4"
        base = before.split("/")
        title, ext = base[2].split(".")
        after = title + ".mp3"
        os.rename(before, f"downloads/mp3/{after}")
        return send_file(f"downloads/mp3/{title}.mp3", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True) 