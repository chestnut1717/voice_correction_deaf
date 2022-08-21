from flask import request,render_template, make_response
from flask_restx import Resource, Api, Namespace
# https://stackoverflow.com/questions/73105877/importerror-cannot-import-name-parse-rule-from-werkzeug-routing

Home = Namespace('Home')

@Home.route('')
class HomeView(Resource):
    def render(self):
        return make_response(render_template('index.html',user="반원",data={'level':60,'point':360,'exp':45000}) )