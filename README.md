Srsync
======

Script python para sincronizar archivos cuando sean modificados, borrados etc...

Esta librería es dependiente del packete python watchdog https://github.com/gorakhargosh/watchdog

Srsync para unidades remotas se necesita (MAC OS X) FUSE http://osxfuse.github.io/

Monstar la unidad remota con Mac Fuse y SSHFS https://www.digitalocean.com/community/articles/how-to-use-sshfs-to-mount-remote-file-systems-over-ssh

```html
sudo apt-get install sshfs

sshfs -o IdentityFile=~/.ssh/<private-key> root@<server>:<server-path> <local-directory> -o volname=<directory-name>

```
