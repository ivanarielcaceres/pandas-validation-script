
# coding: utf-8

# In[9]:


import re
import os
import math
import numpy as np
import pandas as pd
from files.validations.sales_transactional_other import SALES_TRANSACTIONAL_OTHER_VALIDATION
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.WARNING)
logger = logging.getLogger()


# # Read all files in Sales transactional directory

# In[10]:


FILE_NAME_PATTERN = 'YY_MM_SALES_OTH_MX.CSV'
files = os.listdir('files/outbound/it/sales_transactional')
files = list(filter(lambda x: bool(re.match('\d{2}_\d{2}_SALES_OTH_MX.CSV', x)), files))


# # Script to validate each row on the Dataframe

# In[11]:


def validate_row(row):
    global results
    for index, val in row.iteritems():
        logger.debug('Column: {}'.format(row.name))
        logger.debug('Value: {}'.format(str(val)))
        logger.debug('Data type: {}'.format(type(val)))
        logger.debug('Row: {}'.format(index))
        
        # If the filed is empty (NaN or None) and the field validation is not required, continue for the next loop
        if ((type(val) is float and math.isnan(val)) or (val is None))             and (validation_df.loc['required'][row.name] is not True):
            logger.debug('The field is empty and the filed validation is not required, ...')
            continue
            
        # If the filed is empty (NaN or None) and the field validation is required, insert column and row and continue for the next loop
        if ((type(val) is float and math.isnan(val)) or (val is None))             and (validation_df.loc['required'][row.name] is True):
            logger.debug('ERROR required')
            results[1].add('required')
            results[2].append('Column: {}, Row: {}'.format(row.name, index))
            continue
            
         
        #CHECK FOR LENGTH ERRORS FOR STR        
        if type(val) is str:
            if (validation_df.loc['data_type_length'][row.name] and len(val) > validation_df.loc['data_type_length'][row.name]):
                logger.debug('ERROR data_type_length length')
                results[1].add('data_type_length')
                results[2].append('Column: {}, Row: {}'.format(row.name, index))
                
            if (validation_df.loc['min_length'][row.name] and len(val) < validation_df.loc['min_length'][row.name]):
                logger.debug('ERROR min_length length')
                results[1].add('min_length')
                results[2].append('Column: {}, Row: {}'.format(row.name, index))
            
            if (validation_df.loc['max_length'][row.name] and len(val) > validation_df.loc['max_length'][row.name]):
                logger.debug('ERROR max_length length')
                results[1].add('max_length')
                results[2].append('Column: {}, Row: {}'.format(row.name, index))
          
            if (validation_df.loc['exact_length'][row.name] and len(val) != validation_df.loc['exact_length'][row.name]):
                    logger.debug('ERROR exact_length length')
                    results[1].add('exact_length')
                    results[2].append('Column: {}, Row: {}'.format(row.name, index))

        
        # CHECK FOR DATATYPE ERRORS
        # datatype
        if validation_df.loc['data_type'][row.name] and type(val) is not validation_df.loc['data_type'][row.name]:     
            logger.debug('ERROR validation datatype')
            results[1].add('data_type')
            results[3].append('Column: {}, Row: {}'.format(row.name, index))
            
        # only_number 
        if validation_df.loc['only_numbers'][row.name] and validation_df.loc['only_numbers'][row.name] is True and not str(val).isdigit():     
            logger.debug('ERROR validation only_numbers')
            results[1].add('only_numbers')
            results[3].append('Column: {}, Row: {}'.format(row.name, index))
            
        #only_char
        if validation_df.loc['only_chars'][row.name] and validation_df.loc['only_chars'][row.name] is True and not bool(re.match('^[a-zA-Z]+$', str(val))):     
            logger.debug('ERROR validation only_chars')
            results[1].add('only_chars')
            results[3].append('Column: {}, Row: {}'.format(row.name, index))
            
        # CHECK FOR PATTERN ERRORS
        # datatype
        #if validation_df.loc['pattern'][row.name]:     
            #print('ERROR validation pattern')
            #results[4].append('Column: {}, Row: {}'.format(row.name, index))


# # Iterate over each files and do validation

# In[12]:


def retrieve_in_chunk(file):
    mylist = []
    for chunk in  pd.read_csv('files/outbound/it/sales_transactional/{}'.format(file), sep='|', chunksize=20000, converters={'/BIC/HMMATPAD': lambda x: str(x)}):
        mylist.append(chunk)
    df = pd.concat(mylist, axis= 0)
    del mylist
    return df


# In[13]:


for file in files:
    validation_df = pd.DataFrame.from_dict(SALES_TRANSACTIONAL_OTHER_VALIDATION)
    df = retrieve_in_chunk(file)
    df.replace(r'\s+', np.nan, regex=True, inplace=True)
    check = []
    n_check = set()
    l_check = []
    t_check = []
    p_check = []
    results = [check, n_check, l_check, t_check, p_check]
    df.head(5).apply(lambda x: validate_row(x))
    if len(results[2]) > 0:
        results[2].insert(0, 'Your file contains: {} Length errors'.format(len(results[2])))
    else:
        results[2].insert(0, 'Your file does not have Length errors')

    if len(results[3]) > 0:
        results[3].insert(0, 'Your file contains: {} Datatype errors'.format(len(results[3])))
    else:
        results[3].insert(0, 'Your file does not have Data type errors')

    # If n_check, l_check, t_check or p_check is greater than 1, then the files has errors 
    if len(results[1]) > 1 or len(results[2]) > 1 or len(results[3]) > 1 or len(results[4]) > 1:
        results[0].insert(0, 'The file {} has errors'.format(file))
    else:
        results[0].insert(0, 'Your file does not have errors')    
        
    logger.warning(results)

