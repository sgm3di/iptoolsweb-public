@app.route("/api/scan")
def scan_ports():
    import socket

    host = request.args.get("host", "")
    ports_param = request.args.get("ports", "")
    if not host:
        return jsonify({"error": "Missing host parameter"}), 400

    # Determinar puertos a escanear
    if ports_param:
        try:
            ports = [int(p.strip()) for p in ports_param.split(",") if p.strip().isdigit()]
        except ValueError:
            return jsonify({"error": "Invalid ports parameter"}), 400
    else:
        # Puertos comunes por defecto
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 587, 993, 995, 3306, 8080, 8443]

    if len(ports) > 20:
        return jsonify({"error": "Too many ports. Limit to 20."}), 400

    results = {}
    for port in ports:
        try:
            with socket.create_connection((host, port), timeout=2):
                results[port] = "open"
        except (socket.timeout, socket.error):
            results[port] = "closed"

    return jsonify({"host": host, "results": results})