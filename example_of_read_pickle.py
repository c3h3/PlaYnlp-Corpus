'''
Created on Mar 1, 2014

@author: c3h3
'''

import pickle

with open("PTT___R_Language.pickle","rb") as read_file:
    read_pickle = pickle.load(read_file)

articles_df,articles_push_df = read_pickle

print articles_df.head(10)
print articles_df.shape

print articles_push_df.head(10) 
print articles_push_df.shape


if __name__ == '__main__':
    pass