# coding=utf8
"""
@app.route('/phase/byweek/', methods=['POST'])
def phaseByWeek():
    phase = PhaseDAO()
    s = []
    try:
        if request.method == 'POST':
            conn = Connexion().connect()
            for p in phase.getAllByFilter(conn, False, [], ('numWeek', request.form['numWeek'])):
                s.append(p.serial())
            return json.dumps(s, encoding="utf-8")
    except pymysql.err.Error:
        Connexion().exception()
    finally:
        Connexion().disconnect(conn)
"""

"""
@app.route('/phase/siteId/', methods=['POST'])
def phaseBySiteId():
    phases = PhaseDAO()
    assign = AssignmentDAO()
    need = NeedDAO()
    s = []
    try:
        conn = Connexion().connect()
        if request.method == 'POST':
            for i in phases.getAllByFilter(conn, False, [], ('numSite', request.form['num'])):
                k = 0
                for j in assign.getAllByFilter(conn, False, [], ('phase', str(i.num))):
                    k = k + 1
                    i.nbWorkers = k
                    total = 0
                    for n in need.getAllByFilter(conn, False, [], ("numPhase", str(i.num))):
                        total = total + n.need
                        i.totalWorkers = total
                        s.append(i.serial())
            return json.dumps(s, encoding="utf-8")
    except pymysql.err.Error:
        Connexion().exception()
    finally:
        Connexion().disconnect(conn)
"""