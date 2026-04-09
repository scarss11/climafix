import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from config import Config
import models.usuarios as Usuarios
import models.clientes as Clientes
import models.tecnicos as Tecnicos
import models.equipos as Equipos
import models.ordenes as Ordenes
import models.mantenimientos as Mantenimientos
import models.repuestos as Repuestos
import models.cotizaciones as Cotizaciones

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# ── No-cache en rutas protegidas ──────────────────────────────
@app.after_request
def no_cache(resp):
    if request.path.startswith(('/admin', '/tecnico', '/cliente', '/api')):
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        resp.headers['Pragma'] = 'no-cache'
    return resp

# ── Helpers ───────────────────────────────────────────────────
def login_required(rol=None):
    """Devuelve redirect si el usuario no está logueado o no tiene el rol."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if rol and session.get('rol') != rol:
        return redirect(url_for('dashboard'))
    return None

# ════════════════════════════════════════════════════════════
# AUTH
# ════════════════════════════════════════════════════════════
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email','').strip()
        pw    = request.form.get('password','')
        user  = Usuarios.get_by_email(email)
        if user and Usuarios.verify_password(user, pw):
            session['user_id'] = user['id']
            session['nombre']  = user['nombre']
            session['rol']     = user['rol']
            session['email']   = user['email']
            return redirect(url_for('dashboard'))
        flash('Credenciales incorrectas', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    guard = login_required()
    if guard: return guard
    rol = session['rol']
    if rol == 'admin':
        stats = Ordenes.count_by_estado()
        clientes  = Clientes.get_all()
        tecnicos  = Tecnicos.get_all()
        ordenes   = Ordenes.get_all()
        cots      = Cotizaciones.get_all()
        return render_template('admin/dashboard.html',
            stats=stats, clientes=clientes, tecnicos=tecnicos,
            ordenes=ordenes, cotizaciones=cots)
    if rol == 'tecnico':
        tec = Tecnicos.get_by_usuario(session['user_id'])
        ordenes = Ordenes.get_by_tecnico(tec['id']) if tec else []
        return render_template('tecnico/dashboard.html', ordenes=ordenes, tecnico=tec)
    # cliente
    cli = Clientes.get_by_usuario(session['user_id'])
    ordenes = Ordenes.get_by_cliente(cli['id']) if cli else []
    cots    = Cotizaciones.get_by_cliente(cli['id']) if cli else []
    equipos = Equipos.get_by_cliente(cli['id']) if cli else []
    return render_template('cliente/dashboard.html',
        ordenes=ordenes, cotizaciones=cots, equipos=equipos, cliente=cli)

# ════════════════════════════════════════════════════════════
# ADMIN — CLIENTES
# ════════════════════════════════════════════════════════════
@app.route('/admin/clientes')
def admin_clientes():
    guard = login_required('admin')
    if guard: return guard
    return render_template('admin/clientes.html', clientes=Clientes.get_all())

@app.route('/admin/clientes/crear', methods=['POST'])
def admin_clientes_crear():
    guard = login_required('admin')
    if guard: return guard
    Clientes.create(
        request.form['nombre'],
        request.form.get('telefono',''),
        request.form.get('direccion','')
    )
    flash('Cliente creado', 'ok')
    return redirect(url_for('admin_clientes'))

@app.route('/admin/clientes/<int:cid>/editar', methods=['POST'])
def admin_clientes_editar(cid):
    guard = login_required('admin')
    if guard: return guard
    Clientes.update(cid, request.form['nombre'], request.form.get('telefono',''), request.form.get('direccion',''))
    flash('Cliente actualizado', 'ok')
    return redirect(url_for('admin_clientes'))

@app.route('/admin/clientes/<int:cid>/eliminar', methods=['POST'])
def admin_clientes_eliminar(cid):
    guard = login_required('admin')
    if guard: return guard
    Clientes.delete(cid)
    flash('Cliente eliminado', 'ok')
    return redirect(url_for('admin_clientes'))

# ════════════════════════════════════════════════════════════
# ADMIN — TÉCNICOS
# ════════════════════════════════════════════════════════════
@app.route('/admin/tecnicos')
def admin_tecnicos():
    guard = login_required('admin')
    if guard: return guard
    return render_template('admin/tecnicos.html', tecnicos=Tecnicos.get_all())

@app.route('/admin/tecnicos/crear', methods=['POST'])
def admin_tecnicos_crear():
    guard = login_required('admin')
    if guard: return guard
    Tecnicos.create(request.form['nombre'], request.form.get('especialidad',''))
    flash('Técnico creado', 'ok')
    return redirect(url_for('admin_tecnicos'))

@app.route('/admin/tecnicos/<int:tid>/editar', methods=['POST'])
def admin_tecnicos_editar(tid):
    guard = login_required('admin')
    if guard: return guard
    Tecnicos.update(tid, request.form['nombre'], request.form.get('especialidad',''))
    flash('Técnico actualizado', 'ok')
    return redirect(url_for('admin_tecnicos'))

@app.route('/admin/tecnicos/<int:tid>/eliminar', methods=['POST'])
def admin_tecnicos_eliminar(tid):
    guard = login_required('admin')
    if guard: return guard
    Tecnicos.delete(tid)
    flash('Técnico eliminado', 'ok')
    return redirect(url_for('admin_tecnicos'))

# ════════════════════════════════════════════════════════════
# ADMIN — EQUIPOS
# ════════════════════════════════════════════════════════════
@app.route('/admin/equipos')
def admin_equipos():
    guard = login_required('admin')
    if guard: return guard
    return render_template('admin/equipos.html',
        equipos=Equipos.get_all(), clientes=Clientes.get_all())

@app.route('/admin/equipos/crear', methods=['POST'])
def admin_equipos_crear():
    guard = login_required('admin')
    if guard: return guard
    Equipos.create(
        request.form['tipo'], request.form.get('marca',''),
        request.form.get('modelo',''), request.form.get('numero_serie',''),
        request.form['cliente_id']
    )
    flash('Equipo creado', 'ok')
    return redirect(url_for('admin_equipos'))

@app.route('/admin/equipos/<int:eid>/eliminar', methods=['POST'])
def admin_equipos_eliminar(eid):
    guard = login_required('admin')
    if guard: return guard
    Equipos.delete(eid)
    flash('Equipo eliminado', 'ok')
    return redirect(url_for('admin_equipos'))

# ════════════════════════════════════════════════════════════
# ADMIN — ÓRDENES
# ════════════════════════════════════════════════════════════
@app.route('/admin/ordenes')
def admin_ordenes():
    guard = login_required('admin')
    if guard: return guard
    return render_template('admin/ordenes.html',
        ordenes=Ordenes.get_all(),
        clientes=Clientes.get_all(),
        tecnicos=Tecnicos.get_all(),
        equipos=Equipos.get_all())

@app.route('/admin/ordenes/crear', methods=['POST'])
def admin_ordenes_crear():
    guard = login_required('admin')
    if guard: return guard
    Ordenes.create(
        request.form.get('descripcion',''),
        request.form['cliente_id'],
        request.form['tecnico_id'],
        request.form['equipo_id']
    )
    flash('Orden creada', 'ok')
    return redirect(url_for('admin_ordenes'))

@app.route('/admin/ordenes/<int:oid>/estado', methods=['POST'])
def admin_ordenes_estado(oid):
    guard = login_required('admin')
    if guard: return guard
    Ordenes.update_estado(oid, request.form['estado'])
    flash('Estado actualizado', 'ok')
    return redirect(url_for('admin_ordenes'))

@app.route('/admin/ordenes/<int:oid>/eliminar', methods=['POST'])
def admin_ordenes_eliminar(oid):
    guard = login_required('admin')
    if guard: return guard
    Ordenes.delete(oid)
    flash('Orden eliminada', 'ok')
    return redirect(url_for('admin_ordenes'))

@app.route('/admin/ordenes/<int:oid>')
def admin_orden_detalle(oid):
    guard = login_required('admin')
    if guard: return guard
    orden = Ordenes.get_by_id(oid)
    mantenimientos = Mantenimientos.get_by_orden(oid)
    repuestos = Repuestos.get_all()
    return render_template('admin/orden_detalle.html',
        orden=orden, mantenimientos=mantenimientos, repuestos=repuestos)

# ════════════════════════════════════════════════════════════
# ADMIN — COTIZACIONES
# ════════════════════════════════════════════════════════════
@app.route('/admin/cotizaciones')
def admin_cotizaciones():
    guard = login_required('admin')
    if guard: return guard
    return render_template('admin/cotizaciones.html',
        cotizaciones=Cotizaciones.get_all(),
        clientes=Clientes.get_all(),
        ordenes=Ordenes.get_all())

@app.route('/admin/cotizaciones/crear', methods=['POST'])
def admin_cotizaciones_crear():
    guard = login_required('admin')
    if guard: return guard
    Cotizaciones.create(
        request.form['total'],
        request.form.get('notas',''),
        request.form['cliente_id'],
        request.form.get('orden_id') or None
    )
    flash('Cotización creada', 'ok')
    return redirect(url_for('admin_cotizaciones'))

@app.route('/admin/cotizaciones/<int:cid>/estado', methods=['POST'])
def admin_cotizaciones_estado(cid):
    guard = login_required('admin')
    if guard: return guard
    Cotizaciones.update_estado(cid, request.form['estado'])
    flash('Estado actualizado', 'ok')
    return redirect(url_for('admin_cotizaciones'))

@app.route('/admin/cotizaciones/<int:cid>/eliminar', methods=['POST'])
def admin_cotizaciones_eliminar(cid):
    guard = login_required('admin')
    if guard: return guard
    Cotizaciones.delete(cid)
    flash('Cotización eliminada', 'ok')
    return redirect(url_for('admin_cotizaciones'))

# ════════════════════════════════════════════════════════════
# TÉCNICO
# ════════════════════════════════════════════════════════════
@app.route('/tecnico/orden/<int:oid>')
def tecnico_orden(oid):
    guard = login_required('tecnico')
    if guard: return guard
    orden = Ordenes.get_by_id(oid)
    mantenimientos = Mantenimientos.get_by_orden(oid)
    repuestos = Repuestos.get_all()
    return render_template('tecnico/orden_detalle.html',
        orden=orden, mantenimientos=mantenimientos, repuestos=repuestos)

@app.route('/tecnico/orden/<int:oid>/registrar', methods=['POST'])
def tecnico_registrar_mantenimiento(oid):
    guard = login_required('tecnico')
    if guard: return guard
    row = Mantenimientos.create(
        request.form['tipo'],
        request.form.get('descripcion',''),
        request.form.get('evidencia_url',''),
        oid
    )
    if row:
        mid = row['id']
        rep_ids = request.form.getlist('repuesto_id')
        cantidades = request.form.getlist('cantidad')
        for rid, cant in zip(rep_ids, cantidades):
            if rid and cant:
                Mantenimientos.add_repuesto(mid, int(rid), int(cant))
        # Si se marcan como completada
        if request.form.get('completar'):
            Ordenes.update_estado(oid, 'completada')
    flash('Mantenimiento registrado', 'ok')
    return redirect(url_for('tecnico_orden', oid=oid))

# ════════════════════════════════════════════════════════════
# CLIENTE
# ════════════════════════════════════════════════════════════
@app.route('/cliente/solicitar', methods=['POST'])
def cliente_solicitar():
    guard = login_required('cliente')
    if guard: return guard
    cli = Clientes.get_by_usuario(session['user_id'])
    if not cli:
        flash('No tienes perfil de cliente', 'error')
        return redirect(url_for('dashboard'))
    Ordenes.create(
        request.form.get('descripcion',''),
        cli['id'], None,
        request.form.get('equipo_id') or None
    )
    flash('Solicitud enviada correctamente', 'ok')
    return redirect(url_for('dashboard'))

# ════════════════════════════════════════════════════════════
# API JSON — para el dashboard stats
# ════════════════════════════════════════════════════════════
@app.route('/api/stats')
def api_stats():
    guard = login_required('admin')
    if guard: return jsonify({'error': 'unauthorized'}), 401
    stats  = Ordenes.count_by_estado()
    total_cots = len(Cotizaciones.get_all() or [])
    total_cli  = len(Clientes.get_all() or [])
    total_tec  = len(Tecnicos.get_all() or [])
    return jsonify({
        'ordenes': stats,
        'cotizaciones': total_cots,
        'clientes': total_cli,
        'tecnicos': total_tec
    })

if __name__ == '__main__':
    app.run(debug=True)
