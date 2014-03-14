Srsync
======

Script python para sincronizar archivos cuando sean modificados, borrados etc...

Esta librería es dependiente del packete python watchdog https://github.com/gorakhargosh/watchdog

Srsync para unidades remotas se necesita (MAC OS X) FUSE http://osxfuse.github.io/

Monstar la unidad remota con Mac Fuse y SSHFS:
----------------------------------------------

https://www.digitalocean.com/community/articles/how-to-use-sshfs-to-mount-remote-file-systems-over-ssh

```html
sudo apt-get install sshfs

sshfs -o IdentityFile=~/.ssh/<llave-privada> root@<servidor>:<camino-al-directorio-REMOTO> <camino-al-directorio-LOCAL> -o volname=<nombre-de-directorio-en-local>

```

Configuración del Srsync:
-------------------------

```html
self.folderBase = "<nombre-directorio-base-comun-en-LOCAL-y-REMOTO>"
self.localPath = "<camino-al-directorio-LOCAL>"
self.remotePath = "<camino-al-directorio-REMOTO>"
```

Ejecutar el Srsync:
-------------------

```html
python watch.py <directorio-que-va-escuchar-watch>
```
