import click
import subprocess
import os
import shlex
import zipfile
import yaml
import requests

@click.command()
@click.argument('inputzipurl')
@click.argument('fifoname')
@click.argument('collectorip')
def steersherpa(inputzipurl,fifoname,collectorip):


  r = requests.get(inputzipurl)
  if not r.ok:
      click.Abort()
  with open('input.zip','w') as f:
      f.write(r.content)
  zipped     = zipfile.ZipFile('input.zip')
  arethafile = [f for f in zipped.filelist if 'aretha.yml' in f.filename][0].filename
  zipped.extractall()
  arethayml = yaml.load(open(arethafile))
  runcard   = '{}/{}'.format(os.path.dirname(arethafile),arethayml['runcard'])

  fullfifoname = fifoname+'.hepmc2g'

  click.secho('running on runcard {} and fifo {}'.format(runcard,fullfifoname), fg = 'green')
  os.mkfifo(fullfifoname)
  sherpa = subprocess.Popen(shlex.split('Sherpa -f {} OUTFILE:={}'.format(runcard,fifoname)))

  import time
  time.sleep(1)
  subprocess.check_call(shlex.split('mprtect_server {} {}'.format(os.path.abspath(fullfifoname),collectorip)))
  sherpa.wait()
  click.secho('Bye', fg = 'green')
  os.remove(fullfifoname)
  
if __name__ == '__main__':
  steersherpa()
