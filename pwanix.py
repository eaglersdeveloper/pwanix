#!/usr/bin/python3

## Imports  
import gi
import os
import sys
import json
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

# Loading PWA's manifest  
try:
	manifest = json.load(open("manifest.json"))
except FileNotFoundError:
	print("""
Couldn't find the manifest.

Try the following:
* Make sure that you run pwanix in the correct folder.
* Check that the manifest is named "manifest.json".

Details:
https://developer.mozilla.org/en-US/docs/Web/Manifest
https://developers.google.com/web/fundamentals/web-app-manifest/
""")
	quit()

# Setting window title  
try:
	bar.set_title(manifest["short_name"])
except KeyError:
	print("""
Missing "short_name" in the manifest.

Try the following:
* Make sure that the manifest is written without errors.

Details:
https://developer.mozilla.org/en-US/docs/Web/Manifest
https://developers.google.com/web/fundamentals/web-app-manifest/
""")
	quit()

# Enable fullscreen or open PWA in browser?  
try:
	if manifest["display"] == "fullscreen":
		main.fullscreen()
	elif manifest["display"] == "browser-ui":
		os.system("x-www-browser " + manifest["scope"])
		quit()
except KeyError:
	print("""
Missing "display" in the manifest.

Try the following:
* Make sure that the manifest is written without errors.

Details:
https://developer.mozilla.org/en-US/docs/Web/Manifest
https://developers.google.com/web/fundamentals/web-app-manifest/
""")
	quit()

# And finaly WebView!  
try:
	web = WebKit2.WebView(settings=websettings)
	web.load_uri("file://" + Path.cwd() + manifest["start_url"])
	main.add(web)
except KeyError:
	print("""
Missing "start_url" in the manifest.

Try the following:
* Make sure that the manifest is written without errors.

Details:
https://developer.mozilla.org/en-US/docs/Web/Manifest
https://developers.google.com/web/fundamentals/web-app-manifest/
""")
	quit()

main.show_all()
Gtk.main()