# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 20:30:11 2016

@author: dhartig
"""

from job_income_process import *

def main():
    occ_list = get_occ_list(['Computer Development', 'Computer Support'])
    #occ_list = get_occ_list(get_occ_options())
    #occ_list = [('Training Managers', ['11-3131']), ('Management Analysts', ['13-1111']), ('Training Specialists', ['13-1151']) ]
    
    data = get_numbers_for_occ(occ_list, 100000)
    data = merge_metros(data)
    data = add_total_column(data)
    
    output_to_file(data, ['Computer Development', 'Computer Support'])
    #output_to_file(data, ['Training Managers', 'Management Analysts', 'Training Specialists'])
    
    



main()