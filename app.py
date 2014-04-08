import os
from flask import Flask, render_template, send_from_directory
from calendar_parser import CalendarParser

# initialization
app = Flask(__name__)
app.config.update(
	DEBUG=True,
)

events = {}
# settings

ics_url = "https://www.google.com/calendar/ical/88kil28s7t686h1p5aoem6ui24%40group.calendar.google.com/public/basic.ics"


class Event(object):
	name = ''
	location = ''
	start_time = None
	end_time = None
	description = ''
	clean_dates = ''


def tidytime(start, end):
	output = ''
	if start.day + 1 == end.day:
		sameday = True
	else:
		sameday = False
	if start.month == end.month:
		samemonth = True
	else:
		samemonth = False
	if start.year == end.year:
		sameyear = True
	else:
		sameyear = False
	if sameyear and samemonth and sameday:
		output = start.strftime("%A, %d %B %Y")
	elif sameyear and samemonth and not sameday:
		output = start.strftime("%A, %d-") + end.strftime("%d %B %Y")
	elif sameyear and not samemonth:
		output = start.strftime("%d %B - ") + end.strftime("%d %B %Y")
	return output

# controllers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.route("/")
def index():
	return render_template('index.html')


@app.route("/update")
def reset_events():
	global events
	event_list = []
	cal = CalendarParser(ics_url=ics_url)
	for event in cal.parse_calendar():
		NewEvent = Event()
		NewEvent.name = event["name"]
		NewEvent.location = event["location"]
		NewEvent.start_time = event["start_time"]
		NewEvent.end_time = event["end_time"]
		NewEvent.description = event["description"]
		NewEvent.clean_dates = tidytime(event["start_time"], event["end_time"])
		event_list.append(NewEvent)
	event_list.sort(key=lambda r: r.start_time)
	k = 0
	for event in event_list:
		events[k] = event
		k += 1
	# print events

	return render_template('reset.html', events=events)


# launch
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='127.0.0.1', port=port)