# -*- coding: utf-8 -*-
import re
import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_object(__name__)


def get_whois(domain_or_ip):
    """get whois information of domain or ip"""
    return  subprocess.Popen(["whois", domain_or_ip], stdout=subprocess.PIPE).communicate()[0]


def input_testing(test_input):
    """test and split input user"""
    test_input_obr = test_input.strip()
    if re.compile(u'^http:\/\/').match(test_input_obr):
        test_input_obr = test_input_obr.replace('http://', '')
    if re.compile(u'^www\.').match(test_input_obr):
        test_input_obr = test_input_obr.replace('www.', '')
    if re.compile(u'^[а-яёА-ЯЁa-zA-Z0-9\-\.]+$').match(test_input_obr):
        return test_input_obr
    else:
        return False


@app.route('/', methods=['GET'])
def index():
    u"""view for user

    GET-params:
      domain: search whois-info for this domain
    """
    domain = request.args.get('domain')
    if domain:
        search_domain = input_testing(domain)
        if search_domain:
            info_whois = get_whois(search_domain).decode("utf-8")
            info_whois_template = info_whois.split("\n")
            return render_template('main.html', info_whois=info_whois_template,
                                   input_domain=search_domain,
                                   novalid=False)
        else:
            return render_template(
                'main.html', input_domain=False,
                novalid=u"Вы ввели неправильное имя домена"
                    u" или неверный IP-адрес, пожалуйста, попробуйте снова")
    else:
        return render_template('main.html', input_domain=False, info_whois=None)

if __name__ == "__main__":
    app.run(debug=True)
