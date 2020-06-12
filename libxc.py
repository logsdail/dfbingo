#!/usr/bin/env python3

# import os
# os.environ["PYTHONPATH"]="/home/andrew/Software/libxc-4.3.4/lib/python3.7/site-packages:$PYTHONPATH"
# import pylibxc

def get_functional_kind(value):
    '''
    Function to translate integer value into string for functional type

    Parameters:
    value: Integer
    '''
    from pylibxc import flags

    if value is flags.XC_EXCHANGE:
        return "an exchange"
    elif value is flags.XC_CORRELATION:
        return "a correlation"
    elif value is flags.XC_EXCHANGE_CORRELATION:
        return "an exchange-correlation"
    elif value is flags.XC_KINETIC:
        return "a kinetic"
    return "an unknown"

def get_functional_family(value):
    '''
    Function to translate integer value into string for functional family

    Parameters:
    value: Integer
    '''
    from pylibxc import flags

    if value is flags.XC_FAMILY_LDA:
        return "LDA"
    elif value is flags.XC_FAMILY_GGA:
        return "GGA"
    elif value is flags.XC_FAMILY_HYB_GGA:
        return "Hybrid GGA"
    elif value is flags.XC_FAMILY_MGGA:
        return "MGGA"
    elif value is flags.XC_FAMILY_HYB_MGGA:
        return "Hybrid MGGA"
    return "unknown"

def get_citations(dois):
    '''
    Function that translates a list of DOIs into a citation count

    Parameters:
    dois: List of strings
        Contains all relevant DOIs, as obtained from LibXC
    '''
    # Citations from scopus using Rose, Michael E. and John R. Kitchin: 
    # "pybliometrics: Scriptable bibliometrics using a Python interface to Scopus", SoftwareX 10 (2019) 100263.
    from pybliometrics.scopus import AbstractRetrieval
    citations = 0
    for doi in dois:
        try:
            ab = AbstractRetrieval(doi)
            #print(ab.citedby_count)
            citations += ab.citedby_count
        except:
            continue
    return citations

def get_doi_text(dois):
    '''
    Function to translates a list of DOIs into a text output

    Parameters:
    dois: List of strings
        Contains all relevant DOIs, as obtained from LibXC
    '''
    func_doi = ""
    for doi in dois:
        # Check there is content
        if len(doi):
            func_doi += "https://dx.doi.org/" + doi + ", "
    if len(func_doi):
        return ". Read more: " + func_doi[:-2]
    else:
        return func_doi
    
def get_functional_information(func_name):
    '''
    Present in Tweet ready form all the information associated with the functional identified.

    Parameters:
    func_name: String
        LibXC value for the functional name, so the correct functional can be initialised.
    '''
    from pylibxc import LibXCFunctional

    # Interaction with libxc taken from this page: https://www.tddft.org/programs/libxc/installation/#python-library
    func = LibXCFunctional(func_name, "unpolarized")
    func_textname = func.get_name()
    func_kind = get_functional_kind(func.get_kind())
    func_family = get_functional_family(func.get_family())
    information = func_textname + ", which is " + func_kind + " functional from the " + func_family + " family" 

    # Get DOI and present information
    func_doi = get_doi_text(func.get_doi())
    information += func_doi 

    # Try to get citations - some problems with empty DOIs so need to handle zero counts
    func_citations = get_citations(func.get_doi())
    if func_citations:
        information += " (Citations: " + str(func_citations) + ")."
    else:
        #print(func.get_doi())
        information += " (Citations unavailable)."  

    # Return the information string
    return information

def get_random_functional():
    '''
    Return a random string dependent on the day of the year (and year itself)
    '''
    # Get day and year 
    from datetime import datetime
    day_of_year = datetime.now().timetuple().tm_yday
    current_year = datetime.now().year

    # Randomise functionals
    from random import seed, random, shuffle
    # seed random number generator
    rand_seed = day_of_year * current_year
    seed(rand_seed)

    from pylibxc import util
    # Mix all the functionals and then pick 
    functionals = list(util.xc_available_functional_numbers())
    shuffle(functionals)

    # Double random - mix the XC functionals and pick using day of the year
    func_id = functionals[day_of_year]
    func_name = util.xc_functional_get_name(func_id)

    # Produce output information, include pre-amble if appropriate
    output = ""
    information = get_functional_information(func_name)
    if "exchange-correlation" in information:
        output += "Winner! "
    else:
        from bingo import calls
        #print(func_id)
        if calls.get(str(func_id % 100)):
            output += calls.get(str(func_id % 100)) + "; "
    
    output += "Today's functional is "  
    output += information
    
    # Return Tweet
    return output

