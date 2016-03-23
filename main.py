import jinja2
import webapp2
from google.appengine.ext import ndb

env= jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
class MainHandler(webapp2.RequestHandler):#this handles the default url and render index.html
    def get(self):
        template = env.get_template('index.html')
        event = Event.query().fetch() #Getting content from datastore
        template_variable= {"events": event}
        self.response.write(template.render(template_variable))

class Event(ndb.Model):
    event_name = ndb.StringProperty(required=True)
    event_host = ndb.StringProperty(required=True)
    event_details = ndb.TextProperty(required=True)
    event_date = ndb.StringProperty(required=True)
    start_time = ndb.StringProperty(required=True)
    end_time = ndb.StringProperty(required=True)
    eventbrite = ndb.StringProperty(required=True)
    additional_notes = ndb.TextProperty(required=True)
    # private  = ndb.BooleanProperty(required=True)

class EventHandler(webapp2.RequestHandler):#requesthandler: where you process the request, manipulate data, and issues a response
    def get(self):
        template = env.get_template('create_event.html')
        self.response.write(template.render())
    def post(self): # Take user input, turns it into a post, and adds it to the database
        event_name= self.request.get('event_name')
        event_host= self.request.get('event_host')
        event_details= self.request.get('event_details')
        event_date=self.request.get('event_date')
        start_time=self.request.get('start_time')
        end_time=self.request.get('end_time')
        eventbrite=self.request.get('eventbrite')
        additional_notes=self.request.get('additional_notes')
        # private=self.request.get('private')
        event = Event(event_name=event_name,
                        event_host=event_host,
                        event_details=event_details,
                        event_date=event_date,
                        start_time=start_time,
                        end_time=end_time,
                        eventbrite=eventbrite,
                        additional_notes=additional_notes)
                        # private=private)
        event.put()#DO NOT PUT UR PUTS UNDER REDIRECT
        self.redirect("/")

# class PostEventHandler (webapp2.RequestHandler):
#     def get(self):
#         landing_page= env.get_template('create_event.html')
#         self.response.write(landing_page.render())
#     def post(self):
#         events_page=env.get_template('events.html')
#         event_variables={'event_name':self.request.get('event_name'),'event_host':self.request.get('event_host'),'event_details':self.request.get('event_details'),'event_date':self.request.get('event_date'),'start_time':self.request.get('start_time'), 'end_time':self.request.get('end_time'),'eventbrite':self.request.get('eventbrite'), 'additional_notes':self.request.get('additional_notes'), 'private':self.request.get('private') }
#         self.response.write(events_page.render(event_variables))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create_event', EventHandler)
], debug=True)
