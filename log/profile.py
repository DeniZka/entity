import pstats
p = pstats.Stats("log/out.stat")

p.strip_dirs().sort_stats("tottime").print_stats()

#-m cProfile -o log/out.stat
#pyprof2calltree -i out.stat -o out.kgrind
#rund KCachegrind