import socket
import ipaddress
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

LANGS = {
    'en': {
        'title': 'Network Tester',
        'ip_address': 'IP Address',
        'subnet': 'Subnet',
        'domain': 'Domain',
        'port': 'Port',
        'test': 'Test',
        'invalid_ip': 'Invalid IP address',
        'ip_in_subnet': 'IP {ip} is in subnet {subnet}',
        'ip_not_in_subnet': 'IP {ip} is NOT in subnet {subnet}',
        'domain_resolves': 'Domain {domain} resolves to {ip}',
        'domain_fail': 'Domain {domain} could not be resolved',
        'port_open': 'Port {port} is OPEN on {ip}',
        'port_closed': 'Port {port} is CLOSED on {ip}',
    },
    'tr': {
        'title': 'Ag Dı Testleri',
        'ip_address': 'IP Adresi',
        'subnet': 'Alt Ağ (subnet)',
        'domain': 'Alan Adı',
        'port': 'Port',
        'test': 'Test Et',
        'invalid_ip': 'Geçersiz IP adresi',
        'ip_in_subnet': 'IP {ip}, {subnet} alt ağında',
        'ip_not_in_subnet': 'IP {ip}, {subnet} alt ağında DEĞİL',
        'domain_resolves': '{domain} alan adı {ip} adresine çözüldü',
        'domain_fail': '{domain} alan adı çözülemedi',
        'port_open': '{ip} adresinde {port} portu AÇIK',
        'port_closed': '{ip} adresinde {port} portu KAPALI',
    },
    'ru': {
        'title': 'Сетевой Тестер',
        'ip_address': 'IP Адрес',
        'subnet': 'Субнет',
        'domain': 'Домен',
        'port': 'Порт',
        'test': 'Тест',
        'invalid_ip': 'Неверный IP-адрес',
        'ip_in_subnet': 'IP {ip} в сети {subnet}',
        'ip_not_in_subnet': 'IP {ip} НЕ в сети {subnet}',
        'domain_resolves': 'Домен {domain} разрешён в {ip}',
        'domain_fail': 'Домен {domain} не разрешился',
        'port_open': 'Порт {port} открыт на {ip}',
        'port_closed': 'Порт {port} закрыт на {ip}',
    },
    'tk': {
        'title': 'Ulgam Synagçy',
        'ip_address': 'IP Salgy',
        'subnet': 'Subnet',
        'domain': 'Domen',
        'port': 'Port',
        'test': 'Synag et',
        'invalid_ip': 'Nädogry IP salgysy',
        'ip_in_subnet': '{ip} {subnet} ulgamynda',
        'ip_not_in_subnet': '{ip} {subnet} ulgamynda DÄL',
        'domain_resolves': '{domain} domeni {ip} salgyýsyna döndü',
        'domain_fail': '{domain} domeni dönmedi',
        'port_open': '{ip} salgysynda {port} porty AÇYK',
        'port_closed': '{ip} salgysynda {port} porty ×YKLY',
    }
}


def translate(key, lang):
    return LANGS.get(lang, LANGS['en']).get(key, key)


@app.route('/', methods=['GET', 'POST'])
def index():
    lang = request.args.get('lang', 'en')
    result = None
    if request.method == 'POST':
        ip = request.form.get('ip')
        subnet = request.form.get('subnet')
        domain = request.form.get('domain')
        port = request.form.get('port')
        # IP validation
        try:
            ip_obj = ipaddress.ip_address(ip)
        except ValueError:
            result = translate('invalid_ip', lang)
            return render_template('index.html', t=translate, lang=lang, result=result)

        # Subnet test
        if subnet:
            try:
                net = ipaddress.ip_network(subnet, strict=False)
                if ip_obj in net:
                    result = translate('ip_in_subnet', lang).format(ip=ip, subnet=subnet)
                else:
                    result = translate('ip_not_in_subnet', lang).format(ip=ip, subnet=subnet)
            except ValueError:
                result = translate('invalid_ip', lang)
        # Domain test
        elif domain:
            try:
                domain_ip = socket.gethostbyname(domain)
                result = translate('domain_resolves', lang).format(domain=domain, ip=domain_ip)
            except socket.gaierror:
                result = translate('domain_fail', lang).format(domain=domain)
        # Port test
        elif port:
            try:
                port_int = int(port)
                s = socket.socket()
                s.settimeout(2)
                if s.connect_ex((ip, port_int)) == 0:
                    result = translate('port_open', lang).format(ip=ip, port=port)
                else:
                    result = translate('port_closed', lang).format(ip=ip, port=port)
                s.close()
            except Exception:
                result = translate('port_closed', lang).format(ip=ip, port=port)
    return render_template('index.html', t=translate, lang=lang, result=result)


if __name__ == '__main__':
    app.run(debug=True)
