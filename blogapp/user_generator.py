import string
import random

rand_str = lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)])
f = open('users.csv', 'w')
f.write('username,password,email,phone_num,address,dob,gender,created_at,blog_slug,blog_text,blog_is_published,blog_comments_allowed,blog_is_public,comment_text,ip\n')

for i in range(0, 5):
    user = rand_str(5)
    f.write(user + ',pass_john1,john@email.com,9248484848,76Street6-UK,2017-06-07,M,2017-04-01 18:00:00,blog1,This is blog text,TRUE,TRUE,TRUE,This is comment,127.0.0.1\n')
f.close()
