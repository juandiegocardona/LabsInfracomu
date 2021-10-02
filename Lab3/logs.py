
#log
fecha = datetime.now()
filesize=os.path.getsize(filename)
log_name=f"{fecha.year}-{fecha.month}-{fecha.day}-{fecha.hour}-{fecha.minute}-{fecha.second}-log.txt"

file_log = open(f"servidor/Logs/{log_name}","x")

file_log.write(f"LOG {fecha}\n\n")
file_log.write(f"Archivo enviado: {filename.split('/')[2]}\n")
file_log.write(f"Tamaño archivo: {filesize} bytes\n")
file_log.write(f"Numero de Conexiones: {len(log_info)}\n\n")
file_log.write(f"Info de conexiones: \n")

for data in log_info:
    elementes=list(data.items())
    elementes.sort()
    for(key,val) in elements:
        file_log.write(f"\t{key}:{val}\n")
    file_log.write(f"\n")

file_log.close()

#recoleccion info log
conn_info=dict()
conn_info["Client ID"]=self.id
conn_info["Client IP"]=self.ip
conn_info["Client PORT"]=self.port
conn_info["Transfer Status"]= "Success" if hash_stat == "OK" else "ERROR"
conn_info["Transfer time"]= "%s miliseconds" % ((finish_time - start_time)*1000"
