from flask import Flask, render_template, request, jsonify
import os
from mylog import get_log
from sql import get_all_repo_list, get_history, delete_object, add_object, update_object, search_checkcode, get_all_user_list, get_all_user_log, update_user_info, check_user_exist, set_card_status, get_in_count, get_out_count, user_get_in, user_get_out
import serial
from pdu import get_pdu_data
import time

LAST_SEND_SMS = 0

# ser1 = serial.Serial("/dev/ttyS1", 115200)

logger = get_log('INFO')

# os.environ["PYDEVD_USE_FRAME_EVAL"] = "NO"
# os.environ["GEVENT_SUPPORT"] = 'True'

app = Flask(__name__, static_url_path='')

repo_status = {
    "temp": 25,
    "wet": 20,
    "co2": 0,
    "ch2O": 0,
    "tvoc": 0,
    "pm2.5": 0,
    "pm10": 0,
    "smoke": False,
    "error": False
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api", methods=['POST'])
def api():
    request_body = request.get_json()
    print(request_body)
    response_body = jsonify(request_body)
    return response_body


@app.route("/api/repo/get_status", methods=['GET'])
def repo_get_status():
    repo_status['in'] = get_in_count()
    repo_status['out'] = get_out_count()
    response_body = jsonify(repo_status)
    return response_body


@app.route("/api/repo/list", methods=['GET'])
def repo_list():
    response_body = jsonify(get_all_repo_list())
    return response_body


@app.route("/api/repo/history", methods=['POST'])
def repo_history():
    history = get_history(request.get_json()['id'])
    history.sort(key=lambda x: x['id'])
    response_body = jsonify(history)
    return response_body


@app.route("/api/repo/delete", methods=['POST'])
def repo_delete():
    delete_object(request.get_json()['id'])
    return jsonify({"code": 0, "msg": "success"})


@app.route("/api/repo/add", methods=['POST'])
def repo_add():
    add_object(request.get_json()['name'], 0)
    return jsonify({"code": 0, "msg": "success"})


@app.route("/api/repo/in", methods=['GET'])
def repo_item_in():
    update_object(request.args.get('id'), 1)
    return jsonify({"code": 0, "msg": "success"})


@app.route("/api/repo/out", methods=['GET'])
def repo_item_out():
    update_object(request.args.get('id'), 3)
    return jsonify({"code": 0, "msg": "success"})


@app.route("/api/repo/takeout", methods=['POST'])
def repo_item_takeout():
    update_object(request.get_json()['id'], 2)
    return jsonify({"code": 0, "msg": "success"})


@app.route("/api/repo/delete", methods=['POST'])
def repo_item_delete():
    delete_object(request.get_json()['id'])
    return jsonify({"code": 0, "msg": "success"})


@app.route("/api/repo/card", methods=['GET'])
def repo_in():
    card = request.args.get("card")
    if card is None:
        return jsonify({"code": 1, "msg": "card is null"})
    set_card_status(card)
    return jsonify({"code": 0, "msg": card})
    # update_object(request.get_json()['id'], 1)
    # return jsonify({"code": 0, "msg": "success"})


@app.route("/api/repo/status", methods=['GET'])
def repo_set_status():
    global repo_status, LAST_SEND_SMS
    repo_status['temp'] = float(str(request.args.get("temp")))
    repo_status['wet'] = float(str(request.args.get("humi")))
    repo_status['co2'] = float(str(request.args.get("CO2")))
    repo_status['ch2o'] = float(str(request.args.get("CH2O")))
    repo_status['tvoc'] = float(str(request.args.get("TVOC")))
    repo_status['pm2.5'] = float(str(request.args.get("PM2.5")))
    repo_status['pm10'] = float(str(request.args.get("PM10")))
    if repo_status['temp'] > 20:
        if time.time()-LAST_SEND_SMS > 60:
            print("温度过高！！！")
            # ser1.write(get_pdu_data(
            #     f"温度过高，当前温度 {repo_status['temp']} ℃").encode())
            # time.sleep(1)
            # ser1.read(ser1.in_waiting)
            LAST_SEND_SMS = time.time()
        repo_status['error'] = True
    else:
        repo_status['error'] = False
    req = request.args
    return jsonify({"code": 0, "msg": req})
    # update_object(request.get_json()['id'], 1)
    # return jsonify({"code": 0, "msg": "success"})


@app.route("/api/repo/search", methods=['POST'])
def repo_search():
    try:
        return jsonify(search_checkcode(request.get_json()['checkcode'])[0])
    except:
        return jsonify({})


@app.route("/api/user/list", methods=['GET'])
def user_list():
    return jsonify(get_all_user_list())


@app.route("/api/user/log", methods=['GET'])
def user_log():
    return jsonify(get_all_user_log())


@app.route("/api/user/get_in", methods=['GET'])
def user_log_get_in():
    id, name, temp = request.args.get("id"), request.args.get(
        "name"), request.args.get("temp")
    user_get_in(id, name, temp)
    return jsonify({"code": 0, "msg": "success"})


@app.route("/api/user/get_out", methods=['GET'])
def user_log_get_out():
    id, name, temp = request.args.get("id"), request.args.get(
        "name"), request.args.get("temp")
    user_get_out(id, name, temp)
    return jsonify({"code": 0, "msg": "success"})


@app.route("/api/user/modify", methods=['POST'])
def user_modify():
    update_user_info(request.get_json()['uid'], request.get_json()[
                     'password'], request.get_json()['permission'])
    return jsonify({"code": 0, "msg": "success"})


@app.route("/api/user/signin", methods=['POST'])
def user_signin():
    if check_user_exist(request.get_json()['username'], request.get_json()[
            'password']):
        return jsonify({"code": 0, "msg": "success"})
    else:
        return jsonify({"code": 1, "msg": "fail"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
