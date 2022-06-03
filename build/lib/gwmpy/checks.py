# -*- coding: utf-8 -*-

def get_all_obligated(constraints):
    all_obligated = [k for k,v in constraints.items() if v == 'obligated']
    return(all_obligated)

def check_missing_args(inputs, constraints, method):
    """
    

    Parameters
    ----------
    inputs : dictionary
        input arguments, with arguments as keys
    constraints : dictionary
        constraints for all possible input arguments, with arguments as keys.
        values: optional, obligated
    method:
        description of method (string)
        

    Raises
    ------
    Exception
        If obligated input arguments from the constraint dictionary are missing
        in the inputs dictionary

    Returns
    -------
    None.

    """
    
    available = [elem in list(inputs.keys()) for elem in get_all_obligated(constraints)] 
    obligated = all(available)
    
    if obligated:
        pass
    else:
        nonavailable =  list(set(list(get_all_obligated(constraints)))-set(list(inputs.keys())))
        print(nonavailable)
        raise Exception("Obligated input arguments missing for '{}': {}".format(method,''.join(str(e)+' ' for e in nonavailable)))
