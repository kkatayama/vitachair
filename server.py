from bottle import Bottle, route, request, run, template, static_file, debug, response, redirect
from rich import print
from pathlib import Path
import sys
import os

app = Bottle(__name__)

@app.route("/", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def index():
    response = {
        "message": "available_commands",
        "POST": {
            "/savedata": {
                "params": ["data", "filename"],
                "Example": {
                    "data": "heart_rate = 130\ntime=2022-03-10 10:40:01 AM",
                    "filename": "heart_rate_1.txt"
                },
                "NOTE": "This will store the data to /data/heart_rate_1.txt"
            }
        },
        "GET": {
            "/data/:filename": {
                "params": ["filename"],
                "Example": "https://vitachair.hopto.org/data/heart_rate_1.txt",
                "NOTE": "will retrieve the file: heart_rate_1.txt"
            }
        }
    }
    print(response)
    return response

@app.route('/savedata', method=["POST"])
def savedata():

    data = request.forms.get('data')
    filename = request.forms.get('filename')
    savepath = Path('data', filename)
    d = f'{data}'.replace('\\n', '\n')

    print(repr(data))
    print(repr(d))

    if isinstance(data, str):
        with open(savepath, 'w') as f:
            f.write(d)
    else:
        with open(savepath, 'wb') as f:
            f.write(d)

    response = f'file saved: {savepath}'
    print(response)
    return response


##########################################
#   ALLOW LOADING OF ALL STATIC FILES    #
##########################################
# Static Routes
@app.route('/data/<filename:re:.*\.*>')
def send_init(filename):
    print('here...')
    dirname = sys.path[0] + '/data/' # os.path.dirname(sys.argv[0])
    print('dirname = {}'.format(dirname))
    print('filename = {}'.format(filename))
    print(f'sending {filename}')
    return static_file(filename, root='{}'.format(dirname))

if __name__ == '__main__':
    # -- Run Web Server
    port = int(os.environ.get('PORT', 8282))
    run(app, host='0.0.0.0', port=port, reloader=True)
