import webapp2
import re

form="""<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>
  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
    <table>
      <tr>
        <td class="label">
            Username
        </td>
        <td>
            <input type="text" name="Username">
        </td>
        <td class="error">
            %(error_username)s
        </td>
      </tr>

      <tr>
        <td class="label">
            Password
        </td>
        <td>
            <input type="password" name="Password">
        </td>
        <td class="error">
            %(error_password)s
        </td>
      </tr>

      <tr>
        <td class="label">
            Verify Password
        </td>
        <td>
            <input type="password" name="Verify">
        </td>
        <td class="error">
            %(error_verify)s
        </td>
      </tr>

      <tr>
        <td class="label">
            Email(optional)
        </td>
        <td>
            <input type="text" name="Email">
        </td>
        <td class="error">
            %(error_email)s
        </td>
      </tr>
    </table>
    <input type="submit">
    </form>
  </body>

</html>"""

welcome_form="""<!DOCTYPE html>

<html>
    <head>
        <title>Unit 2 welcome page!</title>
    </head>

    <body>
        <h2>Welcome, %(username)s!</h2>

    </body>
</html>"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form)
    def write_form(self,username="",password="",verify="",email=""):
        self.response.out.write(form%{"error_username":username,"error_password":password,"error_verify":verify,"error_email":email})
    def post(self):
        have_Error=False
        username=self.request.get('Username')
        password=self.request.get('Password')
        verify=self.request.get('Verify')
        email=self.request.get('Email')
		
        if not valid_username(username):
            self.write_form("That was an invalid username",password,verify,email)
            have_Error=True

        elif not valid_password(password):
            self.write_form(username,"That was an invalid password",verify,email)
            have_Error=True
        elif password!=verify:
            self.write_form(username,password,"Your passwords did not match",email)

        elif not valid_email(email):
            self.write_form(username,password,verify,"That was an invalid email")
            have_Error=True
    
        #if have_Error:
            #self.response.out.write(form)
        else:
            self.redirect('/welcome?username=%s'%username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username=self.request.get("username")
        if valid_username(username):
            self.response.out.write(welcome_form%{"username":username})
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
('/',Signup),('/welcome',Welcome)
], debug=True)
