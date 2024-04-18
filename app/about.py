from flask import Blueprint, request, redirect, render_template

about = Blueprint('about', __name__ )

@about.route('/sobre', methods=['GET'])
def about_page():
   return render_template('about/index.html')