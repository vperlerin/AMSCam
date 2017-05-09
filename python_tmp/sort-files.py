import glob
import os

images = glob.glob('jpgs_sort/*.jpg')
lu = 0
ld = 0
ru = 0
rd = 0
llu = 0
lld = 0
rru = 0
rrd = 0
lluu = 0
lldd = 0
rruu = 0
rrdd = 0

for fname in images:
   if 'leftup' in fname and lu < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      lu = lu + 1
   if 'leftdown' in fname and ld < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      ld = ld + 1
   if 'rightdown' in fname and rd < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      rd = rd + 1
   if 'rightup' in fname and ru < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      ru = ru + 1
   if 'rightrightup' in fname and rru < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      rru = rru + 1
   if 'rightrightdown' in fname and rrd < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      rrd = rrd + 1
   if 'leftleftup' in fname and llu < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      llu = llu + 1
   if 'leftleftdown' in fname and lld < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      lld = lld + 1
   if 'leftleftdowndown' in fname and lldd < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      lldd = lldd + 1
   if 'leftleftupup' in fname and lluu < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      lluu = lluu + 1
   if 'rightrightupup' in fname and rruu < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      rruu = rruu + 1
   if 'rightrightdowndown' in fname and rrdd < 5:
      new_fname = fname.replace("jpgs_sort", "jpgs_final")
      cmd = "cp " + fname + " " + new_fname
      os.system(cmd)
      rrdd = rrdd + 1

