import os
if os.environ.get('APP_NAME') == None:
    check = 'development'
else:
    check = 'production'

print check