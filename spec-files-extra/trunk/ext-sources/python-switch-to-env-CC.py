import re, os
import distutils.sysconfig
#exmaple hipster 2018
#
print "CC=\'" + re.sub(r'^/usr/.*/gcc', os.environ.get('CC'), distutils.sysconfig.get_config_var('CC')) + "\'" \
" CXX=\'" + re.sub(r'^/usr/.*/g\+\+', os.environ.get('CXX'), distutils.sysconfig.get_config_var('CXX')) + "\'" \
" LDSHARED=\'" + re.sub(r'^/usr/.*/gcc', os.environ.get('CC'), distutils.sysconfig.get_config_var('LDSHARED')) + "\'"

