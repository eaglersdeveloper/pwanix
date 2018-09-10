#!/usr/bin/python3

## Imports  
import gi
import os
import sys
import json
import urllib
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
	path = str(Path.cwd()) + "/"
elif sys.argv[1][0] == "/":
	path = sys.argv[1] + "/"
else:
	path = "/" + str(Path.cwd()) + "/" + sys.argv[1] + "/"

# Loading PWA's manifest
manifest = json.load(open(path + "manifest.json"))

# Setting window title  
bar.set_title(manifest["short_name"])

# Enable fullscreen or open PWA in browser?  
if manifest["display"] == "fullscreen":
	main.fullscreen()
elif manifest["display"] == "browser-ui":
	os.system("x-www-browser " + manifest["scope"])
	quit()

# And finaly WebView!  
web = WebKit2.WebView()
web.load_uri("file://" + path + manifest["start_url"])
main.add(web)

main.show_all()
Gtk.main()