def get_best_match(incoming, match, funcs):
    '''
    Compare incoming request to library of options, and return the best match

    Parameters:
    incoming: String
        The functional name identified from the Tweet
    match: List of integers
        The indices for all matching functionals in pre-screen on LibXC (based on functional type)
    funcs: List of strings
        Names of all the functionals
    '''
    import difflib

    # Create a list with all the functional names for the identified matches
    match_funcs = [funcs[m] for m in match]

    # Use difflib to return the most promising matches (3 by default)
    matches = difflib.get_close_matches(incoming, match_funcs)

    # Return the index of best match
    #return funcs.index(matches[0])
    return [funcs.index(m) for m in matches]

def search_functional_information(incoming_words):
    '''
    Take an incoming Tweet and see if we can identify a functional from the request.
    If so, we'll return all the simple information we know about that functional.

    Parameters:
    incoming_words: List of strings
        The initial tweet, decomposed into lowercase punctuation-free words
    '''

    # Search for occurence of the word functional
    try:
        func = incoming_words.index("functional")
    except ValueError:
        # Return if we don't find any kind of functional
        response = "Sorry, I don't know how to handle your enquiry currently."
        response += ' The easiest sentence for me to understand is  "What is the XXX functional?"'
        return response

    # See if a specific type of functional is requested
    if incoming_words[func-1] == "kinetic":
        masks = ["_k_"]
        func -= 1
    elif incoming_words[func-1] == "exchange":
        masks = ["_x_"]
        func -= 1
    elif incoming_words[func-1] == "correlation":
        if incoming_words[func-2] == "exchange":
            masks = ["_xc_"]
            func -= 2
        else:
            masks = ["_c_"]
            func -= 1
    elif incoming_words[func-1] == "exchangecorrelation":
        masks = ["_xc_"]
        func -= 1
    # If not, just return results for all functionals
    else:
        masks = ["_x_", "_c_", "_xc_", "_k_"]

    from pylibxc import util
    # Get all the possible XC functionals so we can search the list
    func_ids = list(util.xc_available_functional_numbers())
    func_names = list(util.xc_available_functional_names())

    # Create objects to hold the functionals that match the desired outcome type
    selected_func_names = []
    selected_func_ids = []

    # Introduce method to remove punctuation - necessary because some functionals are stored as e.g. PBE_SOL
    import string
    table = str.maketrans('', '', string.punctuation)

    # Return all appropriate functional names to be reviewed for the "best match"
    for mask in masks:
        msk = [mask in s for s in func_names]
        selected_func_names += [func_names[i].split(mask)[1].translate(table) for i in range(len(func_names)) if msk[i]]
        selected_func_ids += [func_ids[i] for i in range(len(func_ids)) if msk[i]]

    match = get_best_match(incoming_words[func-1], [i for i in range(len(selected_func_names))], selected_func_names)

    # Create the response Tweet to return
    response = "" 
    if len(match) >= 1:
        response += "The closest match is "
        response += get_functional_information(func_names[func_ids.index(selected_func_ids[match[0]])])
    else:
        response = "Sorry, I cannot find the '" + incoming_words[func-1] + "'" 
        if len(masks) == 1:
            if masks[0] == "_k_":
                response += " kinetic"
            elif masks[0] == "_x_":
                response += " exchange"
            elif masks[0] == "_c_":
                response += " correlation"
            elif masks[0] == "_xc_":
                response += " exchange-correlation"
        response +=" functional from your tweet." 
        response += " The best next option is to consult the Libxc webpages: https://www.tddft.org/programs/libxc/functionals/" 

    return response
