import click
import subprocess
import os
import shlex

@click.command()
@click.argument('fifoname')
@click.argument('collectorip')
def steersherpa(fifoname,collectorip):

  fullfifoname = fifoname+'.hepmc2g'

  click.secho('running on fifo {}'.format(fullfifoname), fg = 'green')

  os.mkfifo(fullfifoname)
  sherpa = subprocess.Popen(shlex.split('Sherpa -f dummy.dat OUTFILE:={}'.format(fifoname)))

  import time
  time.sleep(1)
  subprocess.check_call(shlex.split('mprtect_server {} {}'.format(os.path.abspath(fullfifoname),collectorip)))
  sherpa.wait()
  click.secho('Bye', fg = 'green')
  os.remove(fullfifoname)
  
if __name__ == '__main__':
  steersherpa()
