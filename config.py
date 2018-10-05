

mail = Mail()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drumcircle.sqlite'
app.config['SECRET_KEY'] = 'su93r-su93r-s3cr3t-qu1t3-h@r6-t0-h@ck'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 534
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'drummerscirclesupport@gmail.com'
app.config['MAIL_PASSWORD'] = 'drumc1rcl3@001'

admin = Admin(app)
mail.init_app(app)
