# rpi-dashboard

Created using Claude AI

Dashboard for raspberry pi

Build tutorial

    mkdir -p /home/claude/rpi-dashboard/templates && cd /home/claude/rpi-dashboard && ls -la

After sending files to raspberry pi
Put index.html file in /home/claude/rpi-dashboard/templates directory
And then continue

    cd /home/claude/rpi-dashboard && pip install --break-system-packages -q -r requirements.txt 2>&1 | tail -20
    
    cd /home/claude/rpi-dashboard && python3 -c "import ast; ast.parse(open('app.py').read())" && echo "app.py: OK syntax" &&          python3 -c "
    import html.parser
    class P(html.parser.HTMLParser):
        pass
    p = P()
    p.feed(open('templates/index.html').read())
    print('index.html: parsed without error')
    "

    cd /home/claude/rpi-dashboard && nohup python3 app.py > /tmp/flask.log 2>&1 & sleep 2 && cat /tmp/flask.log

