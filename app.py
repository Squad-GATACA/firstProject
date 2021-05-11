from flask import Flask, render_template, request, send_file, send_from_directory, safe_join, redirect, url_for, flash
import pytube
import instaloader
import os
import os.path
import sys
from instaloader import Post
from instaloader import Profile
import time
import re
import requests as r
import wget

app = Flask(__name__)
app.config['SECRET_KEY'] = "dgdhjdkkdkfkf"


@app.route('/')
def home():
    return render_template("main.html")


@app.route('/youtube')
def youtube():
    return render_template("yt.html")


@app.route('/instagram')
def instagram():
    return render_template("insta.html")


@app.route('/facebook')
def facebook():
    return render_template("fb.html")


@app.route('/aboutus')
def aboutus():
    return render_template("about.html")


@app.route('/contactus')
def contactus():
    return render_template("contact.html")


@app.route("/download-youtube-video", methods=["GET", "POST"])
def youtube_video():
    if(request.method == "POST"):
        youtube_url = request.form["link"]
        if(youtube_url != ""):
            try:
                x = r.get(youtube_url)
            except:
                flash("Enter Valid Youtube Link!!!", "danger")
                return redirect('youtube')

            local_download_path = pytube.YouTube(
                youtube_url).streams[0].download()
            fname = local_download_path.split("//")[-1]
            return send_file(fname, as_attachment=True)
        flash("Enter Valid Youtube Link!!!", "danger")
        return redirect('youtube')
    return render_template("page1.html")


@app.route('/download-instagram-video', methods=["GET", "POST"])
def instagram_video():
    if(request.method == "POST"):
        url = request.form["link"]
        ftype = request.form["filetype"]
        if(ftype == "POST"):
            if(url != ""):
                try:
                    u = url.split('/')[-2]
                    os.system(
                        f"instaloader --filename-pattern={u} --login=life_is_very_easy2021 --password=SquadPccoe2021 -- -{u}")
                    fname = u.strip()
                    u_jpg = "-".strip()+u.strip()+"/"+fname+".jpg"
                    u_mp4 = "-".strip()+u.strip()+"/"+fname+".mp4"
                    if(os.path.isfile(u_mp4)):
                        return send_file(u_mp4, as_attachment=True)
                    else:
                        return send_file(u_jpg, as_attachment=True)
                except IndexError:
                    flash("Invalid Url!!!", "danger")
                    return redirect('instagram')
            flash(
                "This feature is not available right now!!! We are working on it.", "danger")
            return redirect('instagram')
        elif(ftype == "PROFILE-PICTURE"):
            flash(
                "This feature is not available right now!!! We are Working on it.", "danger")
            return redirect('instagram')
        else:
            flash("Invalid Content Type!!!", "danger")
            return redirect('instagram')
    return redirect('instagram')


@app.route('/download-facebook-video', methods=["GET", "POST"])
def facebook_video():
    if(request.method == "POST"):
        ERASE_LINE = '\x1b[2K'
        url = request.form["link"]
        if(url != ""):
            try:
                fname = url.split('/')[-2]
            except IndexError:
                flash("Invalid Url!!!", "danger")
                return redirect('facebook')
            filedir = os.path.join(fname+".mp4")
            try:
                html = r.get(url)
                hdvideo_url = re.search('hd_src:"(.+?)"', html.text)[1]
            except r.ConnectionError as e:
                flash("OOPS!! Connection Error.", "danger")
                return redirect('facebook')
            except r.Timeout as e:
                flash("OOPS!! Timeout Error", "danger")
                return redirect('facebook')
            except r.RequestException as e:
                flash("OOPS!! General Error or Invalid URL", "danger")
                return redirect('facebook')
            except (KeyboardInterrupt, SystemExit):
                flash("Something Went Wrong!!!", "danger")
                return redirect('facebook')
                sys.exit(1)
            except TypeError:
                flash("Video May Private or Hd version not avilable!!!", "danger")
                return redirect('facebook')
            else:
                hd_url = hdvideo_url.replace('hd_src:"', '')
                wget.download(hd_url, filedir)
                sys.stdout.write(ERASE_LINE)
                return send_file(fname.strip()+'.mp4', as_attachment=True)
        flash("Enter Valid Facebook Link!!!", "danger")
        return redirect('facebook')
    return redirect('facebook')


if __name__ == '__main__':
    app.run()
