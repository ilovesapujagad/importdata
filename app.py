import json
import os
import requests
from sys import stderr
from flask import Flask, request, jsonify,make_response

app = Flask(__name__)

api_key = os.environ.get("API_KEY", "")
if api_key == "":
    print("api key is required", file=stderr)

api_base_url = "https://api.stagingv3.microgen.id/query/api/v1/" + api_key

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask</h2>'


# @app.post("/api/importnote")
# def importnote():
#     source = str(request.args.get('JSESSIONID'))
#     filex = request.files['file']
#     name = request.form['name']
#     cookies = f"JSESSIONID={source}"
#     text = filex.read()
#     xx = json.loads(text)
#     print(cookies)
#     try:
#         response2 = requests.post('https://ipqlftmgzk.function.microgen.id/api/createnote?'+cookies+'',json={"name":str(name)})
#         data = response2.json()
#         sdata = str(data["body"])
#         try:
#             for  paragraphs in xx['paragraphs']:
#                 text= str(paragraphs['text'])
#                 texts= "Paragraph insert revised"
#                 url2 = 'https://ipqlftmgzk.function.microgen.id/api/notebook/'+sdata+'/paragraph?'+cookies+''
#                 response3 = requests.post(url2,json={"title": texts,"text":text })
#             return data    
#         except:
#             return jsonify({"msg": "error paragraph"}), 400
#     except:
#         return jsonify({"msg": "error create notebook"}), 400

@app.post("/api/importnote")
def importnote():
    source = str(request.args.get('JSESSIONID'))
    filex = request.files['file']
    name = request.form['name']
    cookies = f"JSESSIONID={source}"
    text = filex.read()
    xx = json.loads(text)
    print(cookies)
    try:
        response2 = requests.post('https://ipqlftmgzk.function.microgen.id/api/createnote?'+cookies+'',json={"name":str(name)})
        data = response2.json()
        sdata = str(data["body"])

        for  paragraphs in xx['paragraphs']:

            try:
                text= str(paragraphs['text'])
                texts= "Paragraph insert revised"
                url2 = 'https://ipqlftmgzk.function.microgen.id/api/notebook/'+sdata+'/paragraph?'+cookies+''
                response3 = requests.post(url2,json={"title": texts,"text":text })
            except:
                continue
            else:
                continue

        return data
    except:
        return jsonify({"msg": "error create notebook"}), 400

@app.post("/api/create/sourcecode")
def sourcecode():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        request_data = request.get_json()
        database = request_data['database']
        table = request_data['table']
        path_file = request_data['path_file']
        name = request_data['name']
        zepPass = str(request_data['zepPass'])
        zepUser = str(request_data['zepUser'])
        if not database:
            return jsonify({"msg": "Missing database parameter"}), 400
        if not table:
            return jsonify({"msg": "Missing table parameter"}), 400
        if not path_file:
            return jsonify({"msg": "Missing path_file parameter"}), 400
        if not name:
            return jsonify({"msg": "Missing name parameter"}), 400
        try:
            url = 'https://ipqlftmgzk.function.microgen.id/api/login'
            response1 = requests.post(url,data={'username': zepPass, 'password':zepUser})
            source = str(response1.json()["Set-Cookie"])
            try:
                url1 = 'https://ipqlftmgzk.function.microgen.id/api/createnote?'+source+''
                response2 = requests.post(url1,json={"name":str(name)})
                data = response2.json()
                sdata = str(data["body"])
                try:
                    text1 = "%md\r\n\r\n## Overview\r\n\r\nThis notebook will show you how to create and query a table or DataFrame that you uploaded to HIVE. \r\n\r\nThis notebook is written in **Python** so the default cell type is Python. However, you can use different languages by using the\r\n`%LANGUAGE` syntax. Python, Scala, SQL, and R are all supported."
                    url3 = 'https://ipqlftmgzk.function.microgen.id/api/notebook/'+sdata+'?'+source+''
                    responseget = requests.get(url3)
                    data = responseget.json()
                    paragraphid = str(data["body"]["paragraphs"][0]["id"])
                    url4 = 'https://ipqlftmgzk.function.microgen.id/api/notebook/'+sdata+'/paragraph/'+paragraphid+'?'+source+''
                    responseput = requests.put(url4,json={"text":str(text1)})
                    try:
                        text = "%jdbc(hive)\nLOAD DATA INPATH '"+path_file+"' INTO TABLE "+database+"."+table+"\n"
                        url2 = 'https://ipqlftmgzk.function.microgen.id/api/notebook/'+sdata+'/paragraph?'+source+''
                        response3 = requests.post(url2,json={"title": "Paragraph insert revised","text":text })
                        try:
                            text12 = "%jdbc(hive)\nselect * from "+database+"."+table+"\n"
                            url12 = 'https://ipqlftmgzk.function.microgen.id/api/notebook/'+sdata+'/paragraph?'+source+''
                            response1 = requests.post(url12,json={"title": "Paragraph insert revised","text":text12 })
                            url = "https://sapujagad.id/sjnotebook/"+sdata+""
                            my_dict = {}
                            my_dict['Url']= url
                            xs = make_response(my_dict)
                            return xs
                        except:
                            return jsonify({"msg": "Missing create paragraph2 code"}), 500
                    except:
                        return jsonify({"msg": "Missing create paragraph code"}), 500
                except:
                    return jsonify({"msg": "Missing update paragraph code"}), 500
            except:
                return jsonify({"msg": "Missing create note"}), 500
        except:
            return jsonify({"msg": "Missing Authorization"}), 400
    except:
        return jsonify({"msg": "error json input"}), 400

@app.post("/api/importsc/python")
def importpython():
    filess = request.files['file']
    name = request.form['name']
    try:
        cookies = str(request.args.get('JSESSIONID'))
        source = f"JSESSIONID={cookies}"
        try:
            url1 = 'https://ipqlftmgzk.function.microgen.id/api/createnote?'+source+''
            response2 = requests.post(url1,json={"name":str(name)})
            data = response2.json()
            sdata = str(data["body"])
            try:
                text1 = "%md"
                url3 = 'https://ipqlftmgzk.function.microgen.id/api/notebook/'+sdata+'?'+source+''
                responseget = requests.get(url3)
                data = responseget.json()
                paragraphid = str(data["body"]["paragraphs"][0]["id"])
                url4 = 'https://ipqlftmgzk.function.microgen.id/api/notebook/'+sdata+'/paragraph/'+paragraphid+'?'+source+''
                responseput = requests.put(url4,json={"text":str(text1)})
                try:
                    
                    text = filess.read()
                    xx = text.decode("utf-8")
                    xxx = "%python\r\n\r\n"
                    zzzz = xxx+xx
                    texts = {}
                    texts['text']= zzzz
                    texts['title'] = "Paragraph insert revised"
                    url2 = 'https://ipqlftmgzk.function.microgen.id/api/notebook/'+sdata+'/paragraph?'+source+''
                    response3 = requests.post(url2,json=texts)
                    url = "https://sapujagad.id/sjnotebook/"+sdata+""
                    my_dict = {}
                    my_dict['Url']= url
                    xs = make_response(my_dict)
                    return xs
                except:
                    return jsonify({"msg": "Missing create paragraph code"}), 500
            except:
                return jsonify({"msg": "Missing update paragraph code"}), 500
        except:
            return jsonify({"msg": "Missing create note"}), 500
    except:
        return jsonify({"msg": "Missing Authorization"}), 400

if __name__ == "__main__":
    app.run(debug=True)
