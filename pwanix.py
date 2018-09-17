#!/usr/bin/python3

## Imports  
import gi
import os
import sys
import json
import urllib.request
from pathlib import Path

gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, Gio, WebKit2

## Window  
main = Gtk.Window()
main.connect("destroy", Gtk.main_quit)
bar = Gtk.HeaderBar(show_close_button=True)
main.set_titlebar(bar)
main.set_default_size(972, 512)

# Locate PWA  
if len(sys.argv) == 1:
	path = "file://" + str(Path.cwd()) + "/"
elif sys.argv[1][:7] == "http://" or sys.argv[1][:8] == "https://":
	path = sys.argv[1] + "/"
elif sys.argv[1][0] == "/":
	path = "file://" + sys.argv[1] + "/"
else:
	path = "file://" + "/" + str(Path.cwd()) + "/" + sys.argv[1] + "/"

# Load PWA's manifest
manifest = json.load(urllib.request.urlopen(path + "manifest.json"))

# Set window title  
try:
	bar.set_title(manifest["short_name"])
except KeyError:
	bar.set_title(manifest["name"])

# Enable fullscreen or open PWA in browser?  
if manifest["display"] == "fullscreen":
	main.fullscreen()
elif manifest["display"] == "browser-ui":
	os.system("x-www-browser " + manifest["scope"])
	quit()

# Add WebView and load PWA's main page  
web = WebKit2.WebView()
web.get_settings().set_allow_file_access_from_file_urls(True)
web.load_uri(path + manifest["start_url"])
main.add(web)

main.show_all()
Gtk.main()